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


def fracciones(geom, lat, lon, resolucion: float = 0.25):
    """Fracción (0–1) de cada celda de la malla (centros lat, lon) que cae dentro de la geometría.

    Permite que cada celda pese en el promedio según la parte del territorio que cubre:
    una celda mitad mar y mitad provincia pesa la mitad. Devuelve un DataArray (lat, lon).
    """
    import shapely
    import xarray as xr

    lat, lon = np.asarray(lat, dtype=float), np.asarray(lon, dtype=float)
    LO, LA = np.meshgrid(lon, lat)
    h = resolucion / 2
    cajas = shapely.box(LO - h, LA - h, LO + h, LA + h)
    shapely.prepare(geom)
    frac = shapely.area(shapely.intersection(geom, cajas)) / (resolucion ** 2)
    return xr.DataArray(np.clip(frac, 0, 1), coords={"lat": lat, "lon": lon}, dims=("lat", "lon"), name="fraccion")


def celdas(geom, resolucion: float = 0.25, minimo: float = 1e-3):
    """Celdas de la malla (centros múltiplos de `resolucion`) que tocan la geometría, con su fracción."""
    import pandas as pd

    n, o, s, e = recuadro(geom, resolucion, margen_celdas=0)
    lat = np.round(np.arange(s, n + 1e-9, resolucion), 4)
    lon = np.round(np.arange(o, e + 1e-9, resolucion), 4)
    fr = fracciones(geom, lat, lon, resolucion).to_series().rename("fraccion").reset_index()
    return fr[fr["fraccion"] > minimo].reset_index(drop=True)


def promedio_ponderado(da, frac):
    """Promedio espacial ponderado por la fracción de área dentro de la zona y por el coseno de la latitud.

    `frac` puede estar en otra malla: se toma la fracción de la celda más cercana a cada punto de `da`.
    """
    f = frac.reindex(lat=da["lat"], lon=da["lon"], method="nearest", tolerance=1e-6).fillna(0)
    return da.weighted(f * np.cos(np.deg2rad(da["lat"]))).mean(["lat", "lon"])


# ------------------------------------------------------------------ ayuda para elegir la zona
def tabla_zonas(provincia_nombre: str | None = None):
    """Provincias (si `provincia_nombre` es None) o cantones de una provincia, con lo necesario para elegir.

    Columnas: código DPA, nombre tal como se elige en la celda 1, región o provincia, superficie (km²)
    y número de celdas de ERA5 (0,25°) que tocan la zona.
    """
    import pandas as pd

    if provincia_nombre is None:
        gdf = cargar("provincias")
        gdf = gdf[gdf["region"] != "Zona no delimitada"]
        nombres, extra = gdf["nombre"], ("región", gdf["region"])
    else:
        fila_p, _ = provincia(provincia_nombre)
        gdf = cargar("cantones")
        gdf = gdf[gdf["provincia"] == fila_p["nombre"]]
        nombres, extra = gdf["nombre_dpa"].str.title(), ("provincia", gdf["provincia"])
    km2 = gdf.to_crs(32717).area / 1e6
    out = pd.DataFrame({"código DPA": gdf["codigo"].values, "nombre": nombres.values, extra[0]: extra[1].values,
                        "superficie_km2": km2.round(0).astype(int).values,
                        "celdas_ERA5": [len(celdas(g, 0.25)) for g in gdf.geometry]})
    out = out.iloc[out["nombre"].map(normalizar).argsort().values]
    return out.reset_index(drop=True).rename_axis("n.º").rename(lambda i: i + 1)


def mapa_zonas(zona_sel: dict, ax=None):
    """Mapa de la provincia con sus cantones numerados (o del país, si la zona es una provincia)."""
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(7, 7))
    if zona_sel["tipo"] == "provincia":
        gdf = cargar("provincias")
        insular = zona_sel["nombre"] == "Galápagos"  # Galápagos se muestra sola; el continente, sin ella
        gdf = gdf[(gdf["region"] != "Zona no delimitada") & ((gdf["nombre"] == "Galápagos") == insular)]
        etiqueta = gdf["nombre"]
        titulo = f"Provincias del Ecuador {'insular' if insular else 'continental'} · elegida: {zona_sel['nombre']}"
    else:
        gdf = cargar("cantones")
        gdf = gdf[gdf["provincia"] == zona_sel["provincia"]]
        etiqueta = gdf["nombre_dpa"].str.title()
        titulo = f"Cantones de {zona_sel['provincia']} · elegido: {zona_sel['nombre']}"
    gdf.plot(ax=ax, color="#EDEDED", edgecolor="0.45", linewidth=0.5)
    import geopandas as gpd

    gpd.GeoSeries([zona_sel["geom"]]).plot(ax=ax, color="#F2A65A", edgecolor="k", linewidth=1)
    for nombre, g in zip(etiqueta, gdf.geometry):
        p = g.representative_point()
        ax.annotate(nombre.replace(" de los ", "\nde los "), (p.x, p.y), ha="center", va="center", fontsize=6.5)
    ax.set_title(titulo, fontsize=10)
    ax.set_xlabel("Longitud"); ax.set_ylabel("Latitud")
    return ax
