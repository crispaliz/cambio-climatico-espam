"""Límites provinciales y cantonales del Ecuador: selección, recuadro de descarga y máscara.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.
"""
from __future__ import annotations

import pathlib
import unicodedata

import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parents[1]
CAPAS = {
    "provincias": RAIZ / "datos" / "limites" / "ecuador_provincias.geojson",
    "cantones": RAIZ / "datos" / "limites" / "ecuador_cantones.geojson",
}


def normalizar(texto: str) -> str:
    """Minúsculas, sin tildes y sin espacios repetidos: 'Los Ríos' -> 'los rios'."""
    t = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return " ".join(t.lower().replace("provincia de", "").split())


def slug(texto: str) -> str:
    """Nombre apto para archivos: 'Santo Domingo de los Tsáchilas' -> 'santo_domingo_de_los_tsachilas'."""
    return "_".join(normalizar(texto).split())


def cargar(capa: str = "provincias"):
    """Lee la capa de provincias o de cantones (GeoJSON simplificado, EPSG:4326)."""
    import geopandas as gpd

    return gpd.read_file(CAPAS[capa])


def provincia(nombre: str):
    """Devuelve (fila, geometría) de una provincia; acepta el nombre con o sin tildes."""
    gdf = cargar("provincias")
    sel = gdf[gdf["nombre"].map(normalizar) == normalizar(nombre)]
    if sel.empty:
        raise ValueError(f"No encontré '{nombre}'. Opciones: {sorted(gdf['nombre'])}")
    return sel.iloc[0], sel.geometry.iloc[0]


def canton(nombre: str, provincia_nombre: str | None = None):
    """Devuelve (fila, geometría) de un cantón; la provincia desambigua nombres repetidos."""
    gdf = cargar("cantones")
    sel = gdf[gdf["nombre_dpa"].map(normalizar) == normalizar(nombre)]
    if provincia_nombre:
        sel = sel[sel["provincia"].map(normalizar) == normalizar(provincia_nombre)]
    if sel.empty:
        raise ValueError(f"No encontré el cantón '{nombre}'.")
    if len(sel) > 1:
        raise ValueError(f"'{nombre}' existe en varias provincias: {sorted(sel['provincia'])}. Indique la provincia.")
    return sel.iloc[0], sel.geometry.iloc[0]


def recuadro(geom, resolucion: float = 0.25, margen_celdas: int = 1) -> list[float]:
    """Recuadro [N, O, S, E] que contiene la geometría, ajustado a la malla y con un margen.

    Es el parámetro `area` de las solicitudes al Climate Data Store.
    """
    o, s, e, n = geom.bounds
    r, m = resolucion, margen_celdas * resolucion
    return [
        round(float(np.ceil(n / r) * r + m), 4),
        round(float(np.floor(o / r) * r - m), 4),
        round(float(np.floor(s / r) * r - m), 4),
        round(float(np.ceil(e / r) * r + m), 4),
    ]


def mascara(da, geom, min_celdas: int = 4):
    """Máscara booleana (lat, lon) de las celdas cuyo centro cae dentro de la geometría.

    Si hay menos de `min_celdas` centros dentro (provincias pequeñas o mallas gruesas),
    usa las celdas que tocan el recuadro de la geometría. Devuelve (máscara, n_celdas, método).
    """
    import regionmask

    reg = regionmask.Regions([geom], names=["zona"], abbrevs=["Z"])
    m = reg.mask(da["lon"], da["lat"]) == 0
    n = int(m.sum())
    if n >= min_celdas:
        return m, n, "centros dentro del límite"
    dlat = float(abs(da["lat"].diff("lat").median()))
    dlon = float(abs(da["lon"].diff("lon").median()))
    o, s, e, nn = geom.bounds
    m = ((da["lat"] >= s - dlat / 2) & (da["lat"] <= nn + dlat / 2)
         & (da["lon"] >= o - dlon / 2) & (da["lon"] <= e + dlon / 2))
    return m, int(m.sum()), "celdas que tocan el recuadro del límite"


def promedio_area(da, masc):
    """Promedio espacial ponderado por el coseno de la latitud dentro de la máscara."""
    peso = np.cos(np.deg2rad(da["lat"]))
    return da.where(masc).weighted(peso).mean(["lat", "lon"])


def zona(provincia_nombre: str, canton_nombre: str | None = None) -> dict:
    """Zona de trabajo: una provincia o, si se indica, un cantón de esa provincia.

    Devuelve un diccionario con nombre, slug (para carpetas), tipo, código DPA, región y geometría.
    """
    fila_p, geom_p = provincia(provincia_nombre)
    if canton_nombre:
        fila_c, geom = canton(canton_nombre, fila_p["nombre"])
        nombre = f"{fila_c['nombre_dpa'].title()} ({fila_p['nombre']})"
        return {"nombre": nombre, "slug": f"{slug(fila_p['nombre'])}__{slug(fila_c['nombre_dpa'])}",
                "tipo": "cantón", "codigo": fila_c["codigo"], "provincia": fila_p["nombre"],
                "region": fila_p["region"], "geom": geom}
    return {"nombre": fila_p["nombre"], "slug": slug(fila_p["nombre"]), "tipo": "provincia",
            "codigo": fila_p["codigo"], "provincia": fila_p["nombre"], "region": fila_p["region"], "geom": geom_p}
