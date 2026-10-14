"""Datos preparados por el docente y publicados como releases del repositorio, organizados por provincia.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Releases (un archivo por provincia, todo el periodo, recuadro de la provincia más un margen):
    era5-v1   era5_diario_<provincia>.nc     día local (UTC-5)
    core-v1   core_diario_<provincia>.nc     día 06–06 UTC (01:00–01:00 hora local)
              core_mensual_<provincia>.nc    medias mensuales; pr en mm/mes
Variables: tmed, tmax, tmin (°C), pr (mm/día), hr (%), q (g/kg), ps (hPa), u10, v10 (m/s).

El estudiante descarga solo el archivo de su provincia; si trabaja un cantón, se recorta al
recuadro del cantón y el archivo provincial se borra. Así su Drive guarda solo su zona.
"""
from __future__ import annotations

import os
import pathlib
import shutil
import urllib.request

REPO = "crispaliz/cambio-climatico-espam"
ETIQUETAS = {"era5": "era5-v1", "core": "core-v1"}
RESOLUCION = {"era5": 0.25, "core": 1.875}


def nombre(fuente: str, frecuencia: str, slug_provincia: str) -> str:
    return f"{fuente}_{frecuencia}_{slug_provincia}.nc"


def url(fuente: str, archivo: str) -> str:
    return f"https://github.com/{REPO}/releases/download/{ETIQUETAS[fuente]}/{archivo}"


def _traer(fuente: str, archivo: str, destino: pathlib.Path) -> bool:
    """Descarga un archivo del release (o lo copia de CC_RELEASE_LOCAL, para pruebas)."""
    local = os.environ.get("CC_RELEASE_LOCAL")
    destino.parent.mkdir(parents=True, exist_ok=True)
    try:
        if local:
            shutil.copy(pathlib.Path(local) / archivo, destino)
        else:
            urllib.request.urlretrieve(url(fuente, archivo), destino)
        return True
    except Exception as err:
        print(f"No disponible: {ETIQUETAS[fuente]}/{archivo} ({err})")
        return False


def obtener(fuente: str, frecuencia: str, zona: dict, area, anios, carpeta_datos) -> pathlib.Path | None:
    """Trae el archivo de la provincia, lo recorta al recuadro de la zona y a los años, y lo guarda.

    `zona` es el diccionario de `limites.zona`. Devuelve la ruta del recorte o None si no existe.
    """
    import xarray as xr

    carpeta_datos = pathlib.Path(carpeta_datos)
    salida = carpeta_datos / nombre(fuente, frecuencia, zona["slug"])
    if salida.exists():
        return salida
    from herramientas.limites import slug

    archivo = nombre(fuente, frecuencia, slug(zona["provincia"]))
    tmp = carpeta_datos / f"_tmp_{archivo}"
    if not _traer(fuente, archivo, tmp):
        return None
    n, o, s, e = area
    with xr.open_dataset(tmp) as ds:
        sub = ds.sel(lat=slice(s, n), lon=slice(o, e), time=slice(f"{min(anios)}-01-01", f"{max(anios)}-12-31")).load()
    sub.to_netcdf(salida, encoding={v: {"zlib": True, "complevel": 4} for v in sub.data_vars})
    tmp.unlink()
    return salida


def por_provincia(fuente: str, archivos_anuales, carpeta_salida, mensual=None) -> list[pathlib.Path]:
    """(Docente) Reparte los archivos anuales de Ecuador en un archivo por provincia (todo el periodo).

    Cada archivo cubre el recuadro de la provincia ajustado a la malla de la fuente, con una celda de margen.
    Si se pasa `mensual` (función diario -> mensual), también genera `<fuente>_mensual_<provincia>.nc`.
    """
    import xarray as xr

    from herramientas import limites

    carpeta_salida = pathlib.Path(carpeta_salida)
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    provs = limites.cargar("provincias")
    provs = provs[provs["region"] != "Zona no delimitada"]
    cajas = {limites.slug(r["nombre"]): limites.recuadro(r.geometry, RESOLUCION[fuente], 1) for _, r in provs.iterrows()}
    partes = {s: [] for s in cajas}
    for f in sorted(archivos_anuales):
        with xr.open_dataset(f) as ds:
            for s, (n, o, so, e) in cajas.items():
                partes[s].append(ds.sel(lat=slice(so, n), lon=slice(o, e)).load())
    salidas = []
    for s, lista in partes.items():
        ds = xr.concat(lista, "time")
        enc = {v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in ds.data_vars}
        f = carpeta_salida / nombre(fuente, "diario", s)
        ds.to_netcdf(f, encoding=enc)
        salidas.append(f)
        if mensual is not None:
            fm = carpeta_salida / nombre(fuente, "mensual", s)
            mensual(ds).to_netcdf(fm, encoding=enc)
            salidas.append(fm)
    return salidas
