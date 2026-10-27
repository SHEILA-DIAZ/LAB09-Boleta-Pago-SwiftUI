# Evidencias y límites de verificación

Las evidencias son archivos producidos por herramientas o transcripciones identificadas de sus salidas. No hay capturas de iOS inventadas ni afirmación de compilación de la interfaz en Windows.

| Evidencia | Qué comprueba |
| --- | --- |
| `documento.json` | Ruta de origen, hash SHA-256 y lectura de nueve tablas del Word original |
| `../referencias/guia_extraida.md` | Extracción completa en orden del cuerpo del documento y partes auxiliares |
| `swift_resultados.json` | 276 comprobaciones del modelo, 16 escenarios y sus 14 importes |
| `swift_ejecucion.txt` | Transcripción de la ejecución real Swift 6.4 Windows y advertencias del toolchain |
| `formulas_recalculadas.json` | Resultados realmente evaluados desde fórmulas XLSX por `formulas`; no son la caché ni Excel nativo |
| `pruebas_python.txt` | Resultado de la suite de integridad, respuestas oficiales y cruces entre motores |
| `excel_com_intentos.txt` | Intentos fallidos de automatización de Microsoft Excel y HRESULT recibidos |

## Qué se considera validado

Los casos 1–3 tienen respuestas oficiales en la guía; el caso 4 es calculado por el proyecto. El verificador compara todos los conceptos y los tres netos oficiales. El modelo compiló y se ejecutó en Windows con Swift 6.4. La interfaz SwiftUI utiliza ese mismo archivo del modelo, pero su compilación iOS y presentación visual requieren Xcode.

Estado final: 276 comprobaciones Swift aprobadas; 448 importes recalculados aprobados (16 escenarios × 14 conceptos × 2 hojas); 12 entradas inválidas bloqueadas y cambio de RMV propagado. El parseo sintáctico de los tres archivos Swift pasó con código 0; no equivale a compilación SwiftUI. La suite Python ejecuta 9 pruebas: 8 aprobadas y 1 omitida por Excel COM no disponible.

La evaluación del libro con `formulas` lee sus fórmulas reales y recalcula resultados, tanto en `Casos` como en el formulario `Boleta`. Comprueba también el bloqueo por entradas inválidas y un cambio de RMV que debe propagarse. `FORMULATEXT`, estilos, diálogos, impresión y controles visuales quedan fuera del alcance de ese motor. La suite distingue una comprobación de caché de un recálculo real.

## Diferencia de redondeo encontrada y corregida

En un caso adicional, sueldo 240.96 con una hora extra al 25%, el importe matemático del tramo es 1.255. Swift Decimal redondeó a 1.26. El motor de fórmulas, al evaluar divisiones con coma flotante, obtenía 1.2549999999999999 y lo redondeaba a 1.25, con diferencia de un céntimo en remuneraciones y neto. Los cuatro casos de la guía no presentaban esa diferencia.

Se modificaron las fórmulas de sueldo computable y HE de ambas hojas para normalizar el importe completo en céntimos y redondear a céntimos enteros: `ROUND(ROUND(importe*100,8),0)/100`. El valor hora no se redondea anticipadamente. Se volvió a evaluar el libro. Los resultados finales y el estado de las comprobaciones constan en los archivos estructurados; no se corrigió ningún resultado pegando un valor ni se alteró el evaluador para hacerlo coincidir.

## Excel nativo

Excel está instalado. La automatización COM falló primero por sesión de inicio inexistente (0x80070520) y luego por llamada rechazada (0x80010001). No existe evidencia de recálculo nativo exitoso y esa comprobación se marca como omitida. El primer libro `Excel/Boleta_Semana09.xlsx` quedó bloqueado por la sesión de Office: se conserva sin borrarlo, excluido de Git. **El entregable final es `Excel/Boleta_Pago_Semana09.xlsx`**. No se terminaron procesos de Office del usuario para liberar la primera versión.

El script COM ahora guarda el primer error y protege el cierre de la instancia. Puede repetirse en una sesión de Office funcional; si tiene éxito produce `excel_recalculado.json`, que la suite contrasta con los mismos escenarios. La inspección visual debe realizarse abriendo el libro final, con cálculo automático, verificando la barra de fórmulas y las cuatro hojas.

## Pendientes verificables en un Mac

1. Abrir el proyecto Xcode y ejecutar la compilación indicada en el README.
2. Ejecutar los casos 1–4 en un simulador y comprobar cifras, desplazamiento, Picker AFP y etiquetas en cero.
3. Probar errores, coma decimal, teclado y cambio de tamaño de texto en iPhone e iPad.
4. Capturar formulario, cada caso y un mensaje de validación. Añadir aquí capturas reales y enlazarlas en el README.
5. Si se prueba en dispositivo, configurar firma y registrar versión de Xcode, iOS y dispositivo utilizado.

## Pendientes externos de análisis

Registrar el caso propio del segundo participante y comparar con dos compañeros que proporcionen oferta, fecha, sueldo y boleta. Los escenarios de sensibilidad incluidos son cálculos del proyecto y no evidencia de trabajos de compañeros. La localización del índice oficial de la RMV no equivale a haber leído íntegramente el decreto individual; el alcance está descrito en `docs/fuentes.md`.
