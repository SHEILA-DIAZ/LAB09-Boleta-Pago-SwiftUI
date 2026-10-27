# Cómo funciona el código, explicado desde cero

El programa calcula cuánto le falta cobrar a un trabajador al final del mes. Recibe su sueldo y los datos del mes, suma lo ganado, resta pensión y adelantos y muestra el neto. El aporte de EsSalud se muestra aparte porque lo paga la empresa.

Hay dos partes principales: **la pantalla recoge y muestra datos; el modelo realiza los cálculos**. El Excel hace las mismas operaciones para poder revisar los resultados.

## En qué orden leer los archivos

1. [BoletaPagoApp.swift](../App/BoletaPagoApp.swift): inicia la aplicación y abre la pantalla.
2. [ContentView.swift](../App/ContentView.swift): dibuja el formulario, recibe lo escrito y muestra la boleta.
3. [Boleta.swift](../App/Model/Boleta.swift): contiene los datos, parámetros, validaciones y fórmulas.
4. [main.swift del verificador](../Tests/Verifier/main.swift): prueba el modelo con entradas y resultados esperados.

Los comentarios `//` y `///` están dentro de esos archivos. Sirven para explicar el código a quien lo lee; no son instrucciones que ejecute la aplicación.

## Qué sucede al pulsar Calcular

Por ejemplo, escribes `2500` en sueldo, `30` en días, seleccionas sin hijos y ONP, y dejas horas y adelantos en cero:

1. El formulario guarda `"2500"` y `"30"` como **texto**. Las comillas indican que todavía no son números para operar.
2. El botón llama a la función `calcular()` de `ContentView`.
3. `Entrada.datos(...)` convierte el sueldo a `Decimal` y los días a `Int`. Rechaza textos como `abc` y comprueba las reglas.
4. La pantalla llama a `Boleta().calcular(datos)` y le entrega un `DatosBoleta` con todas las entradas.
5. El modelo obtiene sueldo computable 2,500 / 30 × 30 = 2,500.00; ONP 2,500 × 13% = 325.00; neto 2,500 − 325 = 2,175.00. EsSalud es 225.00 y se informa aparte.
6. El modelo devuelve `ResultadoBoleta`, con las filas de los tres bloques.
7. La pantalla guarda ese resultado en `@State`. SwiftUI actualiza lo visible y muestra la boleta debajo del botón.

Si alguna entrada falla, `throw` envía un error y `catch` lo recibe. Entonces aparece un mensaje en rojo y no se muestra una boleta calculada con esos datos.

## Palabras que verás en Swift

| Código | Qué significa en este proyecto |
| --- | --- |
| `import SwiftUI` | Permite construir la pantalla de la app. |
| `import Foundation` | Permite usar Decimal, formateadores y otras herramientas del modelo. |
| `struct` | Agrupa datos relacionados. `DatosBoleta` reúne sueldo, días, hijos, pensión, horas y adelantos. |
| `class Boleta` | Define la calculadora que valida los datos y obtiene los importes. |
| `enum Sistema` | Limita el sistema de pensiones a ONP o AFP. |
| `enum Parametros` | Reúne las constantes y tasas para encontrarlas en un solo lugar. |
| `let` | Define un valor que no se reasigna. |
| `var` | Define un valor que puede cambiar. |
| `String` | Texto: por ejemplo `"2500"` o `"Ejemplo"`. |
| `Int` | Número entero, como los días laborados. |
| `Bool` | Un valor verdadero o falso; representa Sí/No para hijos. |
| `Decimal` | Número decimal usado para las operaciones de dinero y horas. |
| `@State` | Hace que SwiftUI conserve una variable de la pantalla y actualice lo visible cuando cambie. |
| `$sueldo` | Conecta el campo con la variable: leer o escribir en el campo utiliza ese estado. |
| `Binding<String>` | Es esa conexión para leer y modificar un texto desde una vista auxiliar. |
| `func` | Define una función, una tarea que se puede ejecutar por su nombre. |
| `static` | Permite usar una propiedad o función del tipo sin crear una instancia, como `Parametros.rmv`. |
| `self.sueldo` | Señala la propiedad sueldo del objeto o estructura actual. |
| `private` | Limita el acceso a una parte interna, como las funciones auxiliares de la vista. |
| `public` | Permite que el verificador use el modelo desde otro módulo. |
| `guard` | Comprueba una condición necesaria; si falla, sale de esa función. |
| `throws`, `try`, `catch` | Indican, ejecutan y manejan respectivamente una operación que puede fallar. |
| `?` al final de un tipo | Permite que todavía no exista un valor. `resultado` puede ser `nil` antes de calcular. |
| `if let` | Permite usar un valor opcional solo cuando existe. |
| `condición ? A : B` | Elige A si la condición es verdadera y B si es falsa. |
| `[Concepto]` | Un array: una lista ordenada de filas de la boleta. |
| `[String: TasasAFP]` | Un diccionario: busca las tasas a partir del nombre de una AFP. |
| `reduce` | En este modelo suma los montos de las filas para obtener un total. |
| `map` | En las pruebas toma cada fila y extrae su monto para compararlo. |
| `!` después de un valor | Fuerza a usar un opcional; se reserva aquí para constantes controladas o datos comprobados previamente. No significa que sea válido cualquier texto ingresado. |

## Qué hace cada control de la pantalla

- `Text`: muestra títulos, etiquetas y resultados.
- `TextField`: permite escribir sueldo, días, horas y adelantos.
- `Picker`: permite elegir hijos, ONP/AFP y la AFP correspondiente.
- `Button`: ejecuta el cálculo cuando lo pulsas.
- `VStack`: ordena elementos verticalmente.
- `HStack`: coloca el nombre y monto de una fila uno junto al otro.
- `ScrollView`: permite desplazarte porque formulario y boleta no caben completos en la pantalla.

Los modificadores como `.font`, `.padding` y `.foregroundStyle` cambian la presentación. `.keyboardType` sugiere un teclado, pero no reemplaza la validación.

## Qué contiene Boleta.swift

| Parte | Responsabilidad |
| --- | --- |
| `Dinero` | Redondear los conceptos y dar formato a los montos al mostrarlos. |
| `TasasAFP` | Guardar fondo, comisión y seguro de una AFP. |
| `Parametros` | Guardar RMV, porcentajes, jornada y diccionario de AFP. |
| `Sistema` | Representar ONP o AFP. |
| `DatosBoleta` | Guardar las entradas ya convertidas a tipos numéricos. |
| `Concepto` | Representar una fila con nombre y monto. |
| `ResultadoBoleta` | Reunir arrays de remuneraciones, descuentos y aportaciones, y obtener sus totales. |
| `ErrorEntrada` | Transportar un mensaje de validación que la pantalla pueda mostrar. |
| `Entrada` | Convertir los textos del formulario a datos numéricos. |
| `Boleta` | Validar las reglas y calcular los conceptos. |

La división evita escribir las fórmulas dentro del botón o repetirlas en la pantalla. Si se cambia la tasa ONP, se busca en `Parametros`; si se cambia el aspecto, se trabaja en `ContentView`.

## Tres decisiones que debes poder explicar

**Redondeo por concepto:** el caso 3 tiene comisión AFP 52.048, que se redondea a 52.05, y seguro 43.9155, que pasa a 43.92. Después se suman. No basta con dar formato de dos decimales al resultado final.

**EsSalud separado:** su monto se guarda en aportaciones, no en descuentos. Así no se resta del sueldo que recibe el trabajador.

**AFP Ejemplo separada de las reales:** para los casos del profesor se usan exactamente las tasas de prueba de la guía. Las otras AFP muestran tasas de flujo consultadas y fechadas en fuentes. No deben confundirse con una planilla legal completa.

## Para qué sirven los demás archivos de código

- `Package.swift`: indica cómo compilar el mismo modelo sin SwiftUI para probarlo en Windows. No es la pantalla iOS.
- `Tests/fixtures.json`: guarda entradas y resultados esperados de 16 escenarios. Los casos 1–4 son los de la guía; hay otros para revisar límites y redondeo.
- `Tests/Verifier/main.swift`: calcula esos escenarios, compara los conceptos y prueba entradas inválidas. Guarda los resultados en evidencias.
- `scripts/generar.py`: construye el Excel con fórmulas y el proyecto Xcode; también puede extraer el Word si se le pasa su ruta. Regenerarlo restablece el libro generado, así que se deben guardar aparte las ediciones manuales.
- `scripts/evaluar_formulas.py`: abre las fórmulas del Excel y las calcula con un motor independiente para compararlas con los resultados esperados.
- `scripts/verificar.py`: comprueba la estructura del libro, resultados oficiales, referencias de archivos y las evidencias de los distintos motores.
- `scripts/recalcular_excel.ps1`: intenta hacer la comprobación usando Excel instalado mediante automatización. En este equipo falló y quedó documentado.

## Una explicación breve para tu exposición

“Separé el proyecto en pantalla y modelo. La pantalla recoge los datos con TextField y Picker. Al pulsar Calcular, los textos se convierten a números y se validan. La clase Boleta calcula cada remuneración y descuento con redondeo a dos decimales; devuelve arrays de conceptos que la pantalla muestra en tres bloques. EsSalud va aparte y el neto es remuneraciones menos descuentos. El mismo modelo se prueba en Windows y se contrasta con las fórmulas del Excel.”

El modelo se ha compilado y probado en Windows. Para afirmar que la pantalla funciona en iOS todavía hay que abrir el proyecto en Xcode y ejecutarla en un Mac. Este documento describe cómo está programada; no sustituye esa verificación pendiente.
