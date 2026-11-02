# Bitácora del evento El Niño 2026–2027 (común)

Los datos de reanálisis del curso terminan en 2024, así que el evento en curso **no entra** en el análisis climatológico del capítulo 1. Se sigue aparte, en esta bitácora, que va como **anexo del capítulo 1** y se retoma en la Unidad II (respuesta real al evento).

Una fila por consulta, al menos una vez por semana. Todo lo que se registra aquí es **preliminar**: los índices se corrigen y los reportes se actualizan. Se puede llevar en papel cuando no haya energía, con las mismas columnas, y pasarla al CSV después.

## Cómo se llena

**Los cuadernos crean y alimentan la bitácora solos.** Cada vez que ejecuta `IA1_03` (Ambiental, sección 8) o `RD1_01` (Riesgos, sección 5), se agrega una fila a su archivo en Drive:

| Carrera | Archivo |
|---|---|
| Ingeniería Ambiental | `Mi unidad/CC_Ambiental/bitacora/bitacora_el_nino_<zona>.xlsx` |
| Ingeniería en Riesgos de Desastres | `Mi unidad/CC_Riesgos/bitacora/bitacora_el_nino_<zona>.xlsx` |

- La fila trae ya `fecha_consulta`, `mes_indice`, `icen`, `icen_categoria`, `oni`, `fuente` y `url`.
- Si ya hay una fila con la fecha de hoy, solo se actualizan los índices. Lo que usted escribió nunca se borra.
- Usted completa `comunicado`, `alerta_sngr`, `incidentes_zona` y `observacion_propia`: abra el archivo desde Drive (se edita en Hojas de cálculo de Google sin convertirlo) o en Excel, escriba y cierre.
- Ejecute la celda al menos una vez por semana. En Riesgos, el equipo entrega una sola bitácora.
- El ICEN que calcula el curso usa Niño 1+2 de NOAA; contrástelo con el valor oficial del IGP.

El archivo [`bitacora_el_nino.csv`](bitacora_el_nino.csv) de esta carpeta es solo la **plantilla vacía** (encabezados) para llevar la bitácora en papel u otra hoja cuando no haya energía; luego se pasan las filas al .xlsx.

| Columna | Contenido |
|---|---|
| `fecha_consulta` | AAAA-MM-DD, el día en que usted consultó la fuente |
| `icen`, `icen_categoria` | Último valor del ICEN y su categoría (cálida débil, moderada, fuerte, extraordinaria) |
| `oni` | Último valor del ONI |
| `mes_indice` | Mes al que corresponde el valor (AAAA-MM): el índice siempre va atrasado |
| `comunicado` | Estado oficial vigente: comunicado del ERFEN o del INAMHI (número y fecha) |
| `alerta_sngr` | Alerta o SitRep vigente de la SNGR para su zona |
| `incidentes_zona` | Lo que pasó en su zona desde la consulta anterior: tipo, cantón, fecha (ECU 911, SitRep, GAD o prensa) |
| `observacion_propia` | Lo que usted vio o midió (lluvia en la estación, crecida de un río, oleaje), con lugar |
| `fuente`, `url` | De dónde sale cada dato; obligatorio |

## Fuentes

| Dato | Dónde |
|---|---|
| ONI y Niño 1+2 | NOAA CPC; los cuadernos `RD1_01` e `IA1_03` imprimen los últimos valores |
| ICEN oficial | Instituto Geofísico del Perú, ENFEN |
| Comunicados del ERFEN | INAMHI e INOCAR |
| SitRep y reportes de monitoreo | [Secretaría Nacional de Gestión de Riesgos](https://www.gestionderiesgos.gob.ec/informes-de-situacion-actual-por-eventos-adversos-ecuador/) |
| Incidentes diarios por parroquia | ECU 911, Base de Emergencias (Datos Abiertos); `RD1_02` deja el archivo de su zona en `RD1_02_ecu911_<zona>.csv` |
