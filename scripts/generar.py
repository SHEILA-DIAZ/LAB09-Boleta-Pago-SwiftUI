"""Genera Excel, fixtures y proyecto Xcode de forma reproducible. Python 3.10+."""
from pathlib import Path
from decimal import Decimal as D, ROUND_HALF_UP
import hashlib
import json
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools'))
import xlsxwriter

DATE = '2026-10-26'
SBS = 'https://www.sbs.gob.pe/app/spp/empleadores/comisiones_spp/Paginas/comision_prima.aspx'
OFERTA = 'https://pe.indeed.com/viewjob?jk=1a5d74a196f5ecab'
RMV = 'https://busquedas.elperuano.pe/dispositivo/NL/2559163-1'
FUENTES = [
    ('RMV', '1230; desde 01/10/2026 según guía', RMV, 'D.S. 015-2026-TR; índice oficial localizado; ver fuentes.md'),
    ('Asignación familiar', '10% RMV = 123', 'https://www.gob.pe/institucion/mtpe/noticias/601761-quienes-tienen-derecho-a-percibir-la-asignacion-familiar', 'Ley 25129; no prorratear en este laboratorio'),
    ('ONP', '13%', 'https://www.gob.pe/institucion/onp/noticias/1190488-como-saber-si-tu-empleador-esta-pagando-tus-aportes-al-snp', 'D.L. 19990'),
    ('EsSalud', '9%', 'https://www.sunat.gob.pe/legislacion/oficios/2007/oficios/i0032007.htm', 'Ley 26790; la guía excluye base mínima'),
    ('Horas extras', '25% y 35%', 'https://www.gob.pe/institucion/sunafil/noticias/1100081-conoce-las-diferencias-entre-trabajo-forzoso-y-trabajo-en-sobretiempo', 'D.S. 007-2002-TR; horas ingresadas por tramo'),
    ('AFP Ejemplo', '10%; 1.60%; 1.35%', 'Actividad_Grupo_B.docx, sección 4', 'Tasas ficticias de prueba, no tasas SBS'),
    ('AFP reales: flujo', 'Habitat 1.47%; Integra 1.55%; Prima 1.60%; Profuturo 1.69%', SBS, 'Fondo 10%; seguro 1.37%; devengue 2026-10'),
    ('Oferta propia', '3500–4000 mensuales; se toma 3500', OFERTA, 'Desarrollador Full Stack; solo sueldo publicado, personas ficticias'),
    ('Base mensual y jornada', '30 días; 8 horas', 'Actividad_Grupo_B.docx, sección 4', 'Convención académica'),
    ('Redondeo', '2 decimales por concepto antes de sumar', 'Actividad_Grupo_B.docx, sección 4', 'Mitades alejándose de cero; valor hora sin redondeo previo'),
]
AFPS = {'Ejemplo': ('0.10', '0.016', '0.0135'), 'Habitat (flujo)': ('0.10', '0.0147', '0.0137'),
        'Integra (flujo)': ('0.10', '0.0155', '0.0137'), 'Prima (flujo)': ('0.10', '0.016', '0.0137'),
        'Profuturo (flujo)': ('0.10', '0.0169', '0.0137')}
LABELS = ['Sueldo computable', 'Asignación familiar', 'Horas extras 25%', 'Horas extras 35%',
          'Total remuneraciones', 'ONP', 'AFP fondo', 'AFP comisión', 'AFP seguro', 'Adelantos',
          'Total descuentos', 'Neto a pagar', 'EsSalud', 'Costo empleador']

def r(n):
    return n.quantize(D('.01'), rounding=ROUND_HALF_UP)

def calcular(i):
    sueldo, dias = D(i['sueldo']), D(i['dias'])
    hora = sueldo / 30 / 8
    rem = [r(sueldo / 30 * dias), D('123') if i['hijos'] else D(0),
           r(hora * D('1.25') * D(i['horas25'])), r(hora * D('1.35') * D(i['horas35']))]
    total = sum(rem)
    afp = AFPS[i['afp']]
    des = [r(total * D('.13')) if i['sistema'] == 'ONP' else D(0)]
    des += [r(total * D(t)) if i['sistema'] == 'AFP' else D(0) for t in afp]
    des += [D(i['adelantos'])]
    ess = r(total * D('.09'))
    return rem + [total] + des + [sum(des), total - sum(des), ess, total + ess]

def entrada(sueldo, dias=30, hijos=False, sistema='ONP', h25='0', h35='0', adelanto='0', afp='Ejemplo'):
    return dict(sueldo=str(sueldo), dias=dias, hijos=hijos, sistema=sistema, afp=afp,
                horas25=h25, horas35=h35, adelantos=adelanto)

def casos():
    items = [
        ('Caso 1', entrada(2500)),
        ('Caso 2', entrada(1800, 27, True)),
        ('Caso 3', entrada(3000, 30, True, 'AFP', '4', '4', '200')),
        ('Caso 4', entrada(4200, 24, True, 'AFP', '2', '2', '100')),
        ('Propio: oferta 3500 ONP', entrada(3500)),
        ('Sensibilidad A: 3750 AFP Prima (no compañero)', entrada(3750, sistema='AFP', afp='Prima (flujo)')),
        ('Sensibilidad B: 4000 AFP Habitat (no compañero)', entrada(4000, sistema='AFP', afp='Habitat (flujo)')),
        ('Caso 3 con ONP', entrada(3000, 30, True, 'ONP', '4', '4', '200')),
        ('Caso 2 con 30 días', entrada(1800, 30, True)),
        ('Redondeo valor hora', entrada('1234.56', 19, True, 'AFP', '1.25', '2.75', '10.01')),
        ('Empate medio centavo', entrada('240.96', 30, False, 'ONP', '1', '0')),
        ('Neto negativo permitido', entrada(2500, adelanto='3000')),
    ]
    for nombre, afp in AFPS.items():
        if nombre != 'Ejemplo':
            items.append((f'AFP {nombre}', entrada('2345.67', 1, True, 'AFP', '0.5', '0.25', '1.01', nombre)))
    return [dict(name=n, input=i, expected=[f'{x:.2f}' for x in calcular(i)]) for n, i in items]

def extraer_docx(origen):
    destino = ROOT / 'referencias' / 'Actividad_Grupo_B.docx'
    shutil.copy2(origen, destino)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(origen) as z:
        body = ET.fromstring(z.read('word/document.xml')).find('w:body', ns)
        lineas = ['# Extracción íntegra del cuerpo del Word', '', 'Párrafos y tablas en orden de aparición. La paginación depende del editor.', '']
        tablas = 0
        for node in body:
            if node.tag.endswith('}p'):
                lineas.append(''.join(t.text or '' for t in node.findall('.//w:t', ns)))
            elif node.tag.endswith('}tbl'):
                tablas += 1
                lineas.append(f'\nTabla {tablas}:')
                for fila in node.findall('w:tr', ns):
                    lineas.append(' | '.join(' '.join(t.text or '' for t in c.findall('.//w:t', ns)) for c in fila.findall('w:tc', ns)))
                lineas.append('')
        for nombre in z.namelist():
            if nombre.startswith(('word/header', 'word/footer', 'word/footnotes', 'word/endnotes')) and nombre.endswith('.xml'):
                lineas += ['', nombre, ''.join(t.text or '' for t in ET.fromstring(z.read(nombre)).findall('.//w:t', ns))]
    (ROOT / 'referencias' / 'guia_extraida.md').write_text('\n'.join(lineas), encoding='utf-8')
    (ROOT / 'evidencias' / 'documento.json').write_text(json.dumps(dict(origen=str(origen), sha256=hashlib.sha256(destino.read_bytes()).hexdigest(), tablas=tablas, nota='DOCX sin contador de páginas en metadatos; lectura íntegra del XML y partes auxiliares'), indent=2), encoding='utf-8')

def libro(fixtures):
    w = xlsxwriter.Workbook(ROOT / 'Excel' / 'Boleta_Pago_Semana09.xlsx')
    w.set_properties({'title': 'Boleta de pago: del sueldo al neto', 'subject': 'Semana 9 · niveles 1 y 2', 'author': 'Equipo Semana 9'})
    w.set_calc_mode('auto')
    title = w.add_format({'bold': True, 'font_size': 19, 'font_color': '#FFFFFF', 'bg_color': '#17365D'})
    head = w.add_format({'bold': True, 'bg_color': '#DCE6F1', 'text_wrap': True, 'border': 1})
    money = w.add_format({'num_format': '#,##0.00;[Red]-#,##0.00', 'border': 1})
    inp = w.add_format({'num_format': '#,##0.00', 'bg_color': '#FFF2CC', 'border': 1})
    integer = w.add_format({'num_format': '0', 'bg_color': '#FFF2CC', 'border': 1})
    txt = w.add_format({'text_wrap': True, 'valign': 'top', 'border': 1})
    editxt = w.add_format({'bg_color': '#FFF2CC', 'border': 1})
    percent = w.add_format({'num_format': '0.00%', 'border': 1})
    rate = w.add_format({'num_format': '0.00%', 'bg_color': '#FFF2CC', 'border': 1})
    sheets = {name: w.add_worksheet(name) for name in ['Parámetros', 'Boleta', 'Casos', 'Explicación']}
    for s in sheets.values():
        s.hide_gridlines(2); s.freeze_panes(3, 1); s.set_landscape(); s.fit_to_pages(1, 0)
    p = sheets['Parámetros']
    p.merge_range('A1:E1', 'SEMANA 9 · PARÁMETROS EDITABLES', title)
    p.write_row('A3', ['Parámetro', 'Valor', 'Unidad', 'Fuente / observación', 'Consulta'], head)
    parametros = [('RMV', 1230, 'S/', FUENTES[0][2]), ('Asignación familiar', .10, '% RMV', FUENTES[1][2]),
                  ('ONP', .13, '% remuneraciones', FUENTES[2][2]), ('EsSalud', .09, '% remuneraciones', FUENTES[3][2]),
                  ('Días del mes', 30, 'días', 'Guía sección 4'), ('Horas de jornada', 8, 'horas', 'Guía sección 4'),
                  ('Factor extra 25%', 1.25, 'multiplicador', FUENTES[4][2]), ('Factor extra 35%', 1.35, 'multiplicador', FUENTES[4][2])]
    for row, (nombre, valor, unidad, fuente) in enumerate(parametros, 3):
        p.write(row, 0, nombre, txt); p.write_number(row, 1, valor, rate if row in (4, 5, 6) else inp)
        p.write(row, 2, unidad, txt); p.write(row, 3, fuente, txt); p.write(row, 4, DATE, txt)
        p.set_row(row, 42)
        p.data_validation(row, 1, row, 1, {'validate': 'decimal', 'criteria': '>', 'value': 0, 'error_type': 'stop', 'error_message': 'El parámetro debe ser positivo.'})
    for nombre, celda in [('RMV','B4'),('TasaAF','B5'),('TasaONP','B6'),('TasaEsSalud','B7'),('DiasMes','B8'),('HorasDia','B9'),('Factor25','B10'),('Factor35','B11')]:
        w.define_name(nombre, f"='Parámetros'!${celda[0]}${celda[1:]}")
    p.write_row('A14', ['AFP', 'Fondo', 'Comisión flujo', 'Seguro', 'Fuente'], head)
    for row, (nombre, tasas) in enumerate(AFPS.items(), 14):
        p.write(row, 0, nombre, txt)
        for col, val in enumerate(tasas, 1): p.write_number(row, col, float(val), rate)
        p.write(row, 4, 'Guía: prueba' if nombre == 'Ejemplo' else SBS, txt)
        p.set_row(row, 40)
    w.define_name('ListaAFP', "='Parámetros'!$A$15:$A$19")
    p.merge_range('A22:E23', 'Amarillo = editable. Casos 1–4: RMV 1230 y AFP Ejemplo. AFP reales: modalidad flujo, devengue octubre 2026. No se aplica tope de seguro ni base mínima EsSalud por simplificación de la guía. No se modela comisión sobre saldo ni renta de quinta.', txt)
    p.write_row('A26', ['Dato', 'Valor', 'Fuente', 'Alcance', 'Consulta'], head)
    for row, (dato, valor, fuente, alcance) in enumerate(FUENTES, 26):
        p.write_row(row, 0, [dato, valor, fuente, alcance, DATE], txt); p.set_row(row, 65)
    p.set_column('A:A', 26); p.set_column('B:C', 24); p.set_column('D:D', 70); p.set_column('E:E', 45)

    b = sheets['Boleta']
    b.merge_range('A1:D1', 'BOLETA DE EJEMPLO · DEL SUELDO AL NETO', title)
    b.merge_range('A2:D2', 'Edita amarillo. Fórmulas en B; texto visible en C. Sin renta de quinta categoría.', txt)
    b.write_row('A3', ['Entrada', 'Valor editable', 'Regla', 'Ayuda'], head)
    inputs = [('Sueldo básico', 2500, 'Mayor que 0; hasta 2 decimales'), ('Días laborados', 30, 'Entero de 1 a 30'),
              ('¿Tiene hijos?', 'No', 'No / Sí'), ('Sistema', 'ONP', 'ONP / AFP'), ('AFP', 'Ejemplo', 'Solo se utiliza si eliges AFP'),
              ('Horas extras 25%', 0, 'No negativas; hasta 2 decimales'), ('Horas extras 35%', 0, 'No negativas; hasta 2 decimales'),
              ('Adelantos', 0, 'No negativos; hasta 2 decimales')]
    for row, (nombre, val, regla) in enumerate(inputs, 3):
        b.write(row, 0, nombre, txt); b.write(row, 1, val, editxt if isinstance(val, str) else (integer if row == 4 else inp)); b.write(row, 2, regla, txt)
    def validar(s, row, col, tipo, opciones):
        s.data_validation(row, col, row, col, {'validate': tipo, 'error_type': 'stop', 'error_title': 'Dato inválido', 'error_message': 'Revisa la regla indicada; sin separadores de miles.', **opciones})
    for row in (3,7,8,9,10):
        cell = f'B{row+1}'
        limite = 10000 if row in (8,9) else 100000000
        if row == 7: continue
        validar(b,row,1,'custom', {'value':f'=AND(ISNUMBER({cell}),{cell}{">" if row==3 else ">="}0,{cell}<={limite},ROUND({cell},2)={cell})'})
    validar(b,4,1,'integer', {'criteria': 'between', 'minimum':1,'maximum':30})
    validar(b,5,1,'list', {'source':['No','Sí']}); validar(b,6,1,'list', {'source':['ONP','AFP']}); validar(b,7,1,'list', {'source':'=ListaAFP'})
    valido = '=IFERROR(IF(AND(ISNUMBER(B4),B4>0,B4<=100000000,ROUND(B4,2)=B4,ISNUMBER(B5),B5=INT(B5),B5>=1,B5<=30,OR(B6="No",B6="Sí"),OR(B7="ONP",B7="AFP"),OR(B7="ONP",COUNTIF(ListaAFP,B8)=1),ISNUMBER(B9),B9>=0,B9<=10000,ROUND(B9,2)=B9,ISNUMBER(B10),B10>=0,B10<=10000,ROUND(B10,2)=B10,ISNUMBER(B11),B11>=0,B11<=100000000,ROUND(B11,2)=B11),"OK","Datos inválidos: revisa las reglas de entrada"),"Datos inválidos: revisa las reglas de entrada")'
    b.write('A13','Validación',head); b.write_formula('B13',valido,txt,'OK')
    b.merge_range('A14:D14','Los campos numéricos son obligatorios. Si pegas datos inválidos, se oculta el cálculo.',txt)
    formulas = [
        '=ROUND(ROUND(B4/DiasMes*B5*100,8),0)/100', '=IF(B6="Sí",ROUND(RMV*TasaAF,2),0)',
        '=ROUND(ROUND(B4/DiasMes/HorasDia*Factor25*B9*100,8),0)/100', '=ROUND(ROUND(B4/DiasMes/HorasDia*Factor35*B10*100,8),0)/100',
        '=SUM(B17:B20)', '=IF(B7="ONP",ROUND(B21*TasaONP,2),0)',
        '=IF(B7="AFP",ROUND(B21*VLOOKUP(B8,\'Parámetros\'!$A$15:$D$19,2,FALSE),2),0)',
        '=IF(B7="AFP",ROUND(B21*VLOOKUP(B8,\'Parámetros\'!$A$15:$D$19,3,FALSE),2),0)',
        '=IF(B7="AFP",ROUND(B21*VLOOKUP(B8,\'Parámetros\'!$A$15:$D$19,4,FALSE),2),0)',
        '=B11', '=SUM(B22:B26)', '=B21-B27', '=ROUND(B21*TasaEsSalud,2)', '=B21+B29']
    b.write_row('A16', ['Concepto', 'Monto (S/)', 'Fórmula visible', 'Bloque'], head)
    for row,(label,formula,value) in enumerate(zip(LABELS,formulas,fixtures[0]['expected']),16):
        b.write(row,0,label,head if row in (20,26,27,29) else txt)
        b.write_formula(row,1,'=IF($B$13="OK",'+formula[1:]+',"")',money,float(value))
        b.write_formula(row,2,f'=FORMULATEXT(B{row+1})',txt,'=IF($B$13="OK",'+formula[1:]+',"")')
        b.write(row,3,'Remuneraciones' if row<21 else ('Retenciones / descuentos' if row<27 else ('Neto' if row==27 else 'Empleador')),txt)
        b.set_row(row,48)
    b.merge_range('A32:D33','EsSalud se informa aparte: no reduce el neto. Valor hora no se redondea antes de calcular cada tramo. Un neto negativo señala adelantos excesivos; no se reemplaza por cero.',txt)
    b.set_column('A:A',28); b.set_column('B:B',32); b.set_column('C:C',95); b.set_column('D:D',28)
    b.print_area('A1:D33')

    c = sheets['Casos']
    c.merge_range('A1:J1','CASOS · CONTROL CRUZADO CON SWIFT',title)
    c.merge_range('A2:J2','Filas 4–7: guía. Filas 8–10: oferta y sensibilidades, no resultados de compañeros. Editar entradas invalida el contraste original.',txt)
    headers = ['Caso','Sueldo','Días','Hijos','Sistema','AFP','HE25','HE35','Adelanto'] + LABELS + ['Neto oficial','Contraste guía','Neto / remuneraciones','Referencia']
    c.write_row(2,0,headers,head)
    c.freeze_panes(3,1)
    for row, caso in enumerate(fixtures,3):
        i=caso['input']; n=row+1
        c.write_row(row,0,[caso['name'],float(i['sueldo']),i['dias'],'Sí' if i['hijos'] else 'No',i['sistema'],i['afp'],float(i['horas25']),float(i['horas35']),float(i['adelantos'])],editxt)
        formulas_c = [f'ROUND(ROUND(B{n}/DiasMes*C{n}*100,8),0)/100', f'IF(D{n}="Sí",ROUND(RMV*TasaAF,2),0)',
            f'ROUND(ROUND(B{n}/DiasMes/HorasDia*Factor25*G{n}*100,8),0)/100',f'ROUND(ROUND(B{n}/DiasMes/HorasDia*Factor35*H{n}*100,8),0)/100', f'SUM(J{n}:M{n})',
            f'IF(E{n}="ONP",ROUND(N{n}*TasaONP,2),0)']
        formulas_c += [f'IF(E{n}="AFP",ROUND(N{n}*VLOOKUP(F{n},\'Parámetros\'!$A$15:$D$19,{col},FALSE),2),0)' for col in (2,3,4)]
        formulas_c += [f'I{n}',f'SUM(O{n}:S{n})',f'N{n}-T{n}',f'ROUND(N{n}*TasaEsSalud,2)',f'N{n}+V{n}']
        for col,(formula,val) in enumerate(zip(formulas_c,caso['expected']),9): c.write_formula(row,col,'='+formula,money,float(val))
        oficial = ['2175.00','1516.41','2631.73'][row-3] if row<6 else None
        if oficial:
            c.write_number(row,23,float(oficial),money)
            c.write_formula(row,24,f'=IF(ROUND(U{n}-X{n},2)=0,"COINCIDE","REVISAR")',txt,'COINCIDE')
        else: c.write(row,24,'Calculado; sin respuesta oficial' if row==6 else 'Comparar con Swift',txt)
        c.write_formula(row,25,f'=U{n}/N{n}',percent,float(caso['expected'][11])/float(caso['expected'][4]))
        c.write(row,26,OFERTA if row in (7,8,9) else 'Guía / prueba automática',txt)
        c.set_row(row,42)
    c.autofilter(2,0,2+len(fixtures),26)
    c.set_column('A:A',46); c.set_column('B:I',19); c.set_column('J:W',21); c.set_column('X:Z',27); c.set_column('AA:AA',65)
    c.conditional_format(3,24,2+len(fixtures),24,{'type':'text','criteria':'containing','value':'REVISAR','format':w.add_format({'bg_color':'#FFC7CE'})})
    # Espacios explícitos para completar la comparación real solicitada por el profesor.
    fila = len(fixtures)+7
    c.merge_range(f'A{fila}:I{fila}','PENDIENTE: resultados reales de dos compañeros (no inventados)',head)
    c.write_row(f'A{fila+1}',['Compañero ficticio/alias','Oferta y fecha','Sueldo','Neto','% neto/bruto','Observación'],head)
    for rr in (fila+1,fila+2):
        c.write(rr,0,'Por completar',editxt); c.write(rr,5,'Solicitar boleta y fuente a un compañero',txt)
        c.write_formula(rr,4,f'=IF(AND(ISNUMBER(C{rr+1}),ISNUMBER(D{rr+1}),C{rr+1}>0),D{rr+1}/C{rr+1},"")',percent,'')

    e = sheets['Explicación']
    e.merge_range('A1:D1','CADA FÓRMULA EN PALABRAS',title)
    e.write_row('A3',['Concepto','Explicación sencilla','Ejemplo numérico','Fórmula Excel en Boleta'],head)
    palabras = [
        ('Divide el sueldo entre 30 y multiplícalo por los días trabajados.','Caso 2: 1800 / 30 × 27 = 1620.00'),
        ('Si tiene hijos, entrega el 10% de RMV completo; no lo dividas por días.','Caso 2: 1230 × 10% = 123.00'),
        ('Divide sueldo entre 30 y 8, aumenta 25% y multiplica por las horas de este tramo.','Caso 3: 3000 / 30 / 8 × 1.25 × 4 = 62.50'),
        ('Usa el valor hora sin redondear, aumenta 35% y multiplica por las horas de este tramo.','Caso 3: 12.50 × 1.35 × 4 = 67.50'),
        ('Suma sueldo computable, asignación y ambos tramos, ya redondeados.','Caso 3: 3000 + 123 + 62.50 + 67.50 = 3253.00'),
        ('Si eligió ONP, retén el 13% de todas las remuneraciones; si AFP, muestra cero.','Caso 2: 1743 × 13% = 226.59'),
        ('Si eligió AFP, multiplica remuneraciones por tasa del fondo de la AFP elegida.','Caso 3: 3253 × 10% = 325.30'),
        ('Multiplica remuneraciones por la comisión de flujo, redondeada individualmente.','Caso 3: 3253 × 1.60% = 52.048 → 52.05'),
        ('Multiplica remuneraciones por la prima de seguro y redondea.','Caso 3: 3253 × 1.35% = 43.9155 → 43.92'),
        ('Copia el adelanto, que ya tiene como máximo dos decimales.','Caso 3: 200.00'),
        ('Suma ONP o los tres aportes AFP y agrega adelantos.','Caso 3: 325.30 + 52.05 + 43.92 + 200 = 621.27'),
        ('Resta todos los descuentos del total de remuneraciones.','Caso 3: 3253.00 − 621.27 = 2631.73'),
        ('Calcula 9% de remuneraciones; lo paga la empresa adicionalmente.','Caso 3: 3253 × 9% = 292.77'),
        ('Suma remuneraciones y EsSalud para este costo mensual simplificado.','Caso 3: 3253 + 292.77 = 3545.77')]
    for row, (label,(palabra,ejemplo),formula) in enumerate(zip(LABELS,palabras,formulas),3):
        e.write_row(row,0,[label,palabra,ejemplo],txt); e.write_string(row,3,formula,txt); e.set_row(row,68)
    e.merge_range('A19:D20','Redondeo: 2 decimales por concepto, luego SUM. Sueldo y HE usan ROUND(ROUND(importe*100,8),0)/100: normalizar residuos a 8 decimales de céntimo y redondear a céntimos enteros. Ejemplo 1.2549999999999999 → 125.5 → 126 → 1.26. No se redondea el valor hora por separado.',txt)
    e.merge_range('A22:D23','Lectura: revisa Parámetros → edita Boleta → examina Casos → explica cada paso. Ctrl+` alterna fórmulas; C en Boleta ya muestra FORMULATEXT. Cambiar tasas recalcula todos los casos; los esperados oficiales permanecen fijos.',txt)
    e.merge_range('A25:D26','Análisis completo y fuentes en docs/analisis.md y docs/fuentes.md. Las sensibilidades de la oferta no sustituyen la comparación con dos compañeros, que queda pendiente de sus resultados reales.',txt)
    e.set_column('A:A',28); e.set_column('B:B',65); e.set_column('C:C',65); e.set_column('D:D',90)
    w.close()

def xcode():
    # Proyecto tradicional sin dependencias externas. IDs deterministas de 24 dígitos.
    files = ['BoletaPagoApp.swift','ContentView.swift','Model/Boleta.swift']
    ids = lambda n: f'{n:024X}'
    file_objects='\n'.join(f'{ids(10+i)} = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = "{f}"; sourceTree = "<group>"; }};' for i,f in enumerate(files))
    build_objects='\n'.join(f'{ids(20+i)} = {{isa = PBXBuildFile; fileRef = {ids(10+i)}; }};' for i in range(3))
    sources=', '.join(ids(20+i) for i in range(3))
    refs=', '.join(ids(10+i) for i in range(3))
    pbx=f'''// !$*UTF8*$!
{{ archiveVersion = 1; classes = {{}}; objectVersion = 56;
objects = {{
{file_objects}
{build_objects}
{ids(1)} = {{isa = PBXProject; attributes = {{BuildIndependentTargetsInParallel = YES; LastUpgradeCheck = 1600; }}; buildConfigurationList = {ids(30)}; compatibilityVersion = "Xcode 14.0"; developmentRegion = es; hasScannedForEncodings = 0; knownRegions = (es, en, Base); mainGroup = {ids(2)}; productRefGroup = {ids(4)}; projectDirPath = ""; projectRoot = ""; targets = ({ids(5)}); }};
{ids(2)} = {{isa = PBXGroup; children = ({ids(3)}, {ids(4)}); sourceTree = "<group>"; }};
{ids(3)} = {{isa = PBXGroup; path = App; children = ({refs}); sourceTree = "<group>"; }};
{ids(4)} = {{isa = PBXGroup; name = Products; children = ({ids(6)}); sourceTree = "<group>"; }};
{ids(5)} = {{isa = PBXNativeTarget; buildConfigurationList = {ids(31)}; buildPhases = ({ids(7)}, {ids(8)}, {ids(9)}); buildRules = (); dependencies = (); name = BoletaPago; productName = BoletaPago; productReference = {ids(6)}; productType = "com.apple.product-type.application"; }};
{ids(6)} = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = BoletaPago.app; sourceTree = BUILT_PRODUCTS_DIR; }};
{ids(7)} = {{isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = ({sources}); runOnlyForDeploymentPostprocessing = 0; }};
{ids(8)} = {{isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; }};
{ids(9)} = {{isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; }};
{ids(30)} = {{isa = XCConfigurationList; buildConfigurations = ({ids(32)}, {ids(33)}); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release; }};
{ids(31)} = {{isa = XCConfigurationList; buildConfigurations = ({ids(34)}, {ids(35)}); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release; }};
'''
    for n, name, target in [(32,'Debug',False),(33,'Release',False),(34,'Debug',True),(35,'Release',True)]:
        settings='CLANG_ENABLE_MODULES = YES; SDKROOT = iphoneos; IPHONEOS_DEPLOYMENT_TARGET = 17.0; SWIFT_VERSION = 5.0;'
        if target:
            settings+=' CODE_SIGN_STYLE = Automatic; GENERATE_INFOPLIST_FILE = YES; INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES; INFOPLIST_KEY_UILaunchScreen_Generation = YES; INFOPLIST_KEY_CFBundleDisplayName = "Boleta de ejemplo"; PRODUCT_BUNDLE_IDENTIFIER = "pe.edu.semana09.boletapago"; PRODUCT_NAME = "$(TARGET_NAME)"; TARGETED_DEVICE_FAMILY = "1,2"; SUPPORTED_PLATFORMS = "iphoneos iphonesimulator"; MARKETING_VERSION = 1.0; CURRENT_PROJECT_VERSION = 1; SWIFT_EMIT_LOC_STRINGS = YES;'
        if name=='Debug': settings+=' SWIFT_OPTIMIZATION_LEVEL = "-Onone"; DEBUG_INFORMATION_FORMAT = dwarf; SWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG;'
        else: settings+=' SWIFT_COMPILATION_MODE = wholemodule; SWIFT_OPTIMIZATION_LEVEL = "-O";'
        pbx+=f'{ids(n)} = {{isa = XCBuildConfiguration; buildSettings = {{{settings}}}; name = {name}; }};\n'
    pbx+=f'}}; rootObject = {ids(1)}; }}\n'
    project=ROOT/'BoletaPago.xcodeproj'; project.mkdir(exist_ok=True)
    (project/'project.pbxproj').write_text(pbx,encoding='utf-8')
    scheme=project/'xcshareddata'/'xcschemes'; scheme.mkdir(parents=True,exist_ok=True)
    (scheme/'BoletaPago.xcscheme').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<Scheme LastUpgradeVersion="1600" version="1.3"><BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES"><BuildActionEntries><BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES"><BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{ids(5)}" BuildableName="BoletaPago.app" BlueprintName="BoletaPago" ReferencedContainer="container:BoletaPago.xcodeproj"/></BuildActionEntry></BuildActionEntries></BuildAction><LaunchAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" launchStyle="0" useCustomWorkingDirectory="NO" ignoresPersistentStateOnLaunch="NO" debugDocumentVersioning="YES" debugServiceExtension="internal" allowLocationSimulation="YES"><BuildableProductRunnable runnableDebuggingMode="0"><BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{ids(5)}" BuildableName="BoletaPago.app" BlueprintName="BoletaPago" ReferencedContainer="container:BoletaPago.xcodeproj"/></BuildableProductRunnable></LaunchAction><ProfileAction buildConfiguration="Release" shouldUseLaunchSchemeArgsEnv="YES" savedToolIdentifier="" useCustomWorkingDirectory="NO" debugDocumentVersioning="YES"/><AnalyzeAction buildConfiguration="Debug"/><ArchiveAction buildConfiguration="Release" revealArchiveInOrganizer="YES"/></Scheme>''',encoding='utf-8')

def main():
    for path in ['Excel','Tests','evidencias','referencias','docs']:
        (ROOT/path).mkdir(exist_ok=True)
    origen=Path(sys.argv[1]) if len(sys.argv)>1 else None
    if origen: extraer_docx(origen)
    fixtures=casos()
    (ROOT/'Tests'/'fixtures.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2),encoding='utf-8')
    libro(fixtures)
    xcode()
    print(f'Generados XLSX, proyecto Xcode y {len(fixtures)} casos. No se ha ejecutado Excel ni Xcode en este paso.')

if __name__=='__main__': main()
