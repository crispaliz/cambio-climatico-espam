# Guía de la evaluación formativa — Capítulo 1 (borrador)

**Cambio Climático · Ingeniería en Riesgos de Desastres · ESPAM MFL** · Guía CC-IRD-C1-F · Versión 1.0 · octubre de 2026

| | |
|---|---|
| Unidad y resultado de aprendizaje | Unidad I · **RA A**: aplicar los fundamentos del sistema climático para interpretar las causas y evidencias del cambio climático en la gestión de riesgos de desastres |
| Práctica | Práctica 1: `CR01`, `CR02`, `RD1_01_ciclo_anual_enso` y `RD1_02_extremos_eventos` |
| Producto | Borrador del capítulo 1, secciones 1 a 5 y anexo B, según la [plantilla](capitulo-1_plantilla.md) |
| Trabajo | En equipo de dos, una provincia por equipo (o un cantón de ella), la misma zona en todos los cuadernos |
| Valor | **2 puntos** |
| Entrega | Al cerrar `RD1_02`, en la fecha que fija el docente en el aula virtual |

## 1. Para qué sirve esta evaluación

El borrador no busca un texto pulido: busca comprobar que el equipo **corrió bien los cuadernos para su provincia y lee correctamente sus resultados** antes de interpretarlos. El docente devuelve observaciones numeradas (O1, O2, …) que el equipo debe atender en el capítulo definitivo; esa atención se califica en la evaluación sumativa ([guía sumativa](guia_sumativa.md), criterio 7).

## 2. Qué se entrega

- **Un solo archivo PDF por equipo**, con el nombre `CC-IRD-C1_borrador_<provincia>_<apellido1>-<apellido2>.pdf` (por ejemplo, `CC-IRD-C1_borrador_loja_mendoza-zambrano.pdf`).
- Portada mínima: asignatura, título del capítulo, provincia (y cantón, si lo eligieron), integrantes y fecha.
- **Secciones 1 a 5** de la plantilla, con sus figuras y tablas, y **respuestas en borrador** a las preguntas de los cuadernos (`CR02` 1–2, `RD1_01` 1–5, `RD1_02` 1–6), integradas en el texto de cada sección, no como cuestionario aparte.
- **Anexo B (reproducibilidad):** enlace a las copias de los cuadernos en el Drive de cada integrante y lista de los archivos producidos. Si el equipo complementó el registro de eventos con su CSV (`ARCHIVO_EVENTOS`), se adjunta con la fuente de cada fila.
- Extensión orientativa: 5 a 7 páginas sin anexos.

No se entregan todavía la sección 6 (discusión y conclusiones) ni el anexo A (bitácora); sí conviene empezar la bitácora desde octubre.

## 3. Antes de escribir: verifique su corrida

Compare lo que imprimió su cuaderno con la tabla del [anexo](#anexo-su-provincia-en-los-datos-del-curso). Si trabaja con la provincia completa, los números deben coincidir; si eligió un cantón, deben ser menores o iguales.

| Revise | Dónde lo ve en el cuaderno | Si no coincide |
|---|---|---|
| La misma zona en `CR01`, `CR02`, `RD1_01` y `RD1_02` | Celda 1 (formulario) y nombre de la carpeta `<zona>` | Vuelva a correr con la zona correcta; no mezcle productos de zonas distintas |
| La estación elegida | Línea «Estación usada» y la lista de estaciones del curso que imprime `RD1_02` | Deje `ARCHIVO_ESTACION` vacío; si escribió un archivo, verifique que sea de su zona |
| Eventos de DesInventar | Conteo por origen en la sección 9 de `RD1_02` y `RD1_02_desinventar_<zona>.csv` | Revise que `USAR_DESINVENTAR` esté marcado y que la zona sea la correcta |
| Días del ECU 911 | Conteo por origen y `RD1_02_ecu911_<zona>.csv` | Revise `USAR_ECU911`; el cuaderno compara solo hasta 2024, porque allí terminan las series |
| Variables de la estación | Ficha de la estación: meses de Tmáx, Tmín, Tmed y lluvia | Si la estación no tiene una variable, esa variable se compara **solo entre ERA5 y CORe**, y se dice así en la sección 2 |

## 4. Qué debe mostrar cada sección

| Sección | Lo mínimo que se revisa | Preguntas que integra |
|---|---|---|
| **1. Territorio** | Mapa de la zona con las celdas de los reanálisis; relieve, cuencas principales, población expuesta y antecedentes de desastres de la provincia | `CR02` 1–2 |
| **2. Datos y métodos** | ERA5, CORe y la estación (nombre, código, red, coordenadas, altitud, variables y sus limitaciones); periodos de referencia; índice de ENSO usado; índices ETCCDI; prueba de tendencia; GEV; fuentes del registro de eventos y su vacío 2008 – junio de 2021 | «Para el informe» de `RD1_02` |
| **3. Clima normal y su variabilidad** | Temporada lluviosa con P10–P90 y máximo; meses en que actúan El Niño y La Niña, con su significancia; lluvia de la temporada según la intensidad del evento; zonas más sensibles en el mapa | `RD1_01` 1–5 |
| **4. Evidencias de cambio y extremos** | Tendencias de temperatura media y lluvia anual por década, con su significancia corregida y sin los años de El Niño; índices de extremos con tendencia; niveles de retorno de 10 y 25 años (1 y 5 días), zona frente a celda; extremos por fase de ENSO | `RD1_02` 1–4 |
| **5. Eventos registrados frente a la lluvia** | Cuántos eventos y de qué tipo trae cada fuente; porcentaje de inundaciones y deslizamientos con lluvia sobre el P95, **por fuente**; un evento con lluvia común explicado y una lluvia extrema sin registro; comparación DesInventar–ECU 911 | `RD1_02` 5–6 |

## 5. Rúbrica (2 puntos)

Cinco criterios de **0,40 puntos** cada uno. Cada criterio se califica en uno de cinco niveles.

| Criterio | Logrado (0,40) | Suficiente (0,30) | En proceso (0,20) | Inicial (0,10) | No presenta (0) |
|---|---|---|---|---|---|
| **1. Territorio, datos y métodos** (secciones 1 y 2) | Mapa con celdas; territorio descrito con relieve, cuencas, población y antecedentes; estación declarada con nombre, código, red, variables y limitaciones; periodos, índices y pruebas nombrados; vacío del registro reconocido | Todo lo anterior, con uno o dos elementos incompletos (por ejemplo, la estación sin sus limitaciones) | Falta el mapa o la declaración de la estación, o los periodos no corresponden a los del cuaderno | Descripción genérica de la provincia, sin datos ni métodos de la práctica | No se presentan las secciones |
| **2. Clima normal y ENSO** (sección 3) | Temporada lluviosa cuantificada (mm, P10–P90, máximo); meses de influencia de El Niño y La Niña con significancia; relación con la intensidad del evento y años más lluviosos identificados; zona sensible en el mapa con cantones | Resultados correctos con alguna pregunta respondida sin números del territorio | Figuras presentes pero mal leídas en un aspecto central (por ejemplo, confunde la señal de El Niño con la de La Niña) | Solo figuras, sin lectura | No se presenta |
| **3. Evidencias y extremos** (sección 4) | Tendencias por década con unidades, significancia corregida y prueba sin El Niño; índices de extremos con tendencia y concordancia entre fuentes; niveles de retorno de 10 y 25 años con intervalo, zona frente a celda y cuál usar para diseño | Correcto en lo esencial, con una omisión (por ejemplo, sin la prueba sin El Niño o sin intervalos) | Tendencias reportadas sin significancia o confundiendo zona y celda | Valores copiados sin interpretación | No se presenta |
| **4. Eventos frente a la lluvia** (sección 5) | Conteo por fuente y tipo; porcentaje sobre el P95 por fuente, sin sumar ni promediar fuentes; un evento con lluvia común y una lluvia extrema sin registro explicados; diferencias entre DesInventar y ECU 911 razonadas por lo que registra cada base | Correcto, con una explicación débil o sin el contraste entre bases | Mezcla las fuentes en un solo porcentaje o trata los incidentes del ECU 911 como desastres verificados | Solo la tabla o la figura del registro, sin análisis | No se presenta |
| **5. Forma y reproducibilidad** | Figuras y tablas numeradas, con título, fuente, unidad y escala, citadas antes de aparecer; respuestas integradas en el texto; citas APA 7; anexo B completo; los números coinciden con los productos del Drive | Uno o dos elementos de forma ausentes | Varias figuras sin unidad, fuente o escala, o anexo B incompleto | Documento desordenado; no se puede rastrear de dónde sale cada número | Sin anexo B y sin formato mínimo |

**Penalizaciones** (se descuentan del total del borrador): entrega fuera de plazo sin justificación, 0,20 por día; productos de una zona distinta a la declarada, el criterio afectado se califica como «Inicial».

## 6. Cómo se devuelve la retroalimentación

El docente devuelve el borrador con observaciones numeradas por sección (O1, O2, …). El equipo responde cada una en el **anexo C** del capítulo definitivo (matriz de atención a observaciones, ver la [guía sumativa](guia_sumativa.md#3-atención-a-las-observaciones-del-borrador)).

## Anexo. Su provincia en los datos del curso

Lo que deben encontrar los cuadernos para la **provincia completa** (repositorio a octubre de 2026). Sirve para verificar la corrida, no reemplaza el análisis.

- **Estación**: la que `RD1_02` elige sola con `ARCHIVO_ESTACION` vacío. Meses válidos de 1981–2024 (máximo 528). La lluvia del INAMHI 1964–2018 está rellenada con Climatol (apoyo CHIRPS).
- **DesInventar**: eventos hidrometeorológicos con fecha exacta, 1970–2007, y los dos tipos más frecuentes. «Niño» cuenta los eventos entre octubre de 1982 y julio de 1983, y entre octubre de 1997 y junio de 1998.
- **ECU 911**: días con incidentes de inundación, deslizamiento o lluvia intensa entre julio de 2021 y diciembre de 2024; entre paréntesis, los de 2023.

| Provincia | Estación que elige `RD1_02` | Meses válidos 1981–2024 | Limitación de la estación | DesInventar 1970–2007 (tipos principales) | Niño 1982–83 / 1997–98 | ECU 911, días jul 2021–2024 (2023) |
|---|---|---|---|---|---|---|
| Azuay | Mariscal Lamar (`synop/azuay_mariscal_lamar_84239.csv`) | Tmáx 152 · Tmín 133 · lluvia 456 | solo ~12 años de temperatura | 144 (deslizamiento 63, inundación 40) | 0 / 14 | 303 (80) |
| Bolívar | Chillanes (`synop/bolivar_chillanes_84189.csv`) | Tmáx 1 · Tmín 0 · lluvia 456 | sin temperatura en la estación | 42 (deslizamiento 19, inundación 9) | 1 / 13 | 6 (2) |
| Carchi | San Gabriel (`synop/carchi_san_gabriel_84036.csv`) | Tmáx 124 · Tmín 97 · lluvia 473 | solo ~10 años de temperatura | 22 (inundación 8, deslizamiento 6) | 0 / 0 | 3 (1) |
| Cañar | Cañar (`synop/canar_canar_84226.csv`) | Tmáx 126 · Tmín 41 · lluvia 456 | solo ~10 años de temperatura | 23 (deslizamiento 11, inundación 7) | 0 / 9 | 58 (13) |
| Chimborazo | Chimborazo (`synop/chimborazo_chimborazo_84176.csv`) | Tmáx 27 · Tmín 36 · lluvia 456 | sin temperatura en la estación | 80 (deslizamiento 45, inundación 14) | 6 / 13 | 100 (17) |
| Cotopaxi | Rumipamba (`synop/cotopaxi_rumipamba_84143.csv`) | Tmáx 144 · Tmín 89 · lluvia 478 | solo ~12 años de temperatura | 15 (inundación 7, deslizamiento 5) | 0 / 5 | 34 (6) |
| El Oro | Santa Rosa Aeropuerto (`synop/el_oro_santa_rosa_aeropuerto_84252.csv`) | Tmáx 92 · Tmín 69 · lluvia 3 | solo ~7 años de temperatura; sin lluvia en la estación | 154 (inundación 71, sequía 22) | 9 / 22 | 24 (14) |
| Esmeraldas | La Concordia (`synop/esmeraldas_la_concordia_84050.csv`) | Tmáx 181 · Tmín 134 · lluvia 491 | — | 186 (inundación 88, deslizamiento 43) | 7 / 32 | 19 (10) |
| Galápagos | Baltra (`redes/galapagos_baltra_84001.csv`) | Tmáx 30 · Tmín 28 · lluvia 0 | sin temperatura en la estación; sin lluvia en la estación | 13 (incendio forestal 4, lluvia intensa 3) | 2 / 4 | 0 (0) |
| Guayas | José Joaquín de Olmedo (Guayaquil) (`synop/guayas_simon_bolivar_intl_jose_joaqui_84203.csv`) | Tmáx 151 · Tmín 132 · lluvia 456 | solo ~12 años de temperatura | 416 (inundación 288, lluvia intensa 38) | 22 / 70 | 63 (30) |
| Imbabura | Inguincho (`synop/imbabura_inguincho_84045.csv`) | Tmáx 67 · Tmín 8 · lluvia 473 | solo ~5 años de temperatura | 56 (deslizamiento 19, inundación 14) | 0 / 2 | 98 (40) |
| Loja | Loja/La Argelia (`synop/loja_loja_la_argelia_84270.csv`) | Tmáx 131 · Tmín 86 · lluvia 476 | solo ~10 años de temperatura | 84 (deslizamiento 37, inundación 20) | 2 / 20 | 46 (15) |
| Los Ríos | Pichilingue (`synop/los_rios_pichilingue_84140.csv`) | Tmáx 145 · Tmín 98 · lluvia 486 | solo ~12 años de temperatura | 179 (inundación 139, deslizamiento 16) | 9 / 47 | 13 (7) |
| Manabí | Manta Aeropuerto Eloy Alfaro (METAR) (`manabi_manta_aeropuerto_semt_metar.csv`) | Tmáx 224 · Tmín 224 · Tmed 224 · lluvia 456 | — | 387 (inundación 188, deslizamiento 85) | 18 / 116 | 9 (5) |
| Morona Santiago | Coronel Edmundo Carvajal (`synop/morona_santiago_coronel_edmundo_carvajal_84217.csv`) | Tmáx 57 · Tmín 86 · lluvia 456 | solo ~7 años de temperatura | 31 (deslizamiento 16, aluvión 6) | 0 / 3 | 5 (0) |
| Napo | Baeza (`inamhi/napo/m0215.csv`) | Tmáx 0 · Tmín 0 · lluvia 456 | sin temperatura en la estación | 38 (deslizamiento 15, inundación 12) | 0 / 5 | 9 (1) |
| Orellana | Nuevo Rocafuerte (`synop/orellana_nuevo_rocafuerte_84132.csv`) | Tmáx 123 · Tmín 86 · lluvia 456 | solo ~10 años de temperatura | 16 (inundación 10, lluvia intensa 3) | 0 / 2 | 13 (2) |
| Pastaza | Puyo (`synop/pastaza_puyo_84179.csv`) | Tmáx 107 · Tmín 61 · lluvia 468 | solo ~8 años de temperatura | 74 (inundación 33, deslizamiento 21) | 0 / 6 | 18 (7) |
| Pichincha | Izobamba (`synop/pichincha_izobamba_84088.csv`) | Tmáx 177 · Tmín 134 · lluvia 506 | solo ~14 años de temperatura | 320 (deslizamiento 98, inundación 96) | 27 / 4 | 161 (33) |
| Santa Elena | General Ulpiano Paez (`synop/santa_elena_general_ulpiano_paez_84200.csv`) | Tmáx 91 · Tmín 89 · lluvia 456 | solo ~7 años de temperatura | 25 (inundación 13, oleaje 5) | 1 / 10 | 1 (0) |
| Santo Domingo de los Tsáchilas | Puerto Ila (`synop/santo_domingo_de_los_tsachilas_puerto_ila_84105.csv`) | Tmáx 116 · Tmín 71 · lluvia 489 | solo ~9 años de temperatura | 49 (inundación 23, deslizamiento 18) | 0 / 1 | 14 (6) |
| Sucumbíos | Nueva Loja Aeropuerto (`synop/sucumbios_nueva_loja_aeropuer_84063.csv`) | Tmáx 66 · Tmín 91 · lluvia 41 | solo ~7 años de temperatura; sin lluvia en la estación | 20 (inundación 10, deslizamiento 7) | 0 / 1 | 7 (1) |
| Tungurahua | Querochaca (`synop/tungurahua_querochaca_84160.csv`) | Tmáx 142 · Tmín 95 · lluvia 470 | solo ~11 años de temperatura | 86 (deslizamiento 42, inundación 15) | 0 / 4 | 99 (29) |
| Zamora Chinchipe | Zamora (`inamhi/zamora_chinchipe/m0207.csv`) | Tmáx 0 · Tmín 0 · lluvia 456 | sin temperatura en la estación | 67 (deslizamiento 36, inundación 13) | 2 / 10 | 24 (3) |

**Cómo leer el anexo.**

- *Sin temperatura en la estación* (Bolívar, Chimborazo, Napo, Zamora Chinchipe, Galápagos): la temperatura se compara solo entre ERA5 y CORe; no se busca otra estación fuera de la provincia salvo indicación del docente.
- *Sin lluvia en la estación* (El Oro, Sucumbíos, Galápagos): la lluvia se analiza solo con ERA5 y CORe. En El Oro y Sucumbíos, la lista que imprime `RD1_02` muestra estaciones del INAMHI de solo lluvia; el equipo puede escribir una de ellas en `ARCHIVO_ESTACION` y volver a correr para comparar la lluvia, y lo declara en la sección 2.
- *Pocos años de temperatura*: no alcanzan para una tendencia; sirven para comparar el sesgo de los reanálisis en los años comunes.
- *Pocos eventos* (Carchi, Cotopaxi, Orellana, Sucumbíos, Santa Elena, Galápagos o un cantón): el porcentaje sobre el P95 se reporta con el número de eventos (por ejemplo, «3 de 5»), no como porcentaje solo.
- *Pichincha* registra más eventos en 1982–83 que en 1997–98, al revés que la Costa: es un resultado para discutir, no un error.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
