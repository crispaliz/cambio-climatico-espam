# herramientas/reanalisis

| Módulo | Contenido |
|---|---|
| `era5.py` | ERA5 (ECMWF / Copernicus): credencial personal, descarga por celda de las series horarias, paso de horario a diario en hora local, malla y mensual de la zona, terreno |
| `core.py` | CORe (NOAA/NCEP CPC): descarga parcial por rangos de bytes; diario o mensual por zona (opción A) y diario para Ecuador (docente) |
| `release.py` | Opción B: nombres, descarga y recorte de los archivos del release de datos |
| `preparar_releases.py` / `.ipynb` | (Docente) Genera los archivos de las 24 provincias y los publica con `herramientas/publicar.py` |

## Dos opciones, los mismos archivos

| Archivo en `CC_datos/<zona>/` | Opción A (`"propio"`) | Opción B (`"release"`) |
|---|---|---|
| `era5_diario_<zona>.nc` | `era5.descargar_zona`: una solicitud por celda de 0,25° que toca la zona | Release, recortado a la zona |
| `era5_mensual_<zona>.nc` | De los diarios | Release |
| `era5_terreno_<zona>.nc` | `era5.descargar_terreno`: 1 solicitud pequeña | Release |
| `core_diario_<zona>.nc` | `core.diario_zona` (`CORE_DIARIO = True`): 4 archivos de 6 h por día, solo los 8 campos de cada uno; reanudable por mes | Release |
| `core_mensual_<zona>.nc` | De los diarios; o, con `CORE_DIARIO = False`, `core.mensual_zona` (promedios mensuales de NOAA, sin Tmax ni Tmin) | Release (de los diarios) |

## Variables (iguales en todas las fuentes)

| Columna | Variable | Unidad |
|---|---|---|
| `tmed`, `tmax`, `tmin` | Temperatura a 2 m | °C |
| `pr` | Precipitación | mm/día (mm/mes en series mensuales) |
| `hr` | Humedad relativa a 2 m | % |
| `q` | Humedad específica a 2 m | g/kg |
| `ps` | Presión en superficie | hPa |
| `u10`, `v10` | Componentes del viento a 10 m | m/s |
| `ws` | Velocidad del viento: media de las velocidades horarias (ERA5) o de 6 h (CORe diario) | m/s |
| `wd` | Dirección de procedencia, del viento medio vectorial (se calcula en los cuadernos) | ° |

Las fórmulas derivadas están en `herramientas/variables.py`.

## ERA5 por celdas: por qué representa bien la zona

El conjunto `reanalysis-era5-single-levels-timeseries` guarda ERA5 ordenado por lugar (formato ARCO): una celda con 44 años hora a hora se entrega en segundos, mientras que un recorte espacial de los mismos 44 años obliga al CDS a leer cientos de miles de campos globales. Se piden **todas** las celdas que tocan la zona, se pasa de horario a diario y se vuelve a armar la malla. El promedio de la zona pondera cada celda por la fracción de su área dentro del límite (`limites.fracciones` y `limites.promedio_ponderado`).

## Definición del día

| Fuente | Día |
|---|---|
| ERA5 | Hora local (UTC-5) desde `inicio_dia` (0 por defecto; 7 para comparar con lluvia del INAMHI). En el release: 00–24 h |
| CORe | 06–06 UTC = 01:00–01:00 hora local |

En ERA5, la precipitación de cada hora es la acumulada en la hora que termina en la marca de tiempo: se asigna a la hora anterior antes de sumar. Solo se guardan días con las 24 horas.

## Cuidado de los servidores

- **CDS:** una solicitud por celda, en serie; reintentos con espera creciente (30 s, 1, 2, 4 min); se detiene si falta aceptar una licencia o el token es inválido; nada se pide dos veces (cada celda queda guardada al llegar).
- **CPC:** solo los bytes necesarios (rangos HTTP según el `.idx`), inventario reutilizado y validado (cada mensaje debe empezar con `GRIB`), 3 o 4 hilos que solo descargan, pausa aleatoria, respeto de 429/503 y `Retry-After`.
- **Opción B:** el estudiante descarga un archivo por producto desde GitHub, no desde los servidores de origen.

## Costo de CORe diario por estudiante (opción A)

CORe se distribuye en archivos **globales** de 6 h, así que el costo no depende del tamaño de la zona: 1981–2024 son ~64 000 solicitudes y ~25 GB transferidos (de 1,6 MB por archivo se piden ~0,4 MB), aunque en el Drive quede solo el recorte de la zona (pocos MB). Con 4 descargas simultáneas, calcule **4 a 8 horas**, reanudable por mes. La lectura usa eccodes directamente (~12 ms por archivo). Con un curso entero en paralelo, el servidor de CPC podría limitar las descargas: si aparecen errores 429 o 503 repetidos, conviene escalonar los grupos o usar la opción B.

## Límites conocidos y verificaciones pendientes

- Con `CORE_DIARIO = False`: `ws` de CORe es la del viento medio vectorial (algo menor que la media de las velocidades); no hay Tmax ni Tmin (la media mensual de los máximos de 6 h no equivale a la media de las máximas diarias), y la humedad relativa se calcula con medias mensuales de q, T y presión (aproximación).
- CORe es de 6 h, no horario: su día se arma con 4 valores; ERA5, con 24.
- CORe no trae la altura de su terreno en los archivos de flujos: su presión y temperatura no se corrigen por altura.
- **Verificar antes del uso masivo:** que el servidor de CPC responda a pedidos por rangos de bytes (código 206; si responde 200 se descarga el archivo completo y se recorta, más lento) y que el conjunto de series por punto de ERA5 ofrezca las seis variables de `era5.VARIABLES_SERIES` en todo el periodo.
