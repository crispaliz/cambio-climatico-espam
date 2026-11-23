# Guía del estudiante — RD2_02 · Vulnerabilidad y riesgo de los cantones prioritarios

**Cambio Climático · Ingeniería en Riesgos de Desastres · ESPAM MFL** · Guía CC-IRD-P2-02-G · Versión 1.0 · noviembre de 2026

| | |
|---|---|
| Cuaderno | [`RD2_02_vulnerabilidad`](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-2/RD2_02_vulnerabilidad.ipynb) |
| Pregunta que responde | ¿Qué tan vulnerables son los cantones más expuestos y cuál tiene el mayor riesgo, frente a qué amenaza y por qué? |
| Necesita | Los productos de `RD2_01` en `Mi unidad/CC_Riesgos/practica-2/<provincia>/`, con el inventario completo |
| Tiempo | 1 hora en clase (secciones 1 a 6 y primera corrida provisional) y 2 horas sin docente (planilla) |
| Deja en su Drive | `RD2_02_vulnerabilidad_<provincia>.xlsx` (planilla), 3 figuras, 4 tablas y `RD2_02_metadatos.json` |
| Va al capítulo 2 | Sección 3, «Vulnerabilidad y riesgo», y anexo A (planilla resumida) |
| Nivel | Básico a medio: buscar datos en el Censo y el PDOT, calificar con una escala y leer un índice |

## 1. La idea en un minuto

Dos cantones pueden estar igual de expuestos a la misma inundación y sufrir daños muy distintos. La diferencia es la **vulnerabilidad**:

- **Sensibilidad (S):** cuánto daño sufre lo expuesto. Una casa de caña sin cimentación es más sensible que una de hormigón; un barrio sin alcantarillado se inunda más tiempo.
- **Capacidad de adaptación (CA):** cuánto puede el cantón anticiparse, responder y recuperarse. Una alerta temprana, un PDOT que prohíbe construir en la ribera y un fondo de contingencia aumentan la capacidad.

El cuaderno junta todo en dos fórmulas:

- **V = (S + (6 − CA)) / 2.** La capacidad se «invierte» (6 − CA) porque una capacidad alta **baja** la vulnerabilidad.
- **R = (A · E · V)^(1/3).** Es una media geométrica: si uno de los tres componentes es bajo, el riesgo baja, aunque los otros sean altos.

**Ejemplo de cálculo.** En un cantón con S = 4,0 y CA = 2,0, la vulnerabilidad es V = (4,0 + 4,0) / 2 = 4,0. Con amenaza A = 5 y exposición E = 5, el riesgo es R = (5 × 5 × 4)^(1/3) = 100^(1/3) = 4,6, «muy alto». Si la alerta temprana y el PDOT suben la capacidad a CA = 3,0, entonces V = 3,5 y R = (87,5)^(1/3) = 4,4: el riesgo baja **sin tocar la amenaza**.

## 2. Cómo organizar el trabajo del equipo

La planilla tiene **9 filas por cantón** (5 de sensibilidad y 4 de capacidad). Con 4 cantones prioritarios son 36 filas: repártanlas por cantón, no por indicador, para que cada uno conozca a fondo sus cantones.

| Momento | Integrante 1 | Integrante 2 |
|---|---|---|
| En clase | Ejecuta el cuaderno completo (resultado provisional) | Ejecuta el cuaderno completo y abre la planilla |
| Sin docente, día 1 | Busca los datos del Censo 2022 de **todos** los cantones (vivienda, NBI, ocupación, alcantarillado): una sola búsqueda por tema | Busca en el PDOT de cada cantón degradación, alerta temprana, planificación y recursos |
| Sin docente, día 2 | Califica y justifica sus cantones | Califica y justifica sus cantones |
| Cierre | Revisa las calificaciones del otro: ¿la misma escala, la misma fuente? | Ejecuta desde la sección 7 y comparte la carpeta |

**Una sola planilla oficial.** Trabajen sobre el mismo archivo (compartido en Drive) y cópienlo a la carpeta del otro integrante con el mismo nombre antes de ejecutar.

## 3. Paso a paso

| Sección | Qué hace usted | Qué debe ver | Si algo sale mal |
|---|---|---|---|
| **1. Datos** | Nombres y la **misma provincia** de `RD2_01` | «Equipo: … · provincia de …» | — |
| **2. Entorno** | Ejecuta y acepta el acceso a Drive | Las amenazas priorizadas y los cantones prioritarios de `RD2_01` | «Faltan productos de RD2_01»: ejecute primero `RD2_01` con la misma provincia |
| **3. Lo que trae del paso 1** | Lee la exposición y el conteo del inventario | Tabla de exposición y elementos con nombre y fuente por cantón | «⚠ Con menos de 3 elementos»: complete el inventario de `RD2_01` |
| **4. Amenaza** | Lee la sugerencia y decide. Deje el deslizador en 0 para aceptar la sugerencia; muévalo para cambiarla y **escriba la razón** en `J_AMENAZA` | Una calificación de 1 a 5 por amenaza | «⚠ Cambió la sugerencia…»: falta `J_AMENAZA` |
| **5. Datos de apoyo** | Lee la tabla | Por cantón: % en zona baja y ladera, servicios por 10 000 hab, vías, daño histórico y sugerencia de acceso | — |
| **6. Planilla** | Ejecuta. Abre `RD2_02_vulnerabilidad_<provincia>.xlsx` y la completa **sin docente** | «Planilla guardada» o «La planilla ya existe: no la sobrescribo» | Guárdela con **el mismo nombre** en la misma carpeta |
| **7. Vulnerabilidad** | Ejecuta después de llenar la planilla | Tabla de S, CA y V por cantón y figura de barras | «PROVISIONAL»: hay celdas `valor` vacías |
| **8. Riesgo** | Ejecuta | Tabla A, E, V, R, clase; matriz de colores y mapa | — |
| **9. Frases** | Lee las frases de ejemplo | El cantón y la amenaza críticos y los indicadores críticos | Revise los avisos de «Revise antes de entregar» |
| **10. Guardar** | Ejecuta | La lista de archivos `RD2_02_*` | Si dice PROVISIONAL, aún no ha terminado |

### Cómo llenar la planilla: un ejemplo por tipo de indicador

Cada fila trae `como_calificar` (la escala) y `donde_buscar` (la fuente). Usted completa cuatro columnas: `dato_encontrado`, `valor`, `fuente` y `justificacion`.

| Indicador | dato_encontrado | valor | fuente | justificacion |
|---|---|---|---|---|
| Viviendas precarias | 22 % de viviendas con paredes de caña o madera | 4 | INEC, Censo 2022, resultados por cantón (consulta 25-11-2026) | Entre 20 y 30 %: valor 4 |
| Pobreza y población vulnerable | 61 % de pobreza por NBI; 28 % de niñez | 4 | INEC, Censo 2022 | Entre 60 y 80 %: valor 4 |
| Drenaje y agua | 47 % de viviendas sin alcantarillado | 3 | INEC, Censo 2022 | Entre 30 y 50 %: valor 3; en el área rural es mayor |
| Degradación | Relleno de la ribera y deforestación en la cuenca alta | 4 | PDOT 2024–2027, diagnóstico biofísico | Degradación en buena parte del cantón |
| Alerta temprana (capacidad) | Sin alerta comunitaria; comités en 2 de 9 parroquias | 2 | GAD, unidad de gestión de riesgos; SNGR | Alerta débil: valor 2 (**en la capacidad, bajo es malo**) |
| Acceso (capacidad) | 1,8 servicios de salud y emergencia por 10 000 hab; sugerencia 2 | 2 | Dato de apoyo del cuaderno (OpenStreetMap) | Bajo la media del país y vías que se cortan en invierno |
| Planificación (capacidad) | PDOT con mapa de amenazas, sin ordenanza de uso del suelo | 3 | PDOT 2024–2027 y PUGS del cantón | Mapa sí, ordenanza no: valor 3 |

*Los datos de la tabla son ilustrativos: su planilla debe llevar los datos reales de sus cantones.*

**Si no encuentra un dato.** Busque un dato cercano (el de la provincia, otro año o el del cantón vecino), escríbalo, diga que es una aproximación y califique con prudencia. No deje la fila vacía ni invente: una aproximación declarada vale; un número sin fuente, no.

**Dónde están los datos.**

- **Censo 2022 (INEC):** resultados por cantón en el portal del censo ([censoecuador.gob.ec](https://www.censoecuador.gob.ec/)): vivienda (material de paredes), servicios básicos (alcantarillado y agua por red pública), pobreza por NBI, edad y ocupación por rama de actividad.
- **PDOT del cantón:** en la página del GAD municipal (sección «Transparencia» o «Planificación»). Los diagnósticos biofísico, de asentamientos humanos y económico productivo traen casi todo lo que necesita; busque también el componente de gestión de riesgos.
- **SNGR:** [gestionderiesgos.gob.ec](https://www.gestionderiesgos.gob.ec/), con los informes de situación por evento y la información de alerta temprana y de comités comunitarios.

## 4. Cómo leer cada salida

Los ejemplos son de **Manabí**. La exposición y los datos de apoyo son reales (datos del curso); **las calificaciones de vulnerabilidad son ilustrativas**, puestas solo para mostrar cómo se leen los resultados.

### 4.1 Tabla de la amenaza (sección 4; `RD2_02_amenaza_*.csv`)

**Qué muestra:** por amenaza, los desastres de DesInventar y los días del ECU 911, la sugerencia y en qué se basa.

> **Ejemplo.** Manabí registra 199 desastres por inundación y 71 por deslizamiento en DesInventar (1970–2007); la sugerencia es 5 para las dos. Un equipo puede aceptar 5 para la inundación y bajar el movimiento en masa a 4, si su capítulo 1 muestra que los deslizamientos se concentran en pocos cantones. Esa decisión **se escribe** en `J_AMENAZA`.

### 4.2 Datos de apoyo (sección 5)

> **Ejemplo.** Chone tiene 1,8 servicios de salud y emergencia por 10 000 habitantes (sugerencia de acceso 2) y 7,4 km de vías principales por 100 km², frente a los 3,8 servicios y 44,6 km de Manta. Entre 1970 y 2007, Portoviejo y Chone registraron cerca de 31 afectados por cada 1 000 habitantes, cinco veces más que Manta (6). Estos datos apoyan una capacidad de acceso menor en Chone y una sensibilidad histórica alta en Portoviejo y Chone.

### 4.3 Vulnerabilidad (`RD2_02_vulnerabilidad_*.png` y `.csv`)

**Qué muestra:** tres barras por cantón: sensibilidad, falta de capacidad (6 − CA) y vulnerabilidad.

**Cómo leerla:** compare las dos primeras barras. Si pesa más la sensibilidad, las medidas deben mejorar viviendas, drenaje o ecosistemas; si pesa más la falta de capacidad, deben fortalecer la alerta, la planificación o los recursos.

> **Ejemplo ilustrativo.** Chone (V = 4,0) y Bolívar (V = 3,9) son los más vulnerables. En Bolívar pesa más la falta de capacidad (4,2) que la sensibilidad (3,6): no tiene fondos ni alerta temprana. En Manta (V = 2,7), la sensibilidad es baja (2,4) porque depende poco de la agricultura y tiene menos vivienda precaria.

### 4.4 Matriz de riesgo y mapa (`RD2_02_matriz_riesgo_*.png`, `RD2_02_mapa_riesgo_*.png`, `RD2_02_riesgo_*.csv`)

**Qué muestra:** R y su clase para cada cantón y amenaza; el mapa colorea cada cantón por su riesgo más alto.

**Cómo leerla, en tres pasos:**

1. **¿Dónde está el riesgo más alto?** Chone, por inundación: R = 4,6, muy alto.
2. **¿Qué componente pesa más?** La columna `pesa_mas`. Si es la amenaza (A = 5 en toda la provincia), compare los cantones por E y V, porque A es igual para todos.
3. **¿Hay contrastes?** Manta y Portoviejo tienen la misma exposición a la inundación que Chone (E = 5), pero riesgo «alto» y no «muy alto»: su vulnerabilidad es menor (2,7 y 2,9 frente a 4,0). Este es el párrafo más importante de la sección: **la vulnerabilidad explica la diferencia**.

### 4.5 Frases de ejemplo (sección 9)

El cuaderno escribe un esqueleto:

> «En Chone, el riesgo de inundación es muy alto (R = 4.6 de 5): amenaza 5, exposición 5 y vulnerabilidad 4.0. Lo que más pesa es la amenaza. En la vulnerabilidad destacan «viviendas de materiales precarios…» (sensibilidad 4) y una capacidad débil en «alerta temprana…» (2).»

Conviértalo en un párrafo del capítulo agregando **sus datos, sus fuentes y su territorio**:

> «Chone es el cantón con mayor riesgo de inundación de Manabí (R = 4,6, muy alto; Tabla 3.2). Comparte con Portoviejo y Manta la exposición más alta de la provincia (E = 5), por sus 433 servicios críticos y sus 53 eventos de inundación registrados, pero su vulnerabilidad es mayor (V = 4,0): el ___ % de sus viviendas tiene paredes precarias y el ___ % no tiene alcantarillado (INEC, 2023), y no cuenta con alerta temprana comunitaria en la cuenca del río Chone (GAD de Chone, 2024). Por eso, con la misma amenaza y exposición, su riesgo supera al de Manta (R = 4,1).»

### 4.6 Metadatos (`RD2_02_metadatos.json`)

Guarda el cantón y la amenaza críticos, los indicadores críticos y si el resultado es provisional. `RD2_03` lo lee: no lo borre ni lo edite a mano.

## 5. Qué llevar al capítulo 2

| Salida | En el capítulo | Sección |
|---|---|---|
| Tabla de la amenaza con la calificación final y su justificación | Tabla 3.1 | 3.1 Amenaza |
| Datos de apoyo de la sección 5 (solo cantones prioritarios) | En el texto o Tabla 3.2 | 3.2 Vulnerabilidad |
| `RD2_02_vulnerabilidad_*.png` | Figura 3.1 | 3.2 Vulnerabilidad |
| `RD2_02_riesgo_*.csv` (A, E, V, R, clase) | Tabla 3.3 | 3.3 Riesgo |
| `RD2_02_matriz_riesgo_*.png` y `RD2_02_mapa_riesgo_*.png` | Figuras 3.2 y 3.3 | 3.3 Riesgo |
| Planilla con dato, valor y fuente (puede resumirse) | Anexo A | Anexo A |

## 6. Problemas frecuentes

| Problema | Solución |
|---|---|
| «Valores fuera de 1–5 en la planilla» | Revise la fila que indica el mensaje: escribió un porcentaje en `valor`. El porcentaje va en `dato_encontrado`; en `valor`, la calificación de 1 a 5 |
| Todo sale PROVISIONAL aunque llené la planilla | Guardó la planilla con otro nombre o en otra carpeta. Debe llamarse exactamente `RD2_02_vulnerabilidad_<provincia>.xlsx` |
| Edité en Google Sheets y el cuaderno no ve los cambios | Sheets crea una copia en otro formato. Use **Archivo › Descargar › Microsoft Excel** y suba el archivo a la misma carpeta, reemplazando el original |
| «La planilla no tiene filas para…» | Volvió a ejecutar `RD2_01` y cambiaron los cantones prioritarios. Ejecute la sección 6: el cuaderno agrega las filas que faltan sin borrar las suyas |
| Todos los cantones salen con el mismo riesgo | Calificó todo con el mismo valor. La planilla debe distinguir los cantones con datos |
| Los dos integrantes obtienen resultados distintos | Usan planillas distintas. Acuerden una sola y cópienla con el mismo nombre |

## 7. Lista de verificación

- [ ] La amenaza de cada tipo tiene su calificación y, si cambió la sugerencia, su razón.
- [ ] La planilla tiene **todas** las filas con `dato_encontrado`, `valor`, `fuente` y `justificacion`.
- [ ] El resultado **no** dice PROVISIONAL.
- [ ] Sé explicar por qué el cantón crítico tiene más riesgo que otro igual de expuesto.
- [ ] Respondí las 6 preguntas de la sección 11.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
