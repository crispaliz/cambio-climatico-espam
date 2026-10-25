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

Dos usos:
  - Opción A, diario (cada estudiante, `diario_zona`): 4 archivos de 6 h por día, de cada uno solo los
    8 campos (~0,4 MB). Para 1981–2024 son ~64 000 solicitudes y ~25 GB transferidos (en el Drive
    queda solo el recorte de la zona, unos pocos MB): varias horas, reanudable por mes.
  - Opción A, solo mensual (`mensual_zona`): un archivo de promedios por mes, 6 campos (~0,2 MB):
    528 solicitudes para 1981–2024, minutos. Sin Tmax ni Tmin.
  - Opción B (docente, `preparar_diario`): el mismo diario para todo Ecuador, que luego se reparte por
    provincia y se publica en el release de datos.

Variables diarias: tmed, tmax, tmin (°C), pr (mm/día), hr (%), q (g/kg), ps (hPa), u10, v10, ws (m/s).
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

import numpy as np

from herramientas import variables as V

BASE_6H = "https://ftp.cpc.ncep.noaa.gov/CORe/CDAS_clone_temporary/6hr/grb2d"
BASE_MES = "https://ftp.cpc.ncep.noaa.gov/CORe/CDAS_clone_temporary/month/grb2d"
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
# Campos de los promedios mensuales: sin TMAX/TMIN, porque su media mensual de máximos de 6 h no es
# comparable con la media de las máximas diarias.
CAMPOS_MES = {k: v for k, v in CAMPOS.items() if k[0] not in ("TMAX", "TMIN")}
_INVENTARIO = {}
_CANDADO = threading.Lock()


def url_6h(momento: dt.datetime) -> str:
    return f"{BASE_6H}/{momento:%Y}/grb2d{momento:%Y%m%d%H}"


def url_mes(anio: int, mes: int) -> str:
    """Archivo de promedios mensuales de flujos: grb2dAAAAMM (verificado en el servidor de CPC, oct. 2026)."""
    return f"{BASE_MES}/grb2d{anio}{mes:02d}"


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
                req.add_header("Range", f"bytes={rango[0]}-{'' if rango[1] is None else rango[1]}")
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


def _inventario(url: str, campos, clave: str, refrescar: bool = False) -> list[dict]:
    with _CANDADO:
        if refrescar or clave not in _INVENTARIO:
            texto, _ = _get(url + ".idx")
            _INVENTARIO[clave] = seleccion(leer_inventario(texto.decode()), campos)
        return _INVENTARIO[clave]


def descargar_campos(momento: dt.datetime, carpeta) -> pathlib.Path:
    """Descarga solo los 8 campos de un archivo de 6 h y guarda un GRIB1 con exactamente esos mensajes."""
    f = pathlib.Path(carpeta) / f"core_{momento:%Y%m%d%H}.grb"
    return extraer(url_6h(momento), f, CAMPOS, "6h")


def _mensaje(trozo: bytes, codigo: int) -> bytes | None:
    """Devuelve el mensaje GRIB1 completo si es del parámetro esperado; si no, None.

    Comprueba la marca 'GRIB', la edición 1, que el largo total (octetos 5–7 de la sección 0) quepa en el
    trozo y el código de parámetro (octeto 9 de la sección 1). Los archivos de CPC traen 8 bytes de relleno
    entre mensajes (marcas de registro), que aquí se descartan. Así un inventario reutilizado de otro
    archivo nunca entrega un campo equivocado.
    """
    if len(trozo) < 28 or trozo[:4] != b"GRIB" or trozo[7] != 1 or trozo[16] != codigo:
        return None
    largo = int.from_bytes(trozo[4:7], "big")
    if largo > len(trozo) or trozo[largo - 4:largo] != b"7777":
        return None
    return trozo[:largo]


def extraer(url: str, f: pathlib.Path, campos, clave: str) -> pathlib.Path:
    """Guarda en `f` solo los mensajes GRIB de `campos`, pidiendo al servidor únicamente esos bytes."""
    f = pathlib.Path(f)
    f.parent.mkdir(parents=True, exist_ok=True)
    if f.exists() and f.stat().st_size > 0:
        return f
    for intento in (False, True):  # segundo intento: inventario propio de este archivo
        sel = _inventario(url, campos, clave, refrescar=intento)
        piezas, ok = [], True
        for ini, fin in rangos(sel):
            datos, estado = _get(url, (ini, fin))
            if estado == 200:  # el servidor ignoró el rango: se recorta del archivo completo
                datos = datos[ini:] if fin is None else datos[ini:fin + 1]
            for r in (r for r in sel if ini <= r["ini"] and (fin is None or r["ini"] <= fin)):
                trozo = datos[r["ini"] - ini:] if r["fin"] is None else datos[r["ini"] - ini: r["fin"] - ini + 1]
                msj = _mensaje(trozo, campos[(r["var"], r["nivel"])][1])
                if msj is None:
                    ok = False
                    break
                piezas.append(msj)
            if not ok:
                break
        if ok:
            f.write_bytes(b"".join(piezas))
            return f
    raise RuntimeError(f"No se pudieron extraer los campos de {url}")


# ------------------------------------------------------------------ lectura y agregación
def leer_6h(ruta, campos=CAMPOS):
    """Lee los campos de un archivo GRIB1 de CORe y devuelve un Dataset (latitude, longitude).

    Usa eccodes directamente: un solo recorrido del archivo, ~1 ms por campo (cfgrib abre el archivo
    una vez por campo y es decenas de veces más lento, lo que importa con decenas de miles de archivos).
    """
    import eccodes as ec
    import xarray as xr

    nombres = {codigo: nombre for nombre, codigo in campos.values()}
    vars_, lat, lon = {}, None, None
    with open(ruta, "rb") as fh:
        while (h := ec.codes_grib_new_from_file(fh)) is not None:
            try:
                codigo = ec.codes_get(h, "indicatorOfParameter")
                if codigo in nombres:
                    nj, ni = ec.codes_get(h, "Nj"), ec.codes_get(h, "Ni")
                    if lat is None:
                        lat = ec.codes_get_array(h, "distinctLatitudes")
                        lon = ec.codes_get_array(h, "distinctLongitudes")
                    v = ec.codes_get_values(h).reshape(nj, ni)
                    if ec.codes_get(h, "jScansPositively") == 1:  # malla de sur a norte
                        lat_m = np.sort(lat)
                    else:
                        lat_m = np.sort(lat)[::-1]
                    vars_[nombres[codigo]] = (("latitude", "longitude"), v.astype("float32"), {"lat": lat_m})
            finally:
                ec.codes_release(h)
    faltan = set(nombres.values()) - set(vars_)
    if faltan:
        raise ValueError(f"{ruta}: faltan campos {sorted(faltan)}")
    lat_m = next(iter(vars_.values()))[2]["lat"]
    return xr.Dataset({k: (d, v) for k, (d, v, _) in vars_.items()}, coords={"latitude": lat_m, "longitude": lon})


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
        "ws": np.hypot(d["ugrd"], d["vgrd"]).mean("paso"),  # media de las velocidades de cada 6 h (escalar)
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


def _mes(anio: int, mes: int, carpeta_grib, recuadro, ex):
    """Un mes diario: los hilos solo descargan los 6 h; la lectura GRIB y la agregación van en serie."""
    import pandas as pd
    import xarray as xr

    fechas = [d.date() for d in pd.date_range(f"{anio}-{mes:02d}-01", periods=pd.Period(f"{anio}-{mes:02d}").days_in_month)]
    list(ex.map(lambda h: descargar_campos(h, carpeta_grib), [h for d in fechas for h in horas_del_dia(d)]))
    return xr.concat([dia(d, carpeta_grib, recuadro) for d in fechas], "time")


def meses_diarios(anios, recuadro, carpeta_meses, hilos: int = 4, avance: bool = True, etiqueta: str = "CORe"):
    """Genera (reanudable) un NetCDF diario por mes para el recuadro y devuelve sus rutas en orden."""
    from concurrent.futures import ThreadPoolExecutor

    carpeta_meses = pathlib.Path(carpeta_meses)
    carpeta_meses.mkdir(parents=True, exist_ok=True)
    grib = carpeta_meses / "_grib"
    meses = [(a, m) for a in anios for m in range(1, 13)]
    rutas, hechos, t0 = [], 0, time.time()
    with ThreadPoolExecutor(hilos) as ex:
        for k, (a, m) in enumerate(meses, 1):
            f = carpeta_meses / f"d_{a}{m:02d}.nc"
            if not f.exists():
                ds = _mes(a, m, grib, recuadro, ex)
                ds.to_netcdf(f.with_suffix(".parcial"),
                             encoding={v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in ds.data_vars})
                f.with_suffix(".parcial").rename(f)
                hechos += 1
                if avance and (hechos in (1, 3) or k % 12 == 0 or k == len(meses) or len(meses) <= 12):
                    por_mes = (time.time() - t0) / hechos
                    print(f"  {etiqueta}: {k}/{len(meses)} meses · {por_mes / 60:.1f} min por mes · "
                          f"faltan ~{por_mes * (len(meses) - k) / 3600:.1f} h")
            rutas.append(f)
    return rutas


def juntar(rutas):
    """Une archivos NetCDF por tiempo, cargándolos en memoria y cerrándolos."""
    import xarray as xr

    partes = []
    for f in rutas:
        with xr.open_dataset(f) as ds:
            partes.append(ds.load())
    return xr.concat(partes, "time")


def diario_zona(area, anios, carpeta_datos, slug: str, hilos: int = 4, avance: bool = True) -> dict:
    """(Opción A) CORe DIARIO y mensual para el recuadro de la zona, desde los archivos de 6 h.

    Para cada día se piden 4 archivos globales de 6 h, y de cada uno solo los bytes de los 8 campos
    (~0,4 MB): 1 461 archivos por año. Se guarda un archivo por mes (reanudable) y se borran los GRIB.
    Devuelve {"diario": ruta, "mensual": ruta}.
    """
    import xarray as xr

    carpeta_datos = pathlib.Path(carpeta_datos)
    rutas = meses_diarios(anios, area, carpeta_datos / "_dias_core", hilos, avance)
    ds = juntar(rutas)
    ds.attrs = {"title": f"CORe diario, {slug}", "source": "NOAA/NCEP CPC, CORe, CDAS look-alike, flujos de 6 h (GRIB1, T62)",
                "url": BASE_6H, "day": "06–06 UTC (01:00–01:00 hora de Ecuador)",
                "processing": "herramientas/reanalisis/core.py: diario_zona"}
    enc = {v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in ds.data_vars}
    f_d, f_m = carpeta_datos / f"core_diario_{slug}.nc", carpeta_datos / f"core_mensual_{slug}.nc"
    ds.to_netcdf(f_d, encoding=enc)
    mensual_desde_diario(ds).to_netcdf(f_m, encoding=enc)
    return {"diario": f_d, "mensual": f_m}


def preparar_diario(anios, carpeta_trabajo, carpeta_salida, hilos: int = 4, recuadro=RECUADRO_ECUADOR,
                    avance: bool = False) -> list[pathlib.Path]:
    """(Docente) Un NetCDF diario por año para Ecuador. Reanudable por mes."""
    import xarray as xr

    carpeta_salida = pathlib.Path(carpeta_salida)
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    salidas = []
    for a in anios:
        f = carpeta_salida / f"core_ecuador_diario_{a}.nc"
        if not f.exists():
            t0 = time.time()
            rutas = meses_diarios([a], recuadro, pathlib.Path(carpeta_trabajo) / "meses", hilos, avance=avance, etiqueta=f"CORe {a}")
            ds = juntar(rutas)
            ds.attrs = {"title": f"CORe diario para Ecuador, {a}",
                        "source": "NOAA/NCEP CPC, CORe, CDAS look-alike, flujos de 6 h (GRIB1, T62)",
                        "url": BASE_6H, "day": "06–06 UTC (01:00–01:00 hora de Ecuador)",
                        "processing": "herramientas/reanalisis/core.py"}
            ds.to_netcdf(f, encoding={v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in ds.data_vars})
            print(f"guardado {f.name} en {(time.time() - t0) / 60:.1f} min")
        salidas.append(f)
    return salidas


def mensual_desde_diario(ds, min_dias: int = 28):
    """Medias mensuales a partir de las diarias (pr en mm/mes)."""
    return V.mensual_desde_diario(ds, min_dias)


# ------------------------------------------------------------------ mensual por zona (opción A, estudiantes)
def mes_estandar(ds, anio: int, mes: int):
    """Un mes de promedios de flujos (ya recortado) en las variables de trabajo."""
    import calendar

    import pandas as pd

    t_c = ds["tmp"] - 273.15
    p_hpa = ds["pres"] / 100
    out = ds[[]].copy()
    out["tmed"] = t_c
    out["pr"] = ds["prate"] * 86400 * calendar.monthrange(anio, mes)[1]
    out["q"] = ds["spfh"] * 1000
    out["hr"] = V.hr_desde_especifica(ds["spfh"], t_c, p_hpa)
    out["ps"] = p_hpa
    out["u10"], out["v10"] = ds["ugrd"], ds["vgrd"]
    out = V.anotar(out.expand_dims(time=[pd.Timestamp(anio, mes, 1)]))
    out["pr"].attrs["units"] = "mm/mes"
    return out


def mensual_zona(area, anios, carpeta_datos, slug: str, hilos: int = 3, avance: bool = True) -> pathlib.Path:
    """(Estudiante) Promedios mensuales de CORe para el recuadro de su zona. Reanudable por mes.

    De cada archivo mensual global se piden solo los bytes de 6 campos (~0,2 MB). La humedad relativa
    se calcula con las medias mensuales de q, T y presión (aproximación).
    """
    from concurrent.futures import ThreadPoolExecutor

    import xarray as xr

    carpeta_datos = pathlib.Path(carpeta_datos)
    tmp = carpeta_datos / "_meses_core"
    tmp.mkdir(parents=True, exist_ok=True)
    meses = [(a, m) for a in anios for m in range(1, 13)]

    def bajar(am):  # en hilos: solo la descarga (la lectura y escritura de NetCDF no admiten hilos)
        a, m = am
        nc = tmp / f"m_{a}{m:02d}.nc"
        return am, nc, None if nc.exists() else extraer(url_mes(a, m), tmp / f"m_{a}{m:02d}.grb", CAMPOS_MES, "mes")

    hechos = []
    with ThreadPoolExecutor(hilos) as ex:
        for k, ((a, m), nc, g) in enumerate(ex.map(bajar, meses), 1):
            if g is not None:
                mes_estandar(recortar(leer_6h(g, CAMPOS_MES), area).load(), a, m).to_netcdf(nc)
                g.unlink(missing_ok=True)
            hechos.append(nc)
            if avance and (k % 60 == 0 or k == len(meses)):
                print(f"  CORe: {k}/{len(meses)} meses")
    ds = juntar(hechos)
    ds.attrs = {"title": f"CORe mensual, {slug}", "source": "NOAA/NCEP CPC, CORe, CDAS look-alike mensual (GRIB1, T62)",
                "url": BASE_MES, "processing": "herramientas/reanalisis/core.py: mensual_zona"}
    f = carpeta_datos / f"core_mensual_{slug}.nc"
    ds.load().to_netcdf(f, encoding={v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in ds.data_vars})
    return f
