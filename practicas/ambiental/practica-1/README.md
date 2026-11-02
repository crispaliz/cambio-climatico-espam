# Ingeniería Ambiental · Práctica 1 — Diagnóstico del clima observado

Evidencia el RA A de la Unidad I y entrega el **capítulo 1** del proyecto. Trabajo individual, una provincia o un cantón por estudiante.

## Antes: cuadernos comunes

Los cuadernos no están en Drive: se abren desde este repositorio con el botón «Open in Colab» y se guarda una copia con **Archivo › Guardar una copia en Drive**. Los datos se obtienen con los cuadernos comunes a las dos carreras ([`practicas/comun/reanalisis`](../../comun/reanalisis/)): **CR01** descarga y **CR02** series, que quedan en `Mi unidad/CC_datos/<zona>/`.

## Pasos de esta práctica

| Paso | Cuaderno | Qué hace | Productos en `Mi unidad/CC_Ambiental/practica-1/<zona>/` |
|---|---|---|---|
| 1 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-1/IA1_01_climatologia.ipynb) `IA1_01_climatologia` | Climatología 1995–2014 de las 9 variables con ERA5 y CORe; climograma; humedad, presión y viento; diferencias entre reanálisis | `IA1_01_*` |
| 2 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-1/IA1_02_estacion_vs_reanalisis.ipynb) `IA1_02_estacion_vs_reanalisis` | Contraste de la estación del curso elegida automáticamente para la zona ([`datos/estaciones`](../../../datos/estaciones/)) con los dos reanálisis, solo en las variables que mide; métricas mensuales y diarias | `IA1_02_*` |
| 3 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-1/IA1_03_tendencias_enso.ipynb) `IA1_03_tendencias_enso` | Tendencias 1981–2024 (Sen y Mann-Kendall corregido por autocorrelación), prueba sin los años de El Niño, tendencia según el año de inicio, compuestos mensuales por fase de ENSO, señal/ruido y estado actual de ENSO. Evaluación formativa | `IA1_03_*` |

Con los productos de los tres pasos se arma el capítulo 1 con la [plantilla](capitulo-1_plantilla.md): el borrador es la evaluación formativa (2 puntos, [guía y rúbrica](guia_formativa.md)) y el capítulo corregido con su exposición oral, la sumativa (8 puntos, estudio de casos, [guía y rúbrica](guia_sumativa.md)). La guía formativa trae, por provincia, la estación que elige `IA1_02` y las preguntas que aplican. El evento El Niño en curso va en la [bitácora](../../comun/bitacora/), como anexo.

Datos de estación: formato común en [`practicas/comun/estaciones`](../../comun/estaciones/).

## Evaluación

| Entrega | Valor | Guía y rúbrica |
|---|---|---|
| Borrador del capítulo 1 (formativa) | 2 puntos | [`guia_formativa.md`](guia_formativa.md) |
| Capítulo definitivo y exposición oral (sumativa, estudio de casos) | 8 puntos | [`guia_sumativa.md`](guia_sumativa.md) |
