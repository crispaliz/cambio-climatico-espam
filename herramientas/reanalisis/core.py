"""CORe (NOAA/NCEP Conventional Observation Reanalysis): preparación de datos diarios para Ecuador.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Fuente: archivos de flujos de 6 horas del "CDAS look-alike" de CPC, GRIB1, malla gaussiana T62
(192 × 94, ~1,9°), un archivo por hora sinóptica (00, 06, 12, 18 UTC):
    https://ftp.cpc.ncep.noaa.gov/CORe/CDAS_clone_temporary/6hr/grb2d/AAAA/grb2dAAAAMMDDHH
Documentación: https://www.cpc.ncep.noaa.gov/products/CORe/pns/eval/eval_datasets.html
No requiere credenciales.

Optimización y cuidado del servidor:
  - De cada archivo (~1,6 MB, 51 campos) se piden solo los bytes de los 8 campos necesarios,
    agrupados en 4 rangos (~0,4 MB), según el inventario .idx.
  - El inventario se reutiliza mientras la estructura no cambie: cada fragmento debe empezar
    con la marca "GRIB"; si no, se vuelve a leer el .idx de ese archivo.
  - Pocos hilos en paralelo (4 por defecto), reintentos con espera creciente y pausa breve
    entre solicitudes. Todo es reanudable.

Día: archivos de 06, 12 y 18 UTC del día D y de 00 UTC del día D+1, es decir 06–06 UTC
(01:00–01:00 hora de Ecuador).

Variables diarias (release core-v1): tmed, tmax, tmin (°C), pr (mm/día), hr (%), q (g/kg), ps (hPa), u10, v10 (m/s)
q es la humedad específica a 2 m del propio reanálisis (SPFH), promediada en el día.
"""
from __future__ import annotations

import datetime as dt
import pathlib
import random
import threading
import time
import urllib.error
import urllib.request

from herramientas import variables as V

BASE_6H = "https://ftp.cpc.ncep.noaa.gov/CORe/CDAS_clone_temporary/6hr/grb2d"
RECUADRO_ECUADOR = [4.0, -96.0, -7.75, -72.75]  # N, O, S, E: todas las provincias con una celda de ~1,9° de margen

# (variable del inventario, nivel del inventario) -> (nombre interno, código GRIB1 de la tabla 2 de NCEP)
CAMPOS = {
    ("PRATE", "sfc"): ("prate", 59),
    ("PRES", "sfc"): ("pres", 1),
    ("SPFH", "2 m above gnd"): ("spfh", 51),
    ("TMAX", "2 m above gnd"): ("tmax", 15),
    ("TMIN", "2 m above gnd"): ("tmin", 16),
    ("TMP", "2 m above gnd"): ("tmp", 11),
    ("UGRD", "10 m above gnd"): ("ugrd", 33),
    ("VGRD", "10 m above gnd"): ("vgrd", 34),
}
_INVENTARIO = {"regs": None}
_CANDADO = threading.Lock()


def url_6h(momento: dt.datetime) -> str:
    return f"{BASE_6H}/{momento:%Y}/grb2d{momento:%Y%m%d%H}"


# ------------------------------------------------------------------ inventario y descarga parcial
def leer_inventario(texto: str) -> list[dict]:
    """Interpreta un .idx de wgrib: número, byte inicial y final, variable y nivel."""
    regs = []
    for linea in texto.strip().splitlines():
        p = linea.split(":")
        regs.append({"n": int(p[0]), "ini": int(p[1]), "var": p[3], "nivel": p[4], "tiempo": p[5]})
    for a, b in zip(regs, regs[1:]):
        a["fin"] = b["ini"] - 1
    regs[-1]["fin"] = None
    return regs


def seleccion(regs: list[dict], campos=CAMPOS) -> list[dict]:
    sel = [r for r in regs if (r["var"], r["nivel"]) in campos]
    faltan = set(campos) - {(r["var"], r["nivel"]) for r in sel}
    if faltan:
        raise ValueError(f"El inventario no tiene: {sorted(faltan)}")
    return sorted(sel, key=lambda r: r["ini"])


def rangos(sel: list[dict], hueco_max: int = 40_000) -> list[tuple[int, int]]:
    """Agrupa los registros en rangos de bytes, uniendo los separados por menos de `hueco_max`."""
    out = []
    for r in sel:
        if out and r["ini"] - out[-1][1] <= hueco_max:
            out[-1] = (out[-1][0], r["fin"])
        else:
            out.append((r["ini"], r["fin"]))
    return out


def _get(url: str, rango=None, intentos: int = 5, pausa: float = 0.2) -> tuple[bytes, int]:
    """GET con reintentos y espera creciente; respeta 429/503 del servidor."""
    for k in range(intentos):
        try:
            time.sleep(pausa * random.uniform(0.5, 1.5))
            req = urllib.request.Request(url, headers={"User-Agent": "cambio-climatico-espam (docencia ESPAM MFL)"})
            if rango:
                req.add_header("Range", f"bytes={rango[0]}-{rango[1]}")
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read(), r.status
        except urllib.error.HTTPError as err:
            if err.code == 404 or k == intentos - 1:
                raise
            espera = int(err.headers.get("Retry-After", 0) or 0) or 5 * 2 ** k
        except Exception:
            if k == intentos - 1:
                raise
            espera = 5 * 2 ** k
        time.sleep(espera)


def _inventario(url: str, refrescar: bool = False) -> list[dict]:
    with _CANDADO:
        if refrescar or _INVENTARIO["regs"] is None:
            texto, _ = _get(url + ".idx")
            _INVENTARIO["regs"] = seleccion(leer_inventario(texto.decode()))
        return _INVENTARIO["regs"]


def descargar_campos(momento: dt.datetime, carpeta) -> pathlib.Path:
    """Descarga solo los 8 campos de un archivo de 6 h y guarda un GRIB1 con exactamente esos mensajes."""
    carpeta = pathlib.Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    f = carpeta / f"core_{momento:%Y%m%d%H}.grb"
    if f.exists() and f.stat().st_size > 0:
        return f
    url = url_6h(momento)
    for intento in (False, True):  # segundo intento: inventario propio de este archivo
        sel = _inventario(url, refrescar=intento)
        piezas, ok = [], True
        for ini, fin in rangos(sel):
            datos, estado = _get(url, (ini, fin))
            if estado == 200:  # el servidor ignoró el rango: se recorta del archivo completo
                datos = datos[ini:fin + 1]
            for r in (r for r in sel if ini <= r["ini"] <= fin):
                trozo = datos[r["ini"] - ini: r["fin"] - ini + 1]
                if trozo[:4] != b"GRIB":
                    ok = False
                    break
                piezas.append(trozo)
            if not ok:
                break
        if ok:
            f.write_bytes(b"".join(piezas))
            return f
    raise RuntimeError(f"No se pudieron extraer los campos de {url}")


# ------------------------------------------------------------------ lectura y agregación
def leer_6h(ruta):
    """Lee los 8 campos de un archivo de 6 h con cfgrib y devuelve un Dataset (latitude, longitude)."""
    import xarray as xr

    vars_ = {}
    for nombre, codigo in CAMPOS.values():
        ds = xr.open_dataset(ruta, engine="cfgrib", backend_kwargs={
            "filter_by_keys": {"indicatorOfParameter": codigo}, "indexpath": ""})
        da = ds[list(ds.data_vars)[0]]
        vars_[nombre] = da.drop_vars([c for c in da.coords if c not in ("latitude", "longitude")])
    return xr.Dataset(vars_)


def recortar(ds, recuadro=RECUADRO_ECUADOR):
    """Nombres lat/lon, longitudes en -180..180, latitudes crecientes y recorte al recuadro."""
    ren = {k: v for k, v in {"latitude": "lat", "longitude": "lon"}.items() if k in ds.dims or k in ds.coords}
    ds = ds.rename(ren)
    if float(ds["lon"].max()) > 180:
        ds = ds.assign_coords(lon=((ds["lon"] + 180) % 360) - 180)
    ds = ds.sortby("lon").sortby("lat")
    n, o, s, e = recuadro
    return ds.sel(lat=slice(s, n), lon=slice(o, e))


def a_diario(seis_horas: list, fecha: dt.date):
    """Agrega los 4 Dataset de 6 h de un día a las variables de trabajo."""
    import pandas as pd
    import xarray as xr

    if len(seis_horas) != 4:
        raise ValueError(f"{fecha}: se esperaban 4 periodos de 6 h y hay {len(seis_horas)}")
    d = xr.concat(seis_horas, "paso")
    t_c = d["tmp"] - 273.15
    p_hpa = d["pres"] / 100
    out = xr.Dataset({
        "tmed": t_c.mean("paso"),
        "tmax": d["tmax"].max("paso") - 273.15,
        "tmin": d["tmin"].min("paso") - 273.15,
        "pr": (d["prate"] * 21600).sum("paso"),
        "hr": V.hr_desde_especifica(d["spfh"], t_c, p_hpa).mean("paso"),
        "q": (d["spfh"] * 1000).mean("paso"),
        "ps": p_hpa.mean("paso"),
        "u10": d["ugrd"].mean("paso"),
        "v10": d["vgrd"].mean("paso"),
    }).expand_dims(time=[pd.Timestamp(fecha)])
    return V.anotar(out)


def horas_del_dia(fecha: dt.date) -> list[dt.datetime]:
    """Archivos de 6 h que forman el día 06–06 UTC (01:00–01:00 hora de Ecuador)."""
    d0 = dt.datetime(fecha.year, fecha.month, fecha.day)
    return [d0 + dt.timedelta(hours=h) for h in (6, 12, 18, 24)]


def dia(fecha: dt.date, carpeta_trabajo, recuadro=RECUADRO_ECUADOR, borrar_grib: bool = True):
    """Descarga, recorta y agrega un día."""
    partes = []
    for momento in horas_del_dia(fecha):
        f = descargar_campos(momento, carpeta_trabajo)
        partes.append(recortar(leer_6h(f), recuadro).load())
        if borrar_grib:
            f.unlink(missing_ok=True)
    return a_diario(partes, fecha)


def preparar_diario(anios, carpeta_trabajo, carpeta_salida, hilos: int = 4, recuadro=RECUADRO_ECUADOR) -> list[pathlib.Path]:
    """(Docente) Un NetCDF diario por año. Reanudable: salta los años ya guardados."""
    from concurrent.futures import ThreadPoolExecutor

    import pandas as pd
    import xarray as xr

    carpeta_salida = pathlib.Path(carpeta_salida)
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    salidas = []
    for a in anios:
        f = carpeta_salida / f"core_ecuador_diario_{a}.nc"
        if not f.exists():
            t0 = time.time()
            fechas = [d.date() for d in pd.date_range(f"{a}-01-01", f"{a}-12-31", freq="D")]
            with ThreadPoolExecutor(hilos) as ex:
                dias = list(ex.map(lambda d: dia(d, carpeta_trabajo, recuadro), fechas))
            ds = xr.concat(dias, "time")
            ds.attrs = {"title": f"CORe diario para Ecuador, {a}",
                        "source": "NOAA/NCEP CPC, CORe, CDAS look-alike, flujos de 6 h (GRIB1, T62)",
                        "url": BASE_6H, "day": "06–06 UTC (01:00–01:00 hora de Ecuador)",
                        "processing": "herramientas/reanalisis/core.py"}
            ds.to_netcdf(f, encoding={v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in ds.data_vars})
            print(f"guardado {f.name} en {(time.time() - t0) / 60:.1f} min")
        salidas.append(f)
    return salidas


def mensual_desde_diario(ds, min_dias: int = 28):
    """Medias mensuales (pr: total mensual en mm/mes). Meses con menos de `min_dias` válidos quedan vacíos."""
    g = ds.resample(time="MS")
    n = ds["tmed"].notnull().resample(time="MS").sum()
    out = g.mean()
    out["pr"] = g.sum(min_count=1)["pr"]
    out = V.anotar(out.where(n >= min_dias))
    out["pr"].attrs["units"] = "mm/mes"
    return out
