"""ERA5 (ECMWF / Copernicus): credencial personal, descarga por celda y paso de horario a diario y mensual.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Requisitos del usuario:
  1. Cuenta propia en https://cds.climate.copernicus.eu
  2. Licencia aceptada en los conjuntos que use (al final de la pestaña Download de cada uno).
  3. API Token PERSONAL (perfil del sitio): una cuenta por persona, porque el CDS limita por cuenta.
     En Colab, en Secrets con el nombre CDSAPI_KEY, o pasado a `credenciales(token)` desde el cuaderno.

Método (igual para estudiantes y para la preparación del docente):
  1. `celdas`: celdas de 0,25° que tocan la zona, con la fracción de su área dentro.
  2. Una solicitud por celda al conjunto de series horarias por punto
     (reanalysis-era5-single-levels-timeseries), que guarda los datos por lugar y responde en segundos.
  3. `horario_a_diario`: día en hora local (UTC-5), con la hora de inicio que se elija (0 o 7).
     Tmax y Tmin son el máximo y el mínimo de los 24 valores horarios; HR y q se calculan hora a hora;
     la velocidad del viento es el promedio de las velocidades horarias.
  4. Se arma la malla diaria de la zona y, de ella, la mensual. Los archivos horarios se borran.

Archivos que produce en la carpeta de datos:
    era5_diario_<zona>.nc    tmed, tmax, tmin, pr, hr, q, ps, u10, v10, ws
    era5_mensual_<zona>.nc   las mismas, medias mensuales (pr en mm/mes)
    era5_terreno_<zona>.nc   altura del terreno del modelo (m)
"""
from __future__ import annotations

import os
import pathlib
import time
import zipfile

import numpy as np

from herramientas import variables as V

URL_CDS = "https://cds.climate.copernicus.eu/api"
SERIES = "reanalysis-era5-single-levels-timeseries"
MENSUAL = "reanalysis-era5-single-levels-monthly-means"
DOI = {MENSUAL: "10.24381/cds.f17050d7"}
VARIABLES_SERIES = ["2m_temperature", "2m_dewpoint_temperature", "total_precipitation",
                    "surface_pressure", "10m_u_component_of_wind", "10m_v_component_of_wind"]
CORTOS = {"2m_temperature": "t2m", "2m_dewpoint_temperature": "d2m", "total_precipitation": "tp",
          "surface_pressure": "sp", "10m_u_component_of_wind": "u10", "10m_v_component_of_wind": "v10"}
UTC_LOCAL = -5  # Ecuador continental


# ------------------------------------------------------------------ credencial y solicitudes
def credenciales(token: str | None = None, nombre_secreto: str = "CDSAPI_KEY") -> str:
    """Configura la credencial PERSONAL del Climate Data Store para esta sesión.

    Orden: argumento `token` › Colab Secrets (`CDSAPI_KEY`) › variable de entorno › teclado.
    Escribe ~/.cdsapirc en la máquina de la sesión (no en Drive ni en el repositorio) y devuelve
    el token enmascarado, para que el usuario confirme que es el suyo.
    """
    token = (token or "").strip()
    if not token:
        try:
            from google.colab import userdata  # type: ignore

            token = (userdata.get(nombre_secreto) or "").strip()
        except Exception:
            pass
    token = token or os.environ.get(nombre_secreto, "").strip()
    if not token:
        import getpass

        token = getpass.getpass("Pegue SU API Token personal del Climate Data Store y presione Enter: ").strip()
    if len(token) < 20 or " " in token:
        raise ValueError("El token no parece válido: cópielo completo desde su perfil en cds.climate.copernicus.eu.")
    (pathlib.Path.home() / ".cdsapirc").write_text(f"url: {URL_CDS}\nkey: {token}\n")
    os.environ["CDSAPI_URL"], os.environ["CDSAPI_KEY"] = URL_CDS, token
    return f"{token[:4]}…{token[-4:]}"


def _pedir(conjunto: str, solicitud: dict, destino: pathlib.Path, intentos: int = 4) -> pathlib.Path:
    """Solicitud al CDS con reintentos y espera creciente; no repite si el archivo ya existe."""
    destino = pathlib.Path(destino)
    if destino.exists() and destino.stat().st_size > 0:
        return destino
    import cdsapi

    if not (pathlib.Path.home() / ".cdsapirc").exists():
        credenciales()
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(".parcial")
    for k in range(intentos):
        try:
            cdsapi.Client(quiet=True, progress=False).retrieve(conjunto, solicitud, str(tmp))
            tmp.rename(destino)
            return destino
        except Exception as err:
            texto = str(err).lower()
            if k == intentos - 1 or "licence" in texto or "license" in texto or "401" in texto:
                raise
            espera = 30 * 2 ** k
            print(f"  reintento en {espera} s: {err}")
            time.sleep(espera)


def abrir_ds(ruta):
    """Abre una descarga del CDS (NetCDF o zip con varios) con nombres time, lat, lon."""
    import xarray as xr

    ruta = pathlib.Path(ruta)
    archivos = [ruta]
    if zipfile.is_zipfile(ruta):
        carpeta = ruta.with_suffix("")
        with zipfile.ZipFile(ruta) as z:
            z.extractall(carpeta)
        archivos = sorted(carpeta.glob("*.nc"))
    partes = []
    for f in archivos:
        ds = xr.open_dataset(f)
        ren = {k: v for k, v in {"valid_time": "time", "date": "time", "latitude": "lat", "longitude": "lon"}.items()
               if k in ds.dims or k in ds.coords}
        ds = ds.rename(ren)
        for extra in ("number", "expver"):
            if extra in ds.dims:
                ds = ds.isel({extra: 0})
            if extra in ds.coords:
                ds = ds.drop_vars(extra)
        partes.append(ds)
    ds = xr.merge(partes, compat="override")
    return ds.sortby("lat") if "lat" in ds.dims else ds


# ------------------------------------------------------------------ serie horaria de una celda
def descargar_celda(lat: float, lon: float, anios, carpeta) -> pathlib.Path:
    """Serie horaria completa de una celda (todas las variables) en una sola solicitud rápida."""
    a0, a1 = min(anios), max(anios)
    destino = pathlib.Path(carpeta) / f"h_{lat:+.2f}_{lon:+.2f}_{a0}_{a1}.nc"
    solicitud = {"variable": VARIABLES_SERIES, "location": {"latitude": float(lat), "longitude": float(lon)},
                 "date": [f"{a0}-01-01/{a1 + 1}-01-01"], "data_format": "netcdf"}
    return _pedir(SERIES, solicitud, destino)


def horario_a_diario(ds, inicio_dia: int = 0, utc_local: int = UTC_LOCAL):
    """Convierte la serie horaria de una celda en valores diarios del día local.

    `inicio_dia`: hora local en que empieza el día (0 = 00–24 h; 7 = 07–07 h, como la lluvia del INAMHI).
    La precipitación horaria de ERA5 es la acumulada en la hora que TERMINA en la marca de tiempo:
    se asigna a la hora anterior antes de sumar. Solo se conservan días con las 24 horas.
    """
    import pandas as pd
    import xarray as xr

    s = {CORTOS.get(k, k): ds[k].values for k in ds.data_vars}
    t = pd.DatetimeIndex(ds["time"].values)
    df = pd.DataFrame({k: v.ravel() for k, v in s.items()}, index=t)
    t_c, td_c, p = df["t2m"] - 273.15, df["d2m"] - 273.15, df["sp"] / 100
    h = pd.DataFrame({
        "t": t_c, "hr": V.hr_desde_rocio(t_c, td_c), "q": V.especifica_desde_rocio(td_c, p), "ps": p,
        "u10": df["u10"], "v10": df["v10"], "ws": np.hypot(df["u10"], df["v10"]),
    }, index=t)
    corrimiento = pd.Timedelta(hours=utc_local - inicio_dia)
    dia = (t + corrimiento).floor("D")
    dia_pr = (t - pd.Timedelta(hours=1) + corrimiento).floor("D")
    g = h.groupby(dia)
    n = g["t"].count()
    out = pd.DataFrame({"tmed": g["t"].mean(), "tmax": g["t"].max(), "tmin": g["t"].min(),
                        "hr": g["hr"].mean(), "q": g["q"].mean(), "ps": g["ps"].mean(),
                        "u10": g["u10"].mean(), "v10": g["v10"].mean(), "ws": g["ws"].mean()})
    pr = (df["tp"] * 1000).groupby(dia_pr)
    out["pr"] = pr.sum().reindex(out.index)
    out.loc[(n < 24) | (pr.count().reindex(out.index) < 24), :] = np.nan
    out = out.dropna(how="all")
    out.index.name = "time"
    return xr.Dataset.from_dataframe(out[["tmed", "tmax", "tmin", "pr", "hr", "q", "ps", "u10", "v10", "ws"]])


# ------------------------------------------------------------------ zona completa
def descargar_zona(geom, anios, carpeta_datos, slug: str, inicio_dia: int = 0, borrar_horarios: bool = True,
                   avance: bool = True, carpeta_celdas=None) -> dict:
    """Descarga y procesa todas las celdas de la zona. Reanudable celda por celda.

    `carpeta_celdas`: dónde se guardan las series diarias de cada celda (por defecto, `_celdas_era5` dentro de
    `carpeta_datos`). El docente usa una sola para todas las provincias: las celdas de borde compartidas se
    descargan una sola vez.
    Devuelve {"diario": ruta, "mensual": ruta, "celdas": DataFrame}.
    """
    import pandas as pd
    import xarray as xr

    from herramientas import limites

    carpeta_datos = pathlib.Path(carpeta_datos)
    carpeta_datos.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(carpeta_celdas) if carpeta_celdas else carpeta_datos / "_celdas_era5"
    tmp.mkdir(parents=True, exist_ok=True)
    cs = limites.celdas(geom, 0.25)
    sufijo = f"{min(anios)}_{max(anios)}_d{inicio_dia:02d}"
    t0 = time.time()
    for i, r in cs.iterrows():
        diario = tmp / f"d_{r.lat:+.2f}_{r.lon:+.2f}_{sufijo}.nc"
        if not diario.exists():
            h = descargar_celda(r.lat, r.lon, anios, tmp)
            d = horario_a_diario(abrir_ds(h), inicio_dia).expand_dims(lat=[r.lat], lon=[r.lon])
            d = d.sel(time=slice(f"{min(anios)}-01-01", f"{max(anios)}-12-31"))
            d.to_netcdf(diario)
            if borrar_horarios:
                h.unlink(missing_ok=True)
        if avance:
            print(f"  {slug}: celda {i + 1}/{len(cs)} ({r.lat:+.2f}, {r.lon:+.2f}) lista · {(time.time() - t0) / 60:.1f} min")
    partes = [xr.open_dataset(tmp / f"d_{r.lat:+.2f}_{r.lon:+.2f}_{sufijo}.nc") for r in cs.itertuples()]
    malla = xr.combine_by_coords(partes, combine_attrs="drop_conflicts", join="outer").transpose("time", "lat", "lon")
    lat = np.round(np.arange(malla.lat.min(), malla.lat.max() + 1e-9, 0.25), 4)
    lon = np.round(np.arange(malla.lon.min(), malla.lon.max() + 1e-9, 0.25), 4)
    malla = V.anotar(malla.reindex(lat=lat, lon=lon, method="nearest", tolerance=1e-6))
    malla.attrs = {"title": f"ERA5 diario por celda, {slug}", "source": f"C3S Climate Data Store, {SERIES}",
                   "day": f"día local UTC{UTC_LOCAL:+d}, desde las {inicio_dia:02d}:00",
                   "processing": "herramientas/reanalisis/era5.py: horario -> diario por celda"}
    enc = {v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in malla.data_vars}
    f_d = carpeta_datos / f"era5_diario_{slug}.nc"
    f_m = carpeta_datos / f"era5_mensual_{slug}.nc"
    malla.load().to_netcdf(f_d, encoding=enc)
    V.mensual_desde_diario(malla).to_netcdf(f_m, encoding=enc)
    for p in partes:
        p.close()
    return {"diario": f_d, "mensual": f_m, "celdas": cs}


def descargar_terreno(area, destino) -> pathlib.Path:
    """Geopotencial de un mes (fija): da la altura del terreno del modelo. Una solicitud pequeña."""
    sol = {"product_type": ["monthly_averaged_reanalysis"], "variable": ["geopotential"], "year": ["2000"],
           "month": ["01"], "time": ["00:00"], "area": list(area), "data_format": "netcdf", "download_format": "unarchived"}
    return _pedir(MENSUAL, sol, pathlib.Path(destino))


def terreno(ruta):
    """Altura del terreno del modelo (m)."""
    ds = abrir_ds(ruta)
    z = ds["z"].isel(time=0) if "time" in ds["z"].dims else ds["z"]
    return z / 9.80665
