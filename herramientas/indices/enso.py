"""Índices de ENSO, fases mensuales y eventos.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Dos índices, porque en el Ecuador importan las dos regiones del Pacífico:

ONI (Oceanic Niño Index, NOAA CPC): media móvil de 3 meses de la anomalía de TSM en Niño 3.4
    (Pacífico central), ERSSTv5. Episodio cálido (frío) cuando el ONI es ≥ +0,5 °C (≤ −0,5 °C) en al
    menos 5 trimestres móviles consecutivos. Intensidad por el pico: débil 0,5–0,9; moderado 1,0–1,4;
    fuerte 1,5–1,9; muy fuerte ≥ 2,0.
    https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt

ICEN (Índice Costero El Niño, Comisión Multisectorial ENFEN, Perú): media móvil de 3 meses de la
    anomalía de TSM en Niño 1+2 (0°–10° S, 90°–80° O; frente a la costa de Ecuador y Perú), ERSSTv5,
    climatología 1991–2020. Aquí se calcula con las anomalías de Niño 1+2 que publica NOAA CPC con la
    misma base:
    https://www.cpc.ncep.noaa.gov/data/indices/ersst5.nino.mth.91-20.ascii
    El valor operativo oficial lo publica el IGP: http://met.igp.gob.pe/datos/ICEN.txt
    Categorías y regla de persistencia en UMBRALES_ICEN y MESES_ICEN (verifíquelas con la Nota
    Técnica ENFEN vigente antes de publicar resultados).

La fase de cada mes se usa para los compuestos; los eventos (inicio, fin, pico, categoría), para el
registro histórico.
"""
from __future__ import annotations

import os
import pathlib
import urllib.request

import numpy as np
import pandas as pd

URL = {
    "oni": "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt",
    "nino": "https://www.cpc.ncep.noaa.gov/data/indices/ersst5.nino.mth.91-20.ascii",
}
TRIMESTRES = ["DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ"]

UMBRAL_ONI = 0.5
MESES_ONI = 5
INTENSIDAD_ONI = [(2.0, "muy fuerte"), (1.5, "fuerte"), (1.0, "moderado"), (0.5, "débil")]

# Categorías del ICEN (°C), de la Nota Técnica ENFEN: límite inferior de cada categoría cálida y
# límite superior de cada categoría fría. Condición neutra entre −1,0 y +0,4.
UMBRALES_ICEN = {"cálida extraordinaria": 3.0, "cálida fuerte": 1.7, "cálida moderada": 1.0, "cálida débil": 0.4,
                 "fría débil": -1.0, "fría moderada": -1.2, "fría fuerte": -1.4}
MESES_ICEN = 3  # meses consecutivos con condición cálida (fría) para declarar El Niño (La Niña) costero


# ------------------------------------------------------------------ descarga y lectura
def _texto(clave: str, carpeta=None) -> str:
    """Texto del archivo de NOAA. Se guarda una copia en `carpeta` (si se da) por si no hay conexión."""
    local = os.environ.get("CC_ENSO_LOCAL")
    nombre = URL[clave].rsplit("/", 1)[-1]
    if local:
        return (pathlib.Path(local) / nombre).read_text()
    copia = pathlib.Path(carpeta) / nombre if carpeta else None
    try:
        req = urllib.request.Request(URL[clave], headers={"User-Agent": "cambio-climatico-espam (docencia ESPAM MFL)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            texto = r.read().decode()
        if copia:
            copia.parent.mkdir(parents=True, exist_ok=True)
            copia.write_text(texto)
        return texto
    except Exception as err:
        if copia and copia.exists():
            print(f"Sin conexión con NOAA ({err}); uso la copia guardada del {pd.Timestamp(copia.stat().st_mtime, unit='s'):%Y-%m-%d}.")
            return copia.read_text()
        raise


def oni(carpeta=None) -> pd.Series:
    """ONI mensual: el valor del trimestre centrado en cada mes (DJF -> enero)."""
    filas = []
    for linea in _texto("oni", carpeta).splitlines()[1:]:
        p = linea.split()
        if len(p) == 4 and p[0] in TRIMESTRES:
            filas.append((pd.Timestamp(int(p[1]), TRIMESTRES.index(p[0]) + 1, 1), float(p[3])))
    s = pd.Series(dict(filas), name="ONI").sort_index()
    s.index.name = "fecha"
    return s


def nino12(carpeta=None) -> pd.Series:
    """Anomalía mensual de TSM en Niño 1+2 (ERSSTv5, base 1991–2020), °C."""
    filas = []
    for linea in _texto("nino", carpeta).splitlines()[1:]:
        p = linea.split()
        if len(p) >= 4:
            filas.append((pd.Timestamp(int(p[0]), int(p[1]), 1), float(p[3])))
    s = pd.Series(dict(filas), name="Nino12_anom").sort_index()
    s.index.name = "fecha"
    return s


def icen(carpeta=None) -> pd.Series:
    """ICEN: media móvil centrada de 3 meses de la anomalía de Niño 1+2."""
    return nino12(carpeta).rolling(3, center=True).mean().rename("ICEN").dropna()


# ------------------------------------------------------------------ fases y eventos
def categoria_icen(valor: float) -> str:
    if np.isnan(valor):
        return "sin dato"
    for nombre in ("cálida extraordinaria", "cálida fuerte", "cálida moderada", "cálida débil"):
        if valor >= UMBRALES_ICEN[nombre]:
            return nombre
    for nombre in ("fría fuerte", "fría moderada", "fría débil"):
        if valor < UMBRALES_ICEN[nombre]:
            return nombre
    return "neutra"


def _rachas(mascara: pd.Series, minimo: int) -> pd.Series:
    """True en los meses que pertenecen a una racha de al menos `minimo` meses consecutivos."""
    grupo = (mascara != mascara.shift()).cumsum()
    largo = mascara.groupby(grupo).transform("size")
    return mascara & (largo >= minimo)


def fases(indice: pd.Series, tipo: str = "ICEN") -> pd.Series:
    """Fase de cada mes: 'El Niño', 'La Niña' o 'Neutro', con la regla de persistencia del índice."""
    if tipo.upper() == "ONI":
        calido, frio, n = indice >= UMBRAL_ONI, indice <= -UMBRAL_ONI, MESES_ONI
    else:
        calido, frio, n = indice >= UMBRALES_ICEN["cálida débil"], indice < UMBRALES_ICEN["fría débil"], MESES_ICEN
    f = pd.Series("Neutro", index=indice.index, name=f"fase_{tipo.upper()}")
    f[_rachas(calido, n)] = "El Niño"
    f[_rachas(frio, n)] = "La Niña"
    return f


def eventos(indice: pd.Series, tipo: str = "ICEN") -> pd.DataFrame:
    """Tabla de episodios: fase, inicio, fin, meses, pico y categoría (por el valor pico)."""
    f = fases(indice, tipo)
    grupo = (f != f.shift()).cumsum()
    filas = []
    for _, g in f[f != "Neutro"].groupby(grupo[f != "Neutro"]):
        v = indice.loc[g.index]
        pico = v.max() if g.iloc[0] == "El Niño" else v.min()
        if tipo.upper() == "ONI":
            cat = next((n for u, n in INTENSIDAD_ONI if abs(pico) >= u), "débil")
        else:
            cat = categoria_icen(pico).replace("cálida ", "").replace("fría ", "")
        filas.append({"fase": g.iloc[0], "inicio": g.index[0].strftime("%Y-%m"), "fin": g.index[-1].strftime("%Y-%m"),
                      "meses": len(g), "pico": round(float(pico), 2), "mes_pico": v.idxmax().strftime("%Y-%m")
                      if g.iloc[0] == "El Niño" else v.idxmin().strftime("%Y-%m"), "intensidad": cat})
    return pd.DataFrame(filas)


def temporada(serie_mensual: pd.Series, meses=(12, 1, 2, 3, 4, 5), como: str = "sum") -> pd.Series:
    """Agrega una serie mensual por temporada. Si la temporada cruza el año (dic–may), se asigna al año en
    que termina. Solo se conservan temporadas completas."""
    meses = list(meses)
    cruza = meses[0] > meses[-1]
    s = serie_mensual[serie_mensual.index.month.isin(meses)].dropna()
    anio = s.index.year + ((s.index.month >= meses[0]) & cruza).astype(int)
    g = s.groupby(anio)
    out = g.sum() if como == "sum" else g.mean()
    out.index.name = "anio"
    return out[g.count() == len(meses)]
