# Bitácora del evento El Niño 2026–2027 (común)

Los datos de reanálisis del curso terminan en 2024, así que el evento en curso **no entra** en el análisis climatológico del capítulo 1. Se sigue aparte, en esta bitácora, que va como **anexo del capítulo 1** y se retoma en la Unidad II (respuesta real al evento).

Una fila por consulta, al menos una vez por semana. Todo lo que se registra aquí es **preliminar**: los índices se corrigen y los reportes se actualizan. Se puede llevar en papel cuando no haya energía, con las mismas columnas, y pasarla al CSV después.

Plantilla: [`bitacora_el_nino.csv`](bitacora_el_nino.csv).

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
