# Guía de la evaluación sumativa — Capítulo 1 (definitivo y exposición)

**Cambio Climático · Ingeniería Ambiental · ESPAM MFL** · Guía CC-IAM-C1-S · Versión 1.0 · noviembre de 2026

| | |
|---|---|
| Unidad | Unidad I. El sistema climático y las evidencias del cambio climático |
| Resultado de aprendizaje | **RA A.** Aplicar los fundamentos teóricos del sistema climático para interpretar las causas y evidencias del cambio climático en el territorio. |
| Práctica que la sustenta | Práctica 1 — Diagnóstico del clima observado: cuadernos comunes `CR01` y `CR02`, y cuadernos `IA1_01_climatologia`, `IA1_02_estacion_vs_reanalisis` e `IA1_03_tendencias_enso` (repositorio github.com/crispaliz/cambio-climatico-espam). |
| Técnica de evaluación | Estudio de casos: la provincia (o el cantón) de cada estudiante. |
| Productos | 1) Capítulo 1 definitivo «Diagnóstico del clima observado de la provincia» (secciones 1 a 6 y anexos A, B y C). 2) Exposición oral del capítulo. |
| Modalidad de trabajo | Individual: una provincia por estudiante (de preferencia de la Costa) o un cantón de ella, la misma zona en los cinco cuadernos. |
| Tipo de evaluación | Sumativa. |
| Valor | **8,00 puntos**. |
| Entrega | Documento y diapositivas antes de la sesión de la sumativa de la Unidad I, en la plataforma virtual; exposición en esa sesión. |
| Docente | Ing. Cristian Omar Paliz Acosta, MSc. |

## 1. Propósito de la evaluación

El borrador comprobó que los resultados estuvieran bien obtenidos y leídos. El capítulo definitivo **interpreta**: explica las causas físicas de lo observado, separa la señal de cambio climático de la variabilidad natural (en especial ENSO), dice qué tan confiables son los datos de la zona y formula una conclusión calibrada que se compara con la evidencia global del AR6. Cierra señalando qué variables y meses son relevantes para los sistemas ambientales de la provincia, que es el puente hacia la evaluación de impactos de las unidades siguientes.

Además, se verifica que usted **atendió cada observación** del borrador y que **domina su trabajo**, lo que se comprueba en la exposición oral.

## 2. Qué se entrega

| Entregable | Formato y extensión | Nombre del archivo |
|---|---|---|
| Capítulo 1 definitivo: secciones 1 a 6 y anexos A, B y C | PDF generado desde Word; 8 a 12 páginas sin portada ni anexos; letra de 11 puntos, interlineado 1,15 | `CC-IAM-C1_final_<provincia>_<apellido>.pdf` |
| Diapositivas de la exposición | PDF; 6 a 10 diapositivas | `CC-IAM-C1_exposicion_<provincia>_<apellido>.pdf` |

Las secciones 1 a 5 son las del borrador, **corregidas con la retroalimentación** y llevadas de la lectura de resultados a su interpretación. Lo nuevo es la sección 6 y los anexos A y C. El uso de IA se declara al final del documento.

## 3. Qué se pide en cada sección

### Sección 1. Zona de estudio

**Qué debe contener**

- Ubicación: provincia (y cantón si aplica), región natural, límites y superficie.
- Relieve y rangos de altitud; cuencas y ríos principales.
- Población (INEC, Censo 2022) y actividades económicas principales (agricultura, acuicultura, pesca, industria, turismo).
- Ecosistemas relevantes para el análisis ambiental (manglar, bosque seco, bosque húmedo, páramo, humedales) y áreas protegidas.
- Celdas de ERA5 y CORe que cubren la zona y su peso en el promedio (respuesta a `CR02`, preguntas 1–2).

**Qué se agrega respecto del borrador**

- Caracterización orientada al análisis ambiental: qué ecosistemas, recursos hídricos y actividades de la zona dependen más del clima.

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Mapa de `CR01`; pesos de celdas de `CR02`; INEC; PDOT del GAD; SNAP. | `CR02`, preguntas 1 y 2. | 1 página |

### Sección 2. Datos y métodos

**Qué debe contener**

- **Reanálisis:** ERA5 y CORe, variables usadas (temperatura media, máxima y mínima; precipitación; humedad específica y relativa; presión; viento) y periodo 1981–2024.
- **Series de zona:** promedio ponderado por la fracción de área de cada celda (`CR02`).
- **Estación:** la que eligió `IA1_02`: nombre, código, red, coordenadas, altitud, variables que mide, meses válidos y limitaciones (relleno Climatol de la lluvia 1964–2018; temperatura de la red INAMHI desde 2022; corrección de altura aplicada o no).
- **Control de calidad:** límites físicos, completitud mensual y criterio de año completo.
- **Periodo de referencia** 1995–2014 (climatología) y base 1991–2020 (anomalías de ENSO).
- **ENSO:** índice usado (ICEN u ONI), temporada y regla de persistencia.
- **Tendencia:** pendiente de Sen y Mann-Kendall corregido por autocorrelación (Yue y Wang, 2004); prueba sin años de El Niño; tendencia según el año de inicio; señal/ruido.

**Qué se agrega respecto del borrador**

- Limitaciones explicadas en sus consecuencias: qué conclusiones no se pueden sacar por falta de una variable en la estación, por la resolución de los reanálisis o por el periodo disponible.

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| `inventario.json` de `CR01`; `IA1_02_metadatos.json`; `IA1_03_metadatos.json`; ficha de la estación en `datos/estaciones/indice_estaciones.csv`. | «Para el informe» de `IA1_02` e `IA1_03`. | 1 a 1,5 páginas |

### Sección 3. Clima de referencia

**Qué debe contener**

- Clima de la zona con los números del resumen: temperatura media, amplitud térmica, lluvia anual y su estacionalidad, humedad y viento predominante.
- Estación lluviosa y seca: meses y contraste de lluvia, temperatura, humedad y viento.
- Comportamiento de la humedad específica frente a la relativa entre estaciones, explicado con la temperatura y el desplazamiento de la ZCIT.
- Diferencias ERA5–CORe por variable como incertidumbre observacional; por qué la presión depende de la resolución.
- Precipitación anual expresada como un rango que incluya a las dos fuentes.

**Qué se agrega respecto del borrador**

- Explicación física de la estacionalidad: desplazamiento de la ZCIT, corrientes marinas frente a la costa (Humboldt y masas de agua cálida), orografía.
- Lectura de la incertidumbre observacional como parte del resultado, no como defecto.

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Productos `IA1_01_*`. | `IA1_01`, preguntas 1 a 4. | 1,5 páginas |

### Sección 4. Calidad de los datos

**Qué debe contener**

- Variable que reproduce mejor y peor cada reanálisis, con sesgo, RMSE y r, **solo para las variables que mide la estación**.
- Parte del sesgo de temperatura (y de presión, si la estación la mide) que explica la diferencia de altura entre la estación y el terreno del modelo.
- Cambio del sesgo de la lluvia (y de la humedad, si se mide) entre la estación lluviosa y la seca.
- Si la estación mide viento: coincidencia de la dirección predominante y por qué la velocidad medida suele ser menor.
- Si hay datos diarios: porcentaje de días de lluvia que acierta cada reanálisis y su implicación para los índices de extremos.
- Conclusión: qué tan confiables son los reanálisis en su zona y para qué variables.

**Qué se agrega respecto del borrador**

- Explicación de las causas de los sesgos (altura, resolución, representatividad del punto, definición del día, relleno de la serie) y de qué reanálisis conviene usar en las unidades siguientes.

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Productos `IA1_02_*`. | `IA1_02`, preguntas 1 a 5 (las que aplican según su estación; ver anexo). | 1 a 1,5 páginas |

### Sección 5. Tendencias y variabilidad natural

**Qué debe contener**

- Tendencia de la temperatura media por década, significancia corregida, comparación con la prueba clásica y papel de r1.
- Tendencias de máximas y mínimas y su efecto en el rango diario de temperatura.
- Tendencia de la precipitación anual frente a su variabilidad entre años.
- Robustez: tendencia sin años de El Niño y según el año de inicio; variable más robusta y más frágil.
- Compuestos por fase de ENSO: meses y magnitud de los cambios en lluvia y temperatura en El Niño y La Niña, con significancia.
- Relación señal/ruido: si el calentamiento ya emergió de la variabilidad natural (lectura en borrador; la conclusión calibrada va en la sección 6).

**Qué se agrega respecto del borrador**

- Discusión de por qué difieren ERA5 y CORe en las tendencias, si difieren.
- Lectura conjunta de tendencia, robustez y ENSO: qué pesa más en cada variable.

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Productos `IA1_03_*`. | `IA1_03`, preguntas 1 a 6. | 2 páginas |

### Sección 6. Discusión y conclusiones (nueva)

Es la sección que más pesa en la interpretación. Se organiza en cuatro apartados.

**Qué debe contener**

- **6.1 Cambio climático frente a variabilidad natural.** Qué parte de lo observado es tendencia de largo plazo y qué parte variabilidad de ENSO, usando sus resultados: tendencia con y sin El Niño, según el año de inicio, compuestos y señal/ruido.
- **6.2 Causas físicas.** Balance de energía del sistema climático y forzamiento radiativo de los gases de efecto invernadero; retroalimentación del vapor de agua y relación de Clausius-Clapeyron; mecanismo de ENSO para la variabilidad.
- **6.3 Comparación con el AR6.** Su calentamiento por década frente al calentamiento global que reporta el IPCC (AR6, Grupo de Trabajo I, Resumen para responsables de políticas) y lo que dice sobre la región; coincidencias y diferencias, y por qué.
- **6.4 Conclusiones, limitaciones e implicaciones ambientales.** Conclusión en la escala calibrada del IPCC (probable, muy probable; confianza baja, media, alta) justificada por el acuerdo entre fuentes y la robustez de las pruebas; limitaciones de los datos; variables, meses y fases de ENSO más relevantes para los recursos hídricos, los ecosistemas y las actividades de la zona.

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Lectura guiada del balance de energía; clase de detección y atribución; IPCC AR6 GTI (SPM); resultados de las secciones 3 a 5. | `IA1_03`, pregunta 6, y síntesis. | 2 a 3 páginas |

*Ejemplo de conclusión calibrada (valores ilustrativos): «Es muy probable (confianza alta) que la temperatura media de la zona haya aumentado desde 1981: ERA5 y CORe coinciden en una pendiente significativa de 0,15–0,20 °C por década que se mantiene sin los años de El Niño. Para la lluvia anual no se detecta tendencia: su variabilidad está dominada por ENSO».*

### Anexos

| Anexo | Qué debe contener |
|---|---|
| **A. Bitácora de El Niño 2026–2027** | Al menos una entrada semanal desde octubre: fecha, ICEN y ONI vigentes, comunicado del ENFEN o de NOAA, lo observado en su zona y una línea de lectura propia. Marcada como información preliminar, separada del análisis climatológico. Se lleva con el cuaderno común `CB01_bitacora_el_nino` (`practicas/comun/bitacora/`), que llena los índices y los incidentes del ECU 911; se entrega el archivo `bitacora_el_nino_<zona>.xlsx` resumido en una tabla. |
| **B. Reproducibilidad** | Enlaces a sus copias de los cuadernos en Drive, lista de archivos producidos y declaración de uso de IA. |
| **C. Atención a observaciones** | Matriz con cada observación del borrador (O1, O2, …): qué se cambió y dónde (sección y página). Ver el apartado 4. |

## 4. Atención a las observaciones del borrador (anexo C)

Cada observación del docente se responde en una fila. El cambio debe poder verificarse en la página indicada.

| N.º | Observación del docente | Qué se cambió | Dónde |
|---|---|---|---|
| O1 | La tendencia se reporta sin significancia corregida | Se añadió el valor p corregido, r1 y la comparación con la prueba clásica; la conclusión pasó de «aumentó» a «muy probablemente aumentó» | 5.1, p. 7 |
| O2 | Se comparan con la estación variables que no mide | Se eliminaron humedad y viento de la sección 4; se aclara que la estación mide solo Tmáx, Tmín y lluvia | 4, p. 6 |
| O3 | … | … | … |

- Si no está de acuerdo con una observación, indíquelo en la fila y argumente con sus datos; una discrepancia bien sustentada cuenta como atendida.
- Si no entregó el borrador, no tiene observaciones que atender y el criterio 7 vale 0.

## 5. Exposición oral

| Aspecto | Regla |
|---|---|
| Duración | 8 minutos de exposición y 4 minutos de preguntas por estudiante. |
| Estructura sugerida | Zona y datos (1 min) · clima de referencia (1,5 min) · calidad de los datos (1,5 min) · tendencias y ENSO (2 min) · conclusión calibrada e implicaciones ambientales (2 min). |
| Diapositivas | Figuras del capítulo con unidad y fuente legibles; poco texto; una idea o conclusión por diapositiva. |
| Público | Se expone como ante la dirección ambiental del GAD: cómo es el clima de la provincia, qué cambió, con qué confianza y qué importa para el ambiente. |
| Preguntas tipo | ¿Por qué esa tendencia no es solo efecto de El Niño? · ¿Qué reanálisis usaría en su zona y por qué? · ¿Por qué la humedad relativa baja si la específica no cambia? · ¿Qué limitación de sus datos cambia más su conclusión? |

## 6. Rúbrica de evaluación (8,00 puntos)

Ocho criterios de **1,00 punto** cada uno, con cinco niveles. Se asigna un solo nivel por criterio; la nota es la suma de los ocho.

| Criterio e indicadores | Logrado · 1,00 | Suficiente · 0,75 | En proceso · 0,50 | Inicial · 0,25 | No presenta · 0,00 |
|---|---|---|---|---|---|
| **C1. Zona de estudio, datos y métodos (secciones 1 y 2)**<br>Indicadores: zona orientada al análisis ambiental; estación, reanálisis, control de calidad, periodos y métodos; limitaciones y sus consecuencias. | Zona caracterizada con relieve, población, actividades y ecosistemas dependientes del clima; estación, reanálisis, control de calidad, periodos y métodos declarados; limitaciones explicadas con sus consecuencias. | Completo, con una limitación sin declarar o sin su consecuencia. | Falta la declaración de la estación o de los periodos, o la zona no se vincula con el ambiente. | Descripción genérica, sin la información de la práctica. | No presenta las secciones. |
| **C2. Clima de referencia e incertidumbre observacional (sección 3)**<br>Indicadores: clima cuantificado; estacionalidad explicada físicamente; humedades; diferencias ERA5–CORe como incertidumbre. | Clima cuantificado; estacionalidad explicada con la ZCIT, las corrientes marinas y la orografía; comportamiento de las dos humedades explicado; diferencias ERA5–CORe usadas como incertidumbre y lluvia anual como rango. | Resultados correctos con explicación física parcial. | Describe las figuras sin explicar los mecanismos. | Solo figuras. | No presenta la sección. |
| **C3. Calidad de los datos (sección 4)**<br>Indicadores: métricas por variable medida; causas de los sesgos; recomendación de uso. | Métricas por variable medida con unidades; causas de los sesgos explicadas (altura, resolución, representatividad, definición del día, relleno); recomendación argumentada del reanálisis a usar. | Correcto, con una explicación débil. | Métricas sin causas o variables no medidas comparadas. | Solo la tabla. | No presenta la sección. |
| **C4. Tendencias y variabilidad natural (sección 5)**<br>Indicadores: tendencias con significancia corregida; robustez; compuestos ENSO; señal/ruido; concordancia entre fuentes. | Tendencias con unidad, significancia corregida y r1; máximas, mínimas y rango diario; robustez sin El Niño y según el inicio; compuestos con significancia; señal/ruido; concordancia entre ERA5 y CORe discutida. | Correcto, con una omisión. | Tendencias sin significancia o no significativas presentadas como cambio. | Valores sin interpretación. | No presenta la sección. |
| **C5. Cambio climático frente a variabilidad natural y causas (6.1 a 6.3)**<br>Indicadores: separación de señales con resultados propios; causas físicas; comparación con el AR6. | Separa explícitamente la señal de cambio de la de ENSO con sus resultados; explica las causas con balance de energía, forzamiento radiativo y Clausius-Clapeyron; compara con el AR6 citándolo. | Separa las señales con explicación física incompleta o sin el AR6. | Atribuye al cambio climático lo que sus datos muestran como variabilidad de ENSO, o al revés. | Afirmaciones generales sin vínculo con sus resultados. | No presenta la discusión. |
| **C6. Conclusiones, implicaciones ambientales y anexos A y B (6.4)**<br>Indicadores: lenguaje calibrado justificado; limitaciones; implicaciones ambientales; bitácora; reproducibilidad. | Conclusión con escala calibrada del IPCC justificada; limitaciones explícitas; variables, meses y fases de ENSO relevantes para el ambiente de la zona; bitácora con entradas semanales desde octubre; anexo B completo. | Completo, con lenguaje calibrado sin justificar o bitácora con semanas faltantes. | Sin implicaciones ambientales o sin bitácora. | Conclusiones que repiten resultados. | No presenta conclusiones. |
| **C7. Corrección de observaciones del borrador (anexo C)**<br>Indicadores: matriz completa; cambios verificables; discrepancias argumentadas. | Todas las observaciones respondidas en la matriz, con el cambio y su ubicación verificables en el texto, o discrepancias argumentadas con datos. | El 75 % o más atendidas y verificables. | Al menos la mitad atendidas. | Menos de la mitad, o matriz sin cambios verificables. | Sin matriz, o sin borrador previo. |
| **C8. Exposición oral**<br>Indicadores: dominio; tiempo; apoyo visual; respuestas con datos de su zona; lenguaje calibrado. | Expone con dominio y sin leer; respeta el tiempo; figuras legibles con unidad y fuente; responde las preguntas con los números de su zona y explica el porqué; usa lenguaje calibrado. | Buen dominio, con alguna respuesta incompleta o leve exceso de tiempo. | Lee las diapositivas o responde de forma general. | Sin dominio; no responde las preguntas. | No se presenta a la exposición. |

### Condiciones de entrega

- Entregas fuera de plazo: solo con la justificación que establece el reglamento de evaluación estudiantil.
- Plagio (de un compañero, de semestres anteriores o de fuentes no citadas): la calificación es 0, según las políticas de la asignatura.
- Números que no corresponden a los productos de los cuadernos de la zona declarada: el criterio afectado se califica como «Inicial».
- Uso de IA no declarado o resultados que el estudiante no puede explicar en la exposición: se aplican las políticas de la asignatura.

### Hoja de calificación

Estudiante: ______________________________   Provincia/cantón: ____________________   Fecha: ____________

| Criterio | Máximo | Nivel asignado | Puntaje obtenido | Observaciones |
|---|---|---|---|---|
| C1. Zona de estudio, datos y métodos | 1,00 |  |  |  |
| C2. Clima de referencia e incertidumbre observacional | 1,00 |  |  |  |
| C3. Calidad de los datos | 1,00 |  |  |  |
| C4. Tendencias y variabilidad natural | 1,00 |  |  |  |
| C5. Cambio climático frente a variabilidad y causas | 1,00 |  |  |  |
| C6. Conclusiones, implicaciones ambientales y anexos | 1,00 |  |  |  |
| C7. Corrección de observaciones del borrador | 1,00 |  |  |  |
| C8. Exposición oral | 1,00 |  |  |  |
| **Total** | **8,00** |  |  |  |

## 7. Qué discutir según la región de su provincia

Lo que se conoce de cada región es un punto de partida. **Contrástelo con sus propios resultados** y explique si coincide o no. La estación de su provincia está en el anexo de la guía formativa.

| Región | Provincias | Puntos de partida para la discusión |
|---|---|---|
| Costa | Esmeraldas, Manabí, Santa Elena, Guayas, Los Ríos, El Oro, Santo Domingo de los Tsáchilas | Estación lluviosa de diciembre a mayo y seca el resto del año, con un gradiente norte–sur (Esmeraldas húmeda, Santa Elena árida). El Niño costero aumenta mucho la lluvia; el ICEN suele explicarla mejor que el ONI. La humedad relativa alta en la estación seca con poca lluvia se relaciona con las aguas frías de la corriente de Humboldt. Las tendencias de lluvia pueden depender de 1982–83 y 1997–98: pruebe quitarlos. |
| Sierra | Carchi, Imbabura, Pichincha, Cotopaxi, Tungurahua, Bolívar, Chimborazo, Cañar, Azuay, Loja | Régimen bimodal en muchas zonas y amplitud térmica diaria grande; señal de ENSO más débil y distinta según la vertiente. La escala de los reanálisis no resuelve los valles: discuta la diferencia entre la estación y las celdas. |
| Amazonía | Sucumbíos, Napo, Orellana, Pastaza, Morona Santiago, Zamora Chinchipe | Lluvia alta todo el año, humedad casi constante y señal de ENSO débil; pocas estaciones con temperatura. Discuta la representatividad de la estación y la incertidumbre de los reanálisis. |
| Galápagos | Galápagos | Estación cálida y lluviosa (enero–mayo) y estación fría con garúa; señal de El Niño muy fuerte. Sin lluvia de estación: el capítulo se apoya en ERA5 y CORe y lo declara. |

### Antes de entregar

- Revise la lista de verificación de la plantilla del capítulo (columna «Definitivo»).
- Verifique que cada observación del borrador tenga su fila en el anexo C.
- Ensaye la exposición con cronómetro.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
