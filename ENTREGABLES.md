# Dónde está cada entregable · Semana 9

Entrega individual de Sheila: **Boleta de pago: del sueldo al neto**. Los niveles 1 y 2 están implementados. El nivel 3 se distingue como reto opcional.

| Lo que pide la guía | Archivo o carpeta |
| --- | --- |
| Excel con Parámetros, Boleta, Casos y Explicación | **[Descargar el Excel final](Excel/Boleta_Pago_Semana09.xlsx)** |
| Aplicación SwiftUI, una pantalla | [Código de la pantalla](App/ContentView.swift) y [entrada de la app](App/BoletaPagoApp.swift) |
| Proyecto para abrir en Xcode | [BoletaPago.xcodeproj](BoletaPago.xcodeproj) |
| Modelo separado, structs, clase, AFP y arrays | [Boleta.swift](App/Model/Boleta.swift) |
| Cuatro casos y resultados por concepto | Hoja **Casos** del Excel y [casos automatizados](Tests/fixtures.json) |
| Respuestas a las cinco preguntas y desarrollo del caso 4 | [Análisis](docs/analisis.md) |
| Tabla de fuentes, parámetros y fechas de consulta | [Fuentes](docs/fuentes.md) y hoja **Parámetros** del Excel |
| Explicación paso a paso de las fórmulas | Hoja **Explicación** del Excel y [guion Excel](docs/guion_excel.md) |
| Guion para explicar la aplicación | [Guion SwiftUI](docs/guion_app.md) |
| Orden para presentar ambas partes tú sola | [Exposición individual](docs/exposicion_individual.md) |
| Explicación sencilla del código, paso a paso | [Cómo funciona el código](docs/explicacion_codigo.md) |
| Instrucciones de ejecución y organización | [README](README.md) |
| Lista de requisitos del profesor y su cobertura | [Matriz de requisitos](docs/requisitos.md) |
| Pruebas realizadas, evidencias y pendientes | [Registro de evidencias](evidencias/README.md) |
| Resultados reales del modelo Swift | [276 comprobaciones y 16 escenarios](evidencias/swift_resultados.json) |
| Evaluación de las fórmulas reales del Excel | [448 importes recalculados](evidencias/formulas_recalculadas.json) |
| Documento original del profesor | [Actividad_Grupo_B.docx](referencias/Actividad_Grupo_B.docx) |
| Lectura completa del Word, incluidas sus nueve tablas | [Guía extraída](referencias/guia_extraida.md) |

Para descargar el Excel desde GitHub, abre el enlace y utiliza **Download raw file** (icono de descarga). Para abrir la app en un Mac, descarga o clona el repositorio completo y abre `BoletaPago.xcodeproj`; no basta descargar un archivo Swift suelto.

El documento Word en `referencias` es la guía original. Las respuestas desarrolladas están en `docs/analisis.md`; las fórmulas editables están en el Excel.

## Qué queda por comprobar

La app requiere macOS/Xcode para compilar la interfaz, ejecutar el simulador y obtener capturas reales. El modelo sí compiló y pasó las pruebas en Windows. Las fórmulas del libro se recalcularon con un motor independiente; la automatización de Excel nativo falló y queda documentada. Falta revisar visualmente el libro en una sesión funcional de Excel.

La exposición está adaptada a una persona. La guía original menciona dos participantes y una comparación con dos compañeros; no se inventó esa interacción. Se incluye un caso propio con oferta real y dos sensibilidades identificadas como cálculos del proyecto.
