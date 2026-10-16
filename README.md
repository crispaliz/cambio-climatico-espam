# cambio-climatico-espam

Prácticas reproducibles de cambio climático de la ESPAM MFL en Google Colab: reanálisis, datos de estaciones, modelos climáticos y escenarios de cambio climático aplicados al Ecuador.

Docente: Cristian Omar Paliz Acosta, MSc. · ORCID 0000-0002-1738-8131

## Estructura

```
practicas/            cuadernos por asignatura y práctica
  ambiental/            Cambio Climático, Ingeniería Ambiental
  riesgos-desastres/    Cambio Climático, Ingeniería en Riesgos de Desastres
herramientas/         código reutilizable que importan los cuadernos
  limites.py            provincias, cantones, celdas de la zona y pesos por área
  variables.py          humedad relativa y específica, viento y convenciones comunes
  reanalisis/           ERA5, CORe, release de datos por provincia
  publicar.py           (docente) publicación de releases en GitHub
  satelite/             estimaciones satelitales de precipitación
  estaciones/           lectura, control de calidad y métricas
  modelos/              salidas de modelos climáticos
  escenarios/           proyecciones y escenarios
datos/                archivos pequeños y fijos (límites)
```

Los datos grandes (reanálisis, salidas de modelos) no se guardan en el repositorio. Hay dos formas de obtenerlos, y las dos dejan los mismos archivos en el Drive del estudiante:

| | Opción A: `MODO_DATOS = "propio"` | Opción B: `MODO_DATOS = "release"` |
|---|---|---|
| Quién descarga | Cada estudiante, con su cuenta del CDS, en su Colab | El docente, una vez, para todas las provincias |
| Dónde | Su Drive, solo su zona | Release `datos-v1` del repositorio; el estudiante trae su provincia y la recorta |
| ERA5 | Diario y mensual (series por punto, una solicitud por celda) | Diario y mensual |
| CORe | Diario y mensual (o solo mensual, más rápido) | Diario y mensual |

## Cómo trabajar

1. Abra el cuaderno con el botón **Abrir en Colab**.
2. **Archivo › Guardar una copia en Drive**. Trabaje siempre en su copia.
3. Llene solo la celda **1** y ejecute las demás en orden. El cuaderno trae el código de `herramientas/` desde este repositorio.
4. Los resultados se guardan en su Google Drive. Los estudiantes no suben archivos a este repositorio.

## Credenciales

| Fuente | Credencial | Dónde se guarda |
|---|---|---|
| ERA5 (opción A) | API Token **personal** del Climate Data Store: una cuenta por persona | Colab › Secrets, con el nombre `CDSAPI_KEY`, o la variable `CDS_TOKEN` de la celda 1 |
| CORe, release (opción B) | Ninguna | — |
| Publicar el release (solo docente) | Token de GitHub con permiso *Contents: Read and write* sobre este repositorio | Colab › Secrets, con el nombre `GITHUB_TOKEN` |

Cada persona usa su propia cuenta: el CDS limita las solicitudes por cuenta y una cuenta compartida bloquea a todos. Nunca suba un token al repositorio ni comparta un cuaderno que lo tenga escrito.

## Prácticas disponibles

| Asignatura | Práctica | Cuadernos |
|---|---|---|
| Ambiental | 1. Diagnóstico del clima observado (cualquier provincia o cantón; 9 variables) | [practica-1](practicas/ambiental/practica-1/): descarga → series → climatología → estación |

## Preparación de datos (docente)

| Herramienta | Produce |
|---|---|
| `herramientas/reanalisis/preparar_releases.ipynb` (Colab) | Release `datos-v1`: por provincia, `era5_diario`, `era5_mensual`, `era5_terreno`, `core_diario`, `core_mensual` y `manifiesto.json` |
| `python -m herramientas.reanalisis.preparar_releases` (terminal) | Lo mismo, para correrlo en un equipo propio |

Usa el mismo código que la opción A de los estudiantes. Es reanudable: si se corta, se vuelve a ejecutar y sigue donde quedó.

## Derechos

© 2026 Cristian Omar Paliz Acosta. Todos los derechos reservados. Material docente de la ESPAM MFL; su uso fuera de las asignaturas requiere autorización del autor.
