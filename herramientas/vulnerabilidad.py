"""Vulnerabilidad, riesgo por cantón y medidas (Práctica 2 de Riesgos de Desastres).

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Marco del IPCC AR6 (GTII): riesgo = f(amenaza, exposición, vulnerabilidad), con la vulnerabilidad formada por la
sensibilidad y la falta de capacidad de adaptación. Se usan los mismos indicadores y la misma escala 1–5 de
`herramientas/riesgo.py` (los de la ficha de riesgo de Ingeniería Ambiental), pero aplicados a **cantones**:

- A: amenaza de la provincia (1–5), justificada con el capítulo 1 (RD1_01, RD1_02).
- E: exposición del cantón a esa amenaza (1–5), de RD2_01.
- V = (S + (6 − CA)) / 2, con S = media de la sensibilidad y CA = media de la capacidad de adaptación del cantón.
- R = (A · E · V) ** (1/3), media geométrica (GIZ y EURAC, 2017; índice INFORM), en la escala 1–5.

Las calificaciones de S y CA las pone el equipo en una planilla, con un dato y su fuente (Censo 2022, PDOT, SNGR).
Este módulo arma esa planilla, la lee, calcula V y R, y evalúa el efecto de una cartera de medidas sobre el riesgo.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from herramientas import riesgo as RG

SENSIBILIDAD = RG.SENSIBILIDAD
CAPACIDAD = RG.CAPACIDAD

# Cómo calificar cada indicador (orientativo del curso) y dónde buscar el dato.
COMO_CALIFICAR = {
    "vivienda_precaria": "% de viviendas con paredes de caña, madera sin tratar o desechos: 1 < 5 % · 2 5–10 % · 3 10–20 % · 4 20–30 % · 5 > 30 %",
    "poblacion_vulnerable": "% de personas pobres por NBI: 1 < 20 % · 2 20–40 % · 3 40–60 % · 4 60–80 % · 5 > 80 % (suba 1 punto si hay mucha niñez, personas mayores o con discapacidad)",
    "dependencia_clima": "% de la población ocupada en agricultura, ganadería o pesca: 1 < 10 % · 2 10–25 % · 3 25–40 % · 4 40–60 % · 5 > 60 %",
    "degradacion": "1 ecosistemas conservados · 3 degradación en parte del cantón · 5 degradación extendida (deforestación, cauces rellenados, manglar talado, laderas sin cobertura)",
    "drenaje": "% de viviendas SIN alcantarillado (o sin agua por red pública): 1 < 10 % · 2 10–30 % · 3 30–50 % · 4 50–70 % · 5 > 70 %",
    "alerta": "1 no hay alerta temprana ni comités · 3 alerta en parte del cantón o comités sin simulacros · 5 alerta operativa con simulacros cada año",
    "acceso": "Servicios de salud y emergencia por 10 000 habitantes y vías (dato de apoyo de esta planilla): 1 muy pocos · 3 en la media del país · 5 muchos; baje 1 punto si hay comunidades que quedan aisladas en invierno",
    "planificacion": "1 PDOT sin gestión de riesgos · 3 PDOT con mapa de amenazas pero sin ordenanza que limite el uso del suelo · 5 mapa, ordenanza y control efectivo",
    "recursos": "1 sin presupuesto para riesgos ni seguros · 3 presupuesto mínimo o seguro agrícola parcial · 5 fondo de contingencia y seguros extendidos",
}
DONDE_BUSCAR = {
    "vivienda_precaria": "Censo 2022 (INEC), resultados por cantón: material de paredes de la vivienda · PDOT, diagnóstico de asentamientos humanos",
    "poblacion_vulnerable": "Censo 2022: pobreza por NBI, población de 0–14 y de 65 años o más · CONADIS: personas con discapacidad por cantón",
    "dependencia_clima": "Censo 2022: población ocupada por rama de actividad · PDOT, diagnóstico económico productivo",
    "degradacion": "PDOT, diagnóstico biofísico · mapa de cobertura y uso de la tierra del MAATE o MapBiomas Ecuador · Google Earth (imágenes históricas)",
    "drenaje": "Censo 2022: eliminación de aguas servidas y procedencia del agua · PDOT, servicios básicos",
    "alerta": "SNGR (gestiónderiesgos.gob.ec): SAT y comités comunitarios · unidad de gestión de riesgos del GAD · prensa local",
    "acceso": "Dato de apoyo de la planilla (OpenStreetMap) · PDOT, movilidad · albergues y rutas de evacuación de la SNGR",
    "planificacion": "PDOT vigente del cantón (2024–2027, alineado al PND 2025–2029) y ordenanzas de uso y gestión del suelo (PUGS)",
    "recursos": "Presupuesto del GAD (rendición de cuentas) · seguro agrícola del MAG · fondos de contingencia ante El Niño",
}

# Qué componente del riesgo reduce cada medida del catálogo (herramientas/estrategias.py)
REDUCE_EXPOSICION = {"A03", "A06"}

# Prioridad del Marco de Sendai (2015–2030) a la que contribuye cada medida del catálogo
SENDAI = {1: "1. Comprender el riesgo de desastres", 2: "2. Fortalecer la gobernanza del riesgo",
          3: "3. Invertir en la reducción del riesgo para la resiliencia",
          4: "4. Aumentar la preparación para una respuesta eficaz y «reconstruir mejor»"}
SENDAI_MEDIDA = {"A01": 4, "A02": 3, "A03": 2, "A04": 3, "A05": 3, "A06": 3, "A07": 3, "A08": 3, "A09": 3, "A10": 4,
                 "A11": 3, "A12": 4, "A13": 3, "A14": 4, "M05": 3, "M08": 3, "M10": 3, "M11": 3, "M12": 3, "M13": 3, "M15": 3}

ACTORES = [  # (texto del sector del catálogo, actor principal sugerido); se usa el primero que coincide
    ("gestión de riesgos", "GAD cantonal (unidad de gestión de riesgos) con la SNGR"),
    ("asentamientos humanos", "GAD cantonal (planificación y obras públicas)"),
    ("salud", "MSP y GAD cantonal"),
    ("patrimonio natural", "MAATE, GAD provincial y comunidades"),
    ("patrimonio hídrico", "GAD provincial (riego y drenaje) y juntas de agua"),
    ("soberanía alimentaria", "MAG y GAD provincial (fomento productivo)"),
    ("USCUSS", "MAATE (Socio Bosque) y GAD provincial"),
    ("transporte", "GAD cantonal (tránsito y movilidad) y MTOP"),
    ("Energía", "MEM, empresa eléctrica y GAD"),
    ("Residuos", "GAD cantonal (gestión de residuos) con el MAATE"),
    ("Agricultura", "MAG y productores"),
]

ALCANCE = pd.DataFrame(
    [["Qué reduce", "Las emisiones de gases de efecto invernadero: a largo plazo, la amenaza global",
      "La exposición o la vulnerabilidad del cantón: el riesgo local"],
     ["Escala del beneficio", "Global (la atmósfera es una sola); el beneficio local llega por los cobeneficios",
      "Local: lo recibe el territorio donde se aplica"],
     ["Cuándo se nota", "Décadas: el clima responde lento a las emisiones acumuladas",
      "Inmediato o en pocos años, en el próximo invierno o El Niño"],
     ["Cómo se mide", "t CO2-eq evitadas por año", "Cambio del índice de riesgo, personas o viviendas protegidas"],
     ["Instrumento en Ecuador", "Segunda NDC 2026–2035 (componente de mitigación)",
      "PLANACC, Segunda NDC (adaptación), Marco de Sendai, PDOT"],
     ["Límite", "No protege a nadie del próximo evento", "Tiene límites: con más calentamiento, algunas medidas dejan de bastar"]],
    columns=["", "Mitigación", "Adaptación y reducción del riesgo"]).set_index("")


def _num(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else np.nan
    except (TypeError, ValueError):
        return np.nan


def apoyo(t: pd.DataFrame, eventos: pd.DataFrame, pais: pd.DataFrame | None = None) -> pd.DataFrame:
    """Indicadores de apoyo por cantón (no reemplazan la calificación del equipo).

    t: tabla de exposición de la provincia (exposicion.de_provincia); eventos: exposicion.eventos_por_canton;
    pais: exposicion.de_pais(), para ubicar el acceso a servicios en la distribución nacional.
    """
    a = t[["codigo", "canton", "poblacion_2022", "area_km2", "pct_cota_baja", "pct_ladera"]].copy()
    pob = a["poblacion_2022"].replace(0, np.nan)
    a["servicios_salud_emergencia_10k"] = 1e4 * (t["salud"] + t["emergencia"]) / pob
    a["km_vias_100km2"] = 100 * t["km_vias_principales"] / t["area_km2"]
    d = eventos[eventos.fuente == "DesInventar"] if len(eventos) else eventos
    af = d.groupby("codigo")["afectados"].sum() if len(d) else pd.Series(dtype=float)
    vv = d.groupby("codigo")["viviendas"].sum() if len(d) else pd.Series(dtype=float)
    a["afectados_1970_2007"] = a["codigo"].map(af).fillna(0)
    a["afectados_por_1000_hab"] = 1000 * a["afectados_1970_2007"] / pob
    a["viviendas_afectadas_1970_2007"] = a["codigo"].map(vv).fillna(0)
    if pais is not None and len(pais):
        ref = 1e4 * (pais["salud"] + pais["emergencia"]) / pais["poblacion_2022"].replace(0, np.nan)
        ref = ref.dropna()
        a["sugerencia_acceso"] = a["servicios_salud_emergencia_10k"].map(
            lambda v: np.nan if not np.isfinite(v) else int(np.clip(np.ceil(5 * (ref < v).mean() + 1e-9), 1, 5)))
    return a


NOMBRES_APOYO = {"pct_cota_baja": "% población en zona baja", "pct_ladera": "% población en ladera",
                 "servicios_salud_emergencia_10k": "Salud y emergencia por 10 000 hab",
                 "km_vias_100km2": "Vías principales por 100 km²",
                 "afectados_por_1000_hab": "Afectados históricos por 1 000 hab (DesInventar 1970–2007)",
                 "viviendas_afectadas_1970_2007": "Viviendas afectadas (DesInventar 1970–2007)",
                 "sugerencia_acceso": "Sugerencia para «acceso» (1–5, frente al país)"}


def plantilla(cantones, ap: pd.DataFrame) -> pd.DataFrame:
    """Planilla para calificar la sensibilidad y la capacidad de cada cantón prioritario."""
    filas = []
    for c in cantones:
        r = ap.set_index("canton").loc[c] if c in set(ap["canton"]) else None
        for comp, d in (("sensibilidad", SENSIBILIDAD), ("capacidad", CAPACIDAD)):
            for k, nom in d.items():
                dato = ""
                if r is not None and k == "acceso":
                    dato = (f"{r['servicios_salud_emergencia_10k']:.1f} servicios de salud y emergencia por 10 000 hab; "
                            f"{r['km_vias_100km2']:.1f} km de vías principales por 100 km²")
                    if "sugerencia_acceso" in r and pd.notna(r["sugerencia_acceso"]):
                        dato += f"; sugerencia {int(r['sugerencia_acceso'])}"
                if r is not None and k == "poblacion_vulnerable" and r["afectados_1970_2007"] > 0:
                    dato = f"Daño histórico: {r['afectados_por_1000_hab']:.0f} afectados por 1 000 hab en 1970–2007 (DesInventar)"
                filas.append({"canton": c, "componente": comp, "clave": k, "indicador": nom,
                              "como_calificar": COMO_CALIFICAR[k], "donde_buscar": DONDE_BUSCAR[k],
                              "dato_de_apoyo": dato, "dato_encontrado": "", "valor": "", "fuente": "", "justificacion": ""})
    return pd.DataFrame(filas)


def leer_calificaciones(p: pd.DataFrame, cantones) -> tuple[pd.DataFrame, list, bool]:
    """Valida la planilla llena. Devuelve (calificaciones, avisos, provisional).

    Un valor vacío se reemplaza por 3 (provisional): sirve para ver el flujo en clase, no para entregar.
    """
    p = p.copy()
    p["valor"] = p["valor"].map(_num)
    avisos, provisional = [], False
    faltan = [c for c in cantones if c not in set(p["canton"])]
    if faltan:
        avisos.append(f"La planilla no tiene filas para: {', '.join(faltan)}. Bórrela y vuelva a ejecutar la sección 6, o agregue sus filas.")
    fuera = p[p["valor"].notna() & ~p["valor"].between(1, 5)]
    if len(fuera):
        raise ValueError("Valores fuera de 1–5 en la planilla: " + "; ".join(f"{r.canton} · {r.clave} = {r.valor:g}" for r in fuera.itertuples()))
    vacios = p["valor"].isna()
    if vacios.any():
        provisional = True
        avisos.append(f"{int(vacios.sum())} de {len(p)} calificaciones están vacías: se usó 3 (PROVISIONAL). No es válido para entregar.")
        p.loc[vacios, "valor"] = 3
    p["valor"] = p["valor"].round().astype(int)
    for col in ("fuente", "justificacion", "dato_encontrado"):
        p[col] = p[col].fillna("").astype(str).str.strip()
    sin = p[~vacios & ((p["fuente"] == "") | (p["justificacion"] == ""))]
    if len(sin):
        avisos.append(f"{len(sin)} calificaciones no tienen fuente o justificación (por ejemplo, {sin.iloc[0].canton} · {sin.iloc[0].indicador}).")
    for c, g in p.groupby("canton"):
        if g["valor"].nunique() == 1 and not vacios[g.index].all():
            avisos.append(f"{c}: todas las calificaciones son iguales ({g['valor'].iloc[0]}); revise si reflejan el cantón.")
    return p, avisos, provisional


def vulnerabilidad(cal: pd.DataFrame) -> pd.DataFrame:
    """S, CA y V por cantón, con el indicador de sensibilidad más alto y el de capacidad más bajo."""
    filas = []
    for c, g in cal.groupby("canton", sort=False):
        s = g[g.componente == "sensibilidad"].set_index("clave")["valor"]
        ca = g[g.componente == "capacidad"].set_index("clave")["valor"]
        S, CA = s.mean(), ca.mean()
        filas.append({"canton": c, "S": round(S, 2), "CA": round(CA, 2), "falta_de_capacidad": round(6 - CA, 2),
                      "V": round((S + 6 - CA) / 2, 2), "sensibilidad_critica": s.idxmax(), "valor_s": int(s.max()),
                      "capacidad_debil": ca.idxmin(), "valor_ca": int(ca.min())})
    return pd.DataFrame(filas).set_index("canton")


def indice(a: float, e: float, v: float) -> float:
    return round((a * e * v) ** (1 / 3), 2)


def riesgo_cantones(amenazas: dict, expo: pd.DataFrame, vul: pd.DataFrame) -> pd.DataFrame:
    """Riesgo por cantón y amenaza. amenazas: {clave: A}; expo: puntajes de RD2_01 (canton + columnas por amenaza)."""
    E = expo.set_index("canton")
    filas = []
    for c, rv in vul.iterrows():
        for k, a in amenazas.items():
            if not a or k not in E or c not in E.index or pd.isna(E.loc[c, k]):
                continue
            e = int(E.loc[c, k]); r = indice(a, e, rv.V)
            comp = {"amenaza": a, "exposición": e, "vulnerabilidad": rv.V}
            filas.append({"canton": c, "clave": k, "amenaza": RG.AMENAZA_CORTA[k], "A": a, "E": e, "V": rv.V,
                          "R": r, "clase": RG.clase(r), "pesa_mas": max(comp, key=comp.get)})
    return pd.DataFrame(filas).sort_values("R", ascending=False).reset_index(drop=True)


def frase(r: pd.Series, vul: pd.DataFrame) -> str:
    """Frase de ejemplo para el capítulo 2 a partir de una fila de riesgo_cantones."""
    v = vul.loc[r.canton]
    return (f"En {r.canton}, el riesgo de {r.amenaza.lower()} es {r.clase} (R = {r.R:.1f} de 5): amenaza {r.A}, exposición {r.E} "
            f"y vulnerabilidad {r.V:.1f}. Lo que más pesa es la {r.pesa_mas}. En la vulnerabilidad destacan "
            f"«{SENSIBILIDAD[v.sensibilidad_critica].lower()}» (sensibilidad {v.valor_s}) y una capacidad débil en "
            f"«{CAPACIDAD[v.capacidad_debil].lower()}» ({v.valor_ca}).")


def componentes_que_reduce(cat: pd.DataFrame) -> pd.Series:
    """Componente del riesgo (o emisiones) que reduce cada medida del catálogo."""
    out = {}
    for i, r in cat.iterrows():
        c = []
        if r.tipo in ("M", "MA"):
            c.append("emisiones")
        if i in REDUCE_EXPOSICION:
            c.append("exposición")
        if any(f in SENSIBILIDAD for f in r.factores):
            c.append("sensibilidad")
        if any(f in CAPACIDAD for f in r.factores):
            c.append("capacidad")
        if r.tipo in ("A", "MA") and len(c) == (1 if r.tipo == "MA" else 0):
            c.append("vulnerabilidad")
        out[i] = ", ".join(c)
    return pd.Series(out)


def actor(sector: str) -> str:
    for clave, a in ACTORES:
        if clave.lower() in str(sector).lower():
            return a
    return "Defínalo el equipo"


def efecto_cartera(cal_canton: pd.DataFrame, expo_canton: dict, amenazas: dict, cartera: pd.DataFrame, efecto: int = 1) -> tuple[pd.DataFrame, list]:
    """Riesgo del cantón antes y después de aplicar las medidas de adaptación de la cartera (supuesto simple).

    Cada medida A o MA de la cartera mejora en `efecto` puntos los indicadores que atiende (baja la sensibilidad,
    sube la capacidad); A03 y A06 bajan la exposición a sus amenazas. Las medidas solo de mitigación (M) no cambian
    el riesgo local en el corto plazo. Devuelve (tabla antes/después, cambios aplicados).
    """
    s = cal_canton[cal_canton.componente == "sensibilidad"].set_index("clave")["valor"].astype(float).copy()
    ca = cal_canton[cal_canton.componente == "capacidad"].set_index("clave")["valor"].astype(float).copy()
    e = {k: float(v) for k, v in expo_canton.items()}
    cambios = []
    for i, r in cartera.iterrows():
        if r.tipo == "M":
            cambios.append(f"{i}: solo mitigación, sin efecto en el riesgo local a corto plazo")
            continue
        for f in r.factores:
            if f in s.index and s[f] > 1:
                s[f] = max(1, s[f] - efecto); cambios.append(f"{i}: sensibilidad «{f}» −{efecto}")
            if f in ca.index and ca[f] < 5:
                ca[f] = min(5, ca[f] + efecto); cambios.append(f"{i}: capacidad «{f}» +{efecto}")
        if i in REDUCE_EXPOSICION:
            for k in r.amenazas:
                if k in e and e[k] > 1:
                    e[k] = max(1, e[k] - efecto); cambios.append(f"{i}: exposición a {k} −{efecto}")
    S0 = cal_canton[cal_canton.componente == "sensibilidad"]["valor"].mean()
    CA0 = cal_canton[cal_canton.componente == "capacidad"]["valor"].mean()
    V0, V1 = (S0 + 6 - CA0) / 2, (s.mean() + 6 - ca.mean()) / 2
    filas = []
    for k, a in amenazas.items():
        if not a or k not in expo_canton or pd.isna(expo_canton[k]):
            continue
        r0, r1 = indice(a, expo_canton[k], V0), indice(a, e[k], V1)
        filas.append({"clave": k, "amenaza": RG.AMENAZA_CORTA[k], "R_antes": r0, "clase_antes": RG.clase(r0),
                      "R_despues": r1, "clase_despues": RG.clase(r1), "reduccion_%": round(100 * (r0 - r1) / r0, 1),
                      "V_antes": round(V0, 2), "V_despues": round(V1, 2), "E_antes": expo_canton[k], "E_despues": e[k]})
    return pd.DataFrame(filas), cambios


def sugerencia_amenaza(n_eventos: int) -> int:
    """Calificación orientativa de la amenaza por el número de eventos registrados en la provincia."""
    for lim, s in ((1, 1), (6, 2), (21, 3), (61, 4)):
        if n_eventos < lim:
            return s
    return 5
