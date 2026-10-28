"""Añade explicaciones de la app sin reescribir fórmulas ni cachés del XLSX.

Edición XML autorizada por la usuaria ante la ausencia de artifact-tool.
Solo utiliza la biblioteca estándar; verifica invariantes antes de guardar.
"""
from pathlib import Path
from copy import deepcopy
import json
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'Excel/Boleta_Pago_Semana09.xlsx'
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
ET.register_namespace('', NS)
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
N = {'m': NS}
def tag(s): return '{' + NS + '}' + s

def read_package(path):
    with zipfile.ZipFile(path) as z:
        return {i.filename: (i, z.read(i.filename)) for i in z.infolist()}

def signatures(parts):
    formulas, inputs = {}, {}
    for name, (_, data) in parts.items():
        if re.fullmatch(r'xl/worksheets/sheet\d+.xml', name):
            root = ET.fromstring(data)
            for c in root.findall('.//m:sheetData/m:row/m:c', N):
                f, v = c.find('m:f', N), c.find('m:v', N)
                if f is not None:
                    formulas[(name, c.get('r'))] = (ET.tostring(f), ET.tostring(v) if v is not None else None)
                elif v is not None and c.get('t') not in ('s', 'str', 'e'):
                    inputs[(name, c.get('r'))] = v.text
    return formulas, inputs

def cell(root, addr):
    data = root.find('m:sheetData', N)
    number = int(re.search(r'\d+', addr).group())
    row = next((r for r in data if int(r.get('r')) == number), None)
    if row is None:
        row = ET.Element(tag('row'), {'r': str(number)})
        data.append(row)
        data[:] = sorted(data, key=lambda r: int(r.get('r')))
    found = next((c for c in row if c.get('r') == addr), None)
    if found is None:
        found = ET.SubElement(row, tag('c'), {'r': addr})
        def colnum(c):
            value = 0
            for ch in re.match('[A-Z]+', c.get('r')).group(): value = value * 26 + ord(ch) - 64
            return value
        row[:] = sorted(row, key=colnum)
    return found, row

def text(root, addr, value, height=None, style=None):
    c, row = cell(root, addr)
    assert c.find('m:f', N) is None, f'No sobrescribir fórmula: {addr}'
    c[:] = []
    c.set('t', 'inlineStr')
    if style is not None: c.set('s', str(style))
    ET.SubElement(ET.SubElement(c, tag('is')), tag('t')).text = value
    if height:
        row.set('ht', str(max(float(row.get('ht', 15)), height)))
        row.set('customHeight', '1')

def width(root, index, value):
    cols = root.find('m:cols', N)
    for c in cols:
        if int(c.get('min')) == index and int(c.get('max')) == index:
            c.set('width', str(value)); return
    ET.SubElement(cols, tag('col'), {'min': str(index), 'max': str(index), 'width': str(value), 'customWidth': '1'})

def merge(root, addr):
    merges = root.find('m:mergeCells', N)
    ET.SubElement(merges, tag('mergeCell'), {'ref': addr})
    merges.set('count', str(len(merges)))

parts = read_package(BOOK)
original_signatures = signatures(parts)
styles = ET.fromstring(parts['xl/styles.xml'][1])
xfs = styles.find('m:cellXfs', N)
roots = [ET.fromstring(parts[f'xl/worksheets/sheet{i}.xml'][1]) for i in range(1, 5)]

# Reutiliza colores, fuentes y bordes del libro; solo activa ajuste de texto.
def wrapped_style(root, source):
    c, _ = cell(root, source)
    xf = deepcopy(xfs[int(c.get('s', 0))])
    alignment = xf.find('m:alignment', N)
    if alignment is None: alignment = ET.SubElement(xf, tag('alignment'))
    alignment.set('wrapText', '1'); alignment.set('vertical', 'top')
    xf.set('applyAlignment', '1')
    xfs.append(xf); xfs.set('count', str(len(xfs)))
    return len(xfs) - 1

explanation = (ROOT / 'docs/mejoras_explicativas_excel.md').read_text()
sections = explanation.split('## ')
def table_rows(section):
    result = []
    for line in section.splitlines():
        if line.startswith('|') and not line.startswith('| ---'):
            result.append([s.strip() for s in line.strip().strip('|').split('|')])
    return result[1:]

p, b, cases, e = roots
ps = wrapped_style(p, 'D4')
bs = wrapped_style(b, 'C4')
es = wrapped_style(e, 'B4')
cs = wrapped_style(cases, 'AA4')
heading_p = int(cell(p, 'D3')[0].get('s', 0))
heading_c = int(cell(cases, 'AA3')[0].get('s', 0))
heading_e = int(cell(e, 'A3')[0].get('s', 0))

params = table_rows(sections[1])
text(p, 'F3', '¿Qué significa y por qué usamos este número?', 32, heading_p)
width(p, 6, 75)
for row, item in zip(range(4, 12), params[:8]): text(p, f'F{row}', item[1], 100, ps)
text(p, 'F14', '¿Por qué separamos las tasas de AFP?', 32, heading_p)
text(p, 'F15', params[8][1], 100, ps)
for row in range(16, 20):
    text(p, f'F{row}', 'La app busca las tasas de esta AFP por su nombre. Fondo: ahorro para pensión; comisión: administración; seguro: cobertura previsional. ' + params[9][1], 110, ps)
merge(p, 'A39:F39')
text(p, 'A39', 'Las tasas están juntas porque la app también las centraliza en Parametros: cambiar una regla desde aquí actualiza las fórmulas que la usan. Conserva los valores originales para demostrar los casos de la guía.', 48, ps)
p.find('m:dimension', N).set('ref', 'A1:F39')

inputs = table_rows(sections[2])
text(b, 'C3', 'Qué ingresar y por qué lo pedimos', 30)
for row, item in zip(range(4, 12), inputs[:8]): text(b, f'C{row}', item[1], 68, bs)
text(b, 'D13', 'OK permite calcular. Si una entrada no cumple las reglas, la boleta queda vacía.', 48, bs)
text(b, 'D16', 'Qué significa, por qué está aquí y cómo lo usa la app', 34)
width(b, 4, 76)

calculations = table_rows(sections[3])
for row, erow, item in zip(range(17, 31), range(4, 18), calculations):
    text(b, f'D{row}', item[1], 86, bs)
    text(e, f'B{erow}', item[1], 96, es)
    text(e, f'C{erow}', item[2], 96, es)
text(b, 'A2', 'Como en la app: ingresa datos → valida → calcula remuneraciones → descuenta pensión y adelanto → muestra neto. Amarillo: entradas. Columna D: explicación.', 38)
text(b, 'A32', 'EsSalud lo paga la empresa; no reduce el neto. Costo empleador es un dato complementario del Excel calculado también por el modelo, pero no se muestra como fila en la pantalla actual. Los ejemplos de Explicación corresponden a los casos originales.', 48)

def note(row, title, body):
    text(e, f'A{row}', title, 70, es)
    merge(e, f'B{row}:D{row}')
    text(e, f'B{row}', body, 70, es)

merge(e, 'A29:D29')
text(e, 'A29', 'ENTENDER EL EXCEL SEGÚN LO QUE HACE LA APP', 30, heading_e)
notes = [
('Orden del cálculo', 'La app recibe los datos, valida y calcula. Primero obtiene sueldo por días, asignación y horas extras; luego suma remuneraciones; después aplica ONP o AFP y adelantos; finalmente muestra el neto y EsSalud separado. El Excel sigue el mismo orden.'),
('¿Por qué 30 y 8?', 'Son las constantes del modelo: 30 convierte el sueldo mensual a valor diario y 8 convierte ese valor a hora. Ejemplo fijo: 3,000 ÷ 30 ÷ 8 = S/ 12.50. La app no pregunta otra jornada ni usa la cantidad de días del calendario.'),
('¿Por qué 1.25 y 1.35?', 'Incluyen el valor de la hora completa y su recargo. 1.25 = 1 + 0.25; 1.35 = 1 + 0.35. Con valor hora de S/ 12.50, cuatro horas de cada tramo producen S/ 62.50 y S/ 67.50. La app recibe cada cantidad ya separada.'),
('Inasistencias: una sola vez', 'Básico 1,800 y 27 días: 1,800 ÷ 30 × 27 = S/ 1,620. La reducción de S/ 180 ya está en el sueldo computable. Por eso no hay otra fila de descuento por faltas. La app no clasifica descansos médicos o licencias.'),
('¿Por qué S/ 123?', 'La app usa la RMV académica de S/ 1,230 y la tasa 10%: 1,230 × 0.10 = 123. Si hijos es Sí, suma ese importe completo; si es No, suma cero. El básico del trabajador no interviene en este cálculo.'),
('Base de las retenciones', 'En este ejercicio, sueldo computable, asignación y horas extras forman el total de remuneraciones. Sobre ese total se aplica la pensión y EsSalud. El adelanto se resta después: no disminuye esta base.'),
('ONP o AFP', 'El selector de sistema elige una sola alternativa. Si eliges ONP, las tres filas AFP muestran cero. Si eliges AFP, ONP muestra cero y las tasas dependen de la AFP seleccionada. AFP Ejemplo conserva las tasas ficticias de la guía.'),
('Adelanto no es una multa', 'Es una parte del pago que ya se entregó. En el caso 3, antes del adelanto quedan S/ 2,831.73 después de AFP. Como ya se pagaron S/ 200, el depósito pendiente es S/ 2,631.73. El adelanto no cambia lo ganado ni la pensión calculada.'),
('Redondear antes de sumar', 'Cada concepto termina con dos decimales antes de sumarse. Comisión: 52.048 → 52.05; seguro: 43.9155 → 43.92. La app usa Decimal y el Excel REDONDEAR. No se redondea el valor hora intermedio; el doble ROUND estabiliza residuos numéricos del Excel.'),
('¿Qué significa cada cero?', 'Un cero puede indicar que no corresponde un concepto: sin hijos, asignación cero; sin sobretiempo, extras cero; ONP elegida, AFP cero. Se conservan esas filas para entender el desglose, como ocurre en la app.'),
('Validación y límites', 'Como en la app: básico mayor que cero hasta S/ 100,000,000; días enteros 1–30; horas 0–10,000 por tramo; adelanto 0–100,000,000; importes y horas con hasta dos decimales. Los máximos son límites técnicos del ejercicio, no derechos laborales.'),
('Si el neto es negativo', 'El modelo permite mostrarlo para detectar un adelanto excesivo; no lo convierte en cero. Ejemplo fijo: remuneraciones 2,500 − ONP 325 − adelanto 3,000 = −825. La app pide revisar el adelanto.'),
('EsSalud y costo', 'Con remuneraciones 3,253, EsSalud es 3,253 × 9% = S/ 292.77. Lo asume la empresa. El Excel añade el costo simplificado: 3,253 + 292.77 = S/ 3,545.77. Ese costo existe en el modelo, pero la pantalla actual muestra EsSalud y neto, sin una fila de costo.'),
('Cómo leer las fórmulas', 'SI selecciona la regla; SUMA reúne conceptos; BUSCARV recupera tasas AFP; REDONDEAR fija céntimos; FORMULATEXTO muestra la fórmula. RMV y DiasMes son nombres de celdas de Parámetros. Los signos $ fijan referencias al copiar fórmulas.'),
('Ejemplos y actualización', 'Los ejemplos numéricos de esta hoja son textos fijos para estudiar los casos originales. Los resultados vivos están en Boleta y Casos. Excel recalcula con cálculo automático; en la app debes pulsar Calcular de nuevo después de editar.'),
('Alcance de esta versión', 'Se explica solo lo implementado: sueldo por días, asignación, horas extras, ONP/AFP, adelantos, neto y EsSalud. La app no tiene selector de régimen laboral ni calcula CTS, gratificaciones, vacaciones o quinta categoría. ONP/AFP es sistema de pensiones, no régimen laboral.'),
('Prueba para exponer', 'Caso 3: básico 3,000; días 30; hijos Sí; AFP Ejemplo; HE25 4; HE35 4; adelanto 200. Remuneraciones S/ 3,253; descuentos S/ 621.27; neto S/ 2,631.73; EsSalud S/ 292.77. Ingresa los mismos datos en la app y compara concepto por concepto.'),
]
for row, (title, body) in enumerate(notes, 30): note(row, title, body)
e.find('m:dimension', N).set('ref', f'A1:D{29+len(notes)}')

width(cases, 28, 76)
text(cases, 'AB3', '¿Por qué probamos este caso? Relación con la app', 46, heading_c)
case_notes = [
'Prueba básica: 2,500 − ONP 325 = neto 2,175. Sin hijos, extras ni adelantos, se observa la diferencia entre sueldo, pensión y EsSalud adicional.',
'Prueba días incompletos y asignación completa: 1,800 ÷ 30 × 27 = 1,620; más 123 = 1,743. ONP 226.59; neto 1,516.41. No se restan faltas nuevamente.',
'Prueba AFP, ambos tramos de horas y adelanto. Remuneraciones 3,253; AFP 421.27; adelanto 200; neto 2,631.73. Permite explicar todos los bloques de la app.',
'Prueba conjunta con 24 días, hijos, AFP, extras y adelanto. Neto calculado 3,011.17. La guía no publica respuesta oficial para este caso; se entrega para revisión.',
'Aplica el mismo modelo de la app a un sueldo de oferta documentada. Los demás datos son supuestos académicos. No es una boleta real de la empresa anunciante.',
'Escenario de sensibilidad con otra remuneración y AFP Prima de flujo. Es un cálculo para comparar; no representa una boleta enviada por un compañero.',
'Escenario de sensibilidad con otra remuneración y AFP Habitat de flujo. Es un cálculo para comparar; no representa una boleta enviada por un compañero.',
'Cambia únicamente el sistema del caso 3 a ONP: neto 2,630.11 frente a 2,631.73 con AFP Ejemplo. La diferencia es 1.62 con las tasas de prueba; no decide qué pensión conviene.',
'Cambia el caso 2 de 27 a 30 días. Neto 1,673.01. Aumenta 156.60 porque los 180 adicionales también generan 23.40 de ONP. La asignación no cambia.',
'Prueba precisión con días incompletos, horas fraccionarias y adelanto con céntimos. El valor hora no se redondea antes de calcular cada tramo.',
'Prueba el medio céntimo: básico 240.96 y una HE25 producen 1.255 antes del redondeo; el concepto debe quedar en 1.26. Así se contrasta el redondeo con el modelo Swift.',
'Prueba un adelanto mayor que lo disponible. El neto queda negativo y la app pide revisar el adelanto. El modelo no lo reemplaza por cero.',
]
case_notes += ['Prueba la búsqueda de tasas de esta AFP de flujo con las mismas entradas del resto de AFP reales. Solo cambia el perfil seleccionado; fondo, comisión y seguro se redondean por separado.'] * 4
for row, value in enumerate(case_notes, 4): text(cases, f'AB{row}', value, 102, cs)
cases.find('m:dimension', N).set('ref', 'A1:AB26')

for i, root in enumerate(roots, 1):
    name = f'xl/worksheets/sheet{i}.xml'
    parts[name] = (parts[name][0], ET.tostring(root, encoding='utf-8', xml_declaration=True))
parts['xl/styles.xml'] = (parts['xl/styles.xml'][0], ET.tostring(styles, encoding='utf-8', xml_declaration=True))
assert signatures(parts) == original_signatures, 'Deben conservarse fórmulas, cachés y entradas numéricas'

output_dir = ROOT / 'outputs/excel_explicado_app'
output_dir.mkdir(parents=True, exist_ok=True)
destination = output_dir / BOOK.name
with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as z:
    for info, data in parts.values(): z.writestr(info, data)
assert signatures(read_package(destination)) == original_signatures
with zipfile.ZipFile(destination) as z:
    assert z.testzip() is None
    for name in z.namelist():
        if name.endswith('.xml'): ET.fromstring(z.read(name))
BOOK.write_bytes(destination.read_bytes())
print(json.dumps({'updated': str(BOOK), 'delivery': str(destination), 'formulas_preserved': len(original_signatures[0]), 'numeric_inputs_preserved': len(original_signatures[1]), 'sheets': 4}, ensure_ascii=False))
