# Estaciones del curso

Series diarias de **1023 estaciones** del Ecuador continental en el formato común del curso (`practicas/comun/estaciones/plantilla_estacion.csv`), para `IA1_02_estacion_vs_reanalisis` (Ambiental) y `RD1_02_extremos_eventos` (Riesgos de Desastres).

## Cómo se usan

**No hay que hacer nada.** Con `ARCHIVO_ESTACION` vacío (como viene), el cuaderno elige sola la estación del curso para la zona del formulario, completa nombre, código, coordenadas y altitud, y muestra las demás disponibles:

1. Primero las estaciones dentro de la zona; si no hay (cantones pequeños), las más cercanas dentro del área descargada.
2. Entre ellas, primero las que tienen **temperatura y lluvia** (60 meses válidos o más de lluvia y de Tmáx o Tmín), luego las que solo tienen temperatura y al final las que solo tienen lluvia.
3. A igualdad, la de más meses válidos.

Para usar otra, escriba en `ARCHIVO_ESTACION` el valor de la columna `archivo` del índice (por ejemplo, `"inamhi/manabi/m0005.csv"`), o la ruta en Drive de un CSV propio. En `RD1_02`, `"ninguna"` trabaja sin estación.

| Provincia | Estación que se elige | Variables | Estaciones disponibles |
|---|---|---|---|
| Azuay | Mariscal Lamar | temperatura y lluvia | 50 |
| Bolívar | Rio San Antonio-Monjas | lluvia | 30 |
| Carchi | San Gabriel | temperatura y lluvia | 30 |
| Cañar | Canar | temperatura y lluvia | 35 |
| Chimborazo | Chimborazo | lluvia | 64 |
| Cotopaxi | Alternativo Cotopaxi Intl | temperatura y lluvia | 54 |
| El Oro | Santa Rosa Aeropuerto | temperatura | 52 |
| Esmeraldas | La Concordia | temperatura y lluvia | 33 |
| Guayas | Simon Bolivar Intl / Jose Joaquin De Olmedo Intl | temperatura y lluvia | 74 |
| Imbabura | Inguincho | temperatura y lluvia | 64 |
| Loja | Loja/La Argelia | temperatura y lluvia | 84 |
| Los Ríos | Pichilingue | temperatura y lluvia | 33 |
| Manabí | Manta Aeropuerto Eloy Alfaro (METAR) | temperatura y lluvia | 95 |
| Morona Santiago | Coronel Edmundo Carvajal | lluvia | 33 |
| Napo | Baeza | lluvia | 39 |
| Orellana | Nuevo Rocafuerte | temperatura y lluvia | 12 |
| Pastaza | Puyo | temperatura y lluvia | 11 |
| Pichincha | Izobamba | temperatura y lluvia | 120 |
| Santa Elena | General Ulpiano Paez | temperatura y lluvia | 24 |
| Santo Domingo de los Tsáchilas | Puerto Ila | temperatura y lluvia | 18 |
| Sucumbíos | Nueva Loja Aeropuer | temperatura | 17 |
| Tungurahua | Querochaca | temperatura y lluvia | 32 |
| Zamora Chinchipe | Zamora | lluvia | 19 |
| Galápagos | — | — | 0 |

## Índice: [`indice_estaciones.csv`](indice_estaciones.csv)

| Columna | Contenido |
|---|---|
| `archivo` | Lo que se escribe en `ARCHIVO_ESTACION` |
| `provincia`, `estacion`, `omm`, `codigo` | Ubicación, nombre, indicativo OMM y código INAMHI |
| `lat`, `lon`, `altitud_m` | Coordenadas en grados decimales y altitud en metros |
| `desde`, `hasta` | Primer y último día con dato |
| `meses_tmax`, `meses_tmin`, `meses_precip` | Meses de 1981 en adelante que pasan el control de completitud de los cuadernos (temperatura: máximo 4 días faltantes y 2 seguidos; lluvia: mes completo) |
| `variables`, `fuente`, `url` | Columnas del archivo, fuente y enlace de descarga |

## Fuentes

| Archivos | Fuente | Variables | Periodo |
|---|---|---|---|
| `inamhi/<provincia>/<código>.csv` (983 estaciones) | INAMHI. Series con control de calidad y rellenadas con Climatol, con CHIRPS como serie de apoyo | `precip` | 1964–2018 |
| `synop/*.csv` (38 estaciones) | Mensajes SYNOP del Sistema Mundial de Telecomunicaciones de la OMM, obtenidos de OGIMET y resumidos por día. En 35 de ellas la lluvia es la de la estación del INAMHI del mismo sitio (a 5,5 km o menos y con menos de 100 m de diferencia de altitud) | `tmax`, `tmin`, `precip` | 2001–2024 (lluvia del INAMHI: 1964–2018) |
| `manabi_manta_aeropuerto_semt_metar.csv` | METAR del aeropuerto de Manta (OGIMET), días con 12 observaciones o más; lluvia de la estación INAMHI M0074 Manta Aeropuerto | `tmed`, `tmax`, `tmin`, `precip`, `hr`, `pres`, `vv`, `dv` | 2006–2024 (lluvia: 1964–2018) |
| `manabi_calceta_espam.csv` | Estación meteorológica de la ESPAM MFL, Calceta, con control de calidad | `tmed`, `tmax`, `tmin`, `precip`, `hr`, `vv` | 2010–2024 |

**Dónde están.** El índice, las estaciones SYNOP, el METAR y la ESPAM están en esta carpeta de la rama `main`. Las 983 series del INAMHI (unos 62 MB) están en la rama [`estaciones`](https://github.com/crispaliz/cambio-climatico-espam/tree/estaciones), un ZIP por provincia, para que la rama `main` siga siendo liviana: el cuaderno descarga solo el ZIP de la provincia que necesita, una vez por sesión.

**Cómo citar:**
- INAMHI. *Precipitación diaria de la red de estaciones del Instituto Nacional de Meteorología e Hidrología, 1964–2018*. Control de calidad y relleno con Climatol (serie de apoyo CHIRPS): C. Paliz Acosta.
- OGIMET. *Datos SYNOP y METAR del Sistema Mundial de Telecomunicaciones de la OMM*. https://www.ogimet.com. Procesados por C. Paliz Acosta (2026).
- ESPAM MFL. *Estación meteorológica de la ESPAM MFL, Calceta, Manabí. Datos diarios 2010–2024*. Procesados por C. Paliz Acosta (2026).

## Limitaciones (declárelas en el capítulo)

- **Lluvia del INAMHI rellenada:** las series no tienen días faltantes porque los vacíos se rellenaron con Climatol usando CHIRPS como serie de apoyo. Los días rellenados no son observaciones y no se distinguen en el archivo. Terminan en 2018.
- **Lluvia de las SYNOP sin par del INAMHI:** los mensajes no siempre llegan, y como los cuadernos solo aceptan meses de lluvia completos, esas estaciones tienen pocos meses válidos de lluvia.
- **Definición del día:** SYNOP y METAR siguen el día de la fuente; la lluvia del INAMHI, el día pluviométrico de 07:00 a 07:00.
- **Sin temperatura:** Bolívar, Napo y Zamora Chinchipe solo tienen estaciones de lluvia; en Chimborazo y Morona Santiago la temperatura tiene menos de 60 meses válidos, así que también se elige una estación con lluvia. Se probó construir series sintéticas de temperatura interpolando las estaciones vecinas y se descartaron: al reconstruir estaciones conocidas, el sesgo llegó a +2,8 °C (Loja) y +6,8 °C (El Corazón) y la correlación mensual a 0,46 (Puyo), errores del mismo orden que los que la práctica quiere medir en los reanálisis.
- **Galápagos:** sin estación del curso.
- **Coordenadas de la ESPAM:** aproximadas (−0,83; −80,18; 15 m).

Uso docente en las prácticas de Cambio Climático de la ESPAM MFL.
