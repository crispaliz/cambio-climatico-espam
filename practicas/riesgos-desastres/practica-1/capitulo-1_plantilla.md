# Capítulo 1 — Amenazas climáticas observadas en el territorio

**Cambio Climático · Ingeniería en Riesgos de Desastres · ESPAM MFL** · Plantilla CC-IRD-C1 · Versión 1.1 · octubre de 2026

Evidencia el **RA A** de la Unidad I: aplicar los fundamentos teóricos del sistema climático para interpretar las causas y evidencias del cambio climático, en el contexto de la gestión de riesgos de desastres. Es el primer capítulo del proyecto de cada equipo, que se defiende en la Unidad IV, y la base del capítulo 2 (riesgo). Se escribe para un lector externo: la unidad de gestión de riesgos del GAD.

## Dos entregas, un mismo documento

| | Borrador (formativa, 2 pts) | Capítulo definitivo (sumativa, 8 pts, estudio de casos) |
|---|---|---|
| Cuándo | Al cerrar `RD1_02` (extremos y registro de eventos) | Sesión de la sumativa de la Unidad I |
| Qué se entrega | Secciones 1 a 5 con figuras, tablas, el registro de eventos que arma `RD1_02` comentado y respuestas en borrador | El capítulo completo, corregido con la retroalimentación, más la sección 6 y el anexo de la bitácora |
| Qué se revisa | Que los resultados estén completos, bien leídos, con unidades y escala, y que el contraste de eventos y lluvia se lea por fuente (DesInventar y ECU 911) | Que la interpretación sea correcta: causas, evidencias, variabilidad natural y amenaza principal, con lenguaje calibrado |
| Extensión orientativa | 5–7 páginas | 10–14 páginas más anexos |

Los dos integrantes del equipo ejecutan los cuadernos, cada uno en su Drive, y entregan un solo documento.

## Estructura y de dónde sale cada parte

Todos los archivos están en `Mi unidad/CC_Riesgos/practica-1/<zona>/`, salvo las series comunes (`Mi unidad/CC_datos/<zona>/`).

| Sección | Contenido | Insumos | Preguntas que responde |
|---|---|---|---|
| **1. Territorio** | Ubicación, relieve, cuencas, población expuesta y antecedentes de desastres; mapa con las celdas de los reanálisis | Mapa de `CR01`; pesos de celdas de `CR02` | `CR02`, preguntas 1–2 |
| **2. Datos y métodos** | Fuentes: ERA5, CORe y la estación del curso que eligió `RD1_02` (nombre, código, red, coordenadas, altitud y qué variables aporta); periodos (1995–2014 para el ciclo anual, 1981–2010 para los percentiles de extremos, 1991–2020 para ENSO); índice de ENSO; índices ETCCDI y sus simplificaciones; Mann-Kendall corregido; GEV; fuentes del registro de eventos (DesInventar 1970–2007 y ECU 911 desde julio de 2021) y su vacío | `RD1_01_metadatos.json`, `RD1_02_metadatos.json`, la línea «Estación usada» de `RD1_02` y la ficha de la estación en [`datos/estaciones/indice_estaciones.csv`](../../../datos/estaciones/indice_estaciones.csv) | «Para el informe» de `RD1_02` |
| **3. Clima normal y su variabilidad** | Ciclo anual con P10–P90 y máximo; temporada lluviosa; señal de El Niño y La Niña por mes; lluvia de la temporada según la intensidad del evento; zonas más sensibles a El Niño | `RD1_01_ciclo_anual_*.png`, `RD1_01_compuestos_*.png`, `RD1_01_temporada_enso_*.png`, `RD1_01_mapa_nino_*.png`, `RD1_01_episodios_enso.csv` | `RD1_01`, preguntas 1–5 |
| **4. Evidencias de cambio y extremos** | Tendencia de temperatura media y lluvia anual (con y sin años de El Niño); tendencias de los índices de extremos; extremos por fase de ENSO; niveles de retorno de 1 y 5 días | `RD1_02_evidencia_medias_*.png`, `RD1_02_evidencia_medias_*.csv`, `RD1_02_tendencias_*.png`, `RD1_02_extremos_enso_*.png`, `RD1_02_retorno_*.png`, `RD1_02_periodos_retorno_*.csv` | `RD1_02`, preguntas 1–4 |
| **5. Eventos registrados frente a la lluvia** | Registro de eventos de la zona (lo arma `RD1_02`): cuántos eventos y de qué tipo trae cada fuente; contraste con la lluvia previa, por fuente; lluvias extremas sin registro y eventos sin lluvia extrema; comparación entre DesInventar y el ECU 911; vacío 2008 – junio de 2021 | `RD1_02_registro_eventos_*.csv`, `RD1_02_desinventar_*.csv`, `RD1_02_ecu911_*.csv`, `RD1_02_registro_contrastado_*.csv`, `RD1_02_lluvias_candidatas_*.csv`, `RD1_02_eventos_*.png` | `RD1_02`, preguntas 5–6 |
| **6. Discusión y conclusiones** *(solo definitivo)* | Amenaza hidrometeorológica principal, en qué meses y fases de ENSO; qué parte de lo observado es cambio climático y qué parte variabilidad natural, con su causa física; comparación con la evidencia del AR6; limitaciones y vacíos del registro | Clases de extremos y de detección y atribución; AR6 GTI, Resumen para responsables de políticas y capítulo 11 | `RD1_02`, pregunta 7, y síntesis |
| **Anexo A. Bitácora de El Niño 2026–2027** | Registro semanal del evento en curso: índices, comunicados, SitRep, incidentes de la zona | [`practicas/comun/bitacora`](../../comun/bitacora/) | `RD1_01`, pregunta 6 |
| **Anexo B. Reproducibilidad** | Enlace a las copias de los cuadernos en Drive, lista de archivos producidos (incluido `RD1_02_registro_eventos_*.csv`) y, si el equipo complementó el registro, su CSV con la fuente de cada fila | Drive del equipo | — |

## Fuentes del registro de eventos

`RD1_02` arma el registro de la zona **automáticamente**; el equipo no llena ninguna planilla.

| Fuente | Periodo | Qué aporta | En `RD1_02` |
|---|---|---|---|
| [DesInventar Ecuador](https://db.desinventar.org/DesInventar/country_profile.jsp?countrycode=ecu&lang=ES) (UNDRR) | 1970–2007 | Una ficha por desastre con fecha, cantón, tipo, fallecidos, afectados y viviendas, y la fuente original (prensa, Defensa Civil). Incluye El Niño 1982–83 y 1997–98 | Automática (`USAR_DESINVENTAR`) |
| ECU 911, Base de Emergencias (Datos Abiertos) | julio de 2021 en adelante | Fecha, cantón, parroquia y tipo de los incidentes de gestión de riesgos; sin daños | Automática (`USAR_ECU911`) |
| [SitRep de la SNGR](https://www.gestionderiesgos.gob.ec/informes-de-situacion-actual-por-eventos-adversos-ecuador/), GAD y prensa local con fecha | 2008 – junio de 2021 | Eventos del periodo que ninguna base pública cubre evento por evento (por ejemplo, 2008, 2012 y 2017) | **Opcional**: CSV del equipo en `ARCHIVO_EVENTOS`, con la fuente en cada fila |

## Reglas de redacción

- Cada figura y tabla lleva número, título, fuente y elaboración del equipo, y se cita en el texto antes de aparecer.
- Todo número va con su unidad, su fuente y su escala (promedio de la zona, celda o estación). Para diseño se usan la celda o la estación, nunca el promedio de la zona.
- Los periodos de retorno mayores de 50 años se reportan con su intervalo y como extrapolación.
- Las conclusiones usan la escala calibrada del IPCC (probabilidad y confianza), justificada por el acuerdo entre fuentes y la robustez de las pruebas.
- Un incidente del ECU 911 es un día con atención coordinada, no un desastre verificado. Los daños vienen de DesInventar (hasta 2007) o de los SitRep y los GAD; en DesInventar, una cifra vacía significa «no reportado», no cero.
- Los resultados se comparan por fuente: DesInventar y el ECU 911 registran cosas distintas (desastres con daños frente a días de atención), así que sus porcentajes no se suman ni se promedian.
- La estación se declara con su nombre, código, red y variables, y con las limitaciones de su ficha: la lluvia del INAMHI 1964–2018 está rellenada con Climatol (apoyo CHIRPS) y la temperatura de la red INAMHI empieza en 2022. Si la zona no tiene estación con alguna variable, esa variable se compara solo entre ERA5 y CORe.
- El evento El Niño en curso va solo en el anexo A, marcado como preliminar.
- Citas en formato APA 7; las de los datos están al final de cada cuaderno.

## Lista de verificación antes de entregar

| Criterio | Borrador | Definitivo |
|---|---|---|
| Las 5 secciones de resultados tienen sus figuras y tablas con unidades, fuente y escala | ✔ | ✔ |
| Las respuestas usan los números del territorio, no generalidades | ✔ | ✔ |
| El análisis del registro separa DesInventar, ECU 911 (y el registro del equipo, si lo hay) y comenta el vacío 2008 – junio de 2021 | ✔ | ✔ |
| Se revisa si los eventos conocidos que afectaron la zona aparecen en el registro (1982–83 y 1997–98 en DesInventar; 2023 en el ECU 911) y se explica cuando no aparecen | ✔ | ✔ |
| La estación usada está declarada con su fuente y sus limitaciones | ✔ | ✔ |
| Las tendencias se reportan con su significancia corregida y la prueba sin El Niño | ✔ | ✔ |
| Se distingue explícitamente la señal de cambio de la variabilidad de ENSO | | ✔ |
| Las causas se explican con el balance de energía y el forzamiento radiativo, no solo se describen los datos | | ✔ |
| La amenaza principal queda identificada con meses, fases de ENSO y lugares, lista para el capítulo 2 | | ✔ |
| La conclusión usa lenguaje calibrado y se compara con la evidencia del AR6 | | ✔ |
| Se atendió cada observación de la retroalimentación del borrador | | ✔ |
| Anexo de la bitácora con al menos una entrada semanal desde octubre | | ✔ |

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
