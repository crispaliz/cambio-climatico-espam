# Práctica 1 — Diagnóstico del clima observado

Evidencia el RA A de la Unidad I y entrega el **capítulo 1** del proyecto. Funciona para **cualquier provincia del Ecuador** o para **un cantón**: se indica en la celda 1 de cada cuaderno (`PROVINCIA` y, si se quiere, `CANTON`).

Los cuadernos se ejecutan **en orden**; cada uno usa lo que dejó el anterior.

| Orden | Cuaderno | Qué hace | Deja listo | Paso |
|---|---|---|---|---|
| 1 | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-1/P1_01_descarga_datos.ipynb) `P1_01_descarga_datos` | ERA5 mensual del CDS (1 solicitud) y ERA5 diario y CORe del curso, solo para el recuadro de la zona | `Mi unidad/CC_datos/<zona>/` con inventario | — |
| 2 | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-1/P1_02_series.ipynb) `P1_02_series` | Recorta con el límite oficial y promedia sobre la zona | Series mensual y diaria de las dos fuentes | — |
| 3 | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-1/P1_03_climatologia.ipynb) `P1_03_climatologia` | Climatología 1995–2014 de las 9 variables y comparación ERA5–CORe | Tablas, climograma, panel de humedad, presión y viento | 1 |
| 4 | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/ambiental/practica-1/P1_04_estacion_vs_reanalisis.ipynb) `P1_04_estacion_vs_reanalisis` | Contrasta una estación con los dos reanálisis en todas las variables que mida | Métricas, ciclo anual y figuras | 2 |
| 5 | Próximamente | Tendencias y compuestos por fase de ENSO | Borrador del capítulo 1 | 3 |

## Variables

| Variable | Columna | Unidad |
|---|---|---|
| Temperatura media, máxima y mínima a 2 m | `tmed`, `tmax`, `tmin` | °C |
| Precipitación | `pr` | mm/día · mm/mes |
| Humedad relativa | `hr` | % |
| Humedad específica | `q` | g/kg |
| Presión atmosférica en superficie | `ps` | hPa |
| Viento a 10 m: componentes, velocidad, dirección de procedencia | `u10`, `v10`, `ws`, `wd` | m/s · ° |

## Dónde quedan los archivos

```
Mi unidad/
  CC_datos/<zona>/        solo el recorte de su zona (decenas de MB)
  CC_Practica1/<zona>/    series, tablas y figuras
```
La zona es la provincia (`manabi`) o el cantón con su provincia (`manabi__portoviejo`).

## Antes de empezar

- Su **propia** cuenta en https://cds.climate.copernicus.eu y la licencia de ERA5 aceptada. **Cada estudiante usa su cuenta**: el CDS limita las solicitudes por cuenta y una cuenta compartida bloquea a todos.
- Su API Token en Colab › Secrets como `CDSAPI_KEY` (recomendado) o en `CDS_TOKEN`, celda 1 del cuaderno 1. No comparta su copia del cuaderno si escribió el token en ella.
- Para el cuaderno 4: datos de la estación con el formato de `plantilla_estacion.csv`. Solo `fecha` es obligatoria; se comparan las columnas que tenga.

## Formato de los datos de estación

| Columna | Contenido | Unidad |
|---|---|---|
| `fecha` | AAAA-MM-DD (diario) o AAAA-MM-01 (mensual) | — |
| `tmed`, `tmax`, `tmin` | temperatura media, máxima y mínima | °C |
| `precip` | precipitación | mm |
| `hr` | humedad relativa | % |
| `q` | humedad específica (opcional; si falta se calcula de hr, tmed y pres) | g/kg |
| `pres` | presión atmosférica de la estación | hPa |
| `vv` | velocidad del viento | m/s |
| `dv` | dirección de donde sopla (0 = norte) | ° |

Una celda vacía es un dato faltante; nunca escriba 0 donde no hubo medición.

## Definición del día en cada fuente

| Fuente | Día |
|---|---|
| ERA5 diario | 00–24 h, hora local (UTC-5) |
| CORe diario | 01:00–01:00, hora local |
| Estaciones INAMHI (precipitación) | Habitualmente 07:00–07:00, hora local: verificar con la fuente |

## Criterio de evaluación

- Cuadernos ejecutados en orden y de principio a fin, con inventario y metadatos completos.
- Unidades correctas, verificadas con las comprobaciones de cada cuaderno.
- Respuestas a las preguntas finales con los números de su zona.
