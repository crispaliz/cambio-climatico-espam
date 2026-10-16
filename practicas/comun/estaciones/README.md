# Datos de estación (común)

Formato único para todas las prácticas que usan estaciones (Ambiental `IA1_02`, Riesgos `RD1_02` y las que vengan). Plantilla: [`plantilla_estacion.csv`](plantilla_estacion.csv).

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

Solo `fecha` es obligatoria. Una celda vacía es un dato faltante: nunca escriba 0 donde no hubo medición. Lectura y control de calidad: `herramientas/estaciones/calidad.py`.
