# Estaciones del curso

Series diarias de **40 estaciones** del Ecuador en el formato común del curso (`practicas/comun/estaciones/plantilla_estacion.csv`), listas para `IA1_02_estacion_vs_reanalisis` (Ambiental) y `RD1_02_extremos_eventos` (Riesgos de Desastres). Periodo: de 2001 (2010 en la ESPAM) a diciembre de 2024, el mismo final de los reanálisis del curso.

## Cómo se usan

En la celda 1 del cuaderno, escriba en `ARCHIVO_ESTACION` el valor de la columna `archivo` del índice, por ejemplo:

```python
ARCHIVO_ESTACION = "manabi_calceta_espam.csv"
ARCHIVO_ESTACION = "synop/guayas_milagro_84202.csv"
```

No hay que subir nada a Drive: el cuaderno lee el archivo desde el repositorio y completa solo el nombre, el código, las coordenadas y la altitud. Si deja `ARCHIVO_ESTACION` vacío, el cuaderno le muestra las estaciones de su provincia.

## Índice: [`indice_estaciones.csv`](indice_estaciones.csv)

| Columna | Contenido |
|---|---|
| `archivo` | Lo que se escribe en `ARCHIVO_ESTACION` |
| `provincia`, `estacion`, `omm`, `codigo` | Ubicación, nombre, indicativo OMM y código INAMHI (o indicativo de OGIMET si no lo hay) |
| `lat`, `lon`, `altitud_m` | Coordenadas en grados decimales y altitud en metros |
| `desde`, `hasta` | Primer y último día con dato |
| `meses_tmax`, `meses_tmin`, `meses_precip` | Meses que pasan el control de completitud de los cuadernos (temperatura: máximo 4 días faltantes y 2 seguidos; lluvia: mes completo) |
| `variables`, `fuente`, `url` | Columnas del archivo, fuente y enlace directo |

## Fuentes

| Archivos | Fuente | Variables |
|---|---|---|
| `synop/*.csv` (38 estaciones, 23 provincias) | Mensajes SYNOP del Sistema Mundial de Telecomunicaciones de la OMM, obtenidos de OGIMET (https://www.ogimet.com) y resumidos por día | `tmax`, `tmin`, `precip` |
| `manabi_calceta_espam.csv` | Estación meteorológica de la ESPAM MFL, Calceta (cantón Bolívar, Manabí), 2010–2024, con control de calidad | `tmed`, `tmax`, `tmin`, `precip`, `hr`, `vv` |
| `manabi_manta_aeropuerto_semt_metar.csv` | Mensajes METAR del aeropuerto de Manta (SEMT), obtenidos de OGIMET y resumidos por día (días con 12 observaciones o más) | `tmed`, `tmax`, `tmin`, `hr`, `pres`, `vv`, `dv` |

En el METAR, la presión es la de la estación, calculada desde el QNH con la ecuación hipsométrica, y las temperaturas máxima y mínima son las de las observaciones horarias (valores enteros).

**Cómo citar:**
- OGIMET. *Datos SYNOP y METAR del Sistema Mundial de Telecomunicaciones de la OMM*. https://www.ogimet.com. Procesados por C. Paliz Acosta (2026).
- ESPAM MFL. *Estación meteorológica de la ESPAM MFL, Calceta, Manabí. Datos diarios 2010–2024*. Procesados por C. Paliz Acosta (2026).

## Limitaciones (declárelas en el capítulo)

- **Lluvia de las estaciones SYNOP:** los mensajes no siempre llegan, y un día sin mensaje queda vacío. Como los cuadernos solo aceptan meses de lluvia completos, la mayoría de las estaciones tiene pocos meses válidos de lluvia (0 a 42). Para la lluvia en Manabí use la ESPAM (168 meses).
- **Definición del día:** los resúmenes SYNOP y METAR siguen el día de la fuente, no necesariamente el día pluviométrico del INAMHI (07:00–07:00).
- **Coordenadas de la ESPAM:** son aproximadas (−0,83; −80,18; 15 m); se reemplazarán por las de la ficha oficial de la estación.
- **Sin estación útil:** Bolívar, Napo, Zamora Chinchipe y Galápagos; Imbabura y Chimborazo tienen muy pocos datos. En esas provincias se usa la estación que indique el docente.

Uso docente en las prácticas de Cambio Climático de la ESPAM MFL.
