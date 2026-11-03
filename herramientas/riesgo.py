"""Ficha de riesgo climático de un sitio con el marco del IPCC AR6 (GTII).

Riesgo = f(amenaza, exposición, vulnerabilidad); vulnerabilidad = sensibilidad y falta de
capacidad de adaptación. Cada componente se califica de 1 (muy bajo) a 5 (muy alto) con los
descriptores de abajo, que son los mismos de la hoja de campo de la guía.

Índice por amenaza (escala 1–5): R = (A · E · V) ** (1/3), media geométrica (como en el
Vulnerability Sourcebook de GIZ, 2017, y el índice INFORM), con V = (S + (6 − CA)) / 2.
"""
from __future__ import annotations

import math

import pandas as pd

AMENAZAS = {
    "inundacion": "Inundación por lluvia intensa y crecida de ríos",
    "movimiento_masa": "Movimientos en masa (deslizamientos, flujos de lodo)",
    "costera": "Inundación costera, oleaje y erosión",
    "sequia": "Sequía y déficit de agua",
    "calor": "Calor extremo",
}

DESC_AMENAZA = {1: "no hay registros ni evidencia física", 2: "evidencia débil o eventos muy raros",
                3: "eventos ocasionales; evidencia en el sitio (marcas, relatos)",
                4: "eventos frecuentes o intensos; con El Niño se agravan claramente",
                5: "eventos recurrentes y severos; daños documentados repetidos"}

EXPOSICION = {
    "personas": "Personas en el sitio o su área de influencia",
    "viviendas": "Viviendas y edificaciones",
    "servicios": "Servicios críticos (agua, salud, escuelas, vías, energía)",
    "economia": "Actividades económicas (cultivos, pesca, turismo, comercio)",
    "ecosistemas": "Ecosistemas y servicios ecosistémicos (manglar, bosque, río, playa)",
}
DESC_EXPOSICION = {1: "nada o casi nada expuesto", 2: "poco expuesto, disperso", 3: "exposición moderada",
                   4: "mucho expuesto, concentrado", 5: "concentración muy alta en la zona de amenaza"}

SENSIBILIDAD = {
    "vivienda_precaria": "Viviendas de materiales precarios o sin cimentación adecuada",
    "poblacion_vulnerable": "Pobreza, niñez, personas mayores o con discapacidad",
    "dependencia_clima": "Dependencia de actividades sensibles al clima (agricultura de secano, pesca)",
    "degradacion": "Degradación del ecosistema (deforestación, relleno de cauces, manglar talado)",
    "drenaje": "Drenaje, saneamiento o abastecimiento de agua deficiente",
}
CAPACIDAD = {
    "alerta": "Alerta temprana y organización comunitaria ante eventos",
    "acceso": "Acceso a servicios, vías de evacuación y albergues",
    "planificacion": "Gestión del riesgo en el PDOT, ordenanzas y control de uso del suelo",
    "recursos": "Recursos económicos, seguros o fondos de contingencia",
}
DESC_SENSIBILIDAD = {1: "muy baja", 2: "baja", 3: "media", 4: "alta", 5: "muy alta"}
DESC_CAPACIDAD = {1: "inexistente", 2: "débil", 3: "parcial", 4: "buena", 5: "muy buena"}

CLASES = [(1.8, "muy bajo"), (2.6, "bajo"), (3.4, "medio"), (4.2, "alto"), (5.01, "muy alto")]
COLOR_CLASE = {"muy bajo": "#2F6DB5", "bajo": "#7FB3D5", "medio": "#E8C547", "alto": "#E07B39", "muy alto": "#B22222"}


def _valida(d: dict, nombre: str, permite_cero=False):
    for k, v in d.items():
        ok = (v == 0 and permite_cero) or (1 <= v <= 5)
        if not ok:
            raise ValueError(f"{nombre} «{k}» = {v}: use un valor entero de 1 a 5" + (" (0 = no aplica)" if permite_cero else ""))


def clase(r: float) -> str:
    for lim, nom in CLASES:
        if r < lim:
            return nom
    return "muy alto"


def componentes(exposicion: dict, sensibilidad: dict, capacidad: dict) -> dict:
    _valida(exposicion, "Exposición"); _valida(sensibilidad, "Sensibilidad"); _valida(capacidad, "Capacidad")
    E = sum(exposicion.values()) / len(exposicion)
    S = sum(sensibilidad.values()) / len(sensibilidad)
    CA = sum(capacidad.values()) / len(capacidad)
    V = (S + (6 - CA)) / 2
    return {"exposicion": E, "sensibilidad": S, "capacidad_adaptativa": CA, "falta_de_capacidad": 6 - CA, "vulnerabilidad": V}


def indice(amenazas: dict, comp: dict) -> pd.DataFrame:
    """amenazas: {clave: 0–5}; 0 = no aplica en el sitio (se omite)."""
    _valida(amenazas, "Amenaza", permite_cero=True)
    filas = []
    for k, a in amenazas.items():
        if not a:
            continue
        r = (a * comp["exposicion"] * comp["vulnerabilidad"]) ** (1 / 3)
        filas.append({"clave": k, "amenaza": AMENAZAS[k], "A": a, "E": round(comp["exposicion"], 2),
                      "V": round(comp["vulnerabilidad"], 2), "riesgo": round(r, 2), "clase": clase(r)})
    if not filas:
        raise ValueError("Califique al menos una amenaza con un valor de 1 a 5")
    return pd.DataFrame(filas).sort_values("riesgo", ascending=False).reset_index(drop=True)


def factor_dominante(exposicion: dict, sensibilidad: dict, capacidad: dict) -> dict:
    """Indicadores más críticos: exposición y sensibilidad más altas, capacidad más baja."""
    return {"exposicion": max(exposicion, key=exposicion.get), "sensibilidad": max(sensibilidad, key=sensibilidad.get),
            "capacidad": min(capacidad, key=capacidad.get)}


def sugerencia_lluvia(factor_nino: float) -> int:
    """Calificación orientativa de la amenaza por lluvia según cuánto aumenta la lluvia de dic–may en El Niño."""
    if factor_nino is None or (isinstance(factor_nino, float) and math.isnan(factor_nino)):
        return 0
    for lim, s in ((1.15, 2), (1.5, 3), (2.0, 4)):
        if factor_nino < lim:
            return s
    return 5


def sugerencia_calor(tx90p_por_decada: float) -> int:
    if tx90p_por_decada is None or (isinstance(tx90p_por_decada, float) and math.isnan(tx90p_por_decada)):
        return 0
    for lim, s in ((0.5, 1), (1.5, 2), (3.0, 3), (5.0, 4)):
        if tx90p_por_decada < lim:
            return s
    return 5

AMENAZA_CORTA = {"inundacion": "Inundación", "movimiento_masa": "Movimiento en masa", "costera": "Costera (oleaje, erosión)",
                 "sequia": "Sequía", "calor": "Calor extremo"}
