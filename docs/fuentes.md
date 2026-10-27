# Fuentes y parámetros

Fecha de consulta de todas las filas: **26/10/2026**. La versión original de la guía está preservada en `referencias/Actividad_Grupo_B.docx`; se extrajeron sus párrafos y nueve tablas en orden, más encabezados y pies si existen. La paginación depende del editor de Word; el archivo no declara el número de páginas en sus metadatos.

| Dato | Valor usado | Fuente y alcance |
| --- | --- | --- |
| RMV para pruebas | S/ 1,230.00; desde 01/10/2026 según la guía | Guía, sección 4. Se localizó el [índice oficial de El Peruano del 28/09/2026](https://busquedas.elperuano.pe/?ci=ONLY&fechaFin=20260928&fechaIni=20260928&start=0&tipoPublicacion=EX), que identifica el D.S. 015-2026-TR como incremento de RMV. El [texto individual](https://busquedas.elperuano.pe/dispositivo/NL/2559163-1) no se pudo recuperar con el navegador automatizado; el importe y fecha del perfil se sostienen en el documento del laboratorio. No se afirma haber leído ese decreto íntegro. |
| Asignación familiar | 10% de RMV = S/ 123.00 | Ley 25129, [MTPE](https://www.gob.pe/institucion/mtpe/noticias/601761-quienes-tienen-derecho-a-percibir-la-asignacion-familiar). La guía simplifica la acreditación a Sí/No y exige no prorratear. |
| ONP | 13% de remuneraciones | D.L. 19990; [ONP, 19/06/2025](https://www.gob.pe/institucion/onp/noticias/1190488-como-saber-si-tu-empleador-esta-pagando-tus-aportes-al-snp). |
| EsSalud | 9% adicional del empleador | Ley 26790; [SUNAT, informe 003-2007](https://www.sunat.gob.pe/legislacion/oficios/2007/oficios/i0032007.htm). El informe trata también la base mínima, que se excluye expresamente por la guía. |
| Sobretasas | 25% primeras dos horas; 35% siguientes | D.S. 007-2002-TR, art. 10; [SUNAFIL](https://www.gob.pe/institucion/sunafil/noticias/1100081-conoce-las-diferencias-entre-trabajo-forzoso-y-trabajo-en-sobretiempo), [SUNAT: conceptos ONP](https://orientacion.sunat.gob.pe/6722-10-conceptos-afectos-a-onp). La guía recibe horas ya distribuidas y calcula valor hora solo desde el sueldo básico. |
| Mes / jornada | 30 días / 8 horas | Guía, sección 4. Constantes académicas, no dependen del calendario. |
| Redondeo | 2 decimales por concepto, luego suma | Guía, sección 4. Swift `Decimal` y `NSDecimalRound(.plain)`; Excel `ROUND`. Valor hora no se redondea prematuramente. Entradas de dinero y horas: hasta 2 decimales. |
| AFP Ejemplo | Fondo 10%; comisión 1.60%; seguro 1.35% | Guía, valores de prueba. Se conserva exactamente para casos 3 y 4. No es una AFP real ni se identifica con Prima. |
| AFP Habitat | Fondo 10%; comisión flujo 1.47%; seguro 1.37% | [SBS: comisiones y primas, devengue 2026-10](https://www.sbs.gob.pe/app/spp/empleadores/comisiones_spp/Paginas/comision_prima.aspx). |
| AFP Integra | Fondo 10%; comisión flujo 1.55%; seguro 1.37% | Misma tabla SBS. |
| AFP Prima | Fondo 10%; comisión flujo 1.60%; seguro 1.37% | Misma tabla SBS. |
| AFP Profuturo | Fondo 10%; comisión flujo 1.69%; seguro 1.37% | Misma tabla SBS. |
| Modalidad AFP | Solo flujo | [SBS: comisiones y primas](https://www.sbs.gob.pe/usuarios/Comisiones-y-primas). La comisión anual sobre saldo no se trata como descuento mensual sobre sueldo. |
| Oferta propia | S/ 3,500–4,000 mensuales; base elegida S/ 3,500 | [Oferta de Desarrollador Full Stack, Ate](https://pe.indeed.com/viewjob?jk=1a5d74a196f5ecab). Se revisó el sueldo en la publicación; conservar enlace y fecha porque puede caducar. Solo se usa el monto, sin datos personales. |

La tabla SBS también publica una remuneración máxima asegurable de S/ 12,732.70 para ese devengue. El laboratorio exige calcular el seguro sobre todo el total remunerado, por lo que el modelo no implementa dicho tope. Los ejemplos propios quedan debajo del tope. Tampoco se aplican base mínima de EsSalud, impuesto de quinta ni otras reglas de planilla real. Las tasas reales son una referencia fechada de flujo; deben actualizarse para otro mes. No se incorporan tasas de comisión sobre saldo a las fórmulas de este ejercicio.

Las páginas históricas de ONP y EsSalud pueden seguir mostrando una RMV anterior de S/ 1,130. Se usan para sustentar sus porcentajes y no para reemplazar el perfil de pruebas del profesor.

Implementación del redondeo en Excel: las expresiones con divisiones de sueldo y HE normalizan el importe completo en céntimos mediante `ROUND(ROUND(importe*100,8),0)/100`. Es una medida para residuos binarios del cálculo numérico, no una tasa ni una regla laboral adicional. Mantiene el valor hora sin redondear y aplica el redondeo monetario al concepto completo. La prueba de 240.96 de sueldo y una hora al 25% genera matemáticamente 1.255, que debe dar 1.26. El motor independiente sin esta estabilización devolvía 1.25; la incidencia y su corrección están documentadas en evidencias.
