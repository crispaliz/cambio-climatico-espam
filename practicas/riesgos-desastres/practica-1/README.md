# Práctica 1 — Clima, ENSO y extremos del territorio (Riesgos de Desastres)

Evidencia el RA A de la Unidad I y entrega el **capítulo 1** del proyecto de cada equipo. Funciona para cualquier provincia del Ecuador o un cantón, elegidos en el formulario de la celda 1 de cada cuaderno (la misma zona en todos).

## Antes: cuadernos comunes

Los datos se obtienen con los cuadernos comunes a las dos carreras ([`practicas/comun/reanalisis`](../../comun/reanalisis/)): **CR01** descarga y **CR02** series, que quedan en `Mi unidad/CC_datos/<zona>/`. Para el paso 2 descargue CORe diario (`CORE_DIARIO` marcado, por defecto) o use la opción B.

## Pasos de esta práctica

| Paso | Cuaderno | Qué hace | Productos |
|---|---|---|---|
| 1 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-1/RD1_01_ciclo_anual_enso.ipynb) `RD1_01_ciclo_anual_enso` | Ciclo anual con rangos de variabilidad; ICEN y ONI; compuestos mensuales por fase; lluvia de la temporada según la intensidad del evento; mapa de la anomalía en años de El Niño | `RD1_01_*` |
| 2 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-1/RD1_02_extremos_eventos.ipynb) `RD1_02_extremos_eventos` | Índices ETCCDI, tendencias (Sen y Mann-Kendall), extremos por fase de ENSO, periodos de retorno (GEV), lluvias candidatas y registro de eventos contrastado | `RD1_02_*` |

Los productos quedan en `Mi unidad/CC_Riesgos/practica-1/<zona>/`; las series se leen de `CC_datos/<zona>/`. Los dos integrantes del equipo ejecutan los cuadernos, cada uno en su Drive.

## Índices de ENSO

| Índice | Región | Uso | Regla |
|---|---|---|---|
| ICEN (ENFEN) | Niño 1+2, frente a la costa | El Niño costero; recomendado en la Costa | ≥ 0,4 °C (cálida) o < −1,0 °C (fría) durante 3 meses seguidos |
| ONI (NOAA) | Niño 3.4, Pacífico central | Teleconexión de gran escala | ±0,5 °C durante 5 trimestres seguidos |

Ambos se calculan de ERSSTv5 (base 1991–2020) y se descargan de NOAA en cada ejecución; queda una copia en `CC_datos/<zona>/` por si falla la conexión.

## Registro de eventos (`registro_eventos.csv`)

Plantilla en esta carpeta. Una fila por evento, **siempre con su fuente**. Fuentes sugeridas: base DesInventar del Ecuador, informes de situación de la Secretaría Nacional de Gestión de Riesgos, registros de los GAD y prensa local con fecha.

| Columna | Contenido |
|---|---|
| `fecha_inicio`, `fecha_fin` | AAAA-MM-DD |
| `tipo` | inundación, deslizamiento, aluvión, sequía, incendio forestal, vendaval, oleaje u otro |
| `canton`, `parroquia`, `descripcion` | lugar y qué pasó |
| `fallecidos`, `afectados`, `viviendas_afectadas` | vacío si no se reporta (nunca 0 por defecto) |
| `fuente`, `url` | obligatorio |

Súbalo a `Mi unidad/CC_Riesgos/practica-1/<zona>/` o indique su ruta en la celda 1 del paso 2. Si no existe, el cuaderno crea la plantilla allí.

## Cuidados de interpretación

- Las series de zona son **promedios de área**: atenúan la lluvia de un sitio. Para intensidades de diseño use la celda de ERA5 o una estación.
- Con ~40 años de datos, los periodos de retorno mayores de 50 años son extrapolación y se reportan con su intervalo.
- El evento El Niño 2026 en curso va en la bitácora, separado del análisis climatológico: sus datos son preliminares.
