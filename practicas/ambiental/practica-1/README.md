# Ingeniería Ambiental · Práctica 1 — Diagnóstico del clima observado

Evidencia el RA A de la Unidad I y entrega el **capítulo 1** del proyecto. Trabajo individual, una provincia o un cantón por estudiante.

## Antes: cuadernos comunes

Los datos se obtienen con los cuadernos comunes a las dos carreras ([`practicas/comun/reanalisis`](../../comun/reanalisis/)): **CR01** descarga y **CR02** series, que quedan en `Mi unidad/CC_datos/<zona>/`.

## Pasos de esta práctica

| Paso | Cuaderno | Qué hace | Productos en `Mi unidad/CC_Ambiental/practica-1/<zona>/` |
|---|---|---|---|
| 1 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-1/IA1_01_climatologia.ipynb) `IA1_01_climatologia` | Climatología 1995–2014 de las 9 variables con ERA5 y CORe; climograma; humedad, presión y viento; diferencias entre reanálisis | `IA1_01_*` |
| 2 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-1/IA1_02_estacion_vs_reanalisis.ipynb) `IA1_02_estacion_vs_reanalisis` | Contraste de una estación con los dos reanálisis en todas las variables que mida; métricas mensuales y diarias | `IA1_02_*` |
| 3 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-1/IA1_03_tendencias_enso.ipynb) `IA1_03_tendencias_enso` | Tendencias 1981–2024 (Sen y Mann-Kendall corregido por autocorrelación), prueba sin los años de El Niño, tendencia según el año de inicio, compuestos mensuales por fase de ENSO, señal/ruido y estado actual de ENSO. Evaluación formativa | `IA1_03_*` |

Con los productos de los tres pasos se arma el capítulo 1 con la [plantilla](capitulo-1_plantilla.md): el borrador es la evaluación formativa y el capítulo corregido, la sumativa (estudio de casos). El evento El Niño en curso va en la [bitácora](../../comun/bitacora/), como anexo.

Datos de estación: formato común en [`practicas/comun/estaciones`](../../comun/estaciones/).

## Criterio de evaluación

- Cuadernos comunes y de la práctica ejecutados en orden y de principio a fin, con inventario y metadatos completos.
- Unidades correctas, verificadas con las comprobaciones de cada cuaderno.
- Respuestas a las preguntas finales con los números de su zona.
