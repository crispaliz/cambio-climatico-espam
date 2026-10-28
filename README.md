# Rama `estaciones`: datos de estaciones para descarga bajo demanda

Esta rama guarda archivos grandes que los cuadernos descargan solo cuando los necesitan, para que la rama `main` (la que se clona en cada cuaderno) siga siendo liviana. El índice y la documentación están en `main`, en `datos/estaciones/`.

| Archivo | Contenido |
|---|---|
| `inamhi_precip_<provincia>.zip` | Precipitación diaria 1964–2018 de las estaciones del INAMHI de la provincia, un CSV por estación (`fecha`, `precip`). Series rellenadas con Climatol, con CHIRPS como serie de apoyo |

Fuente: Instituto Nacional de Meteorología e Hidrología (INAMHI). Control de calidad y relleno: C. Paliz Acosta (2024–2026).
