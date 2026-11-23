# Práctica 2 — Riesgo climático del territorio y sus medidas (Riesgos de Desastres)

Evidencia el RA B de la Unidad II y entrega el **capítulo 2** del proyecto de cada equipo: qué está expuesto a las amenazas del capítulo 1, qué tan vulnerable es, dónde está el mayor riesgo y qué medidas de reducción del riesgo, adaptación y mitigación convienen, diferenciando su alcance. Equipos de dos, la misma provincia de la Práctica 1. Marco: riesgo = amenaza × exposición × vulnerabilidad (IPCC AR6, GTII).

| Contenido de la Unidad II | Dónde se trabaja |
|---|---|
| 2.1 Marco institucional y normativo: CMNUCC, Acuerdo de París, NDC, Marco de Sendai | `RD2_03`, sección 9 (marco normativo de cada medida) |
| 2.2 Estrategias de mitigación | `RD2_03`, secciones 4 a 6 (medidas M y MA; al menos una de mitigación pura) |
| 2.3 Estrategias de adaptación: basada en ecosistemas, infraestructura resiliente, alerta temprana | `RD2_02` (qué reducir) y `RD2_03` (medidas A y MA) |
| 2.4 Análisis comparativo de mitigación y adaptación; PLANACC | `RD2_03`, secciones 4, 7 y 10 (alcance, matriz y riesgo residual) |

## Pasos de esta práctica

| Paso | Fecha | Cuaderno | Guía del estudiante | Qué hace | Producto |
|---|---|---|---|---|---|
| 1 | Vie 6 nov | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-2/RD2_01_exposicion.ipynb) `RD2_01_exposicion` | [guia_RD2_01](guia_RD2_01.md) | Evidencia de la amenaza del capítulo 1; elementos expuestos por cantón; exposición 1–5 por cantón y amenaza; revisión del equipo; cantones prioritarios; planilla del inventario | Tabla de exposición |
| 2 | Lun 23 nov (clase) y trabajo autónomo hasta el jue 26 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-2/RD2_02_vulnerabilidad.ipynb) `RD2_02_vulnerabilidad` | [guia_RD2_02](guia_RD2_02.md) | Amenaza de la provincia con sugerencia; datos de apoyo por cantón; planilla de sensibilidad y capacidad de adaptación; vulnerabilidad; índice de riesgo por cantón y amenaza; cantón y amenaza críticos | Planilla de vulnerabilidad y matriz de riesgo |
| 3 | Vie 27 nov | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-2/RD2_03_matriz_medidas.ipynb) `RD2_03_matriz_medidas` | [guia_RD2_03](guia_RD2_03.md) | Alcance de mitigación y adaptación; evaluación multicriterio de medidas A, MA y M; robustez; marco normativo (NDC, PLANACC, Sendai, actor); cartera y riesgo residual | Matriz de medidas y cartera |
| — | Dom 29 nov, 23:59 | — | [guia_formativa](guia_formativa.md) | **Evaluación formativa (2 pts)**: borrador de las secciones 1 a 4 | Borrador del capítulo 2 |
| — | Vie 4 dic | — | [guia_sumativa](guia_sumativa.md) | **Sumativa (8 pts)**: capítulo definitivo, caso de resolución de problemas (habilidad blanda) y defensa; con modalidad de contingencia | Capítulo 2 |

Las fechas de entrega son las propuestas por el docente; las que valen son las del aula virtual. Con los productos de los tres cuadernos se arma el capítulo 2 con la [plantilla](capitulo-2_plantilla.md), que trae la organización del trabajo del equipo, un calendario sugerido, la numeración de figuras y tablas y ejemplos de redacción.

Los productos quedan en `Mi unidad/CC_Riesgos/practica-2/<provincia>/`; los del capítulo 1 se leen de `CC_Riesgos/practica-1/<zona>/`. Los dos integrantes del equipo ejecutan los cuadernos, cada uno en su Drive, con **una sola versión** del inventario, de la planilla de vulnerabilidad y de la evaluación de medidas.

## Paso 1 · exposición: qué hacer

**En clase (1 hora con el docente).**

1. Abrir `RD2_01_exposicion` en Colab, **Archivo › Guardar una copia en Drive**, y completar la celda 1 con la misma provincia de la Práctica 1.
2. Revisar la evidencia del capítulo 1 (sección 3) y marcar en la sección 4 las dos o tres amenazas principales, cada una con **el número** que la justifica.
3. Ejecutar las secciones 5 a 8 y leer la matriz: qué cantones son los más expuestos a cada amenaza y por qué indicador.
4. Corregir en la sección 7 lo que el equipo sepa del territorio y la matriz no refleje, con su fuente.

**Sin docente (2 horas).**

5. Completar la planilla `RD2_01_inventario_expuestos_<provincia>.xlsx` (sección 9): para cada cantón prioritario, al menos **tres elementos concretos** expuestos (un barrio o comunidad, un servicio crítico y una vía o un medio de vida), con nombre, ubicación y fuente.
6. Fuentes recomendadas: PDOT del cantón (diagnóstico biofísico y de asentamientos humanos), mapas de amenaza del GAD o de la Secretaría de Gestión de Riesgos, geoportal del IGM, Google Earth.
7. Responder las preguntas de la sección 11: son el borrador de la sección «Exposición» del capítulo 2.

## Paso 2 · vulnerabilidad y riesgo: qué hacer

**En clase.** Ejecutar `RD2_02_vulnerabilidad` completo con la misma provincia: sale un resultado **provisional** que sirve para ver el flujo. Revisar la sugerencia de amenaza (sección 4) y los datos de apoyo (sección 5).

**Sin docente.** Completar la planilla `RD2_02_vulnerabilidad_<provincia>.xlsx` (9 filas por cantón prioritario: dato, valor 1–5, fuente y justificación) con el Censo 2022, el PDOT y la SNGR, y ejecutar el cuaderno desde la sección 7 hasta que no diga «PROVISIONAL».

## Paso 3 · medidas: qué hacer

**En clase.** Ejecutar `RD2_03_matriz_medidas` hasta la sección 5, copiar el bloque de medidas sugeridas y acordar en equipo cuáles evaluar (6 a 10, con al menos una de mitigación pura).

**Sin docente.** Calificar cada medida con su justificación, justificar los pesos, ejecutar el resto y redactar la sección 4 del capítulo.

## Datos

Los cuadernos no descargan nada pesado: leen del repositorio la [tabla nacional de exposición por cantón](../../../datos/exposicion/) y los registros de eventos de [`datos/eventos`](../../../datos/eventos/), y el catálogo de medidas de [`herramientas/estrategias.py`](../../../herramientas/estrategias.py). La calificación de la exposición es relativa a la provincia (quintiles), o al país si la provincia tiene menos de 5 cantones, y la revisa el equipo; ver [`herramientas/exposicion`](../../../herramientas/exposicion/__init__.py). La vulnerabilidad, el riesgo por cantón y el efecto de las medidas están en [`herramientas/vulnerabilidad.py`](../../../herramientas/vulnerabilidad.py).

**La Concordia** se cuenta en Santo Domingo de los Tsáchilas, provincia a la que pertenece desde 2013, aunque la cartografía del curso la ubica en Esmeraldas. Los equipos de esas dos provincias que ejecutaron `RD2_01` antes del 23 de noviembre deben volver a ejecutarlo.
