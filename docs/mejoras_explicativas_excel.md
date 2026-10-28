# Explicaciones incorporadas al Excel según la app

Estos textos sirven de base para las explicaciones incorporadas al libro existente con `scripts/ampliar_explicaciones_excel.py`. El XLSX actualizado conserva las entradas, fórmulas, tasas, validaciones y resultados del laboratorio. Las explicaciones se limitan al funcionamiento implementado en la app; la hoja Explicación incluye aclaraciones y ejemplos adicionales.

## Hoja Parámetros: qué significa cada número y por qué está aquí

| Dato | Explicación para incorporar |
| --- | --- |
| RMV: S/ 1,230 | Es el valor de referencia que establece la guía del profesor. En este ejercicio se usa para calcular la asignación familiar. No significa que todos los trabajadores ganen ese sueldo. Se mantiene este valor para reproducir los casos del laboratorio; su uso aquí no acredita por sí solo la RMV legal aplicable a otra fecha. |
| Asignación familiar: 10% | La guía reconoce una asignación equivalente al 10% de su RMV cuando se marca Sí en hijos. Por eso 1,230 × 0.10 = S/ 123. Se entrega un solo importe, no S/ 123 por cada hijo. El formulario simplifica la acreditación de requisitos a Sí/No. |
| ONP: 13% | Es la tasa utilizada para la retención previsional cuando el trabajador está en ONP. Se aplica al total de remuneraciones del ejercicio, no solo al básico. Ejemplo: 2,500 × 0.13 = S/ 325. Reduce el neto del trabajador. |
| EsSalud: 9% | Es una aportación adicional a cargo de la empresa. Se muestra separada para explicar el costo del empleador. Ejemplo: 2,500 × 0.09 = S/ 225. No se resta al trabajador. La guía no aplica bases mínimas. |
| Mes: 30 días | Se usa como divisor convencional del sueldo mensual, aunque el mes del calendario tenga 28, 29 o 31 días. Ejemplo: 1,800 ÷ 30 = S/ 60 por día. Es la convención exigida para estos casos. |
| Jornada: 8 horas | Es la jornada que asume el laboratorio para obtener el valor hora. Después de calcular el valor diario, se divide entre 8. No se pide la jornada real del trabajador en esta versión. |
| Factor 1.25 | Representa el pago completo de una hora extra más 25% de recargo: 100% + 25% = 125% = 1.25. Multiplicar solo por 0.25 pagaría únicamente el recargo. |
| Factor 1.35 | Representa la hora completa más 35% de recargo: 100% + 35% = 135% = 1.35. El archivo recibe las horas ya clasificadas por tramo. |
| AFP Ejemplo | Es un perfil académico, no una AFP real. Fondo 10%, comisión 1.60% y seguro 1.35% son los valores que exige la guía para los casos 3 y 4. No deben sustituirse antes de demostrar los resultados de referencia. |
| AFP reales | Son referencias de modalidad de flujo con fecha de consulta indicada en el libro. Las tasas pueden cambiar; deben revisarse para otro periodo. La comisión sobre saldo no se agrega como si fuera otra comisión mensual sobre el sueldo. |
| Parámetros centralizados | Los números se guardan aquí para evitar repetirlos en cada fórmula. Así se puede seguir su origen y actualizar una regla desde un solo lugar. Cambiar un parámetro puede cambiar todas las boletas que lo utilizan. |

## Hoja Boleta: explicación de las entradas

| Celda | Texto explicativo |
| --- | --- |
| B4: básico | Escribe el sueldo mensual completo pactado, antes de descuentos. Si hay faltas, no reduzcas aquí el básico: el cálculo lo ajusta con los días de B5. Por ejemplo, ingresa 1,800 y 27 días, no 1,620 y 27 días. |
| B5: días | Indica los días que reconoce el modelo, de 1 a 30. Un mes completo se ingresa como 30. Los días no equivalen únicamente a asistencias físicas: el sueldo mensual también comprende descansos remunerados. Este archivo no clasifica licencias, descansos médicos ni otras incidencias. |
| B6: hijos | Sí activa la asignación familiar de S/ 123 con los parámetros iniciales. No la multiplica por la cantidad de hijos ni la reduce por días. En una planilla real se deben acreditar los requisitos del beneficio. |
| B7: ONP o AFP | Selecciona el sistema de pensiones. Solo se calcula uno de los dos. Esta opción no cambia el régimen laboral del trabajador ni sus derechos a CTS o gratificación. |
| B8: AFP | Selecciona qué fila de tasas utilizar. Solo interviene cuando B7 es AFP; si B7 es ONP, la AFP seleccionada no genera descuento. Usa Ejemplo para reproducir los casos del profesor. |
| B9: HE25 | Escribe la cantidad de horas extras que corresponden al tramo de 25%, no su importe en soles. Las primeras dos horas extras de cada jornada se clasifican en este tramo. |
| B10: HE35 | Escribe las horas extras posteriores a las dos primeras de cada jornada. Cuatro horas extras en un día se separan en 2 al 25% y 2 al 35%; dos horas en cada uno de dos días son 4 al 25%. |
| B11: adelanto | Es dinero que el trabajador ya recibió. Se resta del depósito pendiente, pero no reduce las remuneraciones generadas ni la base previsional del ejercicio. Usa 0 si no hubo adelanto. |
| B13: validación | OK significa que las entradas cumplen las reglas. Si hay datos inválidos, los resultados quedan vacíos. La revisión evita calcular con días 31, sueldo cero, texto o valores no permitidos, incluso si se pegaron datos. |

## Hoja Boleta y Explicación: por qué hacemos cada cálculo

| Celda | Cálculo y motivo | Ejemplo fijo para aprender |
| --- | --- | --- |
| B17 | Básico ÷ 30 × días. Primero obtenemos el valor diario y después reconocemos los días del modelo. Las faltas ya están reflejadas aquí; no se descuentan otra vez. | 1,800 ÷ 30 × 27 = S/ 1,620. |
| B18 | Si corresponde, RMV × 10%. Se añade porque es un ingreso remunerativo incluido por la guía. Su importe depende de la RMV del perfil, no del sueldo básico. | 1,230 × 10% = S/ 123 completos. |
| B19 | Básico ÷ 30 ÷ 8 × 1.25 × HE25. Convertimos el sueldo mensual a valor hora y pagamos la hora completa con recargo. | 3,000 ÷ 30 ÷ 8 = 12.50; 12.50 × 1.25 × 4 = S/ 62.50. |
| B20 | Básico ÷ 30 ÷ 8 × 1.35 × HE35. El segundo tramo tiene una sobretasa mayor. | 12.50 × 1.35 × 4 = S/ 67.50. |
| B21 | Sumamos sueldo computable, asignación y ambos tramos de horas extras. Es lo generado antes de descuentos y la base de pensión y EsSalud del laboratorio. | 3,000 + 123 + 62.50 + 67.50 = S/ 3,253. |
| B22 | Total de remuneraciones × 13%, solo con ONP. El aporte se calcula sobre lo remunerativo incluido, no sobre el neto. | 3,253 × 13% = S/ 422.89. Con AFP, esta fila vale 0. |
| B23 | Total × tasa de fondo de la AFP seleccionada. Representa el aporte al fondo previsional. | Con AFP Ejemplo: 3,253 × 10% = S/ 325.30. |
| B24 | Total × comisión de la AFP seleccionada. Se presenta aparte porque corresponde a administración, no al ahorro del fondo. | 3,253 × 1.60% = 52.048; se redondea a S/ 52.05. |
| B25 | Total × prima de seguro de la AFP seleccionada. Se separa para distinguir la cobertura previsional de fondo y comisión. | 3,253 × 1.35% = 43.9155; se redondea a S/ 43.92. |
| B26 | Se toma el adelanto ingresado sin aplicarle tasas. Lo retiramos del pago pendiente porque ya se entregó. | Si recibió S/ 200 antes, ahora se descuentan esos S/ 200 del depósito pendiente. |
| B27 | Se suman las retenciones previsionales aplicables y el adelanto. Las filas del sistema no elegido quedan en cero. | AFP Ejemplo: 325.30 + 52.05 + 43.92 + 200 = S/ 621.27. |
| B28 | Remuneraciones menos descuentos. Indica cuánto falta pagar, después de considerar la pensión y el adelanto. | 3,253 − 621.27 = S/ 2,631.73. |
| B29 | Total de remuneraciones × 9%. Se muestra aparte porque lo financia el empleador. | 3,253 × 9% = S/ 292.77; no se resta de B28. |
| B30 | Remuneraciones más EsSalud. Muestra el costo simplificado que pide la actividad. No es el costo anual completo. | 3,253 + 292.77 = S/ 3,545.77. |

## Notas para comprender las fórmulas

- Los ejemplos anteriores son fijos: explican los casos originales y no representan necesariamente los datos que se hayan ingresado después.
- SI decide si corresponde un concepto. SUMA reúne importes. BUSCARV busca las tasas de la AFP elegida. REDONDEAR fija el importe de cada concepto en dos decimales. FORMULATEXTO permite leer la operación que hay detrás de un resultado.
- Los nombres RMV, DiasMes o TasaONP apuntan a celdas de Parámetros. Los signos $ fijan una referencia para que no se desplace al copiar la fórmula.
- Cada concepto se redondea antes de sumar. Mostrar dos decimales con formato no equivale a redondear el número utilizado en operaciones.
- El valor hora conserva precisión hasta calcular el importe del tramo. El doble ROUND de algunas fórmulas estabiliza residuos numéricos; no añade un descuento ni una regla laboral.
- La guía calcula el valor hora solo desde el básico. Esta es una simplificación del proyecto; no debe confundirse con todas las reglas de una planilla real.

## Hoja Casos: qué demuestra cada escenario

| Caso | Qué observar y por qué |
| --- | --- |
| 1 | Aísla la lógica básica: mes completo, sin asignación ni extras. S/ 2,500 menos ONP de S/ 325 deja S/ 2,175. Permite explicar pensión y EsSalud sin conceptos adicionales. |
| 2 | Explica días incompletos y asignación completa. Con 27 días, básico 1,800 e hijos, el neto es S/ 1,516.41. Con 30 días sube a S/ 1,673.01: la diferencia neta de S/ 156.60 es menor a S/ 180 porque también aumenta ONP. |
| 3 | Reúne AFP, asignación, ambos tramos de horas extras y adelanto. Permite seguir el cálculo completo hasta el neto de S/ 2,631.73. |
| 4 | Combina días incompletos, AFP, extras y adelanto. El neto calculado es S/ 3,011.17. La guía no publica respuesta oficial para este caso; se presenta para revisión del docente. |
| Caso propio | Usa el sueldo documentado de una oferta con supuestos académicos explícitos. Permite aplicar el procedimiento a otro monto sin atribuir esa liquidación a la empresa anunciante. |
| Sensibilidades | Son escenarios calculados para observar qué cambia al modificar entradas. No son boletas reales proporcionadas por compañeros. |
| Control de resultados | La diferencia entre el neto calculado y el de referencia debe ser cero en los casos oficiales, manteniendo el perfil original. Si se cambia una tasa, esa coincidencia puede dejar de existir. |

## Alcance del archivo

El libro explica la boleta mensual simplificada de los niveles 1 y 2. No calcula CTS, gratificaciones, vacaciones, impuesto de quinta categoría ni cambios de régimen laboral. Tampoco clasifica ausencias o aplica todas las bases y topes de una planilla real. Esos conceptos requieren información y reglas adicionales; no deben agregarse sin más a la base mensual porque pueden tener un tratamiento distinto.

ONP/AFP es el sistema de pensiones; régimen general, microempresa y pequeña empresa son regímenes laborales. Seleccionar AFP no modifica el régimen laboral. Los valores de prueba y las fuentes ya documentadas se conservan.
