# Capítulo 1 — Diagnóstico del clima observado de la provincia

**Cambio Climático · Ingeniería Ambiental · ESPAM MFL** · Plantilla CC-IAM-C1 · Versión 1.1 · noviembre de 2026

Evidencia el **RA A** de la Unidad I: aplicar los fundamentos del sistema climático para interpretar las causas y evidencias del cambio climático en su zona. Es el primer capítulo del proyecto individual que se defiende en la Unidad IV, así que se escribe para un lector externo (un técnico del GAD provincial), no para el docente.

## Dos entregas, un mismo documento

| | Borrador (formativa, 2 pts) · [guía y rúbrica](guia_formativa.md) | Capítulo definitivo (sumativa, 8 pts, estudio de casos) · [guía y rúbrica](guia_sumativa.md) |
|---|---|---|
| Cuándo | Al cerrar el paso 3 (`IA1_03`) | Sesión de la sumativa de la Unidad I |
| Qué se entrega | Secciones 1 a 5 con figuras, tablas y respuestas en borrador | El capítulo completo, corregido con la retroalimentación, más la sección 6, los anexos A y C y la exposición oral |
| Qué se revisa | Que los resultados estén completos, bien leídos, con unidades y fuente, y que la estación se compare solo en las variables que mide | Que la interpretación sea correcta: causas, evidencias y variabilidad natural distinguidas, con lenguaje calibrado y fuentes |
| Extensión orientativa | 4–6 páginas | 8–12 páginas más anexos |

## Estructura y de dónde sale cada parte

Los cuadernos no están en Drive: se abren desde este repositorio con el botón «Open in Colab» y se guarda una copia con **Archivo › Guardar una copia en Drive**. Lo que producen queda en `Mi unidad/CC_Ambiental/practica-1/<zona>/`; los archivos de `CR01` y `CR02` (reanálisis y series de zona), en `Mi unidad/CC_datos/<zona>/`.

| Sección | Contenido | Insumos | Preguntas que responde |
|---|---|---|---|
| **1. Zona de estudio** | Ubicación, superficie, relieve, población y actividades principales; mapa con las celdas de los reanálisis | Mapa de `CR01`; pesos de celdas de `CR02` | `CR02`, preguntas 1–2 |
| **2. Datos y métodos** | Fuentes: ERA5, CORe y la estación del curso que eligió `IA1_02` (nombre, código, red, coordenadas, altitud, variables que mide y limitaciones); periodo de referencia 1995–2014, construcción de las series de zona, control de calidad, criterio de año completo, índice de ENSO y temporada, método de tendencia (Sen y Mann-Kendall corregido) | Metadatos `IA1_02_metadatos.json` e `IA1_03_metadatos.json`; inventario de `CR01`; ficha de la estación en [`datos/estaciones/indice_estaciones.csv`](../../../datos/estaciones/indice_estaciones.csv) | «Para el informe» de `IA1_02` e `IA1_03` |
| **3. Clima de referencia** | Climograma, ciclo anual de las 9 variables, estación lluviosa y seca, humedad y viento; diferencias ERA5–CORe como incertidumbre observacional | `IA1_01_climograma_*.png`, `IA1_01_humedad_presion_viento_*.png`, `IA1_01_resumen_*.csv`, `IA1_01_diferencias_*.csv` | `IA1_01`, preguntas 1–4 |
| **4. Calidad de los datos** | Qué tan bien reproducen los reanálisis la estación, **solo en las variables que mide** (en la mayoría, Tmáx, Tmín y lluvia): sesgo, RMSE y correlación por variable y por estación del año | `IA1_02_metricas_mensuales.csv`, `IA1_02_ciclo_anual.png` | `IA1_02`, preguntas 1–5 (las que aplican a su estación) |
| **5. Tendencias y variabilidad natural** | Tendencia de temperatura y lluvia, prueba sin El Niño, tendencia según el año de inicio, compuestos por fase de ENSO, señal/ruido | `IA1_03_tendencias_*.png`, `IA1_03_sensibilidad_inicio_*.png`, `IA1_03_compuestos_enso_*.png`, `IA1_03_tendencias_*.csv`, `IA1_03_sensibilidad_el_nino_*.csv`, `IA1_03_senal_ruido_*.csv` | `IA1_03`, preguntas 1–6 |
| **6. Discusión y conclusiones** *(solo definitivo)* | Qué causa lo observado (forzamiento radiativo frente a variabilidad interna), cómo se compara con la evidencia global del AR6 y qué tan seguro puede estar; limitaciones | Lectura guiada del balance de energía; clase de detección y atribución; AR6 GTI, Resumen para responsables de políticas | Síntesis de todas |
| **Anexo A. Bitácora de El Niño 2026–2027** | Registro semanal del evento en curso, separado del análisis | [`practicas/comun/bitacora`](../../comun/bitacora/) | `IA1_03`, pregunta 7 |
| **Anexo B. Reproducibilidad** | Enlace a sus copias de los cuadernos en Drive, lista de archivos producidos y declaración de uso de IA | Su Drive | — |
| **Anexo C. Atención a observaciones** *(solo definitivo)* | Matriz con cada observación del borrador, el cambio hecho y dónde | Retroalimentación del borrador | — |

## Reglas de redacción

- Cada figura y tabla lleva número, título, fuente y elaboración propia, y se cita en el texto antes de aparecer.
- Todo número va con su unidad y su fuente (ERA5, CORe o estación). Si las fuentes difieren, se da el rango.
- Las conclusiones usan la escala calibrada del IPCC: probabilidad (*probable*, *muy probable*) y confianza (*baja*, *media*, *alta*), justificada por el acuerdo entre fuentes y la robustez de las pruebas.
- Tendencia y variabilidad no se mezclan: un año extremo no es una tendencia, y una tendencia no significativa no prueba que no haya cambio.
- La estación se declara con su nombre, código, red y variables, y con sus limitaciones: la lluvia del INAMHI 1964–2018 está rellenada con Climatol (apoyo CHIRPS) y la temperatura de la red INAMHI empieza en 2022. Las variables que la estación no mide se comparan solo entre ERA5 y CORe.
- El evento El Niño en curso va solo en el anexo A, marcado como preliminar.
- El uso de herramientas de IA se declara; los números y su lectura deben poder explicarse en la exposición.
- Citas en formato APA 7; las de los datos están al final de cada cuaderno.

## Lista de verificación antes de entregar

| Criterio | Borrador | Definitivo |
|---|---|---|
| Las 5 secciones de resultados tienen sus figuras y tablas con unidades y fuente | ✔ | ✔ |
| Las respuestas usan los números de su zona, no generalidades | ✔ | ✔ |
| Las diferencias ERA5–CORe y el contraste con la estación se usan para decir qué tan confiables son los datos | ✔ | ✔ |
| La estación usada está declarada con sus variables y limitaciones, y solo se comparan las variables que mide | ✔ | ✔ |
| La tendencia se reporta con su significancia corregida y la prueba sin El Niño | ✔ | ✔ |
| Se distingue explícitamente la señal de cambio de la variabilidad de ENSO | | ✔ |
| Las causas se explican con el balance de energía y el forzamiento radiativo, no solo se describen los datos | | ✔ |
| La conclusión usa lenguaje calibrado y se compara con la evidencia global del AR6 | | ✔ |
| Se atendió cada observación de la retroalimentación del borrador (anexo C) | | ✔ |
| Se señalan las variables, meses y fases de ENSO relevantes para el ambiente de la zona | | ✔ |
| Anexo de la bitácora con al menos una entrada semanal desde octubre | | ✔ |

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
