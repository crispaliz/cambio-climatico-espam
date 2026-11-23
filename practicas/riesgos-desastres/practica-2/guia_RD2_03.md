# Guía del estudiante — RD2_03 · Medidas de reducción del riesgo, adaptación y mitigación

**Cambio Climático · Ingeniería en Riesgos de Desastres · ESPAM MFL** · Guía CC-IRD-P2-03-G · Versión 1.0 · noviembre de 2026

| | |
|---|---|
| Cuaderno | [`RD2_03_matriz_medidas`](https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/riesgos-desastres/practica-2/RD2_03_matriz_medidas.ipynb) |
| Pregunta que responde | ¿Qué debería hacer el cantón de mayor riesgo, por qué esas medidas y no otras, y cuánto riesgo quedaría? |
| Contenidos de la Unidad II | 2.1 marco normativo (CMNUCC, París, NDC, Sendai) · 2.2 mitigación · 2.3 adaptación · 2.4 análisis comparativo y PLANACC |
| Necesita | `RD2_01` y `RD2_02` ejecutados con la misma provincia, con la planilla de vulnerabilidad completa |
| Tiempo | 1 hora en clase y 2 horas sin docente |
| Deja en su Drive | `RD2_03_*`: matriz, evaluación, cartera, marco normativo, riesgo residual y metadatos |
| Va al capítulo 2 | Sección 4, «Medidas», y anexo B (evaluación completa). Cierra el **borrador formativo** |
| Nivel | Medio: decidir con criterios y justificar cada decisión |

## 1. La idea en un minuto

Frente al riesgo climático hay dos tipos de respuesta, y el capítulo debe mostrar que sabe **diferenciarlas**:

| | Mitigación | Adaptación y reducción del riesgo |
|---|---|---|
| Qué reduce | Emisiones de gases de efecto invernadero | Exposición o vulnerabilidad del cantón |
| Quién se beneficia | Todo el planeta (y el cantón, por los cobeneficios) | El cantón donde se aplica |
| Cuándo se nota | En décadas | En el próximo invierno o El Niño |
| Cómo se mide | t CO2-eq evitadas por año | Cambio del índice de riesgo, personas protegidas |
| Instrumento | Segunda NDC (mitigación), Acuerdo de París | PLANACC, Segunda NDC (adaptación), Marco de Sendai, PDOT |

Algunas medidas hacen las dos cosas (**MA**): restaurar riberas reduce la erosión y las crecidas y, además, captura carbono.

## 2. Cómo organizar el trabajo del equipo

| Momento | Integrante 1 | Integrante 2 |
|---|---|---|
| En clase | Ejecuta hasta la sección 5 y copia el bloque de medidas | Ejecuta hasta la sección 5 y revisa el catálogo de mitigación |
| Sin docente | Califica las medidas de **adaptación** (A) con sus justificaciones | Califica las medidas de **mitigación** (M y MA) y busca dónde aparecen en la NDC y el PLANACC |
| Juntos (30 min) | Discuten las calificaciones y los pesos hasta ponerse de acuerdo: una sola evaluación | |
| Cierre | Ejecuta desde la sección 6 con la evaluación acordada | Ejecuta lo mismo en su Drive y redacta la sección 4 |

**Por qué discutir juntos.** La sumativa evalúa la **resolución de problemas complejos**: definir el problema, comparar alternativas con criterios explícitos y decidir. Esa discusión es el ensayo.

## 3. Paso a paso

| Sección | Qué hace usted | Qué debe ver | Si algo sale mal |
|---|---|---|---|
| **1. Datos** | Nombres, provincia y `CANTON_FOCO` **vacío** (usa el cantón crítico de `RD2_02`) | «Equipo: …» | Escriba otro cantón solo si lo justifica en el capítulo |
| **2. Entorno** | Ejecuta | «Cantón de trabajo: …» | «RD2_02 está marcado como PROVISIONAL»: complete la planilla de vulnerabilidad |
| **3. Punto de partida** | Lee el riesgo del cantón y sus indicadores críticos (◀) | Tabla de riesgo e indicadores | — |
| **4. Mitigación y adaptación** | Lee la tabla | Tabla de alcance | — |
| **5. Medidas sugeridas** | Lee las sugerencias y el catálogo de mitigación pura; **copia el bloque** impreso al final | Dos tablas y un bloque de texto | — |
| **6. Evaluación** | Ajusta los pesos (o deja los propuestos) y **escribe por qué**; pega el bloque en `EVALUACION`, deja entre 6 y 10 medidas, quita el `#` de al menos una M y califica | — | Vea el ejemplo de la sección 4 de esta guía |
| **7. Matriz** | Ejecuta | Tabla con puntajes, robustez y «Revise antes de entregar» | Atienda cada aviso o explíquelo en el capítulo |
| **8. Figuras** | Ejecuta | Matriz de colores y gráfico efectividad–factibilidad | — |
| **9. Marco normativo** | Revisa la prioridad de Sendai y el actor; corrige el actor si lo sabe (`id; actor`) | Tabla del marco normativo | — |
| **10. Cartera y riesgo residual** | Deja `EFECTO = 1` (o 2 si lo justifica) y ejecuta | Cartera de 6 medidas, tabla antes/después y figura | — |
| **11. Guardar** | Ejecuta | Lista de archivos `RD2_03_*` | — |

## 4. Ejemplo de evaluación (sección 6)

Ejemplo **ilustrativo** para Chone (Manabí), cantón crítico con inundación y movimiento en masa de riesgo muy alto. Cada línea lleva `id; efectividad; costo; factibilidad; cobeneficios; sinergia; mala_adaptacion; alineacion; justificación`:

```
A01; 5; 4; 4; 3; 1; 5; 5; Chone: alerta 2 en RD2_02, el río Chone se desborda en invierno y la SNGR ya opera alertas en Manabí.
A03; 4; 4; 2; 3; 2; 4; 4; Viviendas en la ribera (inventario RD2_01), PDOT con mapa de amenazas pero sin ordenanza (planificación 2).
A13; 4; 2; 3; 3; 1; 4; 4; Vivienda precaria 4 en RD2_02, costo alto para el GAD.
A12; 4; 5; 4; 3; 1; 5; 5; Barrios y escuelas del inventario de RD2_01, simulacros baratos y con apoyo de la SNGR.
A02; 4; 3; 4; 2; 1; 2; 4; Drenaje 4, limpiar cauces es efectivo pero canalizar puede trasladar la inundación aguas abajo.
M11; 3; 3; 3; 5; 5; 4; 4; Restaurar riberas con especies nativas reduce erosión y crecidas y captura carbono, degradación 4.
M10; 3; 3; 2; 5; 5; 5; 4; Conservar el bosque de la cuenca alta del río Chone con Socio Bosque.
M14; 2; 4; 3; 3; 1; 5; 3; Compostaje de orgánicos, reduce metano del botadero y casi no cambia el riesgo local.
```

**Reglas para calificar bien:**

1. **Efectividad depende del tipo.** Una medida A se califica por cuánto reduce el riesgo **del cantón**; una medida M, por cuánto reduce las **emisiones de la provincia**. Por eso M14 tiene efectividad 2: reduce poco frente a las emisiones totales.
2. **Sinergia**: 5 solo si la medida claramente mitiga y adapta (M10, M11). Una alerta temprana no mitiga: sinergia 1.
3. **Mala adaptación**: 5 quiere decir **riesgo bajo** de efectos no deseados. A02 tiene 2 porque canalizar sin espacio para el río traslada la inundación aguas abajo. Si el catálogo trae una alerta (como la de M11 sobre especies exóticas) y usted califica 4 o 5, el cuaderno le pide explicarlo: en el capítulo diga cómo se evita (en el ejemplo, «solo especies nativas»).
4. **Alineación**: 5 si la medida aparece como prioridad en la Segunda NDC, el PLANACC o el PDOT del cantón; búsquela en esos documentos.
5. **La justificación**, una frase con **un dato** de sus cuadernos o de una fuente. **Sin punto y coma**: el punto y coma separa las columnas.

## 5. Cómo leer cada salida

Los resultados de esta sección vienen del ejemplo ilustrativo de Chone.

### 5.1 Matriz y ranking (`RD2_03_matriz_*.png`, `RD2_03_evaluacion_*.csv`)

**Qué muestra:** el puntaje ponderado de cada medida y su rango, con los pesos del equipo y con pesos iguales.

> **Ejemplo.** Las primeras son A01 (alerta temprana, 4,00) y A12 (planes de contingencia y simulacros, 3,85): muy efectivas, baratas y factibles. Les siguen dos medidas MA, M11 (3,70) y M10 (3,60), con menos efectividad inmediata, pero con más cobeneficios y sinergia. La mitigación pura M14 quedó última (2,85): su efecto sobre el riesgo del cantón es casi nulo.

**Robustez:** si 4 o 5 de las 5 primeras se mantienen con pesos iguales, el ranking no depende de los pesos que eligió. Si cambia mucho, explique qué criterio lo mueve.

### 5.2 Efectividad frente a factibilidad (panel b)

| Cuadrante | Lectura | En el ejemplo |
|---|---|---|
| Arriba a la derecha | Priorizar: funcionan y se pueden hacer | A01, A12, A02 |
| Arriba a la izquierda | Valen la pena, pero hay que preparar condiciones (ordenanza, presupuesto, actores) | A03: efectiva pero con factibilidad 2, porque exige una ordenanza |
| Abajo a la derecha | Ganancias rápidas pero pequeñas | M14, en el límite (factibilidad 3, efectividad 2) |

### 5.3 Marco normativo (`RD2_03_marco_normativo_*.csv`)

**Qué muestra:** por medida, el sector de la NDC o el PLANACC, la prioridad del Marco de Sendai y el actor responsable.

> **Ejemplo.** La cartera de Chone cubre las prioridades 2 (gobernanza: A03), 3 (invertir en resiliencia: A13, M10, M11) y 4 (preparación: A01, A12) de Sendai. Queda sin cubrir la **prioridad 1, comprender el riesgo**: el capítulo puede proponer, como paso previo, un mapa de amenaza por inundación del río Chone a escala de barrio.

### 5.4 Cartera y riesgo residual (`RD2_03_cartera_*.csv`, `RD2_03_riesgo_residual_*.png`)

**Qué muestra:** las 6 medidas priorizadas y el riesgo del cantón antes y después de aplicarlas, con un supuesto simple (cada medida mejora 1 punto los indicadores que atiende; si dos medidas atienden el mismo indicador, sus efectos se suman hasta el máximo de la escala).

> **Ejemplo.** Con la cartera, el riesgo de inundación de Chone baja de 4,6 (muy alto) a 4,0 (alto), un 14 %, y el de movimiento en masa de 4,3 a 3,6 (−16 %). La vulnerabilidad baja de 4,0 a 3,2 y el ordenamiento territorial (A03) baja la exposición en 1 punto. **El riesgo sigue alto**: la amenaza no cambia (A = 5) y la exposición solo baja con medidas de largo plazo. Ese **riesgo residual** se gestiona con transferencia (seguro agrícola, fondo de contingencia, A11) y preparación para la respuesta.

**El punto central para el RA B:** las medidas de mitigación de la cartera (M10, M11) bajan el riesgo **por su parte de adaptación** (menos degradación); su parte de mitigación no cambia el riesgo de Chone en este invierno, sino la amenaza global en décadas. Una medida de mitigación pura, como M14, no cambia el riesgo local. Las dos respuestas son necesarias y **no se reemplazan**.

### 5.5 Párrafo modelo para la sección 4.4 del capítulo

> «La cartera priorizada para Chone (Tabla 4.3) combina cuatro medidas de adaptación (A01, A12, A03 y A13) y dos de mitigación con beneficios de adaptación (M10 y M11). En conjunto reducirían el riesgo de inundación de 4,6 a 4,0, de «muy alto» a «alto» (Figura 4.2), bajo el supuesto de que cada medida mejora en un punto el indicador que atiende. El riesgo residual se explica porque la amenaza de El Niño no depende del cantón y porque la exposición de los barrios de la ribera solo baja con ordenamiento territorial, que requiere una ordenanza aún inexistente (factibilidad 2). La mitigación pura evaluada (M14, compostaje) es pertinente para la meta de la Segunda NDC, pero no modifica el riesgo local en el corto plazo: su alcance es global y de largo plazo.»

## 6. Qué llevar al capítulo 2

| Salida | En el capítulo | Sección |
|---|---|---|
| Tabla de alcance mitigación–adaptación (con sus palabras y su cantón) | Tabla 4.1 | 4.1 Mitigación y adaptación |
| `RD2_03_matriz_*.png` | Figura 4.1 | 4.2 Evaluación multicriterio |
| Pesos y su justificación, robustez | En el texto | 4.2 |
| `RD2_03_marco_normativo_*.csv` | Tabla 4.2 | 4.3 Marco normativo |
| `RD2_03_cartera_*.csv` | Tabla 4.3 | 4.4 Cartera y riesgo residual |
| `RD2_03_riesgo_residual_*.png` | Figura 4.2 | 4.4 |
| `RD2_03_evaluacion_*.csv` con todas las justificaciones | Anexo B | Anexo B |

## 7. Problemas frecuentes

| Problema | Solución |
|---|---|
| «Línea n: faltan columnas» | Faltan puntajes o puso un punto y coma de más o de menos. Deben ser 9 campos: id, 7 puntajes y la justificación |
| «Los puntajes deben ser enteros de 1 a 5» | Escribió 3,5 o 0. Use enteros de 1 a 5 |
| «Ids que no están en el catálogo» | Escribió mal el id (por ejemplo, `A1` en vez de `A01`) o dejó el `#` delante del id |
| «No evaluó ninguna medida de mitigación pura» | Quite el `#` de una línea M del bloque y califíquela |
| «EVALUACIÓN POR DEFECTO» en el título de la figura | La celda `EVALUACION` está vacía o solo tiene comentarios. No es válida para entregar |
| La cartera no tiene la medida que el equipo quería | La cartera la arma el puntaje. Si el equipo cree que debería estar, revise sus calificaciones o discútalo en el capítulo |

## 8. Lista de verificación

- [ ] La evaluación tiene entre 6 y 10 medidas, al menos 3 de adaptación, 2 de mitigación y 1 de mitigación pura.
- [ ] Cada medida tiene una justificación con un dato, sin «justifique aquí».
- [ ] Escribí la justificación de los pesos.
- [ ] Atendí o expliqué cada aviso de «Revise antes de entregar».
- [ ] La figura no dice «EVALUACIÓN POR DEFECTO» y `RD2_02` no era provisional.
- [ ] Sé explicar, con mi cartera, qué reduce la adaptación y qué reduce la mitigación.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
