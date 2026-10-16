"""Variables derivadas y convenciones comunes a todas las fuentes.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Nombres y unidades de trabajo (iguales para ERA5, CORe y estaciones):
    tmed, tmax, tmin  °C        temperatura del aire a 2 m
    pr                mm/día    precipitación (mm/mes en series mensuales)
    hr                %         humedad relativa a 2 m
    q                 g/kg      humedad específica a 2 m
    ps                hPa       presión atmosférica en superficie
    u10, v10          m/s       componentes del viento a 10 m (hacia el este y hacia el norte)
    ws                m/s       velocidad del viento
    wd                °         dirección de donde sopla el viento (0 = norte, 90 = este)
"""
from __future__ import annotations

import numpy as np

UNIDADES = {"tmed": "°C", "tmax": "°C", "tmin": "°C", "pr": "mm/día", "hr": "%", "q": "g/kg", "ps": "hPa",
            "u10": "m/s", "v10": "m/s", "ws": "m/s", "wd": "°"}
NOMBRES = {"tmed": "Temperatura media", "tmax": "Temperatura máxima", "tmin": "Temperatura mínima",
           "pr": "Precipitación", "hr": "Humedad relativa", "q": "Humedad específica", "ps": "Presión en superficie",
           "u10": "Viento zonal a 10 m", "v10": "Viento meridional a 10 m",
           "ws": "Velocidad del viento", "wd": "Dirección del viento"}


def presion_saturacion(t_c):
    """Presión de vapor de saturación (hPa) sobre agua, fórmula de Magnus (Alduchov y Eskridge, 1996)."""
    return 6.1094 * np.exp(17.625 * t_c / (t_c + 243.04))


def hr_desde_rocio(t_c, td_c):
    """Humedad relativa (%) a partir de temperatura y punto de rocío (°C)."""
    return (100 * presion_saturacion(td_c) / presion_saturacion(t_c)).clip(0, 100)


def hr_desde_especifica(q, t_c, p_hpa):
    """Humedad relativa (%) a partir de humedad específica (kg/kg), temperatura (°C) y presión (hPa)."""
    e = q * p_hpa / (0.622 + 0.378 * q)
    return (100 * e / presion_saturacion(t_c)).clip(0, 100)


def especifica_desde_presion_vapor(e_hpa, p_hpa):
    """Humedad específica (g/kg) a partir de la presión de vapor y la presión del aire (hPa)."""
    return 1000 * 0.622 * e_hpa / (p_hpa - 0.378 * e_hpa)


def especifica_desde_rocio(td_c, p_hpa):
    """Humedad específica (g/kg) a partir del punto de rocío (°C) y la presión (hPa)."""
    return especifica_desde_presion_vapor(presion_saturacion(td_c), p_hpa)


def especifica_desde_hr(hr, t_c, p_hpa):
    """Humedad específica (g/kg) a partir de humedad relativa (%), temperatura (°C) y presión (hPa)."""
    return especifica_desde_presion_vapor(hr / 100 * presion_saturacion(t_c), p_hpa)


def viento(u, v):
    """Velocidad (m/s) y dirección de procedencia (°, 0 = norte) a partir de u y v."""
    ws = np.hypot(u, v)
    wd = (np.degrees(np.arctan2(-u, -v)) + 360) % 360
    return ws, wd


def componentes(ws, wd):
    """u y v (m/s) a partir de velocidad y dirección de procedencia (°)."""
    r = np.radians(wd)
    return -ws * np.sin(r), -ws * np.cos(r)


def anotar(ds):
    """Agrega unidades y nombres largos a las variables conocidas de un Dataset."""
    for v in ds.data_vars:
        if v in UNIDADES:
            ds[v].attrs.update({"units": UNIDADES[v], "long_name": NOMBRES[v]})
    return ds


def mensual_desde_diario(ds, min_dias: int = 28):
    """Valores mensuales a partir de diarios: medias (pr: total del mes en mm/mes).

    Los meses con menos de `min_dias` días válidos quedan vacíos.
    """
    g = ds.resample(time="MS")
    ref = "tmed" if "tmed" in ds else list(ds.data_vars)[0]
    n = ds[ref].notnull().resample(time="MS").sum()
    out = g.mean()
    if "pr" in ds:
        out["pr"] = g.sum(min_count=1)["pr"]
    out = anotar(out.where(n >= min_dias))
    if "pr" in out:
        out["pr"].attrs["units"] = "mm/mes"
    return out
