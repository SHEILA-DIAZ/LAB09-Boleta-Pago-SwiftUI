# Trazabilidad con Actividad_Grupo_B.docx

Documento leído íntegramente mediante ZIP/XML, incluidas nueve tablas; copia original y extracción en `referencias/`. La copia tiene el mismo SHA-256 registrado en `evidencias/documento.json`. El repositorio estaba vacío, sin commits y con `origin` configurado correctamente.

| Sección de la guía | Requisito | Implementación / estado |
| --- | --- | --- |
| 1–3 | Boleta simplificada; app principal; Excel explicativo; repositorio y análisis | `App/`, `Excel/`, `docs/` y README |
| 3 | Control cruzado al centavo de cuatro casos | Fixtures y verificador Swift; comparación por 14 conceptos; detalle de motores realmente ejecutados en evidencias |
| 4 | Sueldo / 30 × días | `Boleta.calcular`; Excel `Boleta!B17` |
| 4 | Asignación 10% RMV sin prorratear | `Boleta.calcular`; `B18` |
| 4 | Valor hora = básico / 30 / 8; HE al 25% y 35% | `Boleta.calcular`; `B19:B20`; valor hora sin redondeo previo |
| 4 | Total remuneraciones; base ONP y AFP incluye asignación y HE | `ResultadoBoleta`; `B21:B25` |
| 4 | ONP 13%; AFP fondo, comisión, seguro separados | `Parametros.afps`; `B22:B25` |
| 4 | Adelanto íntegro, descuentos, neto | `B26:B28` |
| 4 | EsSalud 9% adicional, sin base mínima | `B29`; array de aportaciones separado |
| 4 | Parámetros centralizados; fuente y fecha | `Parametros`, hoja `Parámetros`, `docs/fuentes.md` |
| 4 | Redondear cada concepto antes de sumar | `Decimal`, `.plain`; Excel `ROUND`; no se suma AFP sin redondear |
| 4 | Sin renta de quinta ni descuento adicional por faltas | Excluidos del perfil de niveles 1 y 2 |
| 5 | Una pantalla: formulario, Calcular y boleta debajo | `ContentView`, `ScrollView` vertical |
| 5 | Solo controles de clase y ScrollView | `Text`, `VStack`, `HStack`, `@State`, `TextField`, `Picker`, `Button`, `ScrollView`; sin navegación, alertas, tablas ni listas nuevas |
| 5 | Sueldo > 0; días 1–30; hijos; ONP/AFP | Parseo y validación de modelo; mensajes visibles |
| 5 | Picker AFP solo al seleccionar AFP | Rama condicional en la pantalla |
| 5 | Horas y adelantos no negativos | Modelo, parser y validación del Excel; campos cero explícitos |
| 5 | Tres bloques verticales, neto y conceptos no aplicables en cero | Arrays y filas en pantalla; `Boleta` y `Casos` en Excel |
| 6 | Nivel 1 obligatorio | Sueldo, días, asignación, ONP, EsSalud, neto; casos 1–2 |
| 6 | Nivel 2 | AFP, HE y adelanto; casos 3–4 |
| 6 | Nivel 3 reto opcional | Documentado y no implementado: identidad ficticia en encabezado, comparación ONP/AFP simultánea en pantalla, renta de quinta |
| 7 | Casos 1, 2, 3 oficiales y 4 calculado | `Tests/fixtures.json`, hoja `Casos`, `docs/analisis.md` |
| 8 | Cinco respuestas razonadas | `docs/analisis.md`; incluye ONP alternativa, costo, 30 días, HE y oferta real |
| 9 | Caso propio por alumno, sueldo de oferta ≥ RMV, URL y fecha | Un caso propio documentado; segundo participante pendiente de datos reales |
| 8–9 | Comparar con dos compañeros | Espacio en Excel y metodología; pendiente de resultados externos; sensibilidades no atribuidas a compañeros |
| 9 | Verificar parámetros variables con fuentes | Fuentes fechadas, SBS consultada; alcance de consulta RMV explícito |
| 9 | Sin DNI/RUC reales; texto “Boleta de ejemplo” | Pantalla sin identificadores personales; solo sueldo de oferta |
| 10 | Structs, clase Boleta, diccionario AFP y arrays | `App/Model/Boleta.swift` |
| 10 | README, evidencias y commits por hito | README y evidencias reales; historial local si permite el entorno; sin push |
| 10 | Cuatro hojas, fórmulas reales y visibles | `Parámetros`, `Boleta`, `Casos`, `Explicación`; `FORMULATEXT` junto a cálculos y explicación de las 14 fórmulas |
| Cierre | Dos participantes, uno explica Excel y otro app | Dos guiones separados en `docs/` |

Límites operativos añadidos y documentados: montos hasta S/ 100,000,000, horas hasta 10,000 por tramo y hasta dos decimales para importes y horas. Evitan desbordamientos y hacen reproducible la comparación; no alteran los casos del profesor. No se impone RMV como mínimo al formulario porque la validación solicitada es sueldo mayor que cero; sí se exige ≥ RMV para el caso de oferta. Días se exigen enteros. El neto puede ser negativo si el adelanto supera el disponible: se informa en pantalla, no se recorta a cero.
