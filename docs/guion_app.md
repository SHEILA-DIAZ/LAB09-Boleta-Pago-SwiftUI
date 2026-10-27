# Guion de exposición individual · Parte 2: SwiftUI

Duración sugerida: 7–9 minutos. La demostración del simulador requiere macOS y Xcode; ensayar los pasos antes de exponer. No presentar capturas ni ejecuciones que aún no se hayan realizado.

## 0:00–1:00 · Pantalla y requisitos

“La app tiene una sola pantalla. Arriba ingresamos el mes y al pulsar Calcular mostramos la boleta debajo. ScrollView permite recorrer todo el contenido. El título dice Boleta de ejemplo y no pedimos DNI ni RUC reales.”

Señalar `Text`, `VStack`, `HStack`, `TextField`, `Picker`, `Button` y el estado `@State`. Los modificadores cambian estilo o teclado, sin introducir otro flujo de navegación. Los datos del cálculo permanecen separados de SwiftUI.

## 1:00–2:00 · Modelo

Abrir `App/Model/Boleta.swift`:

“DatosBoleta es un struct que contiene las entradas. TasasAFP representa las tres tasas. Parametros.afps es el diccionario de AFP. Concepto y ResultadoBoleta representan la boleta; las remuneraciones, descuentos y aportes son arrays. La clase Boleta valida y calcula. La pantalla solo transforma textos en datos y muestra el resultado.”

“Usamos Decimal para los cálculos monetarios y NSDecimalRound con .plain a dos decimales. No usamos el texto formateado para calcular ni redondeamos anticipadamente el valor hora.”

## 2:00–3:00 · Validación

Mostrar sueldo 0 o días 31 y pulsar Calcular: debe aparecer el error y desaparecer el resultado anterior. Probar texto vacío, `abc`, negativos y separadores de miles. Después restaurar valores correctos.

“Se admite punto o coma decimal, sin miles, con hasta dos decimales. Los días son enteros de 1 a 30 y las horas y adelantos no son negativos. El modelo vuelve a validar aun si se llama sin la interfaz. Cuando algo falla no calculamos una boleta parcial.”

## 3:00–4:00 · Nivel 1

Caso 1: sueldo 2500, 30 días, sin hijos, ONP, HE y adelantos 0. “Remuneraciones 2,500; ONP 325; neto 2,175; EsSalud 225 adicional. Las filas AFP permanecen visibles en cero.”

Caso 2: sueldo 1800, 27 días, con hijos. “La asignación de 123 no se prorratea. Total 1,743; ONP 226.59; neto 1,516.41. Las faltas ya se reflejan en 27 días.”

## 4:00–5:15 · Nivel 2

Caso 3: sueldo 3000, 30 días, con hijos, AFP Ejemplo, 4 y 4 horas, adelanto 200. “Al elegir AFP aparece el Picker de AFP. El fondo, comisión y seguro suman 421.27; con adelanto suman 621.27; el neto es 2,631.73. La ONP queda en cero.”

Caso 4: sueldo 4200, 24 días, hijos, AFP Ejemplo, 2 y 2 horas, adelanto 100. Mostrar remuneraciones 3,574; descuentos 562.83; neto 3,011.17 y EsSalud 321.66. Comparar con la fila de Excel.

## 5:15–6:15 · Pruebas reales

“El mismo archivo del modelo que se usa en Xcode forma el módulo BoletaCore en Swift Package Manager. En Windows compilamos y ejecutamos el verificador, sin SwiftUI: 276 comprobaciones sobre 16 escenarios. Además de los cuatro casos, revisamos AFP reales, días incompletos, coma decimal, rechazo de entradas y redondeo de medio centavo. El detalle está en evidencias.”

Precisar el estado real del simulador: solo afirmar que corrió en iOS después de realizarlo en un Mac. La compilación del modelo en Windows no verifica las vistas ni la firma de la app.

## 6:15–7:30 · Arquitectura, límites y cierre de la demostración

“EsSalud está en el array de aportaciones, separado de los descuentos, para evitar restarlo al trabajador. El resultado muestra los datos del último cálculo: editar el formulario requiere pulsar Calcular de nuevo. Si hay un error en ese nuevo cálculo, se retira el resultado anterior.”

“La AFP Ejemplo conserva las tasas de la guía; las opciones de AFP reales están fechadas y son de flujo. No aplicamos comisión de saldo, tope del seguro, base mínima de EsSalud ni renta de quinta. El nivel 3 es opcional: no se ha implementado comparación simultánea en pantalla, encabezado de trabajador/empresa ni cálculo de quinta.”

Preguntas previsibles: por qué Decimal, dónde cambiar tasas, por qué asignación no depende de días, qué pasa si el adelanto produce neto negativo y cómo reproducir los casos. Mostrar el README como guía de ejecución y la matriz de requisitos como evidencia de cobertura.
