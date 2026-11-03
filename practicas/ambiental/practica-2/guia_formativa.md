# Guía de la evaluación formativa — Capítulo 2 (borrador)

**Cambio Climático · Ingeniería Ambiental · ESPAM MFL** · Guía CC-IAM-C2-F · Versión 1.0 · noviembre de 2026

| | |
|---|---|
| Unidad | Unidad II. Estrategias de mitigación y adaptación frente al cambio climático |
| Resultado de aprendizaje | **RA B.** Analizar las estrategias de mitigación y adaptación frente al cambio climático, diferenciando su alcance y pertinencia en la gestión ambiental. |
| Práctica que la sustenta | Práctica 2 — Emisiones, riesgo y estrategias: cuadernos `IA2_01_inventario_emisiones`, `IA2_02_ficha_riesgo` e `IA2_03_matriz_estrategias` (repositorio github.com/crispaliz/cambio-climatico-espam), que se apoyan en los productos de la Práctica 1 (`CR01`, `CR02`, `IA1_03`). |
| Producto | Borrador del capítulo 2 «Emisiones, riesgo climático y estrategias de la provincia»: secciones 1 a 4 y anexo B de la plantilla CC-IAM-C2. |
| Modalidad de trabajo | Individual: la misma provincia del capítulo 1 y un sitio de ella para la ficha de riesgo. |
| Tipo de evaluación | Formativa (con retroalimentación para el capítulo definitivo y la evaluación sumativa de la Unidad II). |
| Valor | **2,00 puntos**. |
| Entrega | Al cerrar `IA2_03` (sesión del 25 de noviembre de 2026), en el espacio que el docente habilite en la plataforma virtual. |
| Docente | Ing. Cristian Omar Paliz Acosta, MSc. |

## 1. Propósito de la evaluación

El capítulo 2 responde una pregunta de gestión ambiental: **¿qué debería hacer su provincia frente al cambio climático, y por qué eso y no otra cosa?** Para responderla con fundamento se necesitan tres piezas que el borrador debe mostrar completas y bien leídas: cuánto y de dónde emite la provincia (inventario), qué riesgo climático enfrenta un sitio concreto (ficha de riesgo) y qué estrategias responden mejor a ambos (matriz).

El borrador comprueba que usted **ejecutó correctamente los tres cuadernos**, que **justificó cada dato y cada calificación** con una fuente o una observación, y que las estrategias **salen de sus resultados** y no de una lista genérica. El lector previsto es un técnico de la dirección ambiental o de gestión de riesgos del GAD provincial.

El docente devuelve el borrador con **observaciones numeradas (O1, O2, …)**. Atenderlas es parte de la evaluación sumativa de la Unidad II (resolución de problemas), donde se evalúa además la habilidad blanda de resolución de problemas complejos.

## 2. La cadena de cuadernos: qué usa cada uno y qué deja en su Drive

Los cuadernos se abren desde el repositorio del curso con el botón «Open in Colab» y se guardan con **Archivo › Guardar una copia en Drive**. Cada uno usa lo que dejó el anterior: por eso la provincia debe ser la misma en todos.

| Paso | Cuaderno | Usa | Deja en `Mi unidad/CC_Ambiental/practica-2/<provincia>/` |
|---|---|---|---|
| 1 | `IA2_01_inventario_emisiones` | Datos de actividad que usted busca (ARCERNNR, INEC-ESPAC, MAATE, Censo 2022) y los factores del IPCC del repositorio | `IA2_01_inventario_detalle_*.csv`, `IA2_01_resumen_sector_*.csv`, `IA2_01_categorias_principales_*.csv`, `IA2_01_comparacion_nacional_*.csv`, `IA2_01_ficha_datos_actividad_*.csv`, `IA2_01_inventario_*.png`, `IA2_01_metadatos.json` |
| 2 | `IA2_02_ficha_riesgo` | Series diarias y mensuales de `CR02` (`CC_datos/<zona>/`), años de El Niño de `IA1_03` (`CC_Ambiental/practica-1/<zona>/`) y su hoja de campo | `IA2_02_ficha_riesgo_*.png`, `IA2_02_evidencia_climatica_*.csv`, `IA2_02_calificaciones_*.csv`, `IA2_02_riesgo_*.csv`, `IA2_02_ficha.json` |
| 3 | `IA2_03_matriz_estrategias` | Categorías principales de `IA2_01` y amenazas e indicadores críticos de `IA2_02` | `IA2_03_matriz_*.png`, `IA2_03_evaluacion_*.csv`, `IA2_03_cartera_*.csv`, `IA2_03_metadatos.json` |

- Si cambió la provincia o el cantón de la Práctica 1, `IA2_02` lee los datos de esa misma zona (celda 1).
- Cada cuaderno termina con una celda de **revisión** («Revise antes de entregar»): el borrador no debe tener avisos pendientes sin explicación.
- `IA2_03` imprime un bloque de opciones sugeridas: cópielo a la celda 6, elija entre 6 y 12, califíquelas y escriba la justificación de cada una.

## 3. Qué se entrega

| Elemento | Detalle |
|---|---|
| Archivo | Un PDF generado desde Word. |
| Nombre del archivo | `CC-IAM-C2_borrador_<provincia>_<apellido>.pdf` (ejemplo: `CC-IAM-C2_borrador_manabi_zambrano.pdf`). |
| Portada | Asignatura, título del capítulo, provincia, sitio evaluado, nombre completo y fecha. |
| Contenido | Secciones 1 a 4 de la plantilla con sus figuras y tablas; respuestas a las preguntas de los tres cuadernos integradas en el texto (no como cuestionario aparte); anexo B. |
| Extensión | 5 a 8 páginas sin portada ni anexos; letra de 11 puntos, interlineado 1,15. |
| No se entrega aún | Sección 5 (discusión, límites de la adaptación y conclusiones) y anexo C (atención a observaciones): van en el capítulo definitivo. |
| Uso de IA | Permitido como apoyo si se declara (herramienta y para qué se usó) al final del documento. Los datos de actividad, las calificaciones y su justificación deben ser suyos y verificables en sus archivos. |

## 4. Antes de escribir: verifique sus tres corridas

| Revise | Dónde lo ve | Si no está bien |
|---|---|---|
| La misma provincia en los tres cuadernos | Celda 1 y nombre de la carpeta `practica-2/<provincia>` | Vuelva a ejecutar con la provincia correcta. |
| Completitud del inventario | Tabla de completitud de `IA2_01` (celda 8) | Las categorías NE no son error, pero se explican en la sección 2. Si quedaron NE por no buscar el dato, búsquelo. |
| Unidades de los datos de actividad | Ficha de datos de actividad (`IA2_01`, celda 10) | Galones, no litros ni barriles; kg de GLP, no cilindros; cabezas, no unidades productivas. |
| Coherencia de la ficha de riesgo | Celda 7 de `IA2_02` («Revise antes de entregar») | Escriba la justificación que falta o explique por qué su calificación difiere de la sugerencia climática. |
| Ubicación del sitio | Celda 3 de `IA2_02` y mapa de la ficha | La longitud en Ecuador es negativa; el punto debe caer en el cantón. |
| Evaluación de la matriz | `IA2_03_metadatos.json`: `evaluacion_por_defecto` debe ser `false` | Si es `true`, no llenó la celda 6: la matriz no es válida. |

## 5. Qué se pide en cada sección

Cada sección indica lo que debe contener, las figuras y tablas mínimas, los archivos de donde salen, las preguntas de los cuadernos que se integran y los errores que más se repiten.

### Sección 1. Introducción: de la evidencia climática a la gestión

Conecta el capítulo 1 con este: qué cambió en el clima de la provincia y por qué eso obliga a mitigar y a adaptarse.

**Qué debe contener**

- Síntesis de dos o tres resultados del capítulo 1 que justifican el capítulo: tendencia de la temperatura, señal de El Niño en la lluvia, extremos.
- Contexto de compromisos: Acuerdo de París, Segunda NDC del Ecuador (meta incondicional de 7 % y condicional de 8 % al 2035 frente al escenario tendencial) y PLANACC.
- Objetivo del capítulo y la cadena del análisis: inventario → riesgo del sitio → estrategias.
- Por qué se eligió el sitio de la ficha (qué representa de la provincia).

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Capítulo 1 (secciones 3 y 5); lectura autónoma sobre el régimen climático y la NDC; `IA2_02_ficha.json` (sitio). | — | 0,5 página |

**Errores frecuentes que se observarán**

- Repetir el capítulo 1 en vez de usarlo.
- Hablar del cambio climático global sin llegar a la provincia.
- No explicar por qué ese sitio.

### Sección 2. Inventario de emisiones de la provincia

**Qué debe contener**

- **Método:** Directrices del IPCC de 2006, Nivel 1; CO₂ equivalente con los PCG del AR5 (CH₄ = 28; N₂O = 265); año de los datos.
- **Datos de actividad** con su fuente y año (tabla de la ficha de `IA2_01`); supuestos propios declarados.
- **Resultados:** total en kt CO₂-eq con su incertidumbre; distribución por sector y por gas; emisiones por habitante.
- **Categorías principales** (las que suman el 95 %) y qué las explica en la provincia.
- **Completitud:** categorías NE y su posible peso; la electricidad como partida informativa (alcance 2) y por qué no se suma.
- **Comparación con el inventario nacional 2022** (perfil por sector y por habitante) y por qué no es directamente comparable.

**Figuras y tablas mínimas**

- Figura: perfil por sector, por gas y categorías (`IA2_01_inventario_*.png`).
- Tabla: datos de actividad y fuentes (`IA2_01_ficha_datos_actividad_*.csv`).
- Tabla: emisiones por sector y categorías principales (`IA2_01_resumen_sector_*.csv`, `IA2_01_categorias_principales_*.csv`).
- Tabla (opcional): comparación nacional (`IA2_01_comparacion_nacional_*.csv`).

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Productos `IA2_01_*`. | `IA2_01`, preguntas 1 a 7. | 1,5 a 2 páginas |

**Errores frecuentes que se observarán**

- Datos de actividad sin fuente ni año.
- Sumar la electricidad al total.
- Reportar con falsa precisión (4 849 123,7 t) en vez de redondear según la incertidumbre.
- Ocultar las categorías NE o presentar un total incompleto como si fuera completo.

**Ejemplo de redacción esperada**

*(Valores ilustrativos) Con datos de 2024, la provincia emitió unas 4 850 kt CO₂-eq (± 17 %), 3,0 t por habitante. La categoría principal fue el transporte por carretera (34 %), seguida de la fermentación entérica de 813 407 vacunos (27 %; INEC, ESPAC 2024). Los procesos industriales y las térmicas locales no se estimaron (NE), por lo que el total está subestimado.*

### Sección 3. Riesgo climático de un sitio

**Qué debe contener**

- **Sitio:** nombre, cantón, parroquia, coordenadas, tipo, fecha de la visita y descripción (población, actividades, eventos anteriores).
- **Marco:** riesgo = amenaza × exposición × vulnerabilidad (IPCC AR6, GTII); vulnerabilidad = sensibilidad y falta de capacidad de adaptación; escala 1–5 y fórmula del índice.
- **Amenazas** con su evidencia climática (factor de El Niño en la lluvia de diciembre a mayo, Rx1day de 25 años, tendencia de días cálidos) y con la evidencia del sitio; explicación de cada diferencia con la sugerencia del cuaderno.
- **Exposición, sensibilidad y capacidad de adaptación:** calificación de cada indicador con su justificación; indicadores críticos.
- **Índice de riesgo por amenaza** y clase; amenaza principal y componente que más la explica.
- **Relación con El Niño 2026–27** en curso (bitácora `CB01`, si la lleva).
- **Limitaciones:** datos climáticos de la zona y no del sitio, subjetividad de las calificaciones, escala.

**Figuras y tablas mínimas**

- Figura: ficha de riesgo del sitio (`IA2_02_ficha_riesgo_*.png`).
- Tabla: evidencia climática (`IA2_02_evidencia_climatica_*.csv`).
- Tabla: calificaciones con su justificación (`IA2_02_calificaciones_*.csv`) y riesgo por amenaza (`IA2_02_riesgo_*.csv`).
- Dos a cuatro fotografías propias del sitio con pie (qué muestran y fecha).

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Productos `IA2_02_*`; hoja de campo (anexo de esta guía); PDOT del GAD; registros de eventos (SGR, ECU 911). | `IA2_02`, preguntas 1 a 6. | 1,5 a 2 páginas |

**Errores frecuentes que se observarán**

- Calificaciones sin justificación, o todas iguales.
- Confundir amenaza con riesgo («el riesgo es la lluvia»).
- Invertir la capacidad de adaptación (más capacidad no es más vulnerabilidad).
- Usar la evidencia de la provincia como si fuera medida en el sitio, sin decirlo.

**Ejemplo de redacción esperada**

*(Valores ilustrativos) El riesgo de inundación del barrio es alto (3,5 de 5). La amenaza (4) se apoya en el aumento de la lluvia de diciembre a mayo en los años de El Niño (factor 1,2 en ERA5) y en las marcas de agua de 2023 a 0,6 m. Lo que más pesa es la vulnerabilidad (3,5): drenaje colmatado (5) y ausencia de alerta temprana (capacidad 2).*

### Sección 4. Matriz de estrategias de mitigación y adaptación

**Qué debe contener**

- **Opciones evaluadas** (6 a 12; al menos 3 de mitigación y 3 de adaptación) y **a qué resultado responde cada una** (categoría del inventario, amenaza o indicador de vulnerabilidad del sitio).
- **Criterios y pesos** con la justificación de los pesos.
- **Matriz y ranking**; prueba de robustez con pesos iguales.
- **Cartera priorizada:** las primeras opciones, su sinergia mitigación–adaptación, alertas de mala adaptación y cómo evitarlas.
- **Actores e instrumentos:** quién ejecutaría la primera opción (GAD, MAATE, MAG, juntas de agua, comunidad) y su vínculo con la NDC, el PLANACC y el PDOT.

**Figuras y tablas mínimas**

- Figura: matriz de evaluación y gráfico de efectividad frente a factibilidad (`IA2_03_matriz_*.png`).
- Tabla: cartera priorizada (`IA2_03_cartera_*.csv`).
- Tabla (anexo o cuerpo): evaluación completa con justificaciones (`IA2_03_evaluacion_*.csv`).

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Productos `IA2_03_*`; clases del 17 y 24 de noviembre; Segunda NDC; PLANACC; PDOT de la provincia. | `IA2_03`, preguntas 1 a 6. | 1,5 a 2 páginas |

**Errores frecuentes que se observarán**

- Opciones que no responden a ningún resultado del inventario ni de la ficha.
- Puntajes sin justificación o copiados del bloque sugerido (todos 3).
- Ignorar las alertas de mala adaptación del catálogo.
- Una cartera solo de mitigación o solo de adaptación.

**Ejemplo de redacción esperada**

*(Valores ilustrativos) La primera opción es el sistema de alerta temprana comunitario (4,25), que responde a la amenaza principal del sitio y a su indicador más débil (alerta, 2). La ganadería silvopastoril (4,05) es la mejor opción de mitigación: reduce la fermentación entérica, segunda categoría del inventario, y además da sombra y retiene agua (sinergia 5). El ranking se mantiene en 4 de las 5 primeras con pesos iguales.*

### Anexo B. Reproducibilidad

- Enlace (con permiso de lectura para el docente) a sus copias de los tres cuadernos en Drive.
- Lista de los archivos `IA2_01_*`, `IA2_02_*` e `IA2_03_*` producidos.
- Hoja de campo escaneada o fotografiada.
- Declaración de uso de herramientas de IA, si las usó.

## 6. Del cuaderno al documento: dónde va cada producto

Use esta tabla como lista de control: cada fila es una pieza que el docente buscará en el borrador.

| Producto (en su Drive) | Cuaderno | Dónde va en el capítulo 2 | Cómo se usa |
|---|---|---|---|
| `IA2_01_ficha_datos_actividad_*.csv` | IA2_01 | Sección 2, tabla de datos | Cada dato con su unidad, fuente y año |
| `IA2_01_inventario_*.png` | IA2_01 | Sección 2, figura principal | Perfil por sector frente al nacional, por gas y categorías |
| `IA2_01_resumen_sector_*.csv` y `IA2_01_categorias_principales_*.csv` | IA2_01 | Sección 2, tabla de resultados | Total, %, categorías principales |
| `IA2_01_metadatos.json` | IA2_01 | Sección 2, texto | Incertidumbre, completitud (NE), PCG, año |
| `IA2_02_evidencia_climatica_*.csv` | IA2_02 | Sección 3, tabla de amenaza | Factor El Niño, Rx1day de 25 años, TX90p |
| `IA2_02_calificaciones_*.csv` | IA2_02 | Sección 3, tabla de componentes | Cada calificación con su justificación |
| `IA2_02_ficha_riesgo_*.png` | IA2_02 | Sección 3, figura principal | Ubicación, componentes y riesgo por amenaza |
| `IA2_02_riesgo_*.csv` | IA2_02 | Sección 3, texto; insumo de IA2_03 | Amenaza principal y clase |
| `IA2_03_matriz_*.png` | IA2_03 | Sección 4, figura principal | Matriz y gráfico efectividad–factibilidad |
| `IA2_03_cartera_*.csv` | IA2_03 | Sección 4, tabla de cartera | Opciones priorizadas, a qué responden y alertas |
| `IA2_03_evaluacion_*.csv` y `IA2_03_metadatos.json` | IA2_03 | Sección 4 y anexo | Puntajes, pesos, robustez |
| Preguntas finales de cada cuaderno | Los tres | Integradas en el texto de las secciones 2 a 4 | No como cuestionario aparte |

## 7. Reglas de forma

- Cada figura y tabla lleva número, título, fuente y «Elaboración propia», y se cita en el texto antes de aparecer.
- Todo número va con su unidad, su fuente y su año. Las emisiones se redondean según su incertidumbre.
- Cada calificación (riesgo y estrategias) tiene una justificación verificable: un dato, una fuente o una observación del sitio.
- Las fotografías son propias, con pie (qué muestran, lugar y fecha); las de terceros, con autor y licencia.
- Citas y referencias en APA 7.ª edición; las de los métodos están al final de cada cuaderno.
- Los números del documento deben coincidir con los archivos de su Drive.

## 8. Rúbrica de evaluación (2,00 puntos)

Cinco criterios de **0,40 puntos** cada uno, con cinco niveles. Se asigna un solo nivel por criterio; la nota es la suma de los cinco.

| Criterio e indicadores | Logrado · 0,40 | Suficiente · 0,30 | En proceso · 0,20 | Inicial · 0,10 | No presenta · 0,00 |
|---|---|---|---|---|---|
| **C1. Introducción y coherencia del capítulo (sección 1 y conexión entre secciones)**<br>Indicadores: resultados del capítulo 1 usados; compromisos del país; objetivo y cadena del análisis; elección del sitio; las estrategias se derivan de las secciones 2 y 3. | Usa resultados concretos del capítulo 1 para justificar el capítulo; sitúa la NDC y el PLANACC; explica la cadena inventario → riesgo → estrategias y por qué eligió el sitio; las secciones se citan entre sí. | Cumple casi todo, con la elección del sitio o el contexto incompletos. | Introducción genérica o sin vínculo con el capítulo 1. | Secciones sueltas, sin hilo. | No presenta la sección 1. |
| **C2. Inventario de emisiones (sección 2)**<br>Indicadores: método y PCG; datos de actividad con fuente y año; total con incertidumbre; sectores, gases y categorías principales; completitud y NE; electricidad aparte; comparación nacional. | Método, PCG y año declarados; cada dato de actividad con unidad, fuente y año; total redondeado con incertidumbre; sectores, gases y categorías principales interpretados; NE explicadas y su efecto en el total; electricidad como memo; comparación nacional con sus límites. | Correcto, con una o dos omisiones (por ejemplo, sin comparación nacional o sin el efecto de las NE). | Datos de actividad sin fuente, electricidad sumada al total o categorías principales mal leídas. | Solo la figura o la tabla del cuaderno, sin lectura. | No presenta la sección. |
| **C3. Ficha de riesgo del sitio (sección 3)**<br>Indicadores: sitio descrito y ubicado; marco AR6 y fórmula; amenazas con evidencia climática y del sitio; componentes justificados; índice e interpretación; limitaciones; fotos propias. | Sitio ubicado y descrito con fecha de visita; marco y fórmula explicados; cada amenaza con evidencia climática y del sitio, y las diferencias con la sugerencia explicadas; todos los indicadores justificados; amenaza principal y componente dominante identificados; limitaciones y fotos con pie. | Correcto, con justificaciones débiles en algunos indicadores. | Calificaciones sin justificar, confusión entre amenaza y riesgo o capacidad invertida. | Solo la figura de la ficha. | No presenta la sección. |
| **C4. Matriz de estrategias (sección 4)**<br>Indicadores: opciones vinculadas a resultados; equilibrio mitigación–adaptación; criterios, pesos y su justificación; ranking y robustez; cartera con sinergias, mala adaptación, actores y alineación. | Entre 6 y 12 opciones, cada una vinculada a una categoría principal, una amenaza o un indicador crítico; al menos 3 de mitigación y 3 de adaptación; pesos justificados; robustez leída; cartera con sinergias, alertas de mala adaptación tratadas, actores responsables y vínculo con NDC, PLANACC y PDOT. | Correcto, con una omisión (por ejemplo, sin actores o sin robustez). | Opciones desvinculadas de sus resultados, puntajes sin justificar o cartera desequilibrada. | Lista de opciones sin evaluación. | No presenta la sección, o evaluación por defecto (todos 3). |
| **C5. Forma, fuentes y reproducibilidad**<br>Indicadores: figuras y tablas completas; respuestas integradas; unidades y redondeo; APA 7; anexo B; coincidencia con el Drive; extensión. | Figuras y tablas numeradas con título, fuente y unidad, citadas antes de aparecer; respuestas integradas; APA 7 correcto; anexo B completo con la hoja de campo; números coinciden con el Drive; extensión dentro de lo pedido. | Uno o dos elementos de forma ausentes. | Varias figuras sin unidad o fuente, o anexo B incompleto. | Documento desordenado; no se puede rastrear el origen de los números. | Sin anexo B y sin formato mínimo. |

### Condiciones de entrega

- Entregas fuera de plazo: solo con la justificación que establece el reglamento de evaluación estudiantil.
- Plagio (de un compañero, de semestres anteriores o de fuentes no citadas): la calificación es 0, según las políticas de la asignatura.
- Productos de una provincia distinta a la declarada o calificaciones copiadas de otro estudiante: el criterio afectado se califica como «Inicial».

### Hoja de calificación

Estudiante: ______________________________   Provincia: ____________________   Sitio: ____________________   Fecha: ____________

| Criterio | Puntaje máximo | Nivel asignado | Puntaje obtenido | Observaciones (O1, O2, …) |
|---|---|---|---|---|
| C1. Introducción y coherencia del capítulo | 0,40 |  |  |  |
| C2. Inventario de emisiones | 0,40 |  |  |  |
| C3. Ficha de riesgo del sitio | 0,40 |  |  |  |
| C4. Matriz de estrategias | 0,40 |  |  |  |
| C5. Forma, fuentes y reproducibilidad | 0,40 |  |  |  |
| **Total** | **2,00** |  |  |  |

## 9. Retroalimentación

El docente devuelve el borrador con observaciones numeradas por sección (O1, O2, …). Usted responde cada una en el **anexo C** del capítulo definitivo (matriz de atención a observaciones), que se presenta en la sumativa de la Unidad II.

## Anexo. Hoja de campo para la ficha de riesgo (IA2_02)

Imprímala o cópiela en su libreta. Llénela en el sitio y pase las calificaciones a las celdas 5 y 6 de `IA2_02`. Cada calificación lleva una evidencia (foto, medida, relato con fuente, documento).

| Dato | Valor |
|---|---|
| Sitio, cantón y parroquia |  |
| Coordenadas (GPS del teléfono, grados decimales) | Lat:              Lon: |
| Fecha y hora de la visita |  |
| Tipo de sitio | ☐ barrio junto a río  ☐ costa o playa  ☐ estuario o manglar  ☐ llanura agrícola inundable  ☐ ladera  ☐ secano  ☐ otro |
| Personas entrevistadas (rol, no nombre) |  |
| Fotografías tomadas (número y tema) |  |

**Amenazas (1–5; 0 si no aplica)**

| Amenaza | 1 | 3 | 5 | Valor | Evidencia |
|---|---|---|---|---|---|
| Inundación por lluvia y crecidas | sin registros | marcas de agua o relatos de eventos ocasionales | inundaciones recurrentes con daños |  |  |
| Movimientos en masa | terreno plano y estable | grietas, taludes cortados | deslizamientos activos o recientes |  |  |
| Costera: oleaje y erosión | lejos del mar | playa angosta, oleajes que llegan a la vía | viviendas afectadas por el mar, retroceso visible |  |  |
| Sequía | agua todo el año | cortes en la estación seca | desabastecimiento prolongado, pérdidas de cosecha |  |  |
| Calor extremo | sombra y ventilación | quejas de calor en la estación seca | afectación a la salud o al trabajo documentada |  |  |

**Exposición, sensibilidad y capacidad de adaptación (1–5)**

| Componente | Indicador | Valor | Evidencia |
|---|---|---|---|
| Exposición | Personas en la zona de amenaza |  |  |
| Exposición | Viviendas y edificaciones |  |  |
| Exposición | Servicios críticos (agua, salud, escuela, vías, energía) |  |  |
| Exposición | Actividades económicas |  |  |
| Exposición | Ecosistemas y sus servicios |  |  |
| Sensibilidad | Viviendas precarias o sin cimentación |  |  |
| Sensibilidad | Pobreza, niñez, personas mayores o con discapacidad |  |  |
| Sensibilidad | Dependencia de actividades sensibles al clima |  |  |
| Sensibilidad | Degradación del ecosistema |  |  |
| Sensibilidad | Drenaje, saneamiento o agua deficientes |  |  |
| Capacidad (5 = muy buena) | Alerta temprana y organización comunitaria |  |  |
| Capacidad (5 = muy buena) | Acceso a servicios, evacuación y albergues |  |  |
| Capacidad (5 = muy buena) | Gestión del riesgo en el PDOT y control del uso del suelo |  |  |
| Capacidad (5 = muy buena) | Recursos, seguros o fondos de contingencia |  |  |

Escalas: exposición 1 nada · 2 poco, disperso · 3 moderado · 4 mucho, concentrado · 5 concentración muy alta. Sensibilidad 1 muy baja a 5 muy alta. Capacidad 1 inexistente · 2 débil · 3 parcial · 4 buena · 5 muy buena.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
