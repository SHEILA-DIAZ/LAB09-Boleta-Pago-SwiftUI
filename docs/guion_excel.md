# Guion de exposición · Participante 1: Excel

Duración sugerida: 7–9 minutos. Tener abierto `Excel/Boleta_Pago_Semana09.xlsx` y `docs/analisis.md`. No modificar el perfil de referencia antes de mostrar los resultados oficiales.

## 0:00–0:45 · Qué resuelve

“Nuestra boleta convierte los datos del mes en remuneraciones, descuentos, aportes del empleador y neto. Excel explica cada paso y permite contrastarlo con el mismo modelo Swift. Los niveles 1 y 2 están desarrollados. El nivel 3 es un reto opcional y no forma parte de este cálculo.”

Mostrar las cuatro hojas y explicar que amarillo significa editable. Señalar que no hay impuesto de quinta, base mínima de EsSalud ni faltas descontadas dos veces.

## 0:45–1:45 · Parámetros

“Toda tasa está centralizada. Usamos RMV 1,230 y asignación de 123. ONP es 13%; EsSalud 9%. AFP Ejemplo tiene valores ficticios fijados por la guía: 10%, 1.60% y 1.35%. Las AFP reales se identifican con su modalidad de flujo y la fecha de consulta SBS.”

Mostrar las fuentes, fecha y nombres definidos. “Cambiar una tasa recalcula los casos; si cambiamos el perfil ya no podemos exigir los importes oficiales originales.” Mostrar que la jornada de 30 días y 8 horas es una convención del laboratorio.

## 1:45–3:45 · Las fórmulas, con caso 3

Introducir en `Boleta!B4:B11`: `3000`, `30`, `Sí`, `AFP`, `Ejemplo`, `4`, `4`, `200`.

“El sueldo computable es 3,000 dividido entre 30 por 30. Si tiene hijos se suman 123 completos. El valor hora es 3,000 entre 30 entre 8: 12.50. Por cuatro horas al 25% obtenemos 62.50, y por cuatro al 35%, 67.50. Sumamos los cuatro conceptos: 3,253.”

“Sobre ese total se calcula cada AFP: fondo 325.30; comisión 52.048 redondeada a 52.05; seguro 43.9155 redondeado a 43.92. Añadimos 200 de adelanto: descuentos 621.27. Neto: 3,253 menos 621.27, igual a 2,631.73. EsSalud es 292.77 y lo paga adicionalmente la empresa.”

Señalar la fórmula de cada fila en columna C y la barra de fórmulas. “Redondeamos cada concepto antes de sumar; el valor hora conserva su precisión hasta terminar el tramo.” Abrir `Explicación` y recorrer las fórmulas 1–14; los ejemplos numéricos están al lado.

## 3:45–4:45 · Casos y control cruzado

“Los casos 1, 2 y 3 dan netos 2,175.00; 1,516.41; 2,631.73. El caso 4 no tenía respuesta publicada: da 3,011.17. Sus remuneraciones son 3,574.00 y descuentos 562.83. No lo presentamos como respuesta oficial del profesor.”

Mostrar los resultados reales en `evidencias/` y explicar qué motor se ejecutó. Si no existe evidencia COM aprobada, decir expresamente que la automatización de Excel nativo falló y que el motor independiente evaluó las fórmulas; no afirmar que se ejecutó Excel por solo mostrar el archivo.

## 4:45–5:30 · Validación

Intentar días 31, sueldo cero o HE negativas y mostrar el rechazo. Explicar que pegar datos puede omitir el diálogo de validación de Excel, por eso `B13` verifica las entradas de nuevo y las fórmulas del resultado quedan vacías si son inválidas. Restaurar el caso de demostración.

## 5:30–7:30 · Análisis

“Con caso 3, ONP deja 2,630.11 y AFP Ejemplo 2,631.73: diferencia 1.62. Eso no basta para elegir sistema de jubilación. El costo solicitado para la empresa es 3,545.77 y el neto representa 74.22%. Con caso 2 a 30 días el neto sube a 1,673.01; de los 180 adicionales se retienen 23.40 para ONP. Las horas extras son aproximadamente 4% del total remunerado.”

“La oferta propia publica entre 3,500 y 4,000; elegimos 3,500. Con ONP y nuestros supuestos el neto es 3,045, un 87%. Las otras dos filas son sensibilidades, no boletas enviadas por compañeros. La comparación real y el caso propio del segundo alumno se completan al recibir sus datos.”

## Preguntas previsibles

- ¿Por qué EsSalud no baja el neto? Es una aportación adicional de la empresa.
- ¿Por qué AFP tiene tres filas? Fondo, administración y cobertura de seguro son conceptos distintos.
- ¿Por qué no hay renta de quinta? La guía la excluye en el cálculo principal y la propone como nivel 3.
- ¿Por qué no se redondea el valor hora? Es un intermedio; la guía pide redondear cada concepto final.
- ¿Se puede usar como planilla legal? Es un modelo académico con simplificaciones expresamente declaradas.
