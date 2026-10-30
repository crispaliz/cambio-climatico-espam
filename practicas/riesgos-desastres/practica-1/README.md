# Práctica 1 — Clima, ENSO y extremos del territorio (Riesgos de Desastres)

Evidencia el RA A de la Unidad I y entrega el **capítulo 1** del proyecto de cada equipo. Funciona para cualquier provincia del Ecuador o un cantón, elegidos en el formulario de la celda 1 de cada cuaderno (la misma zona en todos).

## Antes: cuadernos comunes

Los datos se obtienen con los cuadernos comunes a las dos carreras ([`practicas/comun/reanalisis`](../../comun/reanalisis/)): **CR01** descarga y **CR02** series, que quedan en `Mi unidad/CC_datos/<zona>/`. Para el paso 2 descargue CORe diario (`CORE_DIARIO` marcado, por defecto) o use la opción B.

## Pasos de esta práctica

| Paso | Cuaderno | Qué hace | Productos |
|---|---|---|---|
| 1 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-1/RD1_01_ciclo_anual_enso.ipynb) `RD1_01_ciclo_anual_enso` | Ciclo anual con rangos de variabilidad; ICEN y ONI; compuestos mensuales por fase; lluvia de la temporada según la intensidad del evento; mapa de la anomalía en años de El Niño | `RD1_01_*` |
| 2 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-1/RD1_02_extremos_eventos.ipynb) `RD1_02_extremos_eventos` | Tendencia de la temperatura media y la lluvia anual (con y sin años de El Niño); índices ETCCDI, tendencias (Sen y Mann-Kendall corregido por autocorrelación), extremos por fase de ENSO, periodos de retorno (GEV), lluvias candidatas y registro de eventos de la zona (DesInventar 1970–2007 y ECU 911 desde 2021, automáticos) contrastado con la lluvia previa; estación del curso elegida automáticamente. Evaluación formativa | `RD1_02_*` |

Los productos quedan en `Mi unidad/CC_Riesgos/practica-1/<zona>/`; las series se leen de `CC_datos/<zona>/`. Los dos integrantes del equipo ejecutan los cuadernos, cada uno en su Drive.

Con los productos de los dos cuadernos se arma el capítulo 1 con la [plantilla](capitulo-1_plantilla.md): el borrador es la evaluación formativa y el capítulo corregido, la sumativa (estudio de casos). El evento El Niño en curso va en la [bitácora](../../comun/bitacora/), como anexo.

## Índices de ENSO

| Índice | Región | Uso | Regla |
|---|---|---|---|
| ICEN (ENFEN) | Niño 1+2, frente a la costa | El Niño costero; recomendado en la Costa | ≥ 0,4 °C (cálida) o < −1,0 °C (fría) durante 3 meses seguidos |
| ONI (NOAA) | Niño 3.4, Pacífico central | Teleconexión de gran escala | ±0,5 °C durante 5 trimestres seguidos |

Ambos se calculan de ERSSTv5 (base 1991–2020) y se descargan de NOAA en cada ejecución; queda una copia en `CC_datos/<zona>/` por si falla la conexión.

## Registro de eventos

`RD1_02` arma el registro de la zona **automáticamente** con dos bases públicas; el equipo no llena ninguna planilla.

| Fuente | Periodo | Cómo se usa |
|---|---|---|
| [DesInventar Ecuador](https://db.desinventar.org/DesInventar/country_profile.jsp?countrycode=ecu&lang=ES) (UNDRR) | 1970–2007 | **Automática** (`USAR_DESINVENTAR`): desastres de origen hidrometeorológico con fecha exacta, cantón, tipo y daños. Queda en `RD1_02_desinventar_<zona>.csv`. Datos procesados en [`datos/eventos`](../../../datos/eventos/) |
| ECU 911, [Base de Emergencias](https://www.datosabiertos.gob.ec/dataset/base-de-emergencias) (Datos Abiertos) | julio de 2021 en adelante | **Automática** (`USAR_ECU911`): incidentes diarios de gestión de riesgos por parroquia; fecha y lugar, sin daños. Queda en `RD1_02_ecu911_<zona>.csv` |
| [Informes de situación (SitRep) de la SNGR](https://www.gestionderiesgos.gob.ec/informes-de-situacion-actual-por-eventos-adversos-ecuador/), GAD y prensa local con fecha | 2008 – junio de 2021 | **Opcional**: periodo sin base pública por evento. El equipo puede complementarlo con un CSV propio indicado en `ARCHIVO_EVENTOS` |

El registro completo de la zona queda en `RD1_02_registro_eventos_<zona>.csv`, con la columna `origen` (DesInventar, ECU 911 o equipo). El conjunto «Eventos Peligrosos» que la SNGR publicaba en Datos Abiertos ya no está disponible en el portal (consulta del 22 de octubre de 2026).

**Complemento opcional del equipo.** Mismas columnas que la plantilla [`registro_eventos.csv`](registro_eventos.csv) de esta carpeta, una fila por evento y siempre con su fuente:

| Columna | Contenido |
|---|---|
| `fecha_inicio`, `fecha_fin` | AAAA-MM-DD |
| `tipo` | inundación, deslizamiento, aluvión, lluvia intensa, sequía, incendio forestal, vendaval, oleaje u otro |
| `canton`, `parroquia`, `descripcion` | lugar y qué pasó |
| `fallecidos`, `afectados`, `viviendas_afectadas` | vacío si no se reporta (nunca 0 por defecto) |
| `fuente`, `url` | obligatorio |

## Estación

Con `ARCHIVO_ESTACION` vacío, `RD1_02` agrega sola la estación del curso con más datos para la zona ([`datos/estaciones`](../../../datos/estaciones/)) y muestra las demás disponibles. Con `"ninguna"` trabaja solo con ERA5 y CORe.

## Cuidados de interpretación

- Las series de zona son **promedios de área**: atenúan la lluvia de un sitio. Para intensidades de diseño use la celda de ERA5 o una estación.
- Con ~40 años de datos, los periodos de retorno mayores de 50 años son extrapolación y se reportan con su intervalo.
- El evento El Niño 2026 en curso va en la bitácora, separado del análisis climatológico: sus datos son preliminares.
