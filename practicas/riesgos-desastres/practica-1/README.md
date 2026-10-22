# Práctica 1 — Clima, ENSO y extremos del territorio (Riesgos de Desastres)

Evidencia el RA A de la Unidad I y entrega el **capítulo 1** del proyecto de cada equipo. Funciona para cualquier provincia del Ecuador o un cantón, elegidos en el formulario de la celda 1 de cada cuaderno (la misma zona en todos).

## Antes: cuadernos comunes

Los datos se obtienen con los cuadernos comunes a las dos carreras ([`practicas/comun/reanalisis`](../../comun/reanalisis/)): **CR01** descarga y **CR02** series, que quedan en `Mi unidad/CC_datos/<zona>/`. Para el paso 2 descargue CORe diario (`CORE_DIARIO` marcado, por defecto) o use la opción B.

## Pasos de esta práctica

| Paso | Cuaderno | Qué hace | Productos |
|---|---|---|---|
| 1 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-1/RD1_01_ciclo_anual_enso.ipynb) `RD1_01_ciclo_anual_enso` | Ciclo anual con rangos de variabilidad; ICEN y ONI; compuestos mensuales por fase; lluvia de la temporada según la intensidad del evento; mapa de la anomalía en años de El Niño | `RD1_01_*` |
| 2 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-1/RD1_02_extremos_eventos.ipynb) `RD1_02_extremos_eventos` | Tendencia de la temperatura media y la lluvia anual (con y sin años de El Niño); índices ETCCDI, tendencias (Sen y Mann-Kendall corregido por autocorrelación), extremos por fase de ENSO, periodos de retorno (GEV), lluvias candidatas y registro de eventos contrastado, con los incidentes del ECU 911 de la zona. Evaluación formativa | `RD1_02_*` |

Los productos quedan en `Mi unidad/CC_Riesgos/practica-1/<zona>/`; las series se leen de `CC_datos/<zona>/`. Los dos integrantes del equipo ejecutan los cuadernos, cada uno en su Drive.

Con los productos de los dos cuadernos se arma el capítulo 1 con la [plantilla](capitulo-1_plantilla.md): el borrador es la evaluación formativa y el capítulo corregido, la sumativa (estudio de casos). El evento El Niño en curso va en la [bitácora](../../comun/bitacora/), como anexo.

## Índices de ENSO

| Índice | Región | Uso | Regla |
|---|---|---|---|
| ICEN (ENFEN) | Niño 1+2, frente a la costa | El Niño costero; recomendado en la Costa | ≥ 0,4 °C (cálida) o < −1,0 °C (fría) durante 3 meses seguidos |
| ONI (NOAA) | Niño 3.4, Pacífico central | Teleconexión de gran escala | ±0,5 °C durante 5 trimestres seguidos |

Ambos se calculan de ERSSTv5 (base 1991–2020) y se descargan de NOAA en cada ejecución; queda una copia en `CC_datos/<zona>/` por si falla la conexión.

## Registro de eventos (`registro_eventos.csv`)

Plantilla en esta carpeta. Una fila por evento, **siempre con su fuente**.

| Fuente | Periodo | Cómo se usa |
|---|---|---|
| ECU 911, [Base de Emergencias](https://www.datosabiertos.gob.ec/dataset/base-de-emergencias) (Datos Abiertos) | julio de 2021 en adelante | **Automática** en `RD1_02` (`USAR_ECU911`): incidentes diarios de gestión de riesgos por parroquia; fecha y lugar, sin daños. Queda en `RD1_02_ecu911_<zona>.csv` |
| [DesInventar, Ecuador](https://db.desinventar.org/DesInventar/country_profile.jsp?countrycode=ecu&lang=ES) (UNDRR) | 1970–2007 | A mano: eventos con daños, incluidos El Niño 1982–83 y 1997–98 |
| [Informes de situación (SitRep) de la SNGR](https://www.gestionderiesgos.gob.ec/informes-de-situacion-actual-por-eventos-adversos-ecuador/) | 2016–2026 | A mano: afectados, viviendas y fallecidos por cantón |
| GAD y prensa local con fecha | variable | A mano: completar vacíos, en especial 2008–2015, que no tiene base pública por evento |

El conjunto «Eventos Peligrosos» que la SNGR publicaba en Datos Abiertos ya no está disponible en el portal (consulta del 22 de octubre de 2026).

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
