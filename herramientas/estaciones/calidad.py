"""Datos de estaciones: lectura, control de calidad básico, agregación mensual y métricas.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Formato de entrada (CSV), diario o mensual. Solo `fecha` es obligatoria; las demás columnas,
si existen, se usan:
    fecha   AAAA-MM-DD
    tmed, tmax, tmin   °C
    precip             mm
    hr                 %       humedad relativa
    q                  g/kg    humedad específica (si falta, se calcula de hr, tmed y pres)
    pres               hPa     presión atmosférica de la estación
    vv                 m/s     velocidad del viento
    dv                 °       dirección de donde sopla el viento (0 = norte)
Una celda vacía es un dato faltante; nunca 0 donde no hubo medición.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from herramientas import variables as V

COLUMNAS = ["tmed", "tmax", "tmin", "precip", "hr", "q", "pres", "vv", "dv"]
LIMITES = {"tmed": (-5, 45), "tmax": (-5, 48), "tmin": (-10, 40), "hr": (1, 100), "q": (0.1, 30),
           "pres": (500, 1100), "vv": (0, 60), "dv": (0, 360)}
PROMEDIOS = ["tmed", "tmax", "tmin", "hr", "q", "pres"]


def leer(ruta) -> tuple[pd.DataFrame, dict]:
    """Lee el CSV, elimina fechas duplicadas y detecta la frecuencia."""
    df = pd.read_csv(ruta)
    df.columns = [c.strip().lower() for c in df.columns]
    df["fecha"] = pd.to_datetime(df["fecha"])
    presentes = [c for c in COLUMNAS if c in df.columns]
    for c in COLUMNAS:
        df[c] = pd.to_numeric(df[c], errors="coerce") if c in df.columns else np.nan
    df = df.sort_values("fecha")
    dup = int(df["fecha"].duplicated().sum())
    df = df.drop_duplicates("fecha", keep="first").set_index("fecha")[COLUMNAS]
    paso = df.index.to_series().diff().dt.days.median()
    diario = bool(paso is not None and paso < 2)
    return df, {"duplicadas": dup, "frecuencia": "diaria" if diario else "mensual", "variables": presentes}


def limites_fisicos(df: pd.DataFrame, diario: bool = True) -> tuple[pd.DataFrame, dict]:
    """Anula valores imposibles y Tmax < Tmin. Devuelve el conteo de anulados por variable."""
    df = df.copy()
    lim = dict(LIMITES, precip=(0, 500 if diario else 3000))
    anulados = {}
    for c, (lo, hi) in lim.items():
        malos = (df[c] < lo) | (df[c] > hi)
        anulados[c] = int(malos.sum())
        df.loc[malos, c] = np.nan
    inc = df["tmax"] < df["tmin"]
    anulados["tmax<tmin"] = int(inc.sum())
    df.loc[inc, ["tmax", "tmin"]] = np.nan
    calc = df["q"].isnull() & df[["hr", "tmed", "pres"]].notnull().all(axis=1)
    df.loc[calc, "q"] = V.especifica_desde_hr(df.loc[calc, "hr"], df.loc[calc, "tmed"], df.loc[calc, "pres"])
    calma = (df["vv"] == 0) & df["dv"].notnull()
    df.loc[calma, "dv"] = np.nan  # con calma la dirección no está definida
    return df, {k: v for k, v in anulados.items() if v}


def _max_consecutivos(s: pd.Series) -> int:
    nul = s.isnull().astype(int)
    return int(nul.groupby((nul != nul.shift()).cumsum()).sum().max() or 0)


def mensual(df: pd.DataFrame, diario: bool = True, max_faltantes: int = 4,
            max_consecutivos: int = 2, max_faltantes_p: int = 0) -> pd.DataFrame:
    """Valores mensuales con criterios de completitud (ajustables y declarados en el informe).

    Variables promediadas (temperaturas, hr, pres, viento): el mes se acepta con hasta
    `max_faltantes` días faltantes y hasta `max_consecutivos` seguidos. Precipitación: hasta
    `max_faltantes_p`. El viento se promedia como vector (u, v) y se devuelve como vv y dv.
    """
    df = df.copy()
    df["u"], df["v"] = V.componentes(df["vv"], df["dv"])
    if not diario:
        out = df.copy()
        out.index = out.index.to_period("M").to_timestamp()
        return out[COLUMNAS]
    ini = df.index.min().replace(day=1)
    fin = df.index.max() + pd.offsets.MonthEnd(0)
    d = df.reindex(pd.date_range(ini, fin, freq="D"))
    g = d.groupby(pd.Grouper(freq="MS"))
    out = pd.DataFrame(index=g.size().index)
    for c in PROMEDIOS + ["u", "v", "vv"]:
        out[c] = g[c].mean()
        falt, cons = g[c].apply(lambda s: s.isnull().sum()), g[c].apply(_max_consecutivos)
        out.loc[(falt > max_faltantes) | (cons > max_consecutivos), c] = np.nan
    out["precip"] = g["precip"].sum(min_count=1)
    out.loc[g["precip"].apply(lambda s: s.isnull().sum()) > max_faltantes_p, "precip"] = np.nan
    _, out["dv"] = V.viento(out["u"], out["v"])
    return out[COLUMNAS]


def metricas(obs: pd.Series, mod: pd.Series, relativa: bool = False, circular: bool = False) -> dict:
    """Sesgo, MAE, RMSE y r de Pearson sobre los pares con dato en ambas series.

    Con `circular=True` (dirección del viento) las diferencias se toman en el rango −180..180°.
    """
    ok = obs.notnull() & mod.notnull()
    o, m = obs[ok], mod[ok]
    if ok.sum() == 0:
        return {"n": 0}
    dif = ((m - o + 180) % 360 - 180) if circular else (m - o)
    res = {"n": int(ok.sum()), "media_obs": round(float(o.mean()), 2), "media_mod": round(float(m.mean()), 2),
           "sesgo": round(float(dif.mean()), 2), "mae": round(float(dif.abs().mean()), 2),
           "rmse": round(float(np.sqrt((dif ** 2).mean())), 2)}
    if not circular:
        res["r"] = round(float(o.corr(m)), 3)
    if relativa and o.sum():
        res["sesgo_rel_pct"] = round(float(100 * dif.sum() / o.sum()), 1)
    return res
