# herramientas/estaciones

`calidad.py`

- `leer(ruta)`: lee el CSV (`fecha`, `tmed`, `tmax`, `tmin`, `precip`), elimina fechas duplicadas y detecta si es diario o mensual.
- `limites_fisicos(df, diario)`: anula valores imposibles y Tmax < Tmin, y los cuenta.
- `mensual(df, diario, ...)`: agrega a mensual con criterios de completitud ajustables.
- `metricas(obs, mod, relativa)`: sesgo, MAE, RMSE, r y sesgo relativo.

Una celda vacía es un dato faltante. Nunca se escribe 0 donde no hubo medición.

`catalogo.py`

- `tabla(repo_dir)`: índice de `datos/estaciones/`.
- `de_provincia(provincia, repo_dir)`: estaciones del curso de una provincia.
- `resolver(archivo, repo_dir, provincia)`: devuelve la ruta y la ficha de una estación del curso, o la ruta de un CSV propio; si no lo encuentra, explica qué escribir y lista las estaciones de la provincia.

`preparar_catalogo.py` (docente): reconstruye `datos/estaciones/` y los ZIP de la rama `estaciones` desde las fuentes originales, con las reglas de unión descritas en `datos/estaciones/README.md`.
