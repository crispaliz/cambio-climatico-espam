"""Catálogo de opciones de mitigación y adaptación y evaluación multicriterio.

Cada opción se vincula con categorías del inventario (códigos IPCC de IA2_01), con amenazas
de la ficha de riesgo (claves de herramientas.riesgo.AMENAZAS) y con indicadores de
sensibilidad o capacidad. El cuaderno IA2_03 sugiere las que corresponden a las categorías
principales y a las amenazas de riesgo medio o mayor; el estudiante puede agregar otras.

Fuentes de las opciones: IPCC AR6 GTIII (2022), cap. 7 (AFOLU), 10 (transporte) y 12;
IPCC AR6 GTII (2022), cap. 12 (América Central y del Sur) y cap. 17 (opciones de adaptación);
MAATE (2025), Segunda NDC del Ecuador; MAATE, Plan Nacional de Adaptación al Cambio Climático (PLANACC).
"""
from __future__ import annotations

import pandas as pd

# tipo: M (mitigación), A (adaptación), MA (las dos)
CATALOGO = [
    # id, nombre, tipo, enfoque, categorías IPCC, amenazas, factores de vulnerabilidad, sector NDC/PLANACC, alerta de mala adaptación
    ("M01", "Transporte público eficiente y movilidad activa (ciclovías, rutas troncales)", "M", "infraestructura", ["1A3b"], [], [], "Energía: transporte", ""),
    ("M02", "Renovación de flota y electromovilidad (taxis, buses, motos)", "M", "tecnológico", ["1A3b"], [], [], "Energía: transporte", "Solo reduce si la electricidad es de baja emisión (factor del SNI ≈ 0,16 t/MWh)"),
    ("M03", "Cocción eléctrica de inducción en lugar de GLP", "M", "tecnológico", ["1A4b"], [], [], "Energía: residencial", "Depende de la tarifa y de la confiabilidad del servicio eléctrico"),
    ("M04", "Eficiencia energética y solar fotovoltaica en edificios públicos", "M", "tecnológico", ["Memo"], ["calor"], [], "Energía: generación y eficiencia", ""),
    ("M05", "Ganadería sostenible: pasturas mejoradas y sistemas silvopastoriles", "MA", "basado en ecosistemas", ["3A1", "3A2"], ["calor", "sequia"], ["dependencia_clima", "degradacion"], "Agricultura / PLANACC: soberanía alimentaria y producción", ""),
    ("M06", "Manejo de la dieta y de la carga animal (más producción por cabeza)", "M", "tecnológico", ["3A1"], [], [], "Agricultura", "Si aumenta el hato total, las emisiones no bajan"),
    ("M07", "Biodigestores para el estiércol de granjas porcinas y lecheras", "M", "tecnológico", ["3A2"], [], ["drenaje"], "Agricultura / Residuos", ""),
    ("M08", "Arroz con riego intermitente (alternancia de humedecimiento y secado)", "MA", "tecnológico", ["3C7"], ["sequia"], ["dependencia_clima"], "Agricultura / PLANACC: patrimonio hídrico", "Puede aumentar algo el N2O; requiere control del agua"),
    ("M09", "Fertilización eficiente: dosis según análisis de suelo y aplicación fraccionada", "M", "tecnológico", ["3C4", "3C5"], [], [], "Agricultura", ""),
    ("M10", "Conservación de bosques y control de la deforestación (Socio Bosque, REDD+)", "MA", "basado en ecosistemas", ["3B1b"], ["movimiento_masa", "inundacion", "sequia"], ["degradacion"], "USCUSS / PLANACC: patrimonio natural", ""),
    ("M11", "Restauración de bosque seco y de riberas con especies nativas", "MA", "basado en ecosistemas", ["3B1b"], ["inundacion", "movimiento_masa", "calor"], ["degradacion"], "USCUSS / PLANACC: patrimonio natural", "Plantaciones de una sola especie exótica no restauran el ecosistema"),
    ("M12", "Conservación y restauración de manglar (carbono azul)", "MA", "basado en ecosistemas", ["3B1b"], ["costera"], ["degradacion", "dependencia_clima"], "USCUSS / PLANACC: patrimonio natural", ""),
    ("M13", "Cierre técnico de botaderos y relleno sanitario con captura o quema de metano", "MA", "infraestructura", ["4A"], ["inundacion"], ["drenaje"], "Residuos / PLANACC: salud", ""),
    ("M14", "Separación en la fuente y compostaje de residuos orgánicos", "M", "social", ["4A"], [], [], "Residuos", ""),
    ("M15", "Tratamiento de aguas residuales (lagunas cubiertas con captura de biogás o tratamiento aerobio)", "MA", "infraestructura", ["4D1"], ["inundacion"], ["drenaje"], "Residuos / PLANACC: salud y agua", ""),
    ("A01", "Sistema de alerta temprana comunitario ante crecidas y lluvias intensas", "A", "institucional", [], ["inundacion", "movimiento_masa"], ["alerta"], "PLANACC: asentamientos humanos (gestión de riesgos)", ""),
    ("A02", "Mantenimiento y ampliación del drenaje pluvial y limpieza de cauces antes del invierno", "A", "infraestructura", [], ["inundacion"], ["drenaje"], "PLANACC: asentamientos humanos", "Canalizar sin espacio para el río traslada la inundación aguas abajo"),
    ("A03", "Ordenamiento territorial: prohibir construir en zonas inundables y laderas inestables (PDOT)", "A", "institucional", [], ["inundacion", "movimiento_masa", "costera"], ["planificacion"], "PLANACC: asentamientos humanos", ""),
    ("A04", "Estabilización de taludes con bioingeniería y revegetación", "MA", "basado en ecosistemas", [], ["movimiento_masa"], ["degradacion"], "PLANACC: asentamientos humanos (gestión de riesgos)", ""),
    ("A05", "Defensa costera basada en ecosistemas: manglar, dunas y playas vivas", "MA", "basado en ecosistemas", [], ["costera"], ["degradacion"], "PLANACC: patrimonio natural", ""),
    ("A06", "Reubicación planificada o elevación de viviendas en la franja costera", "A", "infraestructura", [], ["costera", "inundacion"], ["vivienda_precaria"], "PLANACC: asentamientos humanos", "Muros y escolleras sin estudio aceleran la erosión de las playas vecinas"),
    ("A07", "Cosecha de agua lluvia y reservorios comunitarios", "A", "infraestructura", [], ["sequia"], ["drenaje", "dependencia_clima"], "PLANACC: patrimonio hídrico", ""),
    ("A08", "Riego tecnificado y variedades tolerantes a sequía y calor", "A", "tecnológico", [], ["sequia", "calor"], ["dependencia_clima"], "PLANACC: soberanía alimentaria y producción", "Ampliar el riego sin gestión de la demanda agota el acuífero"),
    ("A09", "Arbolado urbano, sombra y horarios de trabajo protegidos ante el calor", "MA", "basado en ecosistemas", [], ["calor"], ["poblacion_vulnerable"], "PLANACC: salud", ""),
    ("A10", "Vigilancia de vectores (dengue, malaria) y saneamiento después de las inundaciones", "A", "institucional", [], ["inundacion"], ["poblacion_vulnerable", "drenaje"], "PLANACC: salud", ""),
    ("A11", "Seguro agrícola y fondo de contingencia del GAD ante El Niño", "A", "institucional", [], ["inundacion", "sequia"], ["recursos", "dependencia_clima"], "PLANACC: soberanía alimentaria y producción", ""),
    ("A12", "Planes de contingencia y simulacros en barrios, escuelas y centros de salud", "A", "social", [], ["inundacion", "movimiento_masa", "costera"], ["alerta", "acceso"], "PLANACC: asentamientos humanos (gestión de riesgos)", ""),
    ("A13", "Mejoramiento de viviendas: materiales resistentes, pisos elevados y cimentación", "A", "infraestructura", [], ["inundacion", "costera", "movimiento_masa"], ["vivienda_precaria"], "PLANACC: asentamientos humanos", ""),
    ("A14", "Vías de evacuación, albergues y accesos alternos", "A", "infraestructura", [], ["inundacion", "movimiento_masa", "costera"], ["acceso"], "PLANACC: asentamientos humanos (gestión de riesgos)", ""),
]
COLUMNAS = ["id", "opcion", "tipo", "enfoque", "categorias", "amenazas", "factores", "sector", "alerta_mala_adaptacion"]

CRITERIOS = {
    "efectividad": "Cuánto reduce las emisiones o el riesgo del sitio (5 = mucho)",
    "costo": "Costo de inversión y operación (5 = bajo costo)",
    "factibilidad": "Factibilidad técnica, institucional y social en la provincia (5 = muy factible)",
    "cobeneficios": "Beneficios adicionales: salud, empleo, biodiversidad, agua (5 = muchos)",
    "sinergia": "Contribuye a la vez a mitigar y a adaptarse (5 = ambas, claramente)",
    "mala_adaptacion": "Riesgo de mala adaptación o de efectos no deseados (5 = riesgo bajo)",
    "alineacion": "Alineación con la NDC, el PLANACC y el PDOT (5 = explícita)",
}
PESOS = {"efectividad": 0.25, "costo": 0.10, "factibilidad": 0.20, "cobeneficios": 0.15, "sinergia": 0.10,
         "mala_adaptacion": 0.10, "alineacion": 0.10}


def catalogo() -> pd.DataFrame:
    return pd.DataFrame(CATALOGO, columns=COLUMNAS).set_index("id")


def sugerir(categorias_principales, amenazas_relevantes, factores_criticos) -> pd.DataFrame:
    """Opciones del catálogo vinculadas con lo que salió en IA2_01 e IA2_02, con el motivo."""
    c = catalogo()
    cp = {x.split(" ")[0] for x in categorias_principales}
    motivos = {}
    for i, r in c.iterrows():
        m = []
        hit = [k for k in r.categorias if k in cp]
        if hit: m.append("inventario: " + ", ".join(hit))
        hit = [k for k in r.amenazas if k in amenazas_relevantes]
        if hit: m.append("riesgo: " + ", ".join(hit))
        hit = [k for k in r.factores if k in factores_criticos]
        if hit: m.append("vulnerabilidad: " + ", ".join(hit))
        if m: motivos[i] = "; ".join(m)
    s = c.loc[list(motivos)].copy()
    s["motivo"] = pd.Series(motivos)
    return s


def leer_evaluacion(texto: str) -> pd.DataFrame:
    """Lee el bloque «id; efectividad; costo; ...; justificación» que escribe el estudiante."""
    filas = []
    for n, linea in enumerate(texto.strip().splitlines(), 1):
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        p = [x.strip() for x in linea.split(";")]
        if len(p) < 1 + len(CRITERIOS):
            raise ValueError(f"Línea {n}: faltan columnas ({len(p)}); se esperan id, {len(CRITERIOS)} puntajes y una justificación")
        try:
            puntos = [int(x) for x in p[1:1 + len(CRITERIOS)]]
        except ValueError:
            raise ValueError(f"Línea {n}: los puntajes deben ser enteros de 1 a 5") from None
        if any(not 1 <= x <= 5 for x in puntos):
            raise ValueError(f"Línea {n}: los puntajes van de 1 a 5")
        filas.append([p[0], *puntos, ";".join(p[1 + len(CRITERIOS):]).strip()])
    return pd.DataFrame(filas, columns=["id", *CRITERIOS, "justificacion"]).set_index("id")


def puntuar(ev: pd.DataFrame, pesos=PESOS) -> pd.Series:
    w = pd.Series(pesos)
    if abs(w.sum() - 1) > 1e-6:
        raise ValueError(f"Los pesos suman {w.sum():.2f}; deben sumar 1")
    return (ev[list(w.index)] * w).sum(axis=1)
