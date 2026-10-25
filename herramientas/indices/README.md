# herramientas/indices

| Módulo | Contenido |
|---|---|
| `enso.py` | ONI e ICEN desde NOAA CPC (ERSSTv5, base 1991–2020), fase mensual con regla de persistencia, tabla de episodios y agregación por temporada |
| `extremos.py` | Índices ETCCDI de precipitación y temperatura, tendencia (pendiente de Sen y Mann-Kendall; `mann_kendall` corrige la significancia por autocorrelación de orden 1 con el tamaño de muestra efectivo n_e = n(1−r1)/(1+r1), siguiendo a Yue y Wang, 2004; `tendencia` reporta el p corregido y el clásico), niveles de retorno (GEV por máxima verosimilitud generalizada con previa sobre la forma, Martins y Stedinger, 2000, e intervalo por remuestreo), acumulados previos a un evento y mayores lluvias independientes |

Las categorías del ICEN (`UMBRALES_ICEN`, `MESES_ICEN`) siguen la Nota Técnica ENFEN; verifíquelas con la versión vigente antes de publicar resultados.
