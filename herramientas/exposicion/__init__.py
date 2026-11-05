"""Exposición del territorio a las amenazas climáticas (Práctica 2 de Riesgos de Desastres).

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

La tabla nacional `datos/exposicion/exposicion_cantones.csv` (ver `preparar.py`) trae, por cantón, la población
y la infraestructura totales y las que están en zona baja (< 10 m) o en ladera (> 20°). Este módulo la filtra
por provincia, le agrega el historial de eventos (DesInventar 1970–2007 y ECU 911 desde 2021) y califica la
exposición de cada cantón a cada amenaza de 1 a 5, por quintiles dentro de la provincia.

La calificación es **relativa a la provincia**: dice qué cantones están más expuestos que sus vecinos, no cuánto
lo están en términos absolutos. El equipo la revisa y la corrige con su conocimiento del territorio.
"""
from __future__ import annotations

import json
import math
import pathlib

import numpy as np
import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[2]
TABLA = RAIZ / "datos" / "exposicion" / "exposicion_cantones.csv"
META = RAIZ / "datos" / "exposicion" / "metadatos.json"
DESINVENTAR = RAIZ / "datos" / "eventos" / "desinventar_ecu_hidromet.csv.gz"
ECU911 = RAIZ / "datos" / "eventos" / "ecu911_gestion_riesgos.csv.gz"

# tipos de evento de los registros del curso que corresponden a cada amenaza de herramientas/riesgo.py
EVENTOS = {
    "inundacion": ["inundación", "aluvión", "lluvia intensa", "lluvia intensa o tormenta"],
    "movimiento_masa": ["deslizamiento", "hundimiento"],
    "costera": ["oleaje"],
    "sequia": ["sequía", "incendio forestal"],
    "calor": [],
}

# indicadores de exposición por amenaza (columnas de la tabla); se usan los que varían dentro de la provincia
INDICADORES = {
    "inundacion": ["poblacion_2022", "poblacion_cota_baja", "servicios", "km_vias_principales", "eventos_inundacion"],
    "movimiento_masa": ["poblacion_ladera", "servicios_ladera", "km_vias_ladera", "eventos_movimiento_masa"],
    "costera": ["poblacion_cota_baja", "servicios_cota_baja", "km_vias_cota_baja", "eventos_costera"],
    "sequia": ["poblacion_2022", "area_km2", "eventos_sequia"],
    "calor": ["poblacion_2022", "densidad_hab_km2"],
}

NOMBRES = {
    "poblacion_2022": "Población 2022 (hab)", "densidad_hab_km2": "Densidad (hab/km²)", "area_km2": "Área (km²)",
    "poblacion_cota_baja": "Población en zona baja < 10 m", "poblacion_ladera": "Población en ladera > 20°",
    "pct_cota_baja": "% de la población en zona baja", "pct_ladera": "% de la población en ladera",
    "escuelas": "Escuelas y colegios", "salud": "Establecimientos de salud", "emergencia": "Bomberos y policía",
    "servicios": "Servicios críticos (escuelas, salud, emergencia)",
    "servicios_cota_baja": "Servicios críticos en zona baja", "servicios_ladera": "Servicios críticos en ladera",
    "km_vias_principales": "Vías principales (km)", "km_vias_cota_baja": "Vías principales en zona baja (km)",
    "km_vias_ladera": "Vías principales en ladera (km)", "puentes": "Puentes en vías",
    "eventos_inundacion": "Eventos de inundación, aluvión y lluvia intensa",
    "eventos_movimiento_masa": "Eventos de deslizamiento y hundimiento", "eventos_costera": "Eventos de oleaje",
    "eventos_sequia": "Eventos de sequía e incendio forestal",
}


def metadatos() -> dict:
    return json.loads(META.read_text(encoding="utf-8")) if META.exists() else {}


def eventos_por_canton(codigo_provincia: str, desde_desinventar=True, desde_ecu911=True) -> pd.DataFrame:
    """Eventos por cantón y amenaza. DesInventar: fichas de desastre (con afectados y viviendas);
    ECU 911: días con incidentes del mismo tipo en el cantón (no son desastres verificados)."""
    cp = str(codigo_provincia).zfill(2)
    filas = []
    if desde_desinventar and DESINVENTAR.exists():
        d = pd.read_csv(DESINVENTAR, dtype={"cod_provincia": str, "cod_canton": str})
        d = d[(d.cod_provincia == cp) & (d.cod_canton.fillna("").str.len() == 4)]
        for a, tipos in EVENTOS.items():
            s = d[d.tipo.isin(tipos)]
            g = s.groupby("cod_canton").agg(n=("tipo", "size"), afectados=("afectados", "sum"), viviendas=("viviendas_afectadas", "sum"))
            for c, r in g.iterrows():
                filas.append({"codigo": c, "amenaza": a, "fuente": "DesInventar", "eventos": int(r.n),
                              "afectados": r.afectados, "viviendas": r.viviendas})
    if desde_ecu911 and ECU911.exists():
        e = pd.read_csv(ECU911, dtype={"cod_parroquia": str})
        e["codigo"] = e["cod_parroquia"].str.zfill(6).str[:4]
        e = e[e["codigo"].str[:2] == cp]
        for a, tipos in EVENTOS.items():
            s = e[e.tipo.isin(tipos)].drop_duplicates(["fecha", "codigo", "tipo"])
            for c, n in s.groupby("codigo").size().items():
                filas.append({"codigo": c, "amenaza": a, "fuente": "ECU 911", "eventos": int(n), "afectados": np.nan, "viviendas": np.nan})
    return pd.DataFrame(filas, columns=["codigo", "amenaza", "fuente", "eventos", "afectados", "viviendas"])


def de_provincia(provincia: str, eventos: pd.DataFrame | None = None) -> pd.DataFrame:
    """Tabla de exposición de los cantones de la provincia, con servicios agregados y eventos por amenaza."""
    from herramientas import limites

    if not TABLA.exists():
        raise FileNotFoundError("Aún no está la tabla de exposición (datos/exposicion/exposicion_cantones.csv). "
                                "Avise al docente: se genera con el flujo «Exposición por cantón» de GitHub Actions.")
    t = pd.read_csv(TABLA, dtype={"codigo": str, "codigo_provincia": str})
    t = t[t["provincia"].map(limites.normalizar) == limites.normalizar(provincia)].copy()
    if t.empty:
        raise ValueError(f"No hay cantones para la provincia «{provincia}»")
    t["canton"] = t["canton"].str.replace("Ð", "Ñ").str.replace("ð", "ñ").str.title()   # Ñ mal codificada en el origen
    for suf in ("", "_cota_baja", "_ladera"):
        cols = [f"{c}{suf}" for c in ("escuelas", "salud", "emergencia") if f"{c}{suf}" in t]
        if cols:
            t[f"servicios{suf}"] = t[cols].sum(axis=1)
    ev = eventos if eventos is not None else eventos_por_canton(t["codigo_provincia"].iloc[0])
    for a in EVENTOS:
        n = ev[ev.amenaza == a].groupby("codigo")["eventos"].sum() if len(ev) else pd.Series(dtype=float)
        t[f"eventos_{a}"] = t["codigo"].map(n).fillna(0).astype(int)
    return t.sort_values("poblacion_2022" if "poblacion_2022" in t else "canton", ascending=False).reset_index(drop=True)


def quintil(s: pd.Series) -> pd.Series:
    """Puntaje 1–5 por posición dentro de la provincia (0 si el valor es 0: no hay nada expuesto)."""
    s = pd.to_numeric(s, errors="coerce").fillna(0)
    pos = s[s > 0]
    out = pd.Series(0, index=s.index, dtype=int)
    if pos.empty:
        return out
    r = pos.rank(pct=True, method="average")
    out[pos.index] = np.ceil(r * 5).clip(1, 5).astype(int)
    return out


def calificar(t: pd.DataFrame, amenazas) -> tuple[pd.DataFrame, dict]:
    """Exposición 1–5 por cantón y amenaza: media de los quintiles de los indicadores que varían en la provincia.

    Un cantón con todos sus indicadores en 0 recibe 1 (nada o casi nada expuesto).
    Devuelve (tabla de puntajes, indicadores usados por amenaza).
    """
    punt, usados = pd.DataFrame({"codigo": t["codigo"], "canton": t["canton"]}), {}
    for a in amenazas:
        cols = [c for c in INDICADORES[a] if c in t and pd.to_numeric(t[c], errors="coerce").fillna(0).gt(0).any()]
        usados[a] = cols
        if not cols:
            punt[a] = np.nan
            continue
        q = pd.concat([quintil(t[c]) for c in cols], axis=1)
        punt[a] = q.mean(axis=1).round().clip(lower=1).astype(int)
    return punt, usados


def resumen_amenaza(t: pd.DataFrame, a: str, n=3) -> pd.DataFrame:
    """Los n cantones más expuestos a la amenaza, con sus indicadores en unidades reales."""
    cols = [c for c in INDICADORES[a] if c in t]
    return t.sort_values(cols[0], ascending=False)[["canton"] + cols].head(n)
