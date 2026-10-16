"""Opción B: datos preparados por el docente y publicados como un release del repositorio.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Un solo release de datos (etiqueta `ETIQUETA`, p. ej. `datos-v1`) con cinco archivos por provincia:

    era5_diario_<provincia>.nc     día local (UTC-5), 00–24 h, celdas de 0,25° que tocan la provincia
    era5_mensual_<provincia>.nc    medias mensuales de las diarias; pr en mm/mes
    era5_terreno_<provincia>.nc    altura del terreno del modelo (m), recuadro de la provincia
    core_diario_<provincia>.nc     día 06–06 UTC (01:00–01:00 hora local), recuadro de la provincia
    core_mensual_<provincia>.nc    medias mensuales de las diarias; pr en mm/mes
    manifiesto.json                tamaño, suma SHA-256, periodo y versión de cada archivo

Los nombres de los archivos que quedan en el Drive del estudiante son los mismos en las dos opciones
(`<fuente>_<frecuencia>_<zona>.nc`), así que el cuaderno común CR02 y las prácticas de cada carrera no distinguen de dónde vinieron.
El estudiante descarga solo el archivo de su provincia; si trabaja un cantón, se recorta al recuadro
del cantón y el archivo provincial se borra.
"""
from __future__ import annotations

import os
import pathlib
import shutil
import urllib.request

REPO = "crispaliz/cambio-climatico-espam"
ETIQUETA = os.environ.get("CC_DATOS_TAG", "datos-v1")
PRODUCTOS = [("era5", "diario"), ("era5", "mensual"), ("era5", "terreno"), ("core", "diario"), ("core", "mensual")]
RESOLUCION = {"era5": 0.25, "core": 1.875}


def nombre(fuente: str, frecuencia: str, slug_zona: str) -> str:
    return f"{fuente}_{frecuencia}_{slug_zona}.nc"


def url(archivo: str, etiqueta: str | None = None) -> str:
    return f"https://github.com/{REPO}/releases/download/{etiqueta or ETIQUETA}/{archivo}"


def _traer(archivo: str, destino: pathlib.Path, etiqueta: str | None = None) -> bool:
    """Descarga un archivo del release (o lo copia de CC_RELEASE_LOCAL, para pruebas)."""
    local = os.environ.get("CC_RELEASE_LOCAL")
    destino.parent.mkdir(parents=True, exist_ok=True)
    parcial = destino.with_suffix(destino.suffix + ".parcial")
    try:
        if local:
            shutil.copy(pathlib.Path(local) / archivo, parcial)
        else:
            urllib.request.urlretrieve(url(archivo, etiqueta), parcial)
        parcial.rename(destino)
        return True
    except Exception as err:
        parcial.unlink(missing_ok=True)
        print(f"No disponible: {etiqueta or ETIQUETA}/{archivo} ({err})")
        return False


def obtener(fuente: str, frecuencia: str, zona: dict, area, anios, carpeta_datos,
            etiqueta: str | None = None) -> pathlib.Path | None:
    """Trae el archivo de la provincia, lo recorta al recuadro de la zona y a los años, y lo guarda.

    `zona` es el diccionario de `limites.zona`. Devuelve la ruta del recorte o None si no existe.
    """
    import xarray as xr

    from herramientas.limites import slug

    carpeta_datos = pathlib.Path(carpeta_datos)
    salida = carpeta_datos / nombre(fuente, frecuencia, zona["slug"])
    if salida.exists():
        return salida
    archivo = nombre(fuente, frecuencia, slug(zona["provincia"]))
    tmp = carpeta_datos / f"_tmp_{archivo}"
    if not tmp.exists() and not _traer(archivo, tmp, etiqueta):
        return None
    n, o, s, e = area
    with xr.open_dataset(tmp) as ds:
        ds = ds.sortby("lat").sortby("lon")
        sub = ds.sel(lat=slice(s, n), lon=slice(o, e))
        if "time" in sub.dims:
            sub = sub.sel(time=slice(f"{min(anios)}-01-01", f"{max(anios)}-12-31"))
        sub = sub.load()
    sub.attrs["origen"] = f"release {etiqueta or ETIQUETA} de {REPO}: {archivo}, recortado a {zona['nombre']}"
    sub.to_netcdf(salida, encoding={v: {"zlib": True, "complevel": 4} for v in sub.data_vars})
    tmp.unlink()
    return salida


def por_provincia(fuente: str, archivos_anuales, carpeta_salida, mensual=None, provincias=None) -> list[pathlib.Path]:
    """(Docente) Reparte los archivos anuales de Ecuador en un archivo por provincia (todo el periodo).

    Cada archivo cubre el recuadro de la provincia ajustado a la malla de la fuente, con una celda de margen.
    Si se pasa `mensual` (función diario -> mensual), también genera `<fuente>_mensual_<provincia>.nc`.
    `provincias`: lista de nombres; None = todas.
    """
    import xarray as xr

    from herramientas import limites

    carpeta_salida = pathlib.Path(carpeta_salida)
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    provs = limites.cargar("provincias")
    provs = provs[provs["region"] != "Zona no delimitada"]
    if provincias:
        quiero = {limites.slug(p) for p in provincias}
        provs = provs[provs["nombre"].map(limites.slug).isin(quiero)]
    cajas = {limites.slug(r["nombre"]): limites.recuadro(r.geometry, RESOLUCION[fuente], 1) for _, r in provs.iterrows()}
    partes = {s: [] for s in cajas}
    for f in sorted(archivos_anuales):
        with xr.open_dataset(f) as ds:
            for s, (n, o, so, e) in cajas.items():
                partes[s].append(ds.sel(lat=slice(so, n), lon=slice(o, e)).load())
    salidas = []
    for s, lista in partes.items():
        ds = xr.concat(lista, "time")
        ds.attrs["title"] = f"{fuente.upper()} diario, provincia {s}"
        enc = {v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in ds.data_vars}
        f = carpeta_salida / nombre(fuente, "diario", s)
        ds.to_netcdf(f, encoding=enc)
        salidas.append(f)
        if mensual is not None:
            fm = carpeta_salida / nombre(fuente, "mensual", s)
            mensual(ds).to_netcdf(fm, encoding=enc)
            salidas.append(fm)
    return salidas
