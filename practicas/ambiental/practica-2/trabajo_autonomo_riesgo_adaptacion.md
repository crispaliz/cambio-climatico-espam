# Trabajo autónomo · Marco de riesgo del AR6 y adaptación

**Cambio Climático · Ingeniería Ambiental · Unidad II · martes 17 de noviembre de 2026**
**Duración:** 60 minutos · **Modalidad:** individual, con la misma provincia de la Práctica 1
**Entrega:** un PDF de 1 a 2 páginas en el aula virtual · **Modalidad:** remota por la contingencia del 16 al 20 de noviembre

## Propósito

Como no habrá salida de campo, usted evalúa el sitio **a distancia** con evidencia verificable. Este trabajo resuelve el **paso 2** de la Práctica 2 (`IA2_02_ficha_riesgo`, calificación del sitio) y deja una lista inicial de opciones para el **paso 3** (`IA2_03_matriz_estrategias`).

Al terminar, usted podrá:

1. Distinguir amenaza, exposición, sensibilidad y capacidad de adaptación en un sitio real.
2. Justificar una calificación de 1 a 5 con evidencia verificable.
3. Proponer opciones de adaptación coherentes con el componente que más pesa en el riesgo y ubicarlas en un sector del PLANACC.

## Lo que necesita

- Su evidencia climática de la Práctica 1: el factor de El Niño en la lluvia de diciembre a mayo, el Rx1day de 25 años y la tendencia de días cálidos (`CR02`, `IA1_03`).
- La [hoja de campo](guia_formativa.md#anexo-hoja-de-campo-para-la-ficha-de-riesgo-ia2_02) del anexo de la guía formativa, con su tabla de equivalencias para la modalidad remota.
- Google Earth (imágenes históricas) y Google Maps (Street View con fecha).
- El PDOT de su cantón (sitio web del GAD) y, si los encuentra, registros de eventos (SGR, ECU 911, prensa local).
- Las diapositivas de la sesión: marco de riesgo, escalas, índice R = ∛(A·E·V) y familias de opciones.

## Parte 1 · El sitio (15 min)

1. Elija **un sitio** de su provincia con buena cobertura de imágenes (Street View o imágenes históricas). Puede ser un barrio junto a un río, una playa, un estuario o manglar, una llanura agrícola inundable, una ladera o una zona de secano.
2. Anote su nombre, cantón, parroquia y coordenadas en grados decimales (Google Earth), con una captura del sitio con escala.
3. Explique en dos o tres líneas **por qué lo eligió**: ¿qué amenaza sospecha y qué hay expuesto?

## Parte 2 · Evidencia remota y calificación (20 min)

1. Reúna **al menos cuatro evidencias** del sitio o de su cantón, con fuente y fecha: dos capturas (Street View o imágenes históricas) y dos más entre eventos registrados (ECU 911, SGR), mapas de amenaza del PDOT, notas de prensa o la evidencia climática de la Práctica 1. Si puede, sume una llamada a un habitante (rol, no nombre).
2. **Califique** la hoja de campo: amenazas (0 a 5), exposición, sensibilidad y capacidad (1 a 5).
3. Para cada valor, escriba **la evidencia que lo sostiene** y cuán segura es (alta, media, baja). Ejemplo: «drenaje = 4; Street View de marzo de 2024 muestra alcantarillas tapadas y basura en el cauce; confianza media».
4. Pase los valores a las celdas 5 y 6 de `IA2_02` y compare con el **índice** calculado a mano para su amenaza principal:

   - E = media de la exposición; S = media de la sensibilidad; CA = media de la capacidad
   - V = (S + 6 − CA) / 2
   - R = ∛(A · E · V)
   - Clases: < 1,8 muy bajo · < 2,6 bajo · < 3,4 medio · < 4,2 alto · ≥ 4,2 muy alto

   Indique el **componente dominante** (la exposición o sensibilidad más alta, o la capacidad más baja).

> Recuerde: en la capacidad de adaptación, **5 es bueno**. No la invierta a mano en la hoja; la fórmula ya usa 6 − CA.

## Parte 3 · Opciones de adaptación preliminares (25 min)

Complete esta tabla con **4 opciones** para su sitio. Al menos una debe ser basada en ecosistemas y al menos una, social o institucional.

| # | Opción | Familia (estructural/física, basada en ecosistemas, social, institucional) | Lado del triángulo que acorta (amenaza, exposición, vulnerabilidad) | Sector del PLANACC | Alerta de mala adaptación | ¿También mitiga? (sí/no y por qué) |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |

**Sectores prioritarios del PLANACC:** asentamientos humanos · soberanía alimentaria, agricultura, ganadería, acuacultura y pesca · patrimonio hídrico · patrimonio natural · salud · sectores productivos y estratégicos.

Puede inspirarse en el catálogo del curso ([`herramientas/estrategias.py`](../../../herramientas/estrategias.py)), por ejemplo A01 alerta temprana, A02 drenaje y limpieza de cauces, A03 ordenamiento territorial, A04 bioingeniería en taludes, A05 defensa costera con manglar y dunas, A07 cosecha de agua lluvia, M11 restauración de riberas y M12 manglar. Si propone una opción que no está en el catálogo, la podrá agregar en `IA2_03`.

Cierre con **una frase** que relacione su mejor opción con el componente dominante de la parte 2. Por ejemplo: «La vulnerabilidad pesa más por el drenaje colmatado; por eso la opción 2 va primero, antes que un muro».

## Preguntas de autoevaluación (respóndalas en 3 a 5 líneas cada una)

1. ¿Por qué la frase «el riesgo del sitio es la lluvia de El Niño» es incorrecta según el AR6?
2. Si en su sitio subiera la capacidad de adaptación de 2 a 4 sin cambiar nada más, ¿cuánto bajaría su índice? Haga la cuenta.
3. ¿Cuál de sus cuatro opciones podría trasladar el riesgo a otra comunidad, y cómo lo evitaría?
4. ¿Qué calificación es la más incierta por no haber visitado el sitio, y cómo cambiaría el índice si estuviera un punto arriba o abajo?

## Lista de cotejo antes de entregar

- [ ] Sitio con nombre, cantón, parroquia, coordenadas y motivo de elección.
- [ ] Cuatro o más evidencias remotas, cada una con fuente y fecha (al menos dos capturas).
- [ ] Hoja de campo calificada, cada valor con su evidencia y confianza.
- [ ] Índice y componente dominante (a mano y en `IA2_02`).
- [ ] Tabla de 4 opciones completa, con al menos una basada en ecosistemas y una social o institucional.
- [ ] Respuestas a las tres preguntas.

Este trabajo no se califica por separado. Su contenido pasa a la sección 3 (riesgo del sitio) y a la sección 4 (matriz de estrategias) del borrador del capítulo 2, que sí es la evaluación formativa ([guía y rúbrica](guia_formativa.md)).

## Fuentes

- IPCC (2022). Summary for Policymakers y Annex II: Glossary. En *Climate Change 2022: Impacts, Adaptation and Vulnerability*. Contribución del Grupo de Trabajo II al AR6. Cambridge University Press.
- MAATE (2023). *Plan Nacional de Adaptación al Cambio Climático del Ecuador*. Ministerio del Ambiente, Agua y Transición Ecológica; PNUD; Fondo Verde para el Clima. [Resumen en la CMNUCC](https://unfccc.int/sites/default/files/resource/Brochure_PNA.pdf).
- Crichton, D. (1999). The risk triangle. En J. Ingleton (ed.), *Natural Disaster Management*. Tudor Rose.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados
