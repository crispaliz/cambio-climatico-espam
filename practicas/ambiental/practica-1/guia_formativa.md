# Guía de la evaluación formativa — Capítulo 1 (borrador)

**Cambio Climático · Ingeniería Ambiental · ESPAM MFL** · Guía CC-IAM-C1-F · Versión 1.0 · noviembre de 2026

| | |
|---|---|
| Unidad | Unidad I. El sistema climático y las evidencias del cambio climático |
| Resultado de aprendizaje | **RA A.** Aplicar los fundamentos teóricos del sistema climático para interpretar las causas y evidencias del cambio climático en el territorio. |
| Práctica que la sustenta | Práctica 1 — Diagnóstico del clima observado: cuadernos comunes `CR01` y `CR02`, y cuadernos `IA1_01_climatologia`, `IA1_02_estacion_vs_reanalisis` e `IA1_03_tendencias_enso` (repositorio github.com/crispaliz/cambio-climatico-espam). |
| Producto | Borrador del capítulo 1 «Diagnóstico del clima observado de la provincia»: secciones 1 a 5 y anexo B de la plantilla CC-IAM-C1. |
| Modalidad de trabajo | Individual: una provincia por estudiante (de preferencia de la Costa) o un cantón de ella, la misma zona en los cinco cuadernos. |
| Tipo de evaluación | Formativa (con retroalimentación para el capítulo definitivo). |
| Valor | **2,00 puntos**. |
| Entrega | Al cerrar `IA1_03`, en la fecha y el espacio que el docente habilite en la plataforma virtual. |
| Docente | Ing. Cristian Omar Paliz Acosta, MSc. |

## 1. Propósito de la evaluación

El borrador no busca todavía un texto pulido. Busca comprobar que usted **ejecutó correctamente los cinco cuadernos para su zona** y que **lee bien sus resultados** (con unidades, fuente y significancia) antes de interpretarlos en el capítulo definitivo. Es el primer capítulo del proyecto individual que defenderá en la Unidad IV.

El lector previsto es externo: un técnico de la dirección ambiental del GAD provincial. Cada resultado debe entenderse sin abrir los cuadernos.

El docente devuelve el borrador con **observaciones numeradas (O1, O2, …)**. Usted debe atenderlas en el capítulo definitivo; esa atención se califica en la evaluación sumativa (criterio 7).

## 2. Dónde están los cuadernos y dónde quedan sus resultados

Los cuadernos **no están en su Drive**: se abren desde el repositorio del curso en Google Colab. En su Drive quedan solo los archivos que producen al ejecutarse.

| Paso | Cuaderno (se abre desde GitHub con el botón «Open in Colab») | Carpeta del repositorio | Qué deja en su Drive |
|---|---|---|---|
| C1 | `CR01_descarga_reanalisis` | `practicas/comun/reanalisis` | `Mi unidad/CC_datos/<zona>/`: `era5_*.nc`, `core_*.nc`, `inventario.json` |
| C2 | `CR02_series_zona` | `practicas/comun/reanalisis` | `Mi unidad/CC_datos/<zona>/`: `serie_diaria_<zona>.csv`, `serie_mensual_<zona>.csv` |
| 1 | `IA1_01_climatologia` | `practicas/ambiental/practica-1` | `Mi unidad/CC_Ambiental/practica-1/<zona>/`: `IA1_01_*` |
| 2 | `IA1_02_estacion_vs_reanalisis` | `practicas/ambiental/practica-1` | Misma carpeta: `IA1_02_*` |
| 3 | `IA1_03_tendencias_enso` | `practicas/ambiental/practica-1` | Misma carpeta: `IA1_03_*` |

- Abra cada cuaderno desde github.com/crispaliz/cambio-climatico-espam y use **Archivo › Guardar una copia en Drive**; la copia queda en «Colab Notebooks».
- En la celda 1 de cada cuaderno elija la **misma zona**. En `CR01` deje `MODO_DATOS = "release"` (no necesita cuenta).
- Ejecute las celdas en orden, de principio a fin, y autorice el acceso a Drive cuando se lo pida.

## 3. Qué se entrega

| Elemento | Detalle |
|---|---|
| Archivo | Un PDF generado desde Word. |
| Nombre del archivo | `CC-IAM-C1_borrador_<provincia>_<apellido>.pdf` (ejemplo: `CC-IAM-C1_borrador_manabi_zambrano.pdf`). |
| Portada | Asignatura, título del capítulo, provincia (y cantón si lo eligió), nombre completo y fecha. |
| Contenido | Secciones 1 a 5 de la plantilla con sus figuras y tablas; respuestas a las preguntas de los cuadernos integradas en el texto de cada sección (no como cuestionario aparte); anexo B. |
| Extensión | 4 a 6 páginas sin portada ni anexos; letra de 11 puntos, interlineado 1,15. |
| No se entrega aún | Sección 6 (discusión y conclusiones) y anexo A (bitácora de El Niño). Conviene empezar la bitácora desde ya con el cuaderno común `CB01_bitacora_el_nino`: se califica en la sumativa. |
| Uso de IA | Permitido como apoyo si se declara (herramienta y para qué se usó) al final del documento; los números y su lectura deben ser suyos y verificables en sus archivos. |

## 4. Antes de escribir: verifique su corrida

| Revise | Dónde lo ve | Si no coincide |
|---|---|---|
| La misma zona en los cinco cuadernos | Celda 1 de cada cuaderno y nombre de la carpeta `<zona>` | Vuelva a ejecutar con la zona correcta; no mezcle productos de zonas distintas. |
| Inventario y comprobaciones | `inventario.json` de `CR01` y celdas «Comprobaciones» de `IA1_01` e `IA1_03` | Si una comprobación falla (unidades, años completos), vuelva a ejecutar desde `CR01` o consulte al docente. |
| La estación usada | Línea «Estación usada» de `IA1_02` y la lista de estaciones que imprime | Compare con el anexo de esta guía. Deje `ARCHIVO_ESTACION` vacío para la elección automática. |
| Variables que mide la estación | Líneas «variables» y «Meses válidos» de `IA1_02` | Solo se comparan las variables que la estación mide; las demás preguntas de `IA1_02` no aplican y se dice así en la sección 4. |
| Años completos de la serie | Sección 3 de `IA1_03` | Las tendencias se calculan con años de doce meses; declare el periodo efectivo en la sección 2. |

## 5. Qué se pide en cada sección

Cada sección indica lo que debe contener, las figuras y tablas mínimas, de dónde salen, las preguntas de los cuadernos que se integran y los errores que más se repiten.

### Sección 1. Zona de estudio

**Qué debe contener**

- Ubicación: provincia (y cantón si aplica), región natural, límites y superficie.
- Relieve y rangos de altitud; cuencas y ríos principales.
- Población (INEC, Censo 2022) y actividades económicas principales (agricultura, acuicultura, pesca, industria, turismo).
- Ecosistemas relevantes para el análisis ambiental (manglar, bosque seco, bosque húmedo, páramo, humedales) y áreas protegidas.
- Celdas de ERA5 y CORe que cubren la zona y su peso en el promedio (respuesta a `CR02`, preguntas 1–2).

**Figuras y tablas mínimas**

- Figura 1: mapa de la zona con las celdas de los reanálisis (de `CR01`).
- Tabla 1 (opcional): datos básicos de la zona.

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Mapa de `CR01`; pesos de celdas de `CR02`; INEC; PDOT del GAD; SNAP. | `CR02`, preguntas 1 y 2. | 0,5 a 1 página |

**Errores frecuentes que se observarán**

- Descripción turística, sin relación con el clima ni con el ambiente.
- Datos sin año ni fuente.
- No explicar qué celdas representan la zona.

### Sección 2. Datos y métodos

**Qué debe contener**

- **Reanálisis:** ERA5 y CORe, variables usadas (temperatura media, máxima y mínima; precipitación; humedad específica y relativa; presión; viento) y periodo 1981–2024.
- **Series de zona:** promedio ponderado por la fracción de área de cada celda (`CR02`).
- **Estación:** la que eligió `IA1_02`: nombre, código, red, coordenadas, altitud, variables que mide, meses válidos y limitaciones (relleno Climatol de la lluvia 1964–2018; temperatura de la red INAMHI desde 2022; corrección de altura aplicada o no).
- **Control de calidad:** límites físicos, completitud mensual y criterio de año completo.
- **Periodo de referencia** 1995–2014 (climatología) y base 1991–2020 (anomalías de ENSO).
- **ENSO:** índice usado (ICEN u ONI), temporada y regla de persistencia.
- **Tendencia:** pendiente de Sen y Mann-Kendall corregido por autocorrelación (Yue y Wang, 2004); prueba sin años de El Niño; tendencia según el año de inicio; señal/ruido.

**Figuras y tablas mínimas**

- Tabla 2: fuentes de datos (nombre, variables, resolución o ubicación, periodo, limitaciones).
- Tabla 3: métodos (prueba, para qué, parámetros).

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| `inventario.json` de `CR01`; `IA1_02_metadatos.json`; `IA1_03_metadatos.json`; ficha de la estación en `datos/estaciones/indice_estaciones.csv`. | «Para el informe» de `IA1_02` e `IA1_03`. | 1 página |

**Errores frecuentes que se observarán**

- Declarar la estación sin sus variables o sin sus limitaciones.
- Comparar con la estación variables que no mide.
- No declarar el periodo efectivo de años completos.

**Ejemplo de redacción esperada**

*Se usó la estación Manta Aeropuerto Eloy Alfaro (METAR, 15 m s. n. m.), que mide temperatura, humedad relativa, presión y viento (224 meses válidos en 1981–2024), con la lluvia de la estación INAMHI M0074; la lluvia de 1964–2018 incluye datos rellenados con Climatol (apoyo CHIRPS).*

### Sección 3. Clima de referencia

**Qué debe contener**

- Clima de la zona con los números del resumen: temperatura media, amplitud térmica, lluvia anual y su estacionalidad, humedad y viento predominante.
- Estación lluviosa y seca: meses y contraste de lluvia, temperatura, humedad y viento.
- Comportamiento de la humedad específica frente a la relativa entre estaciones, explicado con la temperatura y el desplazamiento de la ZCIT.
- Diferencias ERA5–CORe por variable como incertidumbre observacional; por qué la presión depende de la resolución.
- Precipitación anual expresada como un rango que incluya a las dos fuentes.

**Figuras y tablas mínimas**

- Climograma comparado (`IA1_01_climograma_*.png`).
- Humedad, presión y viento (`IA1_01_humedad_presion_viento_*.png`).
- Tabla resumen de la climatología (`IA1_01_resumen_*.csv`).
- Tabla de diferencias ERA5–CORe (`IA1_01_diferencias_*.csv`).

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Productos `IA1_01_*`. | `IA1_01`, preguntas 1 a 4. | 1 a 1,5 páginas |

**Errores frecuentes que se observarán**

- Describir la figura sin valores ni unidades.
- Dar un solo valor de lluvia anual cuando las fuentes difieren.
- Confundir humedad relativa con cantidad de vapor.

### Sección 4. Calidad de los datos

**Qué debe contener**

- Variable que reproduce mejor y peor cada reanálisis, con sesgo, RMSE y r, **solo para las variables que mide la estación**.
- Parte del sesgo de temperatura (y de presión, si la estación la mide) que explica la diferencia de altura entre la estación y el terreno del modelo.
- Cambio del sesgo de la lluvia (y de la humedad, si se mide) entre la estación lluviosa y la seca.
- Si la estación mide viento: coincidencia de la dirección predominante y por qué la velocidad medida suele ser menor.
- Si hay datos diarios: porcentaje de días de lluvia que acierta cada reanálisis y su implicación para los índices de extremos.
- Conclusión: qué tan confiables son los reanálisis en su zona y para qué variables.

**Figuras y tablas mínimas**

- Ciclo anual estación–reanálisis (`IA1_02_ciclo_anual.png`).
- Tabla de métricas mensuales (`IA1_02_metricas_mensuales.csv`).
- Métricas diarias (`IA1_02_metricas_diarias.csv`), si aplica.

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Productos `IA1_02_*`. | `IA1_02`, preguntas 1 a 5 (las que aplican según su estación; ver anexo). | 1 página |

**Errores frecuentes que se observarán**

- Reportar métricas sin unidades o sin decir con cuántos meses se calcularon.
- Concluir que un reanálisis «es malo» sin distinguir sesgo de correlación.
- Responder preguntas de variables que la estación no mide.

### Sección 5. Tendencias y variabilidad natural

**Qué debe contener**

- Tendencia de la temperatura media por década, significancia corregida, comparación con la prueba clásica y papel de r1.
- Tendencias de máximas y mínimas y su efecto en el rango diario de temperatura.
- Tendencia de la precipitación anual frente a su variabilidad entre años.
- Robustez: tendencia sin años de El Niño y según el año de inicio; variable más robusta y más frágil.
- Compuestos por fase de ENSO: meses y magnitud de los cambios en lluvia y temperatura en El Niño y La Niña, con significancia.
- Relación señal/ruido: si el calentamiento ya emergió de la variabilidad natural (lectura en borrador; la conclusión calibrada va en la sección 6).

**Figuras y tablas mínimas**

- Tendencias (`IA1_03_tendencias_*.png`) y su tabla (`IA1_03_tendencias_*.csv`).
- Sensibilidad al año de inicio (`IA1_03_sensibilidad_inicio_*.png`).
- Sensibilidad sin El Niño (`IA1_03_sensibilidad_el_nino_*.csv`).
- Compuestos de ENSO (`IA1_03_compuestos_enso_*.png`).
- Señal/ruido (`IA1_03_senal_ruido_*.csv`).

| Insumos | Preguntas que integra | Extensión orientativa |
|---|---|---|
| Productos `IA1_03_*`. | `IA1_03`, preguntas 1 a 6. | 1,5 a 2 páginas |

**Errores frecuentes que se observarán**

- Pendiente sin unidad (°C/década, mm/década o %/década) o sin significancia.
- Llamar «tendencia» a una pendiente no significativa, o concluir «no hay cambio» por no ser significativa.
- Tomar un año extremo (1983, 1998) como prueba de tendencia.

**Ejemplo de redacción esperada**

*(Valores ilustrativos) La temperatura media de la zona aumentó 0,15 °C por década en 1981–2024 según ERA5 (p corregido = 0,02; r1 = 0,41). La prueba clásica daba p = 0,001: la autocorrelación exageraba la significancia.*

### Anexo B. Reproducibilidad

- Enlace (con permiso de lectura para el docente) a sus copias de los cinco cuadernos en Drive.
- Lista de los archivos producidos por `IA1_01`, `IA1_02` e `IA1_03`.
- Declaración de uso de herramientas de IA, si las usó.

## 6. Reglas de forma

- Cada figura y tabla lleva número, título, fuente y «Elaboración propia», y se cita en el texto antes de aparecer.
- Todo número va con su unidad y su fuente (ERA5, CORe o estación). Si las fuentes difieren, se da el rango.
- Tendencia y variabilidad no se mezclan: un año extremo no es una tendencia, y una tendencia no significativa no prueba que no haya cambio.
- Citas y referencias en APA 7.ª edición; las de los datos están al final de cada cuaderno.
- Los números del documento deben coincidir con los archivos de su Drive.

## 7. Rúbrica de evaluación (2,00 puntos)

Cinco criterios de **0,40 puntos** cada uno, con cinco niveles. Se asigna un solo nivel por criterio; la nota es la suma de los cinco.

| Criterio e indicadores | Logrado · 0,40 | Suficiente · 0,30 | En proceso · 0,20 | Inicial · 0,10 | No presenta · 0,00 |
|---|---|---|---|---|---|
| **C1. Zona de estudio, datos y métodos (secciones 1 y 2)**<br>Indicadores: mapa con celdas; zona descrita con relieve, población, actividades y ecosistemas; estación con variables y limitaciones; control de calidad; periodos y métodos. | Cumple todos los indicadores: mapa con celdas y su peso; zona con relieve, población, actividades y ecosistemas con fuente; estación con nombre, código, red, variables y limitaciones; control de calidad, periodos y métodos iguales a los del cuaderno. | Cumple casi todo, con uno o dos elementos incompletos. | Falta el mapa o la declaración de la estación, o los periodos y métodos no corresponden. | Descripción genérica, sin los datos ni los métodos de la práctica. | No presenta las secciones 1 y 2. |
| **C2. Clima de referencia (sección 3)**<br>Indicadores: clima cuantificado; estaciones lluviosa y seca; humedad específica y relativa explicadas; diferencias ERA5–CORe; lluvia como rango. | Clima descrito con los números del resumen (°C, mm, %, m/s); estaciones lluviosa y seca contrastadas; comportamiento de las dos humedades explicado con la temperatura y la ZCIT; diferencias ERA5–CORe leídas como incertidumbre; lluvia anual como rango. | Correcto, con una o dos preguntas sin números de la zona. | Figuras mal leídas en un aspecto central (por ejemplo, confunde humedad relativa con vapor). | Solo figuras, sin lectura. | No presenta la sección. |
| **C3. Calidad de los datos (sección 4)**<br>Indicadores: métricas por variable medida; efecto de la altura; estacionalidad del sesgo; viento y días de lluvia si aplica; conclusión de confiabilidad. | Sesgo, RMSE y r por variable medida con unidades; efecto de la altura cuantificado; cambio del sesgo entre estaciones; viento y aciertos diarios si aplican; conclusión clara de qué tan confiable es cada reanálisis. | Correcto, con una omisión. | Métricas sin interpretación o variables no medidas comparadas. | Solo la tabla de métricas. | No presenta la sección. |
| **C4. Tendencias y variabilidad natural (sección 5)**<br>Indicadores: tendencias con unidad y significancia corregida; r1; máximas y mínimas; robustez; compuestos ENSO; señal/ruido. | Tendencias por década con unidad y significancia corregida, comparadas con la prueba clásica (r1); máximas, mínimas y rango diario; tendencia sin El Niño y según el inicio; compuestos con meses y significancia; señal/ruido leída. | Correcto en lo esencial, con una omisión. | Tendencias sin significancia o no significativas presentadas como cambio. | Valores copiados sin interpretación. | No presenta la sección. |
| **C5. Forma y reproducibilidad**<br>Indicadores: figuras y tablas completas; respuestas integradas; APA 7; anexo B; coincidencia con el Drive; extensión. | Figuras y tablas numeradas con título, fuente y unidad, citadas antes de aparecer; respuestas integradas; APA 7 correcto; anexo B completo; números coinciden con el Drive; extensión dentro de lo pedido. | Uno o dos elementos de forma ausentes. | Varias figuras sin unidad o fuente, o anexo B incompleto. | Documento desordenado; no se puede rastrear el origen de los números. | Sin anexo B y sin formato mínimo. |

### Condiciones de entrega

- Entregas fuera de plazo: solo con la justificación que establece el reglamento de evaluación estudiantil.
- Plagio (de un compañero, de semestres anteriores o de fuentes no citadas): la calificación es 0, según las políticas de la asignatura.
- Productos de una zona distinta a la declarada: el criterio afectado se califica como «Inicial».

### Hoja de calificación

Estudiante: ______________________________   Provincia/cantón: ____________________   Fecha: ____________

| Criterio | Puntaje máximo | Nivel asignado | Puntaje obtenido | Observaciones (O1, O2, …) |
|---|---|---|---|---|
| C1. Zona de estudio, datos y métodos | 0,40 |  |  |  |
| C2. Clima de referencia | 0,40 |  |  |  |
| C3. Calidad de los datos | 0,40 |  |  |  |
| C4. Tendencias y variabilidad natural | 0,40 |  |  |  |
| C5. Forma y reproducibilidad | 0,40 |  |  |  |
| **Total** | **2,00** |  |  |  |

## 8. Retroalimentación

El docente devuelve el borrador con observaciones numeradas por sección (O1, O2, …) en la hoja de calificación o como comentarios en el PDF. Usted responde cada una en el **anexo C** del capítulo definitivo (matriz de atención a observaciones, explicada en la guía sumativa).

## Anexo. Su provincia en los datos del curso

Estación que `IA1_02` elige para la **provincia completa** con `ARCHIVO_ESTACION` vacío (repositorio a noviembre de 2026), sus meses válidos en 1981–2024 (máximo 528) y las preguntas de `IA1_02` que se pueden responder con ella. Si eligió un cantón, la estación puede ser otra: use la que imprime su cuaderno.

| Provincia | Estación que elige IA1_02 | Meses válidos 1981–2024 | Preguntas de IA1_02 que aplican | Observación |
|---|---|---|---|---|
| Azuay | Mariscal Lamar · 2531 m · `synop/azuay_mariscal_lamar_84239.csv` | Tmáx 152 · Tmín 133 · lluvia 456 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Bolívar | Chillanes · 2330 m · `synop/bolivar_chillanes_84189.csv` | Tmáx 1 · Tmín 0 · lluvia 456 | 1, 3 (lluvia), 5 | sin temperatura: se compara solo la lluvia |
| Carchi | San Gabriel · 2860 m · `synop/carchi_san_gabriel_84036.csv` | Tmáx 124 · Tmín 97 · lluvia 473 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Cañar | Cañar · 3083 m · `synop/canar_canar_84226.csv` | Tmáx 126 · Tmín 41 · lluvia 456 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Chimborazo | Chimborazo · 2740 m · `synop/chimborazo_chimborazo_84176.csv` | Tmáx 27 · Tmín 36 · lluvia 456 | 1, 2 (temperatura), 3 (lluvia), 5 | temperatura de menos de 5 años: su comparación es indicativa |
| Cotopaxi | Rumipamba · 2628 m · `synop/cotopaxi_rumipamba_84143.csv` | Tmáx 144 · Tmín 89 · lluvia 478 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| El Oro (Costa) | Santa Rosa Aeropuerto · 7 m · `synop/el_oro_santa_rosa_aeropuerto_84252.csv` | Tmáx 92 · Tmín 69 · lluvia 3 | 1, 2 (temperatura) | sin lluvia en la estación; puede escribir una estación INAMHI de solo lluvia de la lista |
| Esmeraldas (Costa) | La Concordia · 360 m · `synop/esmeraldas_la_concordia_84050.csv` | Tmáx 181 · Tmín 134 · lluvia 491 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Galápagos | Baltra · `redes/galapagos_baltra_84001.csv` | Tmáx 30 · Tmín 28 | 1, 2 (temperatura) | solo 30 meses de temperatura (red INAMHI 2022–2024) y sin lluvia: la comparación es indicativa |
| Guayas (Costa) | José Joaquín de Olmedo (Guayaquil) · 5 m · `synop/guayas_simon_bolivar_intl_jose_joaqui_84203.csv` | Tmáx 151 · Tmín 132 · lluvia 456 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Imbabura | Inguincho · 3140 m · `synop/imbabura_inguincho_84045.csv` | Tmáx 67 · Tmín 8 · lluvia 473 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Loja | Loja/La Argelia · 2160 m · `synop/loja_loja_la_argelia_84270.csv` | Tmáx 131 · Tmín 86 · lluvia 476 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Los Ríos (Costa) | Pichilingue · 120 m · `synop/los_rios_pichilingue_84140.csv` | Tmáx 145 · Tmín 98 · lluvia 486 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Manabí (Costa) | Manta Aeropuerto Eloy Alfaro (METAR) · 15 m · `manabi_manta_aeropuerto_semt_metar.csv` | Tmáx 224 · Tmín 224 · Tmed 224 · lluvia 456 · humedad relativa, presión y viento (≈224) | 1, 2 (temperatura y presión), 3 (lluvia y humedad), 4, 5 | alternativa: `manabi_calceta_espam.csv` (ESPAM, con humedad relativa y viento) |
| Morona Santiago | Coronel Edmundo Carvajal · 1052 m · `synop/morona_santiago_coronel_edmundo_carvajal_84217.csv` | Tmáx 57 · Tmín 86 · lluvia 456 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Napo | Baeza · 1960 m · `inamhi/napo/m0215.csv` | lluvia 456 | 1, 3 (lluvia), 5 | sin temperatura: se compara solo la lluvia |
| Orellana | Nuevo Rocafuerte · 265 m · `synop/orellana_nuevo_rocafuerte_84132.csv` | Tmáx 123 · Tmín 86 · lluvia 456 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Pastaza | Puyo · 960 m · `synop/pastaza_puyo_84179.csv` | Tmáx 107 · Tmín 61 · lluvia 468 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Pichincha | Izobamba · 3058 m · `synop/pichincha_izobamba_84088.csv` | Tmáx 177 · Tmín 134 · lluvia 506 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Santa Elena (Costa) | General Ulpiano Paez · 5 m · `synop/santa_elena_general_ulpiano_paez_84200.csv` | Tmáx 91 · Tmín 89 · lluvia 456 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Santo Domingo de los Tsáchilas (Costa) | Puerto Ila · 319 m · `synop/santo_domingo_de_los_tsachilas_puerto_ila_84105.csv` | Tmáx 116 · Tmín 71 · lluvia 489 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Sucumbíos | Nueva Loja Aeropuerto · 297 m · `synop/sucumbios_nueva_loja_aeropuer_84063.csv` | Tmáx 66 · Tmín 91 · lluvia 41 | 1, 2 (temperatura), 3 (lluvia), 5 | lluvia de solo 41 meses; puede escribir una estación INAMHI de solo lluvia de la lista |
| Tungurahua | Querochaca · 2910 m · `synop/tungurahua_querochaca_84160.csv` | Tmáx 142 · Tmín 95 · lluvia 470 | 1, 2 (temperatura), 3 (lluvia), 5 | — |
| Zamora Chinchipe | Zamora · 970 m · `inamhi/zamora_chinchipe/m0207.csv` | lluvia 456 | 1, 3 (lluvia), 5 | sin temperatura: se compara solo la lluvia |

- Casi todas las estaciones miden solo temperatura máxima, mínima y lluvia: las preguntas sobre humedad, presión y viento de `IA1_02` solo aplican en Manabí (Manta o Calceta).
- Con pocos años de temperatura, la comparación sirve para estimar el sesgo de los reanálisis, no para tendencias.
- Las tendencias de la sección 5 se calculan con las series de zona de ERA5 y CORe, no con la estación.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
