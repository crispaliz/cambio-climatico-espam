"""Índices de extremos climáticos (ETCCDI), tendencia y periodos de retorno.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Definiciones del Expert Team on Climate Change Detection and Indices (ETCCDI; Zhang et al., 2011,
WIREs Climate Change 2: 851–870; Klein Tank et al., 2009, WCDMP-72). Día lluvioso: P ≥ 1 mm.

Simplificaciones declaradas (escríbalas en el informe):
  - Valor anual faltante si faltan más de `MAX_FALTANTES_ANIO` días en el año.
  - Rachas (CDD, CWD, WSDI, CSDI) contadas dentro de cada año calendario.
  - Percentiles de temperatura por día del año con ventana de 5 días en el periodo base, sin el
    remuestreo (bootstrap) de Zhang et al. (2005) dentro del periodo base.
  - Las series de una zona son promedios de área: suavizan los extremos locales. Un Rx1day de la
    zona es menor que el de cualquiera de sus estaciones; compare con estaciones cuando las tenga.

Entradas: pandas.Series diarias con índice de fechas (pr en mm/día, temperaturas en °C).
"""
from __future__ import annotations

import calendar

import numpy as np
import pandas as pd

MAX_FALTANTES_ANIO = 15
MIN_ANIOS_RETORNO = 20
BASE = (1981, 2010)

DESCRIPCION = {
    "PRCPTOT": ("Precipitación anual en días lluviosos", "mm"),
    "SDII": ("Intensidad diaria simple: P anual / días lluviosos", "mm/día"),
    "R10mm": ("Días con P ≥ 10 mm", "días"),
    "R20mm": ("Días con P ≥ 20 mm", "días"),
    "R50mm": ("Días con P ≥ 50 mm", "días"),
    "CDD": ("Máxima racha de días secos (P < 1 mm)", "días"),
    "CWD": ("Máxima racha de días lluviosos (P ≥ 1 mm)", "días"),
    "Rx1day": ("Máxima precipitación en 1 día", "mm"),
    "Rx5day": ("Máxima precipitación en 5 días consecutivos", "mm"),
    "R95p": ("P anual de días por encima del percentil 95 de días lluviosos (base)", "mm"),
    "R99p": ("P anual de días por encima del percentil 99 de días lluviosos (base)", "mm"),
    "R95pTOT": ("Fracción de PRCPTOT que cae en días > P95", "%"),
    "TXx": ("Máxima de las temperaturas máximas", "°C"),
    "TNn": ("Mínima de las temperaturas mínimas", "°C"),
    "TNx": ("Máxima de las temperaturas mínimas", "°C"),
    "TXn": ("Mínima de las temperaturas máximas", "°C"),
    "TX90p": ("Días cálidos: Tmax > percentil 90 del día del año (base)", "%"),
    "TN90p": ("Noches cálidas: Tmin > percentil 90 del día del año (base)", "%"),
    "TX10p": ("Días fríos: Tmax < percentil 10 del día del año (base)", "%"),
    "TN10p": ("Noches frías: Tmin < percentil 10 del día del año (base)", "%"),
    "WSDI": ("Días en rachas cálidas (≥ 6 días con Tmax > P90)", "días"),
    "TR20": ("Noches tropicales: Tmin > 20 °C", "días"),
    "DTR": ("Rango diario de temperatura medio", "°C"),
}


# ------------------------------------------------------------------ utilidades
def _anual(s: pd.Series, f) -> pd.Series:
    """Aplica `f` por año; anula los años con demasiados faltantes o incompletos."""
    s = s.copy()
    s.index = pd.DatetimeIndex(s.index)
    g = s.groupby(s.index.year)
    dias = g.size()
    esperados = pd.Series([366 if calendar.isleap(a) else 365 for a in dias.index], index=dias.index)
    faltan = g.apply(lambda x: x.isna().sum()) + (esperados - dias)
    out = g.apply(lambda x: f(x.dropna()) if len(x.dropna()) else np.nan).astype(float)
    out[faltan > MAX_FALTANTES_ANIO] = np.nan
    out.index.name = "anio"
    return out


def _racha_max(b: pd.Series) -> int:
    if b.empty:
        return 0
    grupo = (b != b.shift()).cumsum()
    largos = b.groupby(grupo).sum()
    return int(largos.max()) if len(largos) else 0


def _en_base(s: pd.Series, base=BASE) -> pd.Series:
    return s[(s.index.year >= base[0]) & (s.index.year <= base[1])]


def umbral_lluvia(pr: pd.Series, q: float, base=BASE) -> float:
    b = _en_base(pr, base)
    return float(b[b >= 1].quantile(q / 100))


def umbral_diario(t: pd.Series, q: float, base=BASE, ventana: int = 5) -> pd.Series:
    """Percentil `q` por día del año (1–366) con ventana centrada de `ventana` días en el periodo base."""
    b = _en_base(t, base).dropna()
    doy = b.index.dayofyear.values
    medio = ventana // 2
    vals = {}
    for d in range(1, 367):
        dist = np.abs(((doy - d + 183) % 366) - 183)
        vals[d] = np.nanpercentile(b.values[dist <= medio], q) if (dist <= medio).any() else np.nan
    return pd.Series(vals)


# ------------------------------------------------------------------ índices
def precipitacion(pr: pd.Series, base=BASE) -> pd.DataFrame:
    """Índices anuales de precipitación."""
    p95, p99 = umbral_lluvia(pr, 95, base), umbral_lluvia(pr, 99, base)
    out = pd.DataFrame({
        "PRCPTOT": _anual(pr, lambda x: x[x >= 1].sum()),
        "SDII": _anual(pr, lambda x: x[x >= 1].mean() if (x >= 1).any() else 0.0),
        "R10mm": _anual(pr, lambda x: (x >= 10).sum()),
        "R20mm": _anual(pr, lambda x: (x >= 20).sum()),
        "R50mm": _anual(pr, lambda x: (x >= 50).sum()),
        "CDD": _anual(pr, lambda x: _racha_max(x < 1)),
        "CWD": _anual(pr, lambda x: _racha_max(x >= 1)),
        "Rx1day": _anual(pr, lambda x: x.max()),
        "Rx5day": _anual(pr.rolling(5).sum(), lambda x: x.max()),
        "R95p": _anual(pr, lambda x: x[x > p95].sum()),
        "R99p": _anual(pr, lambda x: x[x > p99].sum()),
    })
    out["R95pTOT"] = 100 * out["R95p"] / out["PRCPTOT"]
    out.attrs["umbrales"] = {"P95_mm": round(p95, 1), "P99_mm": round(p99, 1), "base": list(base)}
    return out


def temperatura(tmax: pd.Series, tmin: pd.Series, base=BASE) -> pd.DataFrame:
    """Índices anuales de temperatura."""
    doy_x, doy_n = tmax.index.dayofyear, tmin.index.dayofyear
    tx90 = pd.Series(umbral_diario(tmax, 90, base).reindex(doy_x).values, index=tmax.index)
    tx10 = pd.Series(umbral_diario(tmax, 10, base).reindex(doy_x).values, index=tmax.index)
    tn90 = pd.Series(umbral_diario(tmin, 90, base).reindex(doy_n).values, index=tmin.index)
    tn10 = pd.Series(umbral_diario(tmin, 10, base).reindex(doy_n).values, index=tmin.index)

    def pct(cond: pd.Series, valida: pd.Series):
        return _anual(cond.where(valida.notna()).astype(float), lambda x: 100 * x.mean())

    calido = (tmax > tx90)
    out = pd.DataFrame({
        "TXx": _anual(tmax, lambda x: x.max()), "TXn": _anual(tmax, lambda x: x.min()),
        "TNx": _anual(tmin, lambda x: x.max()), "TNn": _anual(tmin, lambda x: x.min()),
        "TX90p": pct(calido, tmax), "TX10p": pct(tmax < tx10, tmax),
        "TN90p": pct(tmin > tn90, tmin), "TN10p": pct(tmin < tn10, tmin),
        "WSDI": _anual(calido.where(tmax.notna()).astype(float),
                       lambda x: _dias_en_rachas(x.astype(bool), 6)),
        "TR20": _anual(tmin, lambda x: (x > 20).sum()),
        "DTR": _anual(tmax - tmin, lambda x: x.mean()),
    })
    return out


def _dias_en_rachas(b: pd.Series, minimo: int) -> int:
    grupo = (b != b.shift()).cumsum()
    largos = b.groupby(grupo).transform("sum")
    return int((b & (largos >= minimo)).sum())


# ------------------------------------------------------------------ tendencia y retorno
def tendencia(s: pd.Series) -> dict:
    """Pendiente de Sen (por década) y prueba de Mann-Kendall (tau de Kendall frente al tiempo)."""
    from scipy import stats

    s = s.dropna()
    if len(s) < 10:
        return {"n": len(s), "sen_por_decada": np.nan, "tau": np.nan, "p_valor": np.nan, "significativa_5%": False}
    x = np.asarray(s.index, dtype=float)
    pend = stats.theilslopes(s.values, x)[0]
    tau, p = stats.kendalltau(x, s.values)
    return {"n": len(s), "sen_por_decada": round(10 * pend, 3), "tau": round(tau, 3), "p_valor": round(p, 3),
            "significativa_5%": bool(p < 0.05)}


def retorno(maximos: pd.Series, periodos=(2, 5, 10, 25, 50, 100), remuestreos: int = 300, semilla: int = 1) -> pd.DataFrame:
    """Niveles de retorno con una distribución GEV ajustada a los máximos anuales, e intervalo del 90 %
    por remuestreo. Con 30–45 años, los periodos mayores de ~50 años son extrapolaciones."""
    from scipy import stats

    x = maximos.dropna().values
    if len(x) < MIN_ANIOS_RETORNO:
        raise ValueError(f"Solo {len(x)} máximos anuales: se necesitan al menos {MIN_ANIOS_RETORNO} para ajustar una GEV.")
    c, loc, esc = stats.genextreme.fit(x)
    prob = 1 - 1 / np.asarray(periodos, dtype=float)
    nivel = stats.genextreme.ppf(prob, c, loc, esc)
    rng = np.random.default_rng(semilla)
    boot = []
    for _ in range(remuestreos):
        m = rng.choice(x, len(x), replace=True)
        try:
            boot.append(stats.genextreme.ppf(prob, *stats.genextreme.fit(m)))
        except Exception:
            pass
    boot = np.array(boot)
    out = pd.DataFrame({"periodo_anios": periodos, "nivel": nivel.round(1),
                        "inf_5%": np.nanpercentile(boot, 5, axis=0).round(1),
                        "sup_95%": np.nanpercentile(boot, 95, axis=0).round(1)}).set_index("periodo_anios")
    out.attrs["gev"] = {"forma_c": round(c, 3), "posicion": round(loc, 2), "escala": round(esc, 2), "n_anios": len(x)}
    return out


def periodo_empirico(valor: float, maximos: pd.Series) -> float:
    """Periodo de retorno empírico (Weibull) de un valor frente a los máximos anuales."""
    m = maximos.dropna().sort_values(ascending=False).values
    rango = (m >= valor).sum()
    return (len(m) + 1) / rango if rango else np.inf


# ------------------------------------------------------------------ eventos
def acumulados(pr: pd.Series, fecha, dias=(1, 3, 5, 10, 30)) -> dict:
    """Precipitación acumulada en los `dias` que terminan en `fecha` y su percentil entre todas las
    ventanas del mismo largo del registro (qué tan raro fue)."""
    fecha = pd.Timestamp(fecha)
    out = {}
    for d in dias:
        acc = pr.rolling(d).sum()
        v = acc.get(fecha, np.nan)
        out[f"P{d}d_mm"] = round(float(v), 1) if pd.notna(v) else np.nan
        out[f"P{d}d_pct"] = round(float((acc.dropna() < v).mean() * 100), 1) if pd.notna(v) else np.nan
    return out


def secos_previos(pr: pd.Series, fecha, dias: int = 90) -> dict:
    """Para sequías e incendios: días secos y anomalía de precipitación en los `dias` previos."""
    fecha = pd.Timestamp(fecha)
    ventana = pr.loc[fecha - pd.Timedelta(days=dias - 1): fecha]
    acc = pr.rolling(dias).sum()
    clim = acc[acc.index.dayofyear == fecha.dayofyear].mean()
    return {f"dias_secos_{dias}d": int((ventana < 1).sum()),
            f"P{dias}d_anom_%": round(float(100 * (ventana.sum() / clim - 1)), 1) if clim else np.nan}


def mayores(pr: pd.Series, n: int = 15, dias: int = 1, separacion: int = 10) -> pd.DataFrame:
    """Los `n` mayores acumulados de `dias` días, separados al menos `separacion` días (eventos
    independientes). Sirven para buscar en los registros de desastres qué pasó esas fechas."""
    acc = pr.rolling(dias).sum().dropna().sort_values(ascending=False)
    elegidos = []
    for f, v in acc.items():
        if all(abs((f - e).days) > separacion for e, _ in elegidos):
            elegidos.append((f, v))
        if len(elegidos) == n:
            break
    return pd.DataFrame([{"fecha_fin": f.date(), f"P{dias}d_mm": v} for f, v in elegidos])
