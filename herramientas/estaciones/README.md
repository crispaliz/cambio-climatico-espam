# herramientas/estaciones

`calidad.py`

- `leer(ruta)`: lee el CSV (`fecha`, `tmed`, `tmax`, `tmin`, `precip`), elimina fechas duplicadas y detecta si es diario o mensual.
- `limites_fisicos(df, diario)`: anula valores imposibles y Tmax < Tmin, y los cuenta.
- `mensual(df, diario, ...)`: agrega a mensual con criterios de completitud ajustables.
- `metricas(obs, mod, relativa)`: sesgo, MAE, RMSE, r y sesgo relativo.

Una celda vacía es un dato faltante. Nunca se escribe 0 donde no hubo medición.
