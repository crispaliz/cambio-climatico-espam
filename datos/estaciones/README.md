# Estaciones del curso

Series diarias de **1082 estaciones** del Ecuador en el formato común del curso (`practicas/comun/estaciones/plantilla_estacion.csv`), para `IA1_02_estacion_vs_reanalisis` (Ambiental) y `RD1_02_extremos_eventos` (Riesgos de Desastres). Los cuadernos comparan los reanálisis **solo con las variables que cada estación midió**.

## Cómo se usan

**No hay que hacer nada.** Con `ARCHIVO_ESTACION` vacío (como viene), el cuaderno elige sola la estación del curso para la zona del formulario, completa nombre, código, coordenadas y altitud, y muestra las demás disponibles:

1. Primero las estaciones dentro de la zona; si no hay (cantones pequeños), las más cercanas dentro del área descargada.
2. Entre ellas, primero las que tienen **temperatura y lluvia** (60 meses válidos o más de lluvia y de Tmáx, Tmín o Tmed), luego las que solo tienen temperatura y al final las que solo tienen lluvia.
3. A igualdad, la de más meses válidos. Las estaciones con coordenadas por revisar se usan solo si no hay otra.

Para usar otra, escriba en `ARCHIVO_ESTACION` el valor de la columna `archivo` del índice, o la ruta en Drive de un CSV propio. En `RD1_02`, `"ninguna"` trabaja sin estación.

| Provincia | Estación que se elige | Variables | Estaciones disponibles |
|---|---|---|---|
| Azuay | Mariscal Lamar | temperatura y lluvia | 57 |
| Bolívar | Chillanes | lluvia | 31 |
| Carchi | San Gabriel | temperatura y lluvia | 31 |
| Cañar | Canar | temperatura y lluvia | 36 |
| Chimborazo | Chimborazo | lluvia | 67 |
| Cotopaxi | Rumipamba | temperatura y lluvia | 58 |
| El Oro | Santa Rosa Aeropuerto | temperatura | 52 |
| Esmeraldas | La Concordia | temperatura y lluvia | 34 |
| Galápagos | Baltra | temperatura (2022–2024) | 2 |
| Guayas | Simon Bolivar Intl / Jose Joaquin De Olmedo Intl | temperatura y lluvia | 83 |
| Imbabura | Inguincho | temperatura y lluvia | 65 |
| Loja | Loja/La Argelia | temperatura y lluvia | 86 |
| Los Ríos | Pichilingue | temperatura y lluvia | 39 |
| Manabí | Manta Aeropuerto Eloy Alfaro (METAR) | temperatura y lluvia | 99 |
| Morona Santiago | Coronel Edmundo Carvajal | temperatura y lluvia | 34 |
| Napo | Baeza | lluvia | 42 |
| Orellana | Nuevo Rocafuerte | temperatura y lluvia | 13 |
| Pastaza | Puyo | temperatura y lluvia | 12 |
| Pichincha | Izobamba | temperatura y lluvia | 122 |
| Santa Elena | General Ulpiano Paez | temperatura y lluvia | 24 |
| Santo Domingo de los Tsáchilas | Puerto Ila | temperatura y lluvia | 22 |
| Sucumbíos | Nueva Loja Aeropuer | temperatura | 18 |
| Tungurahua | Querochaca | temperatura y lluvia | 32 |
| Zamora Chinchipe | Zamora | lluvia | 19 |

## Índice: [`indice_estaciones.csv`](indice_estaciones.csv)

| Columna | Contenido |
|---|---|
| `archivo` | Lo que se escribe en `ARCHIVO_ESTACION` |
| `provincia`, `estacion`, `omm`, `codigo` | Ubicación, nombre, indicativo OMM y código (INAMHI o de la red) |
| `lat`, `lon`, `altitud_m`, `altitud_fuente` | Coordenadas, altitud y su origen (`declarada` o `DEM`) |
| `coordenadas_corregidas`, `coordenadas_revisar` | Si la ubicación se corrigió con otra fuente, o si sigue dudosa |
| `desde`, `hasta` | Primer y último día con dato (como máximo, 31 de diciembre de 2024) |
| `meses_tmax`, `meses_tmin`, `meses_tmed`, `meses_precip` | Meses de 1981 a 2024 que pasan el control de completitud de los cuadernos (temperatura: máximo 4 días faltantes; lluvia: mes completo) |
| `variables`, `fuente`, `url` | Columnas del archivo, fuentes de cada variable y enlace de descarga |

## Fuentes

| Archivos | Fuente | Variables |
|---|---|---|
| `inamhi/<provincia>/<código>.csv` (995) | INAMHI: lluvia diaria 1964–2018 con control de calidad y relleno Climatol (serie de apoyo CHIRPS). En las estaciones que siguen activas, prolongada a 2024 con la lluvia observada de las redes, y con Tmáx y Tmín de la red INAMHI desde junio de 2022 | `precip`, y `tmax`, `tmin` donde existen |
| `synop/*.csv` (51) | SYNOP del Sistema Mundial de Telecomunicaciones de la OMM (OGIMET), 2001–2024, con los días sin dato de 2022–2024 completados con la red INAMHI de la misma estación. La lluvia es la de la estación del INAMHI del mismo sitio | `tmax`, `tmin`, `precip` |
| `redes/*.csv` (34) | Redes INAMHI (estaciones nuevas, Galápagos incluida), HIDRONACIÓN (temperatura media y lluvia, 2013–2024), CELEC, GYE y CCS | según la estación |
| `manabi_manta_aeropuerto_semt_metar.csv` | METAR del aeropuerto de Manta (OGIMET), con la lluvia del INAMHI M0074 | `tmed`, `tmax`, `tmin`, `precip`, `hr`, `pres`, `vv`, `dv` |
| `manabi_calceta_espam.csv` | Estación meteorológica de la ESPAM MFL, Calceta | `tmed`, `tmax`, `tmin`, `precip`, `hr`, `vv` |

**Reglas de unión** (programa: [`herramientas/estaciones/preparar_catalogo.py`](../../herramientas/estaciones/preparar_catalogo.py)):

1. Primero se corrigen las coordenadas verificadas (17 estaciones; por ejemplo, Inguincho estaba 33 km desplazada en OGIMET).
2. La lluvia del INAMHI se prolonga con la de una red solo si en 2016–2018 coinciden: al menos 85 % de días idénticos, totales con menos de 10 % de diferencia y r ≥ 0,85.
3. Una estación de temperatura toma la lluvia de una estación del INAMHI a 5,5 km o menos y con no más de 100 m de diferencia de altitud. Si hay una en el mismo sitio (a 0,5 km o menos), se usa esa; si no, la de serie más larga.
4. La altitud que falta se toma del modelo digital de elevación en las coordenadas de la estación (34 estaciones, columna `altitud_fuente`).
5. Todo termina el 31 de diciembre de 2024, el fin de los reanálisis del curso.

**Dónde están.** El índice y las carpetas `synop/` y `redes/` están en la rama `main`. Las series del INAMHI están en la rama [`estaciones`](https://github.com/crispaliz/cambio-climatico-espam/tree/estaciones), un ZIP por provincia: el cuaderno descarga solo el de la provincia que necesita.

**Cómo citar:**
- INAMHI. *Datos diarios de la red de estaciones del Instituto Nacional de Meteorología e Hidrología*. Lluvia 1964–2018 con control de calidad y relleno Climatol (apoyo CHIRPS): C. Paliz Acosta.
- OGIMET. *Datos SYNOP y METAR del Sistema Mundial de Telecomunicaciones de la OMM*. https://www.ogimet.com.
- HIDRONACIÓN, CELEC EP, red de Guayaquil y CCS: datos de sus estaciones, recopilados por Clima Ecuatorial (2026).
- ESPAM MFL. *Estación meteorológica de la ESPAM MFL, Calceta, Manabí*.

## Limitaciones (declárelas en el capítulo)

- **Lluvia del INAMHI rellenada (1964–2018):** los días rellenados con Climatol y CHIRPS no son observaciones y no se distinguen en el archivo. De 2019 en adelante, la lluvia prolongada es observada y puede tener días faltantes.
- **Temperatura de la red INAMHI:** empieza en junio de 2022 (unos 30 meses hasta 2024). En Galápagos es la única temperatura disponible.
- **Sin temperatura:** Bolívar, Napo y Zamora Chinchipe solo tienen estaciones de lluvia; en Chimborazo la temperatura tiene menos de 60 meses válidos. Se descartaron las series sintéticas porque, al reconstruir estaciones conocidas, el sesgo llegó a +6,8 °C.
- **Coordenadas por revisar:** 9 estaciones del índice tienen una ubicación dudosa (altitud declarada muy distinta del DEM y una sola fuente); el cuaderno las elige solo si no hay otra.
- **Definición del día:** SYNOP, METAR y redes siguen el día de la fuente; la lluvia del INAMHI, el día pluviométrico de 07:00 a 07:00.
- **Altitud:** algunas estaciones (por ejemplo, las de Galápagos) no tienen altitud ni en la fuente ni en el DEM; el cuaderno avisa y no corrige la temperatura por la diferencia de altura.

Uso docente en las prácticas de Cambio Climático de la ESPAM MFL.
