# Ingeniería Ambiental · Práctica 2 — Emisiones, riesgo y estrategias

Evidencia el RA B de la Unidad II y entrega el **capítulo 2** del proyecto. Trabajo individual, la misma provincia de la Práctica 1.

## Pasos de esta práctica

| Paso | Cuaderno | Qué hace | Productos en `Mi unidad/CC_Ambiental/practica-2/<provincia>/` |
|---|---|---|---|
| 1 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-2/IA2_01_inventario_emisiones.ipynb) `IA2_01_inventario_emisiones` | Inventario simplificado de GEI de la provincia (IPCC 2006, Nivel 1; PCG del AR5): energía, agricultura, USCUSS y residuos; categorías principales, incertidumbre (enfoque 1), completitud y comparación con el inventario nacional 2022 | `IA2_01_*` |
| 2 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-2/IA2_02_ficha_riesgo.ipynb) `IA2_02_ficha_riesgo` | Ficha de riesgo de un sitio con el marco del AR6 (amenaza × exposición × vulnerabilidad): evidencia climática de la Práctica 1 (factor de El Niño, Rx1day de 25 años, días cálidos), calificaciones de campo justificadas, índice por amenaza y ficha de una página | `IA2_02_*` |
| 3 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-2/IA2_03_matriz_estrategias.ipynb) `IA2_03_matriz_estrategias` | Opciones de mitigación y adaptación sugeridas por los pasos 1 y 2, evaluación multicriterio con pesos, robustez, gráfico de efectividad frente a factibilidad y cartera priorizada. Evaluación formativa | `IA2_03_*` |

Con los productos de los tres pasos se arma el capítulo 2 con la [plantilla](capitulo-2_plantilla.md): el borrador es la evaluación formativa (2 puntos, [guía y rúbrica](guia_formativa.md), con la hoja de campo para la ficha de riesgo en su anexo).

## Datos

- **Paso 1:** el cuaderno no descarga datos de actividad; cada estudiante los busca en las fuentes oficiales (tabla de la sección 3 del cuaderno) y los registra con su fuente. La población viene del Censo 2022 ([`datos/inventario`](../../../datos/inventario/)) y los factores, de [`herramientas/inventario`](../../../herramientas/inventario/).
- **Paso 2:** usa las series de `CR02` y los años de El Niño de `IA1_03` de la Práctica 1 ([`herramientas/riesgo.py`](../../../herramientas/riesgo.py)).
- **Paso 3:** usa los productos de los pasos 1 y 2 y el catálogo de opciones de [`herramientas/estrategias.py`](../../../herramientas/estrategias.py).

Lo que no se encuentra queda como **NE (no estimado)** y se discute en el capítulo.
