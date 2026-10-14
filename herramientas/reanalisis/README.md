# herramientas/reanalisis

| Módulo | Fuente | Malla | Credencial | Uso |
|---|---|---|---|---|
| `era5.py` | ERA5, ECMWF / Copernicus | 0,25° | API Token del CDS (Colab › Secrets › `CDSAPI_KEY`) | Mensual: el estudiante, para su zona (1 solicitud). Diario: el docente, para el release `era5-v1` |
| `core.py` | CORe, NOAA/NCEP CPC | ~1,9° (T62) | Ninguna | El docente prepara el release `core-v1` |
| `release.py` | Releases del repositorio | — | Ninguna | Un archivo por provincia; el estudiante descarga el suyo y lo recorta a su zona |

## Variables (iguales en todas las fuentes)

| Columna | Variable | Unidad |
|---|---|---|
| `tmed`, `tmax`, `tmin` | Temperatura a 2 m | °C |
| `pr` | Precipitación | mm/día (mm/mes en series mensuales) |
| `hr` | Humedad relativa a 2 m | % |
| `q` | Humedad específica a 2 m | g/kg |
| `ps` | Presión en superficie | hPa |
| `u10`, `v10` | Componentes del viento a 10 m | m/s |
| `ws`, `wd` | Velocidad y dirección de procedencia (calculadas de u10 y v10) | m/s, ° |

ERA5 mensual trae además `pnm` (presión a nivel del mar). Las fórmulas derivadas están en `herramientas/variables.py`.

## Cuadernos del docente

| Cuaderno | Produce | Solicitudes |
|---|---|---|
| `preparar_era5.ipynb` | `era5_diario_<provincia>.nc` | 4 por año al CDS, en serie |
| `preparar_core.ipynb` | `core_diario_<provincia>.nc`, `core_mensual_<provincia>.nc` | 4 rangos de bytes por archivo de 6 h, 4 hilos |

## Cuidado de los servidores

- **CDS:** variables agrupadas por estadístico, solicitudes en serie (el CDS las encola), reintentos con espera creciente (1, 2, 4… min), sin repetir lo descargado.
- **CPC:** solo los bytes necesarios (rangos HTTP según el `.idx`), inventario reutilizado y validado (cada mensaje debe empezar con `GRIB`), 4 hilos, pausa aleatoria, respeto de 429/503 y `Retry-After`.
- **Estudiantes:** una solicitud mensual al CDS y un archivo por fuente desde GitHub, no desde los servidores de origen.

## Definición del día

| Fuente | Día |
|---|---|
| ERA5 | 00–24 h, hora local (UTC-5) |
| CORe | 06–06 UTC = 01:00–01:00 hora local |

## Límites conocidos

- La humedad relativa y la específica de ERA5 se calculan con el punto de rocío (y la temperatura o la presión) **medios** del día o del mes: ERA5 no ofrece humedad específica a 2 m en el CDS. En CORe, `q` es directa (SPFH a 2 m).
- La velocidad del viento calculada con u10 y v10 medios es la del **viento medio vectorial**, menor o igual que la media de las velocidades.
- CORe no trae la altura de su terreno en los archivos de flujos: su presión y temperatura no se corrigen por altura.
