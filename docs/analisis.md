# Análisis · Semana 9

Perfil común de los casos de la guía: RMV S/ 1,230; asignación S/ 123; AFP Ejemplo fondo 10%, comisión 1.60%, seguro 1.35%. Cada concepto se redondea a dos decimales antes de sumar. Los adelantos ya pagados reducen el depósito de este mes. Los cálculos son la versión simplificada del laboratorio, sin renta de quinta ni bases mínimas de EsSalud.

## 1. ONP o AFP con los datos del caso 3

Las remuneraciones son S/ 3,253.00 en ambos sistemas. Con ONP se retienen S/ 422.89 (13%) y S/ 200.00 de adelanto: neto **S/ 2,630.11**. Con AFP Ejemplo se retienen S/ 325.30 de fondo, S/ 52.05 de comisión, S/ 43.92 de seguro y S/ 200.00 de adelanto: neto **S/ 2,631.73**.

AFP Ejemplo deja S/ 1.62 más este mes. Sus tasas de prueba suman 12.95%, frente al 13% de ONP, pero los tres componentes se redondean separadamente. El mayor neto inmediato no determina la mejor protección a largo plazo: deben evaluarse las condiciones para obtener una pensión, los aportes acumulados, la rentabilidad y riesgos del fondo, las comisiones, y la cobertura de invalidez y sobrevivencia. Las tasas ficticias de este ejercicio no permiten recomendar una afiliación real. La SBS distingue comisión sobre flujo y comisión sobre saldo; no se deben sumar ambas como descuentos mensuales sobre el sueldo. Véanse las [fuentes previsionales](fuentes.md).

## 2. Costo para la empresa

Para el caso 3, el costo mensual solicitado es remuneraciones más EsSalud: **3,253.00 + 292.77 = S/ 3,545.77**. El neto representa **2,631.73 / 3,545.77 × 100 = 74.2217%, aproximadamente 74.22%** de ese costo.

EsSalud lo financia el empleador; no se resta otra vez al trabajador. Este costo solo incluye los conceptos pedidos: no representa el costo laboral anual completo con CTS, gratificaciones o vacaciones. El neto es el depósito pendiente: el trabajador ya recibió S/ 200.00 como adelanto, de modo que el porcentaje de efectivo recibido durante todo el mes sería distinto si incluyéramos ese pago anterior.

## 3. Caso 2 con 30 días

Con 27 días: sueldo computable S/ 1,620.00, asignación S/ 123.00, remuneraciones S/ 1,743.00, ONP S/ 226.59 y neto S/ 1,516.41.

Con 30 días: sueldo computable S/ 1,800.00, asignación S/ 123.00, remuneraciones **S/ 1,923.00**, ONP **S/ 249.99** y neto **S/ 1,673.01**. EsSalud sería S/ 173.07.

La remuneración aumenta S/ 180.00, pero la ONP aumenta S/ 23.40: el neto solo sube **S/ 156.60**. La asignación familiar permanece completa en ambos escenarios, conforme a la convención de la guía. No se vuelve a descontar por faltas porque ya se reflejan en los días laborados.

## 4. Peso de las horas extras

En el caso 3, los dos tramos suman **62.50 + 67.50 = S/ 130.00**. Su participación en las remuneraciones es **130.00 / 3,253.00 × 100 = 3.9963%, aproximadamente 4.00%**. El denominador es el total remunerado, que incluye sueldo computable, asignación y las propias horas extras.

## 5. Sueldo de una oferta real y comparación

Se consultó el **26/10/2026** la [oferta de Desarrollador Full Stack en Ate](https://pe.indeed.com/viewjob?jk=1a5d74a196f5ecab), con rango publicado S/ 3,500–4,000 mensuales. Se toma el límite inferior **S/ 3,500.00**, superior a la RMV de la guía. Se usa únicamente el sueldo publicado: el empleado y la empresa de la boleta son ficticios y no se atribuye al anunciante esta liquidación. Supuestos académicos: régimen general, 30 días, sin hijos, ONP, sin sobretiempo ni adelantos. La publicación del sueldo no acredita por sí sola todos esos supuestos.

| Concepto | Monto S/ |
| --- | ---: |
| Sueldo computable y remuneraciones | 3,500.00 |
| Asignación y horas extras | 0.00 |
| ONP | 455.00 |
| Adelantos | 0.00 |
| Neto | **3,045.00** |
| EsSalud, adicional del empleador | 315.00 |
| Costo simplificado | 3,815.00 |

Neto / remuneraciones = **3,045 / 3,500 × 100 = 87.00%**. Aquí sueldo básico y bruto coinciden porque no hay conceptos adicionales. El Excel también incluye dos sensibilidades del rango de esa oferta:

| Escenario calculado, no compañero | Remuneraciones | Sistema | Neto | Neto/bruto |
| --- | ---: | --- | ---: | ---: |
| Propio | 3,500.00 | ONP | 3,045.00 | 87.00% |
| Sensibilidad A | 3,750.00 | AFP Prima, flujo SBS | 3,263.62 | 87.03% |
| Sensibilidad B | 4,000.00 | AFP Habitat, flujo SBS | 3,486.40 | 87.16% |

Con tasas proporcionales y sin adelantos, cambiar solo el sueldo casi no cambia la proporción; las diferencias entre estas filas proceden del sistema y las comisiones. Los redondeos pueden variar el último decimal. En una planilla real, la renta de quinta podría cambiar esta proporción.

**Pendiente externo:** la guía pide contrastar con dos compañeros que hayan usado otros sueldos y un caso propio por alumno. No se han recibido sus ofertas ni sus boletas. Los escenarios anteriores son sensibilidades calculadas, no resultados aportados por compañeros. El espacio al final de `Casos` permite registrar alias, enlace y fecha de cada oferta, bruto y neto. Al recibirlos, comparar `neto/bruto × 100` y explicar diferencias por pensión, hijos, días, sobretiempo y adelantos. Para el segundo participante aún debe registrarse su caso propio real; no se le atribuye uno inventado.

## Caso 4, desarrollo para revisión del docente

Valor hora: 4,200 / 30 / 8 = S/ 17.50. Sueldo computable: 4,200 / 30 × 24 = S/ 3,360.00. Asignación: S/ 123.00. Horas 25%: 17.50 × 1.25 × 2 = S/ 43.75. Horas 35%: 17.50 × 1.35 × 2 = S/ 47.25. Total: **S/ 3,574.00**.

Fondo AFP: S/ 357.40; comisión: 3,574 × 1.60% = 57.184 → **S/ 57.18**; seguro: 3,574 × 1.35% = 48.249 → **S/ 48.25**. Más S/ 100.00 de adelanto: descuentos **S/ 562.83**. Neto: **S/ 3,011.17**. EsSalud: **S/ 321.66**. Costo simplificado: **S/ 3,895.66**. Este resultado es calculado; la guía no publica una respuesta oficial para el caso 4.
