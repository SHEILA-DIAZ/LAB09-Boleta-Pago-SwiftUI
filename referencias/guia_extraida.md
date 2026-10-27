# Extracción íntegra del cuerpo del Word

Párrafos y tablas en orden de aparición. La paginación depende del editor.

TEMA DE ANÁLISIS · TRABAJO DE UNA SEMANA
Boleta de pago: del sueldo al neto
Una app de una sola pantalla en SwiftUI y una hoja de Excel que explica cada fórmula
1. Contexto
La boleta de pago es el documento donde el empleador muestra al trabajador cuánto gana, cuánto se le descuenta y cuánto recibe. Su formato está previsto en el artículo 19 del D.S. 001-98-TR y tiene tres bloques: Remuneraciones, Retenciones / Descuentos y Aportaciones del empleador, además del Neto a pagar.
En este tema construyen una versión simplificada: el usuario ingresa los datos del mes y la app calcula la boleta. Los alumnos descubren por qué el sueldo que se pacta con la empresa no es lo que llega al bolsillo.
2. Logro esperado
Convertir reglas laborales en un procedimiento de cálculo, en Swift y en Excel.
Modelar con estructuras, clases y colecciones, separando el cálculo de la pantalla.
Validar la app con casos de prueba y contrastar sus resultados con los de la hoja de Excel.
Analizar con datos reales cuánto de un sueldo bruto llega al trabajador.
3. Qué entrega el equipo

Tabla 1:
Entregable | Qué contiene
Aplicación móvil | App SwiftUI de  una sola pantalla : formulario arriba y, al pulsar Calcular, la boleta debajo. Es el entregable principal.
Hoja de Excel | Libro con fórmulas visibles que explica el cálculo: cada fórmula escrita en palabras y con un ejemplo numérico. Sirve también para validar la app.
Repositorio y análisis | Repositorio GitHub con commits por hito, respuestas a las preguntas de análisis y tabla de fuentes.


Control cruzado: la app y el Excel deben dar el mismo resultado, al centavo, en los 4 casos. Si no coinciden, el equipo revisa dónde está la diferencia y lo documenta. El docente revisa el caso 4.
4. Reglas de cálculo

Tabla 2:
Concepto | Cómo se calcula
Sueldo computable | Sueldo básico ÷ 30 × días laborados
Asignación familiar | Si el trabajador tiene hijos: 10% de la RMV. No se prorratea por días
Valor hora | Sueldo básico ÷ 30 ÷ 8
Horas extras al 25% | Valor hora × 1.25 × número de horas
Horas extras al 35% | Valor hora × 1.35 × número de horas
Total remuneraciones | Suma de los conceptos anteriores
ONP | 13% del total de remuneraciones (si el trabajador está en la ONP)
AFP | Tres descuentos sobre el total de remuneraciones: fondo, comisión y seguro (si el trabajador está en una AFP)
Adelantos | Monto ingresado, se resta tal cual
Total descuentos | Pensión (ONP o AFP) + adelantos
Neto a pagar | Total remuneraciones − total descuentos
EsSalud (empleador) | 9% del total de remuneraciones. Lo paga el empleador: no se descuenta al trabajador

Parámetros
Los parámetros no se escriben dentro de las fórmulas: van en un solo lugar (una hoja en Excel, constantes en Swift). Anota la fuente y la fecha de consulta de cada uno.

Tabla 3:
Parámetro | Valor | Fuente
RMV | S/ 1,230.00 | D.S. de la RMV, vigente desde el 1 de octubre de 2026
Asignación familiar | 10% de la RMV = S/ 123.00 | Ley 25129
ONP | 13% | D.L. 19990
EsSalud | 9% | Ley 26790
Recargo de horas extras | 25% las primeras horas, 35% las siguientes | Normas de jornada y sobretiempo
AFP Ejemplo (solo para los casos de prueba) | Fondo 10.00%, comisión 1.60%, seguro 1.35% | Valores de prueba. En datos reales, usa los de la SBS

Convenciones para que todos calculen igual
Cada concepto se redondea a 2 decimales y luego se suman. Montos en soles.
Los descuentos de ONP y AFP se calculan sobre el total de remuneraciones, que incluye asignación familiar y horas extras.
Las horas extras se ingresan ya separadas: cuántas son al 25% y cuántas al 35%.
No se calcula la retención de renta de 5.ª categoría ni se consideran faltas aparte: las faltas ya están reflejadas en los días laborados.
EsSalud se calcula sobre el total de remuneraciones, sin considerar bases mínimas.
5. Datos de entrada y pantalla
La app tiene una sola pantalla. Usa solo los controles vistos en clase: Text, VStack, HStack, @State, TextField, Picker y Button. Como el formulario y la boleta no caben en la pantalla del celular, envuélvelos en un ScrollView, que es el único control nuevo.

Tabla 4:
Dato | Control | Nivel | Validación
Sueldo básico | TextField con teclado decimal | 1 | Mayor que cero
Días laborados | TextField | 1 | Entre 1 y 30
¿Tiene hijos? | Picker (No / Sí) | 1 | —
Sistema de pensiones | Picker (ONP / AFP) | 1 | —
AFP | Picker | 2 | Solo aparece si eligió AFP
Horas extras al 25% | TextField | 2 | Mayor o igual a cero
Horas extras al 35% | TextField | 2 | Mayor o igual a cero
Adelantos | TextField | 2 | Mayor o igual a cero


Si los datos no son válidos, la app muestra un mensaje claro y no calcula.
Cómo se ve el resultado
La boleta imita las tres columnas del formato real. En el celular los tres bloques van uno debajo del otro. Ejemplo con los datos del caso 1:

Tabla 5:
REMUNERACIONES | RETENCIONES / DESCUENTOS | APORTACIONES DEL EMPLEADOR
Sueldo computable | 2,500.00 | ONP | 325.00 | EsSalud (9%) | 225.00
Asignación familiar | 0.00 | AFP fondo | 0.00 |  | 
Horas extras 25% | 0.00 | AFP comisión | 0.00 |  | 
Horas extras 35% | 0.00 | AFP seguro | 0.00 |  | 
 |  | Adelantos | 0.00 |  | 
Total remuneraciones | 2,500.00 | Total descuentos | 325.00 |  | 


NETO A PAGAR: S/ 2,175.00
Los conceptos que no aplican se muestran con 0.00, como en la boleta real.
6. Niveles de avance

Tabla 6:
Nivel | Qué incluye
1 (obligatorio) | Sueldo, días laborados, asignación familiar, ONP, EsSalud y neto. Casos 1 y 2
2 | AFP en lugar de ONP, horas extras y adelantos. Casos 3 y 4
3 (reto) | Encabezado con nombre del trabajador y razón social ficticios; mostrar ONP y AFP lado a lado en la misma pantalla; retención de renta de 5.ª categoría

7. Casos de prueba
Los casos 1, 2 y 3 traen la respuesta para que validen su cálculo. El caso 4 no la trae: lo revisa el docente.
Caso 1 · Sin hijos, ONP, mes completo (con respuesta)
Sueldo S/ 2,500.00 · 30 días laborados · sin hijos · ONP · sin horas extras ni adelantos.

Tabla 7:
Concepto | Cálculo | Monto
Sueldo computable | 2,500 ÷ 30 × 30 | 2,500.00
Total remuneraciones |  | 2,500.00
ONP | 2,500.00 × 13% | 325.00
Neto a pagar | 2,500.00 − 325.00 | 2,175.00
EsSalud (empleador) | 2,500.00 × 9% | 225.00

Caso 2 · Con hijos y días incompletos (con respuesta)
Sueldo S/ 1,800.00 · 27 días laborados · con hijos · ONP · sin horas extras ni adelantos.

Tabla 8:
Concepto | Cálculo | Monto
Sueldo computable | 1,800 ÷ 30 × 27 | 1,620.00
Asignación familiar | 10% × 1,230 | 123.00
Total remuneraciones | 1,620.00 + 123.00 | 1,743.00
ONP | 1,743.00 × 13% | 226.59
Neto a pagar | 1,743.00 − 226.59 | 1,516.41
EsSalud (empleador) | 1,743.00 × 9% | 156.87

Caso 3 · AFP, horas extras y adelanto (con respuesta)
Sueldo S/ 3,000.00 · 30 días laborados · con hijos · AFP Ejemplo · 4 horas extras al 25% · 4 horas extras al 35% · adelanto S/ 200.00.

Tabla 9:
Concepto | Cálculo | Monto
Sueldo computable | 3,000 ÷ 30 × 30 | 3,000.00
Asignación familiar | 10% × 1,230 | 123.00
Horas extras 25% | Valor hora 12.50 (3,000 ÷ 30 ÷ 8) × 1.25 × 4 | 62.50
Horas extras 35% | 12.50 × 1.35 × 4 | 67.50
Total remuneraciones |  | 3,253.00
AFP fondo (10.00%) | 3,253.00 × 10% | 325.30
AFP comisión (1.60%) | 3,253.00 × 1.6% = 52.048 | 52.05
AFP seguro (1.35%) | 3,253.00 × 1.35% = 43.9155 | 43.92
Adelantos |  | 200.00
Total descuentos | 325.30 + 52.05 + 43.92 + 200.00 | 621.27
Neto a pagar | 3,253.00 − 621.27 | 2,631.73
EsSalud (empleador) | 3,253.00 × 9% | 292.77

Caso 4 · Evaluación (sin respuesta)
Sueldo S/ 4,200.00 · 24 días laborados · con hijos · AFP Ejemplo · 2 horas extras al 25% · 2 horas extras al 35% · adelanto S/ 100.00.
8. Preguntas de análisis
ONP o AFP. Con los datos del caso 3, calcula el neto con ONP y con AFP Ejemplo. ¿Cuál deja más dinero este mes? ¿Por qué no basta comparar los porcentajes para decidir cuál conviene al trabajador?
Costo real para la empresa. En el caso 3, ¿cuánto cuesta el trabajador al empleador este mes (remuneraciones más EsSalud)? ¿Qué porcentaje de ese costo llega al trabajador como neto?
Días laborados. Con los datos del caso 2, calcula el neto si el trabajador hubiera laborado los 30 días. ¿Por qué la diferencia en el neto es menor que la diferencia en el sueldo bruto?
Horas extras. En el caso 3, ¿qué porcentaje del total de remuneraciones representan las horas extras?
Con datos reales. Toma un sueldo de una oferta laboral publicada, arma su boleta y calcula qué porcentaje del sueldo bruto llega al trabajador. Compara tu resultado con el de dos compañeros que usaron otros sueldos.
9. Datos reales y fuentes
Un caso propio por alumno: sueldo tomado de una oferta laboral real (guarda el enlace y la fecha de consulta). Debe ser igual o mayor que la RMV. Las demás personas y empresas son ficticias.
Valores que cambian: RMV, tasas de AFP y cualquier otro parámetro se verifican en la fuente oficial. Para las AFP, usa los valores publicados por la SBS.
Tabla de fuentes: dato, valor, fuente y fecha de consulta.
No uses datos personales reales, como DNI o RUC verdaderos. La pantalla debe decir "Boleta de ejemplo".
10. Entregables
Aplicación móvil (SwiftUI)
Pantalla única con el formulario, el botón Calcular y la boleta con sus tres bloques y el neto.
Modelo separado de la pantalla: structs para los datos, una clase Boleta que calcula, un diccionario con las tasas de cada AFP y un array con los conceptos de remuneraciones y descuentos.
Validaciones con mensajes claros.
Repositorio en GitHub con un commit por hito (por ejemplo "modelo: remuneraciones", "ui: formulario", "caso 1 verificado") y README con capturas.
Hoja de Excel
Libro con cuatro hojas: Parámetros, Boleta (datos de entrada y cálculo con fórmulas visibles, sin valores pegados), Casos (los 4 casos y los casos propios) y Explicación.
En la hoja Explicación, cada fórmula escrita en palabras y con un ejemplo numérico, para alguien que no sabe contabilidad.
Análisis
Respuestas a las 5 preguntas y tabla de fuentes, en un archivo aparte o en la hoja Explicación.
Considerar : de dos participantes - 
Va explicar en un excel todas las formulas realizadas
Va explicar la APP
Dos notas  al sistema
Esto se realiza con swiftui



word/header1.xml
Tecsup  |  Programación en Móviles Avanzado 

word/footer1.xml
Página  de 

word/endnotes.xml


word/footnotes.xml
