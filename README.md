# Semana 9 · Boleta de pago: del sueldo al neto

Laboratorio de Programación en Móviles Avanzado, guía del profesor León `Actividad_Grupo_B.docx`. Incluye aplicación SwiftUI de una pantalla, modelo Swift separado, libro Excel de cuatro hojas y análisis. **Niveles 1 y 2 desarrollados; nivel 3 opcional, no implementado.**

La guía original, sus nueve tablas y la extracción completa están en [referencias](referencias/guia_extraida.md). Se revisó todo el contenido del DOCX; su contador de páginas no figura en metadatos. El proyecto se creó en `LAB09-Boleta-Pago-SwiftUI`, que inicialmente solo contenía `.git`, sin desarrollo previo ni commits.

## Abrir los entregables

- Aplicación iOS: [BoletaPago.xcodeproj](BoletaPago.xcodeproj/project.pbxproj).
- Excel funcional: [Boleta_Pago_Semana09.xlsx](Excel/Boleta_Pago_Semana09.xlsx).
- Cinco respuestas y caso 4: [análisis](docs/analisis.md).
- Parámetros, fuentes y fechas: [fuentes](docs/fuentes.md).
- Cobertura de la guía: [matriz de requisitos](docs/requisitos.md).
- Exposición: [guion Excel](docs/guion_excel.md) y [guion SwiftUI](docs/guion_app.md).
- Evidencias reales y pendientes: [registro](evidencias/README.md).

## Cómo ejecutar la app en macOS

Requisitos: Xcode 15 o superior con SDK iOS 17 o superior. Sin librerías externas. El paquete del modelo requiere Swift 5.9 o posterior; se comprobó con Swift 6.4 en Windows. Copiar o clonar el repositorio en un Mac y abrir **BoletaPago.xcodeproj**, no `Package.swift`, para ejecutar la interfaz.

1. Elegir el esquema compartido **BoletaPago** y un simulador iPhone con iOS 17 o superior.
2. Pulsar Run. En simulador no se requiere configurar una cuenta de firma.
3. Para un iPhone físico, seleccionar un equipo de desarrollo en Signing & Capabilities y un identificador de paquete disponible.
4. Introducir uno de los casos de la tabla siguiente, pulsar **Calcular** y desplazarse a los tres bloques y el neto.

Comprobación de compilación para quien disponga de Mac:

```bash
xcodebuild -list -project BoletaPago.xcodeproj
xcodebuild -project BoletaPago.xcodeproj -scheme BoletaPago -configuration Debug -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO build
```

La interfaz SwiftUI, la compilación iOS, el simulador, accesibilidad y firma **requieren verificación en macOS**. No se atribuyen esas pruebas al verificador de Windows. No hay capturas de iOS inventadas.

## Usar el Excel

Abrir `Excel/Boleta_Pago_Semana09.xlsx` con Excel 2016 o superior; no utiliza macros ni conexiones externas. Se recomienda Microsoft 365 o una versión reciente por `FORMULATEXT`. Activar cálculo automático y, si hace falta, `Ctrl+Alt+F9` para recálculo completo.

1. **Parámetros:** tasas y constantes en celdas amarillas; AFP Ejemplo separada de las AFP reales de flujo; fuentes y fechas en la misma hoja.
2. **Boleta:** entradas editables `B4:B11`, validación en `B13`, resultados con fórmulas `B17:B30`, fórmula visible al lado en columna C. La pantalla inicial corresponde al caso 1.
3. **Casos:** cuatro casos de la guía, oferta propia, sensibilidades y pruebas adicionales. Columnas `J:W` contienen fórmulas, `X:Y` contrastan netos oficiales 1–3 y `Z` muestra neto/remuneraciones. Al final hay espacios para incorporar datos reales de compañeros.
4. **Explicación:** las 14 fórmulas en palabras, con ejemplos numéricos y su expresión Excel. Las cinco preguntas están desarrolladas en el archivo de análisis enlazado arriba.

Las funciones del XLSX se guardan en inglés según el formato estándar; Excel en español las presenta como SI, REDONDEAR, SUMA y BUSCARV. Las celdas de cálculo no son importes pegados: contienen fórmulas. Los valores en caché permiten previsualizarlas; esa caché por sí sola no constituye evidencia de recálculo.

## Casos para demostrar

Todos usan AFP **Ejemplo** cuando corresponde y RMV **S/ 1,230.00**.

| Caso | Básico | Días | Hijos | Sistema | HE25 | HE35 | Adelanto | Remuneraciones | Descuentos | Neto | EsSalud |
| --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2,500 | 30 | No | ONP | 0 | 0 | 0 | 2,500.00 | 325.00 | **2,175.00** | 225.00 |
| 2 | 1,800 | 27 | Sí | ONP | 0 | 0 | 0 | 1,743.00 | 226.59 | **1,516.41** | 156.87 |
| 3 | 3,000 | 30 | Sí | AFP | 4 | 4 | 200 | 3,253.00 | 621.27 | **2,631.73** | 292.77 |
| 4 | 4,200 | 24 | Sí | AFP | 2 | 2 | 100 | 3,574.00 | 562.83 | **3,011.17** | 321.66 |

Los casos 1–3 coinciden con respuestas oficiales de la guía; el 4 es nuestro cálculo para revisión del docente. Las pruebas comparan cada concepto, incluidos los ceros no aplicables, y no solo el neto.

## Diseño del cálculo

`DatosBoleta`, `TasasAFP`, `Concepto` y `ResultadoBoleta` son structs; `Boleta` es la clase calculadora. `Parametros.afps` es un diccionario; remuneraciones, descuentos y aportaciones son arrays. El archivo del modelo es el mismo que se compila en el paquete de pruebas y en el proyecto iOS.

La vista usa Text, VStack, HStack, @State, TextField, Picker, Button y ScrollView. El Picker de AFP solo aparece para AFP. Se muestran los tres bloques uno debajo del otro, ceros para conceptos no aplicables y el neto. Un error retira el resultado anterior. El resultado válido incluye los datos usados en el último cálculo para distinguirlo del formulario que se esté editando.

Reglas comunes:

- Sueldo computable = básico / 30 × días. Asignación = 10% RMV si hay hijos, sin prorrateo.
- Valor hora = básico / 30 / 8, conservando precisión. Cada tramo de HE multiplica por 1.25 o 1.35 y sus horas.
- Redondear cada concepto a dos decimales, luego sumar remuneraciones.
- ONP = 13% del total remunerado; AFP = fondo, comisión de flujo y seguro, cada uno redondeado por separado sobre ese total.
- Descuentos = pensión + adelanto; neto = remuneraciones − descuentos.
- EsSalud = 9% de remuneraciones, pagado por el empleador y separado del neto.

Swift usa Decimal y redondeo `.plain`, equivalente al criterio de mitades de `ROUND` para estos importes. El Excel recibe valores numéricos con hasta dos decimales; Swift admite coma o punto y rechaza separadores de miles, texto vacío, notación científica y negativos. Días enteros 1–30; sueldo > 0; HE y adelantos ≥ 0. Los límites técnicos son montos de 100 millones y horas de 10 mil por tramo, con dos decimales. El neto negativo se muestra con aviso, sin recortarlo.

No se calcula renta de quinta, no se descuentan faltas nuevamente, ni se aplican bases mínimas de EsSalud o topes del seguro: son exclusiones de la guía simplificada. Las opciones AFP reales son tasas de flujo SBS fechadas al 26/10/2026 y requieren actualización para otro período. El reto opcional de nivel 3 incluye encabezado de trabajador/empresa ficticios, comparación ONP/AFP simultánea **en la pantalla** e impuesto de quinta; no se ha mezclado con el alcance principal.

## Pruebas y reproducción en Windows

Ejecutar desde la raíz. Se necesita Swift y su toolchain de Windows correctamente instalado para el modelo, y Python 3.10 o superior para los scripts. Las dependencias de Excel se instalan dentro de `.tools`, excluido de Git:

```powershell
python -m pip install --target .tools -r requirements.txt
swift run VerificarBoleta
python -X utf8 scripts\evaluar_formulas.py
python -X utf8 scripts\verificar.py
```

Para regenerar el libro, fixtures y estructura Xcode:

```powershell
python -X utf8 scripts\generar.py
```

El script sin argumento conserva la referencia original. Con una ruta DOCX, además copia la guía, extrae cuerpo/tablas/encabezados/pies y registra su hash. **Regenerar sobrescribe el Excel generado y restablece las entradas de ejemplo**, por lo que debe guardarse aparte cualquier edición manual que interese conservar. También restablece cachés y exige repetir la evaluación de fórmulas y las pruebas.

Intento de recálculo nativo en una sesión de Office operativa:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\recalcular_excel.ps1
python -X utf8 scripts\verificar.py
```

El estado real de cada motor figura en [evidencias](evidencias/README.md). El script COM utiliza una instancia oculta de Excel y prueba todos los casos tanto en `Casos` como en el formulario `Boleta`; no necesita abrir una ventana visible. No se debe afirmar que pasó si solo se dispone de los valores cacheados.

`evaluar_formulas.py` lee y evalúa las fórmulas reales del XLSX con el motor independiente `formulas`, sin usar la caché. Contrasta 14 importes en `Casos` y en `Boleta` para 16 escenarios, entradas inválidas y propagación de un cambio de RMV. Esto comprueba la aritmética y dependencias del libro; no sustituye la revisión visual ni la ejecución nativa de Excel.

Para evitar que un residuo binario transforme 1.255 en 1.2549999999999999, las divisiones de sueldo y HE se llevan a céntimos: `ROUND(ROUND(importe*100,8),0)/100`. Se normalizan residuos a ocho decimales de céntimo y se redondea el concepto a céntimos enteros. No se redondea el valor hora por separado. El caso adicional de medio centavo comprueba esta decisión; las fórmulas y el modelo conservan los resultados oficiales.

## Organización

```text
App/                         App SwiftUI y Model/Boleta.swift
BoletaPago.xcodeproj/         Proyecto iOS y esquema compartido
Package.swift                Paquete del mismo modelo para Windows/macOS
Tests/                       Fixtures y verificador Swift
Excel/                       Libro listo para abrir
scripts/                     Generación y verificaciones reproducibles
docs/                        Análisis, fuentes, requisitos y dos guiones
referencias/                 Word original y extracción
evidencias/                  Resultados reales y verificaciones pendientes
```

## Pendientes de entrega que requieren otras personas o equipos

Ejecutar y revisar la app en Xcode; obtener capturas reales de casos 1–4 y de una validación; verificar visualmente el libro en una sesión funcional de Excel; completar el caso propio del segundo participante y comparar con dos compañeros usando sus ofertas y resultados reales. Las sensibilidades incluidas no se atribuyen a compañeros.

El repositorio mantiene el remoto `https://github.com/SHEILA-DIAZ/LAB09-Boleta-Pago-SwiftUI`. Se preparan hitos locales; **no se ha hecho push a GitHub**. La publicación remota queda para una instrucción posterior.
