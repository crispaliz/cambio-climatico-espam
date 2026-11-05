# Práctica 2 — Riesgo climático del territorio y sus medidas (Riesgos de Desastres)

Evidencia el RA B de la Unidad II y entrega el **capítulo 2** del proyecto de cada equipo: qué está expuesto a las amenazas del capítulo 1, qué tan vulnerable es y qué medidas de reducción del riesgo y adaptación convienen. Equipos de dos, la misma provincia de la Práctica 1. Marco: riesgo = amenaza × exposición × vulnerabilidad (IPCC AR6, GTII).

## Pasos de esta práctica

| Paso | Fecha | Cuaderno | Qué hace | Producto |
|---|---|---|---|---|
| 1 | Vie 6 nov | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-2/RD2_01_exposicion.ipynb) `RD2_01_exposicion` | Evidencia de la amenaza del capítulo 1; elementos expuestos por cantón (población, zona baja, ladera, servicios críticos, vías, eventos); exposición 1–5 por cantón y amenaza; revisión del equipo; cantones prioritarios; planilla del inventario | Tabla de exposición |
| 2 | Vie 20 nov | `RD2_02_vulnerabilidad` (en preparación) | Sensibilidad y capacidad de adaptación de los cantones prioritarios; índice de riesgo | Ficha de vulnerabilidad |
| 3 | Vie 27 nov | `RD2_03_matriz_medidas` (en preparación) | Medidas de reducción del riesgo y adaptación, evaluación multicriterio. Evaluación formativa (2 pts) | Borrador del capítulo 2 |
| — | Vie 4 dic | — | Cierre del capítulo. Sumativa (8 pts): resolución de problemas, con criterio de habilidad blanda | Capítulo 2 |

Los productos quedan en `Mi unidad/CC_Riesgos/practica-2/<provincia>/`; los del capítulo 1 se leen de `CC_Riesgos/practica-1/<zona>/`. Los dos integrantes del equipo ejecutan el cuaderno, cada uno en su Drive.

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

**Antes del 20 de noviembre:** la planilla completa en su carpeta de Drive con el mismo nombre; el paso 2 la lee.

## Datos

El cuaderno no descarga nada: lee del repositorio la [tabla nacional de exposición por cantón](../../../datos/exposicion/) y los registros de eventos de [`datos/eventos`](../../../datos/eventos/). La calificación de la exposición es relativa a la provincia (quintiles) y la revisa el equipo; ver [`herramientas/exposicion`](../../../herramientas/exposicion/__init__.py).
