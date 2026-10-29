# Rama `estaciones`: datos de estaciones para descarga bajo demanda

Esta rama guarda archivos grandes que los cuadernos descargan solo cuando los necesitan, para que la rama `main` (la que se clona en cada cuaderno) siga siendo liviana. El índice y la documentación están en `main`, en `datos/estaciones/`.

| Archivo | Contenido |
|---|---|
| `inamhi_precip_<provincia>.zip` | Estaciones del INAMHI de la provincia, un CSV por estación: lluvia diaria 1964–2018 con control de calidad y relleno Climatol (apoyo CHIRPS), prolongada con la observada de las redes hasta 2024 cuando coinciden en 2016–2018, y Tmáx/Tmín 2022–2024 de la red INAMHI donde existen |

Fuente: Instituto Nacional de Meteorología e Hidrología (INAMHI). Control de calidad y relleno: C. Paliz Acosta (2024–2026).
