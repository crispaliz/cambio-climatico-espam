# herramientas/eventos

Registros de eventos peligrosos para contrastarlos con la lluvia y la temperatura observadas.

| Módulo | Fuente | Periodo | Qué aporta | Qué no aporta |
|---|---|---|---|---|
| `desinventar.py` | [DesInventar Sendai, Ecuador](https://db.desinventar.org/DesInventar/country_profile.jsp?countrycode=ecu&lang=ES) (UNDRR) | 1970–2007 | Una ficha por desastre con fecha, provincia y cantón (código DPA), tipo, fallecidos, afectados y viviendas, y la fuente original (prensa, Defensa Civil) | Eventos posteriores a 2007 |
| `ecu911.py` | SIS ECU 911, [Base de Emergencias](https://www.datosabiertos.gob.ec/dataset/base-de-emergencias) (Datos Abiertos del Ecuador) | Julio de 2021 en adelante, un archivo por mes | Incidentes diarios por parroquia del servicio «Gestión de Riesgos»: inundación, deslizamiento, vendaval, incendio forestal y otros | Fallecidos, afectados y daños; eventos anteriores a 2021 |

`RD1_02` arma el registro de eventos de la zona **automáticamente** con las dos bases; el registro del equipo es un complemento opcional para el vacío de 2008 a junio de 2021.

## DesInventar Ecuador

`datos/eventos/desinventar_ecu_hidromet.csv.gz`: 2 527 desastres de origen hidrometeorológico con fecha exacta, de marzo de 1970 a diciembre de 2007, procesados de la exportación XML oficial (`DI_export_ecu.zip`, descargada el 30 de octubre de 2026). `desinventar.de_zona(ruta, codigo_dpa)` filtra por provincia (2 dígitos) o cantón (4 dígitos).

| Evento de DesInventar | Tipo del curso | Eventos |
|---|---|---|
| Inundación | inundación | 1 123 |
| Deslizamiento | deslizamiento | 658 |
| Lluvias | lluvia intensa | 201 |
| Aluvión, Avenida torrencial | aluvión | 113 |
| Incendio forestal | incendio forestal | 102 |
| Sequía | sequía | 97 |
| Marejada | oleaje | 90 |
| Vendaval, Tempestad | vendaval | 82 |
| Granizada, Helada, Ola de calor, Tormenta eléctrica | otro | 61 |

Particularidades: un 0 en los daños de DesInventar significa «no reportado» y queda vacío; las fichas sin día (0,5 %) se excluyen porque no se pueden cruzar con lluvia diaria; los eventos anteriores a la creación de un cantón llevan el código del cantón del que se separó. Cita: UNDRR. *DesInventar Sendai: base de datos de pérdidas por desastres de Ecuador*. https://db.desinventar.org. Los derechos de la información son de las instituciones que la compilaron.

`ecu911.incidentes()` descarga cada mes una sola vez y guarda solo las filas útiles en una caché (`Mi unidad/CC_datos/_ecu911/`). Si el docente publica un compilado nacional, se usa ese archivo y no se descarga nada.

**Compilado del docente (recomendado).** `python -m herramientas.eventos.preparar_ecu911` en Colab deja `datos/eventos/ecu911_gestion_riesgos.csv.gz` con todo el país (unos 10–20 minutos). Subido al repositorio en esa ruta, `RD1_02` lo usa directamente y los estudiantes no descargan nada del portal.

## Compilado nacional

`datos/eventos/ecu911_gestion_riesgos.csv.gz`: 51 305 incidentes climáticos de gestión de riesgos de todo el país, de julio de 2021 a septiembre de 2026, descargados el 24 de octubre de 2026 de los 63 archivos mensuales publicados. Particularidades de la fuente:

| Particularidad | Efecto |
|---|---|
| Enero de 2024 incompleto en el archivo publicado (≈40 incidentes frente a ≈800 de un mes típico) | Es un vacío de la fuente, no un mes sin eventos |
| Febrero de 2023 sin subtipo | Sus 911 incidentes quedan como «gestión de riesgos sin detalle» |
| En la Costa casi todo viene como «Amenazas naturales» (en Manabí, 985 de 1 095) | El tipo se interpreta con la época del año y la lluvia de esos días |
| En la Sierra, «Incendio forestal» domina de julio a noviembre | Estacionalidad de la temporada seca |

## Fuentes complementarias (opcionales, a mano)

| Fuente | Periodo | Uso |
|---|---|---|
| [Informes de situación (SitRep) de la SNGR](https://www.gestionderiesgos.gob.ec/informes-de-situacion-actual-por-eventos-adversos-ecuador/) | 2016–2026, por evento o época lluviosa | Afectados, viviendas y fallecidos por cantón; incluye el SitRep de las lluvias con incidencia de El Niño desde el 29 de agosto de 2026 |
| [Reportes de monitoreo de la SNGR](https://www.gestionderiesgos.gob.ec/reportes-de-monitoreo-de-amenazas-y-eventos-peligrosos-2025/) | 2025–2026, diarios | Estado de amenazas y eventos del día: insumo de la bitácora |
| Gobiernos autónomos (GAD) y prensa local con fecha | Variable | Completar vacíos, siempre con la fuente |

El conjunto «Eventos Peligrosos» que la SNGR publicaba en Datos Abiertos ya no está disponible en el portal (consulta del 22 de octubre de 2026).
