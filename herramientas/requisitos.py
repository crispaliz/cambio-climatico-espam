"""Comprueba que existan en Drive los productos de los cuadernos anteriores antes de leerlos.

Si falta algo, explica qué cuaderno lo genera y qué zonas sí tiene el estudiante en su Drive,
en lugar de un FileNotFoundError largo de pandas.
"""
from __future__ import annotations

import pathlib

URL = "https://colab.research.google.com/github/crispaliz/cambio-climatico-espam/blob/main/practicas/"
CUADERNO = {
    "inventario.json": ("CR01", URL + "comun/reanalisis/CR01_descarga_reanalisis.ipynb"),
    "serie_diaria": ("CR02", URL + "comun/reanalisis/CR02_series_zona.ipynb"),
    "serie_mensual": ("CR02", URL + "comun/reanalisis/CR02_series_zona.ipynb"),
    "RD1_01": ("RD1_01", URL + "riesgos-desastres/practica-1/RD1_01_ciclo_anual_enso.ipynb"),
    "IA1_01": ("IA1_01", URL + "ambiental/practica-1/IA1_01_climatologia.ipynb"),
    "IA1_03": ("IA1_03", URL + "ambiental/practica-1/IA1_03_tendencias_enso.ipynb"),
}


class FaltanDatos(Exception):
    """Faltan productos de un cuaderno anterior (el mensaje dice cuál ejecutar)."""


def _cuaderno(nombre: str):
    for clave, v in CUADERNO.items():
        if nombre.startswith(clave):
            return v
    return ("el cuaderno anterior", "")


def zonas_con_datos(base) -> list[str]:
    """Carpetas de CC_datos que ya tienen las series de CR02."""
    d = pathlib.Path(base) / "CC_datos"
    if not d.exists():
        return []
    return sorted(p.name for p in d.iterdir() if p.is_dir() and any(p.glob("serie_diaria_*.csv")))


def verificar(base, zona: dict, rutas) -> None:
    """Lanza FaltanDatos con instrucciones si alguna de `rutas` no existe."""
    faltan = [pathlib.Path(r) for r in rutas if not pathlib.Path(r).exists()]
    if not faltan:
        return
    pasos, vistos = [], set()
    for r in faltan:
        nom, url = _cuaderno(r.name)
        if nom not in vistos:
            vistos.add(nom)
            pasos.append(f"   · {nom}: {url}" if url else f"   · {nom}")
    hay = zonas_con_datos(base)
    lineas = [f"Faltan en su Drive productos de cuadernos anteriores para la zona «{zona['nombre']}» (carpeta «{zona['slug']}»):"]
    lineas += [f"   · {r}" for r in faltan]
    lineas += ["", "Qué hacer: ejecute primero, con la MISMA zona de la celda 1 (provincia o cantón), en este orden:"] + pasos
    if hay:
        lineas += ["", f"En su Drive hay series de CR02 para: {', '.join(hay)}.",
                   "Si su zona es una de esas, corrija la celda 1 (nivel provincia o cantón, y el nombre) y vuelva a ejecutar."]
    else:
        lineas += ["", "En su Drive (Mi unidad/CC_datos) no hay series de ninguna zona: o no se ejecutó CR02, o se ejecutó con otra cuenta de Google.",
                   "En equipo, cada integrante debe ejecutar CR01 y CR02 con su propia cuenta (la opción B de CR01 baja los datos ya preparados)."]
    raise FaltanDatos("\n".join(lineas))
