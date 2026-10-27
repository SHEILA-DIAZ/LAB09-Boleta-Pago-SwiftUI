"""Recalcula las fórmulas reales con formulas, sin usar valores cacheados del XLSX."""
from pathlib import Path
from decimal import Decimal as D
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'.tools'))
import formulas

fixtures = json.loads((ROOT/'Tests/fixtures.json').read_text(encoding='utf-8'))
model = formulas.ExcelModel().loads(str(ROOT/'Excel/Boleta_Pago_Semana09.xlsx')).finish()

# Este motor lee las fórmulas del archivo. No toma como prueba los importes
# que XlsxWriter dejó almacenados para previsualizar el libro sin recalcularlo.

def key(hoja, celda):
    return f"'[Boleta_Pago_Semana09.xlsx]{hoja.upper()}'!{celda}"

def numero(solucion, hoja, celda):
    valor = solucion[key(hoja,celda)].value[0,0]
    # Errores (#NAME?, #VALUE!, etc.) nunca se aceptan como valores numéricos.
    return f'{D(str(valor)).quantize(D(".01")):.2f}'

solution = model.calculate()
casos = []
formulario = []
for row, fixture in enumerate(fixtures,4):
    valores = [numero(solution,'CASOS',f'{col}{row}') for col in 'JKLMNOPQRSTUVW']
    assert valores == fixture['expected'], (fixture['name'],valores,fixture['expected'])
    casos.append(dict(name=fixture['name'],values=valores))
    i=fixture['input']
    datos = [float(i['sueldo']),i['dias'],'Sí' if i['hijos'] else 'No',i['sistema'],i['afp'],float(i['horas25']),float(i['horas35']),float(i['adelantos'])]
    nueva = model.calculate(inputs={key('BOLETA',f'B{r}'):v for r,v in enumerate(datos,4)})
    valores = [numero(nueva,'BOLETA',f'B{r}') for r in range(17,31)]
    assert valores == fixture['expected'], ('Formulario',fixture['name'],valores,fixture['expected'])
    formulario.append(dict(name=fixture['name'],values=valores))

# Pruebas del bloqueo por fórmula, incluso al pegar valores que evaden data validation.
invalidos = [('B4',0),('B4','abc'),('B4',2500.001),('B5',0),('B5',31),('B5',1.5),
             ('B6','Tal vez'),('B7','Otro'),('B9',-1),('B10',-1),('B11',-1),('B9',0.001)]
for celda,valor in invalidos:
    nueva = model.calculate(inputs={key('BOLETA',celda):valor})
    assert nueva[key('BOLETA','B13')].value[0,0] != 'OK', (celda,valor)
    assert nueva[key('BOLETA','B28')].value[0,0] == '', (celda,valor)

# Verifica dependencia real de parámetros editables, diferenciando recálculo de caché.
alterada = model.calculate(inputs={key('PARÁMETROS','B4'):2000})
assert numero(alterada,'CASOS','K5') == '200.00'
assert numero(alterada,'CASOS','U5') == '1583.40'
salida=dict(engine='formulas',version=formulas.__version__,cases=casos,form=formulario,
            conceptComparisons=len(fixtures)*14*2,invalidInputsBlocked=len(invalidos),parameterMutationPassed=True,
            scope='Evalúa fórmulas XLSX sin caché; no es ejecución de Microsoft Excel ni verificación visual. FORMULATEXT no se contrasta con este motor.')
(ROOT/'evidencias/formulas_recalculadas.json').write_text(json.dumps(salida,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'OK: {salida["conceptComparisons"]} resultados recalculados; {len(invalidos)} entradas inválidas; cambio de RMV propagado.')
