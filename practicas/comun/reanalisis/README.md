# Reanálisis: ERA5 y CORe (común)

| Orden | Cuaderno | Qué hace | Deja listo en `Mi unidad/CC_datos/<zona>/` |
|---|---|---|---|
| CR01 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/comun/reanalisis/CR01_descarga_reanalisis.ipynb) `CR01_descarga_reanalisis` | Confirma la zona en tabla y mapa; descarga ERA5 y CORe (opción A) o los trae del release (opción B) | `era5_diario`, `era5_mensual`, `era5_terreno`, `core_diario`, `core_mensual` (`_<zona>.nc`) e `inventario.json` |
| CR02 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/comun/reanalisis/CR02_series_zona.ipynb) `CR02_series_zona` | Promedio de la zona ponderado por la fracción de área de cada celda | `serie_diaria_<zona>.csv`, `serie_mensual_<zona>.csv` |

## Dos formas de obtener los datos (celda 1 de CR01)

| `MODO_DATOS` | Qué hace | Necesita | Tiempo |
|---|---|---|---|
| `"propio"` (opción A) | Descarga ERA5 y CORe, diarios y mensuales, para su zona | Su propia cuenta y token del CDS | ERA5: ~0,5–1 min por celda (Manabí: 39; un cantón: 4–10). CORe diario: 4–8 h (`CORE_DIARIO` sin marcar: solo mensual, minutos). Reanudable |
| `"release"` (opción B, predeterminada) | Trae los archivos del release `datos-v1` y los recorta a su zona | Nada | 1–2 min |

**Opción A:** cuenta propia en https://cds.climate.copernicus.eu, licencias aceptadas de *ERA5 hourly time-series data on single levels* y *ERA5 monthly averaged data on single levels*, y API Token en Colab › Secrets (`CDSAPI_KEY`) o en `CDS_TOKEN`. Una cuenta por persona: el CDS limita por cuenta.

## Variables

| Variable | Columna | Unidad |
|---|---|---|
| Temperatura media, máxima y mínima a 2 m | `tmed`, `tmax`, `tmin` | °C |
| Precipitación | `pr` | mm/día · mm/mes |
| Humedad relativa y específica a 2 m | `hr`, `q` | % · g/kg |
| Presión en superficie | `ps` | hPa |
| Viento a 10 m | `u10`, `v10`, `ws`, `wd` | m/s · ° |

## Definición del día

| Fuente | Día |
|---|---|
| ERA5 | 00–24 h hora local (o 07–07 h con `INICIO_DIA = 7`, opción A) |
| CORe | 01:00–01:00 hora local |
| Estaciones INAMHI (lluvia) | Habitualmente 07:00–07:00: verificar con la fuente |

Detalles técnicos y cuidado de los servidores: [`herramientas/reanalisis`](../../../herramientas/reanalisis/).
