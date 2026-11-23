# Guía del estudiante — RD2_01 · Exposición del territorio

**Cambio Climático · Ingeniería en Riesgos de Desastres · ESPAM MFL** · Guía CC-IRD-P2-01-G · Versión 1.0 · noviembre de 2026

| | |
|---|---|
| Cuaderno | [`RD2_01_exposicion`](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-2/RD2_01_exposicion.ipynb) (versión 1.1) |
| Pregunta que responde | ¿Qué hay expuesto en cada cantón de mi provincia a las amenazas del capítulo 1, y qué cantones están más expuestos? |
| Necesita | La provincia de la Práctica 1. Si encuentra los productos de `RD1_02` en su Drive, los usa; si no, el equipo escribe la evidencia a mano |
| Tiempo | 1 hora en clase y 2 horas sin docente (inventario) |
| Deja en su Drive | `Mi unidad/CC_Riesgos/practica-2/<provincia>/RD2_01_*` (9 archivos) |
| Va al capítulo 2 | Sección 2, «Exposición», y anexo A (inventario de elementos expuestos) |
| Nivel | Básico: no hay que programar, solo completar formularios y leer resultados |

## 1. Antes de empezar

- [ ] Tiene una cuenta de Google con espacio en Drive (los resultados pesan menos de 5 MB).
- [ ] Sabe qué amenazas respaldó su capítulo 1 y tiene a mano **sus números**: periodos de retorno de `RD1_02` (Rx1day y Rx5day de 10 y 25 años), factor de El Niño de `RD1_01`, días secos seguidos (CDD), días cálidos (TX90p) y eventos de DesInventar y del ECU 911.
- [ ] Los dos integrantes usan **la misma provincia** en todos los cuadernos.

## 2. Cómo organizar el trabajo del equipo

Los dos integrantes ejecutan el cuaderno, cada uno en su Drive: así los dos dominan el procedimiento y nadie se queda sin productos si falla una cuenta. El trabajo **sin docente** se reparte.

| Tarea | Integrante 1 | Integrante 2 |
|---|---|---|
| Ejecutar el cuaderno en su Drive (secciones 1 a 10) | ✔ | ✔ |
| Escribir la justificación de cada amenaza (sección 4) | ✔ (redacta) | revisa los números |
| Revisión del territorio (sección 7) | busca en el PDOT | busca en la SNGR y la prensa |
| Inventario de elementos expuestos (sección 9) | cantones prioritarios de la amenaza 1 | cantones prioritarios de la amenaza 2 |
| Respuestas de la sección 11 (borrador de la sección «Exposición») | preguntas 1–3 | preguntas 4–6 |
| Revisión cruzada | lee el texto del integrante 2 | lee el texto del integrante 1 |

**Archivo único.** Acuerden cuál de los dos Drive es el «oficial» para el inventario: el que lo complete lo comparte con el otro (clic derecho › Compartir) y el otro lo copia a su carpeta con el mismo nombre antes de ejecutar `RD2_02`.

## 3. Paso a paso

| Sección | Qué hace usted | Qué debe ver | Si algo sale mal |
|---|---|---|---|
| **1. Datos del equipo** | Escribe los nombres y elige la provincia. Deje `ZONA_CAPITULO_1` vacío, salvo que en la Práctica 1 haya trabajado un cantón | «Equipo: … · provincia de …» | — |
| **2. Entorno** | Ejecuta. Colab pide permiso para entrar a su Drive: acéptelo con la cuenta del curso | «Capítulo 1 en … (encontrado)» o «(NO encontrado…)» | «NO encontrado» no es un error: el cuaderno sigue y usted escribe la evidencia a mano. Si sí tiene la Práctica 1, revise que la provincia sea la misma |
| **3. La amenaza** | Ejecuta y **lee** los números | Una tabla con los periodos de retorno, índices y tendencias de su capítulo 1, y otra con los eventos por amenaza y fuente | Si sale vacía, copie los números de su capítulo 1 en la sección 4 |
| **4. Amenazas priorizadas** | Marca 2 o 3 amenazas y escribe **el número** que justifica cada una | Las amenazas marcadas, sin el aviso «⚠ falta la justificación» | Reemplace los `___` del ejemplo por sus números |
| **5. Elementos expuestos** | Ejecuta | Tabla por cantón y 4 mapas: densidad, % en zona baja, % en ladera y servicios | — |
| **6. Calificación** | Ejecuta | Matriz de colores cantón × amenaza (1–5) | En provincias con menos de 5 cantones aparece «se califica frente a los cantones del país»: es lo esperado |
| **7. Revisión del equipo** | Si sabe algo que la matriz no refleja, corrígelo **con su fuente** | Tabla «antes / después» o «Sin correcciones» | Formato: `Chone: inundacion = 5; Jipijapa: sequia = 4` (amenaza sin tildes) |
| **8. Cantones prioritarios** | Ejecuta | Los 3 cantones más expuestos a cada amenaza, con sus números | — |
| **9. Inventario** | Ejecuta; luego, **sin docente**, completa la planilla | `RD2_01_inventario_expuestos_<provincia>.xlsx` en su carpeta | El cuaderno no sobrescribe una planilla ya llena; si quiere una nueva, borre la anterior |
| **10. Guardar** | Ejecuta | La lista de los 9 archivos `RD2_01_*` | — |
| **11. Preguntas** | Las responde en el borrador | — | — |

### Cómo escribir la justificación de una amenaza (sección 4)

| Débil (no sirve) | Buena |
|---|---|
| «Manabí siempre se inunda» | «Rx1day de 25 años = ___ mm (`RD1_02`, ERA5); la lluvia de diciembre a mayo se multiplica por ___ en años de El Niño (`RD1_01`); 199 desastres por inundación en DesInventar 1970–2007» |
| «Hay deslizamientos en la provincia» | «Rx5day de 10 años = ___ mm; 71 desastres por deslizamiento y hundimiento en DesInventar; relieve de colinas con laderas > 20° en el centro de la provincia» |

La regla es simple: **una amenaza sin número no se califica**.

### Cómo llenar el inventario (sección 9)

La planilla trae, para cada cantón prioritario, los conteos automáticos y tres filas vacías. En cada fila vacía escriba **un elemento concreto** con nombre propio:

| canton | amenaza | tipo | elemento | cantidad | nombre_o_lugar | latitud | longitud | fuente |
|---|---|---|---|---|---|---|---|---|
| Chone | Inundación | personas | barrio en la ribera | 350 viviendas | Barrio Las Palmas, margen del río Chone | −0,698 | −80,094 | PDOT Chone, diagnóstico de asentamientos (año) |
| Chone | Inundación | servicios | hospital | 1 | Hospital Napoleón Dávila Córdova | | | Google Earth y mapa de amenaza del GAD |
| Chone | Inundación | vías | puente de la vía principal | 1 | Puente sobre el río Chone, vía a Flavio Alfaro | | | OpenStreetMap y SitRep de la SNGR |

*Los nombres, coordenadas y cantidades de la tabla son ilustrativos: verifique cada dato en su fuente.* Mínimo **tres elementos por cantón prioritario**: un barrio o comunidad, un servicio crítico y una vía o un medio de vida (cultivo, puerto pesquero, captación de agua). `RD2_02` cuenta cuántos tiene cada cantón y le avisa si faltan.

## 4. Cómo leer cada salida

Los ejemplos usan **Manabí** con los datos del curso (tabla de exposición del 5 de noviembre de 2026), con inundación y movimiento en masa como amenazas priorizadas.

### 4.1 Tabla de exposición (`RD2_01_tabla_exposicion_<provincia>.csv`) y mapas (`RD2_01_mapas_exposicion_*.png`)

**Qué muestra:** cuánta gente, cuántos servicios y cuántas vías hay en cada cantón, y cuántos están en zona baja (< 10 m) o en ladera (> 20°).

**Cómo leerla:** compare **números absolutos** (cuántas personas) con **porcentajes** (qué parte de la población). Un cantón grande puede tener mucha gente expuesta aunque su porcentaje sea bajo.

> **Ejemplo (Manabí).** Portoviejo tiene 328 497 habitantes, pero solo el 2,7 % (8 716 personas) vive bajo 10 m; Sucre tiene 60 668 habitantes y el 25,6 % (15 525 personas) vive en zona baja. En número de personas expuestas, Sucre supera a Portoviejo, aunque su población sea cinco veces menor.

**Qué escribir:** una o dos frases como la del ejemplo para la amenaza principal, citando la tabla.

### 4.2 Matriz de exposición (`RD2_01_matriz_exposicion_*.png`) y puntajes (`RD2_01_puntajes_exposicion_*.csv`)

**Qué muestra:** el puntaje de exposición de 1 a 5 de cada cantón para cada amenaza. Es **relativo**: 5 quiere decir «entre el 20 % más expuesto de la provincia» (o del país, si la provincia tiene menos de 5 cantones).

**Cómo leerla:**

1. Busque las filas con 5 y 4: son los cantones que más preocupan.
2. Compare las columnas: ¿un mismo cantón está muy expuesto a las dos amenazas? (Chone: 5 en inundación y 4 en movimiento en masa).
3. Busque contrastes: un cantón con 5 en una amenaza y 2 en otra (Manta: 5 en inundación, 2 en movimiento en masa) dice algo del relieve.

**Error frecuente:** escribir «Portoviejo tiene exposición 5, es decir, muy alta». Lo correcto es «Portoviejo está entre los cantones **más expuestos de Manabí**», porque la escala es relativa.

### 4.3 Cantones prioritarios (`RD2_01_cantones_prioritarios_*.csv`) y mapa de la amenaza principal (`RD2_01_mapa_<amenaza>_*.png`)

**Qué muestra:** los 3 cantones más expuestos a cada amenaza y el **indicador** que más pesa en cada uno. En Manabí, para inundación salen Portoviejo, Manta y Chone; para movimiento en masa, Portoviejo, Chone y Bolívar. Esos 4 cantones son los que `RD2_02` evalúa en vulnerabilidad.

**Cómo leerla:** para cada cantón, diga **por qué** quedó prioritario:

> «Chone es prioritario frente a la inundación por sus 433 servicios críticos (escuelas, salud y emergencia), sus 227 km de vías principales y sus 53 eventos de inundación registrados, el mayor número de la provincia; en cambio, su población en zona baja (4 629 personas) es menor que la de Manta.»

### 4.4 Eventos por cantón (`RD2_01_eventos_por_canton_*.csv`)

**Qué muestra:** los desastres de DesInventar (1970–2007) y los días con incidentes del ECU 911 (desde julio de 2021) en cada cantón.

**Cómo leerla:** úselos para contrastar la exposición calculada con la historia. Si un cantón tiene muchos eventos y poca exposición calculada (o al revés), explique por qué: escala del relieve (90 m), OpenStreetMap incompleto o registros que se concentran en las ciudades. **No sume** DesInventar y ECU 911: registran cosas distintas.

### 4.5 Metadatos (`RD2_01_metadatos.json`)

Guarda las amenazas, las justificaciones, las correcciones y si la calificación fue frente a la provincia o al país. No va al capítulo, pero `RD2_02` lo lee: no lo borre.

## 5. Qué llevar al capítulo 2

| Salida | En el capítulo | Sección |
|---|---|---|
| Tabla de amenazas priorizadas con su número (sección 4 del cuaderno) | Tabla 2.1 | 2.1 Amenazas consideradas |
| `RD2_01_mapas_exposicion_*.png` | Figura 2.1 | 2.2 Elementos expuestos |
| `RD2_01_matriz_exposicion_*.png` | Figura 2.2 | 2.3 Exposición por cantón |
| Cantones prioritarios con sus números (sección 8) | Tabla 2.2 | 2.3 Exposición por cantón |
| Correcciones del equipo con su fuente (sección 7) | En el texto de 2.3 | 2.3 |
| Inventario de elementos expuestos | Anexo A | Anexo A |

Cada figura lleva número, título, fuente («Elaboración propia con WorldPop 2020, Copernicus DEM GLO-90 y OpenStreetMap, cuaderno RD2_01») y se cita en el texto antes de aparecer.

## 6. Problemas frecuentes

| Problema | Solución |
|---|---|
| «Marque al menos una amenaza» | En la sección 4, marque al menos una casilla y vuelva a ejecutar esa celda y las siguientes |
| Un mapa sale todo gris | La provincia no tiene ese indicador (por ejemplo, nada bajo 10 m en la Sierra). Es un resultado, no un error |
| La calificación de un cantón rural parece muy baja | OpenStreetMap puede no tener sus escuelas o vías: corríjalo en la sección 7 con su fuente |
| Se cortó la conexión a mitad | **Entorno de ejecución › Ejecutar todas**: el cuaderno no descarga nada pesado y no pierde el inventario ya creado |
| Su provincia es Esmeraldas o Santo Domingo y ejecutó antes del 23 de noviembre | Vuelva a ejecutar el cuaderno: La Concordia ahora se cuenta en Santo Domingo de los Tsáchilas (provincia a la que pertenece desde 2013) |

## 7. Lista de verificación

- [ ] Cada amenaza marcada tiene **un número** del capítulo 1 en su justificación.
- [ ] Revisé la matriz y corregí lo que sé del territorio, con su fuente (o escribí que no hubo correcciones).
- [ ] El inventario tiene al menos **3 elementos con nombre y fuente** por cantón prioritario.
- [ ] Los 9 archivos `RD2_01_*` están en mi carpeta de Drive.
- [ ] Respondí las 6 preguntas de la sección 11 con números de mi provincia.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
