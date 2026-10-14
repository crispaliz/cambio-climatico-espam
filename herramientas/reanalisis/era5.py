"""ERA5 (ECMWF / Copernicus): credenciales, descarga optimizada desde el Climate Data Store y lectura.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Requisitos del usuario:
  1. Cuenta en https://cds.climate.copernicus.eu
  2. Licencia aceptada en cada conjunto (al final de la pestaña Download).
  3. API Token PERSONAL (perfil del sitio): una cuenta por persona, porque el CDS limita por cuenta.
     En Colab, en Secrets con el nombre CDSAPI_KEY, o pasado a `credenciales(token)` desde el cuaderno.

Optimización y cuidado del servidor:
  - Una sola solicitud mensual con todas las variables, recortada al recuadro de la zona.
  - Diario: las variables que comparten estadístico van juntas (4 solicitudes por año, no 8).
  - Solicitudes en serie (el CDS ya las pone en cola), reintentos con espera creciente y
    archivos que ya existen no se vuelven a pedir.

Variables diarias (release era5-v1, una por año, todo Ecuador, día local UTC-5):
    tmed, tmax, tmin (°C), pr (mm/día), hr (%), q (g/kg), ps (hPa), u10, v10 (m/s)
    hr y q se calculan del punto de rocío (y la presión, para q): ERA5 no ofrece q a 2 m en el CDS.
"""
from __future__ import annotations

import os
import pathlib
import time
import zipfile

from herramientas import variables as V

URL_CDS = "https://cds.climate.copernicus.eu/api"
MENSUAL = "reanalysis-era5-single-levels-monthly-means"
DIARIO = "derived-era5-single-levels-daily-statistics"
DOI = {MENSUAL: "10.24381/cds.f17050d7"}
RECUADRO_ECUADOR = [2.25, -92.75, -5.75, -74.5]  # N, O, S, E: todas las provincias, incluida Galápagos, con margen

# nombre en el CDS -> nombre corto en el NetCDF
CDS = {"2m_temperature": "t2m", "2m_dewpoint_temperature": "d2m", "total_precipitation": "tp",
       "surface_pressure": "sp", "mean_sea_level_pressure": "msl",
       "10m_u_component_of_wind": "u10", "10m_v_component_of_wind": "v10", "geopotential": "z"}
MENSUALES = ["2m_temperature", "2m_dewpoint_temperature", "total_precipitation", "surface_pressure",
             "mean_sea_level_pressure", "10m_u_component_of_wind", "10m_v_component_of_wind"]
# estadístico diario -> variables del CDS que se piden juntas
GRUPOS_DIARIOS = {
    "daily_mean": ["2m_temperature", "2m_dewpoint_temperature", "surface_pressure",
                   "10m_u_component_of_wind", "10m_v_component_of_wind"],
    "daily_maximum": ["2m_temperature"],
    "daily_minimum": ["2m_temperature"],
    "daily_sum": ["total_precipitation"],
}


# ------------------------------------------------------------------ credenciales y cliente
def credenciales(token: str | None = None, nombre_secreto: str = "CDSAPI_KEY") -> str:
    """Configura la credencial PERSONAL del Climate Data Store para esta sesión.

    Cada persona usa su propia cuenta y su propio API Token: así cada una tiene su propia cola
    y su propio límite en el CDS, y nadie queda bloqueado por las descargas de otros.

    Orden de búsqueda del token:
      1. el argumento `token` (lo que el usuario escribió en el cuaderno);
      2. Colab › Secrets, con el nombre `CDSAPI_KEY` (lo más seguro);
      3. la variable de entorno `CDSAPI_KEY`;
      4. si nada de lo anterior existe, se pide por teclado (no queda escrito).
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


def _hay_credencial() -> bool:
    return (pathlib.Path.home() / ".cdsapirc").exists()


def _pedir(conjunto: str, solicitud: dict, destino: pathlib.Path, intentos: int = 4) -> pathlib.Path:
    """Envía una solicitud al CDS con reintentos y espera creciente; no repite si el archivo existe."""
    if destino.exists() and destino.stat().st_size > 0:
        return destino
    import cdsapi

    if not _hay_credencial():
        credenciales()
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(".parcial")
    for k in range(intentos):
        try:
            cdsapi.Client(quiet=True).retrieve(conjunto, solicitud, str(tmp))
            tmp.rename(destino)
            return destino
        except Exception as err:
            if k == intentos - 1 or "licence" in str(err).lower() or "license" in str(err).lower():
                raise
            espera = 60 * 2 ** k
            print(f"Reintento en {espera} s: {err}")
            time.sleep(espera)


def _netcdfs(ruta: pathlib.Path) -> list[pathlib.Path]:
    """El CDS entrega un NetCDF o un .zip con varios (uno por tipo de paso). Devuelve los NetCDF."""
    if not zipfile.is_zipfile(ruta):
        return [ruta]
    carpeta = ruta.with_suffix("")
    with zipfile.ZipFile(ruta) as z:
        z.extractall(carpeta)
    return sorted(carpeta.glob("*.nc"))


def abrir_ds(ruta):
    """Abre la descarga (NetCDF o zip) como un solo Dataset con nombres time, lat, lon."""
    import xarray as xr

    partes = []
    for f in _netcdfs(pathlib.Path(ruta)):
        ds = xr.open_dataset(f)
        ren = {k: v for k, v in {"valid_time": "time", "latitude": "lat", "longitude": "lon"}.items()
               if k in ds.dims or k in ds.coords}
        ds = ds.rename(ren)
        for extra in ("number", "expver"):
            if extra in ds.dims:
                ds = ds.isel({extra: 0})
            if extra in ds.coords:
                ds = ds.drop_vars(extra)
        partes.append(ds)
    return xr.merge(partes, compat="override").sortby("lat")


# ------------------------------------------------------------------ mensual (estudiantes)
def solicitud_mensual(variables, anios, area, meses=range(1, 13)) -> dict:
    return {
        "product_type": ["monthly_averaged_reanalysis"],
        "variable": list(variables),
        "year": [str(a) for a in anios],
        "month": [f"{m:02d}" for m in meses],
        "time": ["00:00"],
        "area": list(area),
        "data_format": "netcdf",
        "download_format": "unarchived",
    }


def descargar_mensual(anios, area, destino, variables=MENSUALES, meses=range(1, 13)) -> pathlib.Path:
    """Una sola solicitud con todas las variables mensuales para el recuadro de la zona."""
    return _pedir(MENSUAL, solicitud_mensual(variables, anios, area, meses), pathlib.Path(destino))


def mensual_estandar(ruta):
    """Convierte la descarga mensual a las variables y unidades de trabajo del curso."""
    import xarray as xr

    ds = abrir_ds(ruta)
    out = xr.Dataset()
    if "t2m" in ds:
        out["tmed"] = ds["t2m"] - 273.15
    if "tp" in ds:
        out["pr"] = ds["tp"] * 1000 * ds["time"].dt.days_in_month
    if "d2m" in ds and "t2m" in ds:
        out["hr"] = V.hr_desde_rocio(ds["t2m"] - 273.15, ds["d2m"] - 273.15)
    if "d2m" in ds and "sp" in ds:
        out["q"] = V.especifica_desde_rocio(ds["d2m"] - 273.15, ds["sp"] / 100)
    if "sp" in ds:
        out["ps"] = ds["sp"] / 100
    if "msl" in ds:
        out["pnm"] = ds["msl"] / 100
        out["pnm"].attrs = {"units": "hPa", "long_name": "Presión a nivel del mar"}
    for c in ("u10", "v10"):
        if c in ds:
            out[c] = ds[c]
    out = V.anotar(out)
    if "pr" in out:
        out["pr"].attrs["units"] = "mm/mes"
    return out


def terreno(ruta):
    """Altura del terreno del modelo (m) a partir de la geopotencial."""
    ds = abrir_ds(ruta)
    z = ds["z"].isel(time=0) if "time" in ds["z"].dims else ds["z"]
    return z / 9.80665


def descargar_terreno(area, destino) -> pathlib.Path:
    return _pedir(MENSUAL, solicitud_mensual(["geopotential"], [2000], area, [1]), pathlib.Path(destino))


# ------------------------------------------------------------------ diario (docente)
def solicitud_diaria(variables, estadistico: str, anio: int, area, zona_horaria: str = "utc-05:00") -> dict:
    return {
        "product_type": "reanalysis",
        "variable": list(variables),
        "year": str(anio),
        "month": [f"{m:02d}" for m in range(1, 13)],
        "day": [f"{d:02d}" for d in range(1, 32)],
        "daily_statistic": estadistico,
        "time_zone": zona_horaria,
        "frequency": "1_hourly",
        "area": list(area),
    }


def diario_estandar(por_estadistico: dict):
    """Une las descargas de un año (una por estadístico) en las variables de trabajo."""
    import xarray as xr

    m, mx, mn, sm = (por_estadistico[k] for k in ("daily_mean", "daily_maximum", "daily_minimum", "daily_sum"))
    out = xr.Dataset({
        "tmed": m["t2m"] - 273.15,
        "tmax": mx["t2m"] - 273.15,
        "tmin": mn["t2m"] - 273.15,
        "pr": sm["tp"] * 1000,
        "hr": V.hr_desde_rocio(m["t2m"] - 273.15, m["d2m"] - 273.15),
        "q": V.especifica_desde_rocio(m["d2m"] - 273.15, m["sp"] / 100),
        "ps": m["sp"] / 100,
        "u10": m["u10"],
        "v10": m["v10"],
    })
    return V.anotar(out)


def preparar_diario(anios, carpeta_trabajo, carpeta_salida, area=RECUADRO_ECUADOR) -> list[pathlib.Path]:
    """(Docente) Un NetCDF por año para Ecuador con las 9 variables diarias. Reanudable."""
    carpeta_trabajo, carpeta_salida = pathlib.Path(carpeta_trabajo), pathlib.Path(carpeta_salida)
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    salidas = []
    for a in anios:
        f = carpeta_salida / f"era5_ecuador_diario_{a}.nc"
        if not f.exists():
            partes = {}
            for est, vars_ in GRUPOS_DIARIOS.items():
                ruta = _pedir(DIARIO, solicitud_diaria(vars_, est, a, area), carpeta_trabajo / f"era5_{est}_{a}.nc")
                partes[est] = abrir_ds(ruta)
            ds = diario_estandar(partes)
            ds.attrs = {"title": f"ERA5 diario para Ecuador, {a}", "source": f"C3S Climate Data Store, {DIARIO}",
                        "day": "día local (UTC-5)", "processing": "herramientas/reanalisis/era5.py",
                        "note": "u10 y v10 son medias diarias de las componentes; la velocidad calculada con ellas es la del viento medio vectorial"}
            ds.to_netcdf(f, encoding={v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in ds.data_vars})
            print("guardado", f.name)
        salidas.append(f)
    return salidas
