# Capítulo 1 — Amenazas climáticas observadas en el territorio

**Cambio Climático · Ingeniería en Riesgos de Desastres · ESPAM MFL** · Plantilla CC-IRD-C1 · Versión 1.0 · octubre de 2026

Evidencia el **RA A** de la Unidad I: aplicar los fundamentos teóricos del sistema climático para interpretar las causas y evidencias del cambio climático, en el contexto de la gestión de riesgos de desastres. Es el primer capítulo del proyecto de cada equipo, que se defiende en la Unidad IV, y la base del capítulo 2 (riesgo). Se escribe para un lector externo: la unidad de gestión de riesgos del GAD.

## Dos entregas, un mismo documento

| | Borrador (formativa, 2 pts) | Capítulo definitivo (sumativa, 8 pts, estudio de casos) |
|---|---|---|
| Cuándo | Al cerrar `RD1_02` (extremos y registro de eventos) | Sesión de la sumativa de la Unidad I |
| Qué se entrega | Secciones 1 a 5 con figuras, tablas, registro de eventos y respuestas en borrador | El capítulo completo, corregido con la retroalimentación, más la sección 6 y el anexo de la bitácora |
| Qué se revisa | Que los resultados estén completos, bien leídos, con unidades, y que el registro tenga fuentes | Que la interpretación sea correcta: causas, evidencias, variabilidad natural y amenaza principal, con lenguaje calibrado |
| Extensión orientativa | 5–7 páginas | 10–14 páginas más anexos |

Los dos integrantes del equipo ejecutan los cuadernos, cada uno en su Drive, y entregan un solo documento.

## Estructura y de dónde sale cada parte

Todos los archivos están en `Mi unidad/CC_Riesgos/practica-1/<zona>/`, salvo las series comunes (`Mi unidad/CC_datos/<zona>/`).

| Sección | Contenido | Insumos | Preguntas que responde |
|---|---|---|---|
| **1. Territorio** | Ubicación, relieve, cuencas, población expuesta y antecedentes de desastres; mapa con las celdas de los reanálisis | Mapa de `CR01`; pesos de celdas de `CR02` | `CR02`, preguntas 1–2 |
| **2. Datos y métodos** | Fuentes (ERA5, CORe, estación si la hay), periodos (1995–2014 para el ciclo anual, 1981–2010 para los percentiles de extremos, 1991–2020 para ENSO), índice de ENSO, índices ETCCDI y sus simplificaciones, Mann-Kendall corregido, GEV, fuentes del registro de eventos | `RD1_01_metadatos.json`, `RD1_02_metadatos.json` | «Para el informe» de `RD1_02` |
| **3. Clima normal y su variabilidad** | Ciclo anual con P10–P90 y máximo; temporada lluviosa; señal de El Niño y La Niña por mes; lluvia de la temporada según la intensidad del evento; zonas más sensibles a El Niño | `RD1_01_ciclo_anual_*.png`, `RD1_01_compuestos_*.png`, `RD1_01_temporada_enso_*.png`, `RD1_01_mapa_nino_*.png`, `RD1_01_episodios_enso.csv` | `RD1_01`, preguntas 1–5 |
| **4. Evidencias de cambio y extremos** | Tendencia de temperatura media y lluvia anual (con y sin años de El Niño); tendencias de los índices de extremos; extremos por fase de ENSO; niveles de retorno de 1 y 5 días | `RD1_02_evidencia_medias_*.png`, `RD1_02_evidencia_medias_*.csv`, `RD1_02_tendencias_*.png`, `RD1_02_extremos_enso_*.png`, `RD1_02_retorno_*.png`, `RD1_02_periodos_retorno_*.csv` | `RD1_02`, preguntas 1–4 |
| **5. Eventos registrados frente a la lluvia** | Registro de eventos con fuentes; contraste con la lluvia previa; lluvias extremas sin registro y eventos sin lluvia extrema; comparación con el ECU 911 | `registro_eventos.csv`, `RD1_02_ecu911_*.csv`, `RD1_02_registro_contrastado_*.csv`, `RD1_02_lluvias_candidatas_*.csv`, `RD1_02_eventos_*.png` | `RD1_02`, preguntas 5–6 |
| **6. Discusión y conclusiones** *(solo definitivo)* | Amenaza hidrometeorológica principal, en qué meses y fases de ENSO; qué parte de lo observado es cambio climático y qué parte variabilidad natural, con su causa física; comparación con la evidencia del AR6; limitaciones y vacíos del registro | Clases de extremos y de detección y atribución; AR6 GTI, Resumen para responsables de políticas y capítulo 11 | `RD1_02`, pregunta 7, y síntesis |
| **Anexo A. Bitácora de El Niño 2026–2027** | Registro semanal del evento en curso: índices, comunicados, SitRep, incidentes de la zona | [`practicas/comun/bitacora`](../../comun/bitacora/) | `RD1_01`, pregunta 6 |
| **Anexo B. Reproducibilidad** | Enlace a las copias de los cuadernos en Drive y lista de archivos producidos | Drive del equipo | — |

## Fuentes del registro de eventos

| Fuente | Periodo | Qué aporta |
|---|---|---|
| ECU 911, Base de Emergencias (Datos Abiertos), automática en `RD1_02` | julio de 2021 en adelante | Fecha, cantón, parroquia y tipo; sin daños |
| [DesInventar, Ecuador](https://db.desinventar.org/DesInventar/country_profile.jsp?countrycode=ecu&lang=ES) | 1970–2007 | Eventos con daños, incluidos El Niño 1982–83 y 1997–98 |
| [SitRep de la SNGR](https://www.gestionderiesgos.gob.ec/informes-de-situacion-actual-por-eventos-adversos-ecuador/) | 2016–2026 | Afectados, viviendas y fallecidos por cantón |
| GAD y prensa local con fecha | variable | Completar vacíos, en especial 2008–2015 |

## Reglas de redacción

- Cada figura y tabla lleva número, título, fuente y elaboración del equipo, y se cita en el texto antes de aparecer.
- Todo número va con su unidad, su fuente y su escala (promedio de la zona, celda o estación). Para diseño se usan la celda o la estación, nunca el promedio de la zona.
- Los periodos de retorno mayores de 50 años se reportan con su intervalo y como extrapolación.
- Las conclusiones usan la escala calibrada del IPCC (probabilidad y confianza), justificada por el acuerdo entre fuentes y la robustez de las pruebas.
- Un incidente del ECU 911 es un día con atención coordinada, no un desastre verificado; los daños vienen de los SitRep o de los GAD.
- El evento El Niño en curso va solo en el anexo A, marcado como preliminar.
- Citas en formato APA 7; las de los datos están al final de cada cuaderno.

## Lista de verificación antes de entregar

| Criterio | Borrador | Definitivo |
|---|---|---|
| Las 5 secciones de resultados tienen sus figuras y tablas con unidades, fuente y escala | ✔ | ✔ |
| Las respuestas usan los números del territorio, no generalidades | ✔ | ✔ |
| El registro de eventos tiene fuente en cada fila y cubre al menos los eventos conocidos (1982–83, 1997–98, 2008, 2012, 2017, 2023) que afectaron la zona | ✔ | ✔ |
| Las tendencias se reportan con su significancia corregida y la prueba sin El Niño | ✔ | ✔ |
| Se distingue explícitamente la señal de cambio de la variabilidad de ENSO | | ✔ |
| Las causas se explican con el balance de energía y el forzamiento radiativo, no solo se describen los datos | | ✔ |
| La amenaza principal queda identificada con meses, fases de ENSO y lugares, lista para el capítulo 2 | | ✔ |
| La conclusión usa lenguaje calibrado y se compara con la evidencia del AR6 | | ✔ |
| Se atendió cada observación de la retroalimentación del borrador | | ✔ |
| Anexo de la bitácora con al menos una entrada semanal desde octubre | | ✔ |

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
