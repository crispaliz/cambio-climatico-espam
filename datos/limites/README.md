# Límites provinciales y cantonales del Ecuador

## Archivos

| Archivo | Contenido | Uso |
|---|---|---|
| `ecuador_provincias.geojson` | Versión simplificada en WGS84 (EPSG:4326) | La leen los cuadernos |
| `ecuador_cantones.geojson` | Versión simplificada en WGS84 (EPSG:4326) | La leen los cuadernos |

## Procesamiento

Origen: shapefiles `ec_provs_df` (25 polígonos, incluida la zona no delimitada) y `pop_2022_FIXED` (224 cantones), guardados por el docente fuera del repositorio.


- Proyección de origen: WGS 84 / UTM zona 17S (EPSG:32717). Reproyectadas a EPSG:4326.
- Simplificación de geometría con tolerancia de 100 m, preservando la topología. Diferencia máxima de área por provincia frente al original: 0,08 %. Suficiente para mallas de 0,1° o más gruesas.
- Columnas de provincias: `codigo` (DPA), `nombre` (con tildes), `nombre_dpa` (como en el original) y `region` (según `REN_CODIGO`: Sierra, Costa, Amazonía, Insular, Zona no delimitada).
- Columnas de cantones: `codigo`, `nombre_dpa`, `codigo_provincia` y `provincia`.
- Se omitieron las columnas de población del original.

## Advertencias

- Los atributos indican `DPA_ANIO = 2010`: verificar la fecha de corte de los límites.
- Santo Domingo de los Tsáchilas consta en la región Sierra según su código. Climáticamente pertenece a la vertiente occidental.
- Las columnas de población del original (`X2001`–`X2020`, `pop_2022`) no son coherentes entre sí; no se usan.

## Fuente

Fuente: [completar: CONALI / INEC] · Versión: [completar] · Fecha de obtención: [completar] · Condiciones de uso: [completar]
