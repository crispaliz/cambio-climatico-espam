# Exposición por cantón

`exposicion_cantones.csv`: una fila por cantón (224) con la población y la infraestructura del cantón, y la parte de ellas que está en **zona baja** (altitud menor de 10 m) o en **ladera** (pendiente mayor de 20°). La usa el cuaderno `RD2_01_exposicion` de la Práctica 2 de Riesgos de Desastres.

La genera el flujo **Exposición por cantón** de GitHub Actions (`.github/workflows/exposicion.yml`, script `herramientas/exposicion/preparar.py`), que descarga las fuentes, calcula la tabla y la guarda aquí junto con `metadatos.json` (fecha, factores de reescalado, avisos). Para recalcularla: cambiar y subir `solicitud.json`, o **Actions › Exposición por cantón › Run workflow**.

## Columnas

| Columna | Significado |
|---|---|
| `codigo`, `canton`, `codigo_provincia`, `provincia` | Código DPA y nombres (de `datos/limites`) |
| `area_km2` | Área del polígono cantonal (UTM 17S) |
| `poblacion_worldpop_2020` | Suma de WorldPop 2020 (1 km) dentro del cantón |
| `factor_censo`, `poblacion_2022` | Reescalado para que cada provincia sume su total del Censo 2022 |
| `densidad_hab_km2` | `poblacion_2022 / area_km2` |
| `poblacion_cota_baja`, `pct_cota_baja` | Población en celdas de 90 m con altitud < 10 m (ponderada por la fracción de cada celda de 1 km) |
| `poblacion_ladera`, `pct_ladera` | Población en celdas de 90 m con pendiente > 20° |
| `escuelas`, `salud`, `emergencia` | Puntos de OpenStreetMap: `amenity` = school, kindergarten, college, university · hospital, clinic, doctors · fire_station, police |
| `*_cota_baja`, `*_ladera` | Los mismos servicios cuyo punto cae en zona baja o en ladera |
| `km_vias_principales` | Km de vías `highway` = motorway, trunk, primary, secondary |
| `km_vias_cota_baja`, `km_vias_ladera` | Tramos de esas vías (muestreados cada 200 m) en zona baja o en ladera |
| `puentes` | Tramos con `bridge` = yes o viaduct en vías principales y terciarias |

## Fuentes y licencias

| Fuente | Uso | Licencia y cita |
|---|---|---|
| WorldPop 2020, 1 km, Ecuador (`ecu_ppp_2020_1km_Aggregated`) | Distribución espacial de la población | CC BY 4.0. WorldPop (2018). *Global High Resolution Population Denominators Project*. University of Southampton. doi:10.5258/SOTON/WP00671 |
| Censo Ecuador 2022 (INEC), total provincial | Reescalado | `datos/inventario/poblacion_censo2022.csv` |
| Copernicus DEM GLO-90 (teselas COG de 1°, AWS) | Zona baja y pendiente | © DLR e.V. 2010–2014 y © Airbus Defence and Space GmbH 2014–2018, provisto bajo el programa COPERNICUS por la ESA. doi:10.5270/ESA-c5d3d65 |
| OpenStreetMap, extracto de Ecuador (Geofabrik) | Servicios, vías y puentes | © colaboradores de OpenStreetMap, ODbL 1.0 |

## Limitaciones

- WorldPop **modela** la distribución de la población (no es un conteo); la suma provincial se ajusta al Censo, pero dentro de la provincia la reparte el modelo.
- Zona baja y ladera son aproximaciones con un relieve de 90 m y una población de 1 km: no sustituyen un mapa de amenaza de inundación ni de susceptibilidad a movimientos en masa. Una ciudad en un valle de la Sierra tiene 0 en zona baja aunque se inunde.
- OpenStreetMap es colaborativo: en cantones rurales faltan escuelas, centros de salud y vías; un 0 puede significar «no mapeado».
- Los límites cantonales tienen atributos de 2010 (ver `datos/limites/README.md`).
