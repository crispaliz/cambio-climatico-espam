"""Inventario simplificado de gases de efecto invernadero (GEI) de una provincia.

Método: Directrices del IPCC de 2006 (Nivel 1, factores por defecto), con potenciales de
calentamiento global a 100 años del AR5 (los mismos que usa el Inventario Nacional del
Ecuador en la Segunda NDC). Cada fila del resultado guarda la categoría IPCC, el gas, el
dato de actividad, el factor usado, su fuente y una incertidumbre por defecto.

Uso:
    from herramientas import inventario as inv
    filas = []
    filas += inv.energia(gasolina_gal=..., diesel_gal=..., glp_kg=...)
    filas += inv.agricultura(otros_vacunos=..., porcinos=..., arroz_ha=...)
    filas += inv.residuos(poblacion=...)
    tabla = inv.tabla(filas)
    inv.resumen(tabla); inv.incertidumbre(tabla)
"""
from __future__ import annotations

import math
import pathlib

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[2]

# Potenciales de calentamiento global a 100 años, IPCC AR5 (GTI, cap. 8, tabla 8.7).
PCG = {"CO2": 1.0, "CH4": 28.0, "N2O": 265.0}
PCG_FUENTE = "IPCC AR5 (2013), PCG a 100 años"

GALON_L = 3.785411784

# ---------------------------------------------------------------- 1. Energía
# Combustibles: densidad (kg/L), poder calorífico neto (TJ/Gg) y factores (kg/TJ).
# IPCC 2006, vol. 2: cap. 1, cuadros 1.2 y 1.4 (PCN y CO2); cap. 3, cuadro 3.2.2 (CH4 y N2O
# en transporte por carretera, sin control); cap. 2, cuadro 2.5 (GLP residencial).
COMBUSTIBLES = {
    "gasolina": {"densidad": 0.74, "pcn": 44.3, "CO2": 69300.0, "CH4": 33.0, "N2O": 3.2,
                 "cat": "1A3b Transporte por carretera", "fuente": "IPCC 2006 v2 c1 t1.2/1.4; c3 t3.2.2"},
    "diesel":   {"densidad": 0.84, "pcn": 43.0, "CO2": 74100.0, "CH4": 3.9, "N2O": 3.9,
                 "cat": "1A3b Transporte por carretera", "fuente": "IPCC 2006 v2 c1 t1.2/1.4; c3 t3.2.2"},
    "glp":      {"densidad": None, "pcn": 47.3, "CO2": 63100.0, "CH4": 5.0, "N2O": 0.1,
                 "cat": "1A4b Residencial", "fuente": "IPCC 2006 v2 c1 t1.2/1.4; c2 t2.5"},
}
# Factor del SNI continental para inventarios y huella de carbono (alcance 2), estadística 2024.
FE_RED = 0.1616  # t CO2-eq/MWh
FE_RED_FUENTE = "CENACE/MAE, Factor de emisión de CO2 del SNI, Informe 2024"

# ---------------------------------------------------------------- 3. Agricultura
# Fermentación entérica, Nivel 1, América Latina (kg CH4/cabeza/año). IPCC 2006 v4 c10, cuadros 10.10 y 10.11.
ENTERICA = {"vacas_leche": 72.0, "otros_vacunos": 56.0, "porcinos": 1.0, "ovinos": 5.0,
            "caprinos": 5.0, "caballos": 18.0, "mulas_asnos": 10.0}
# CH4 de gestión del estiércol, Nivel 1, América Latina, clima cálido (kg CH4/cabeza/año).
# IPCC 2006 v4 c10, cuadros 10.14, 10.15 y 10.16.
ESTIERCOL = {"vacas_leche": 1.0, "otros_vacunos": 1.0, "porcinos": 1.0, "ovinos": 0.20,
             "caprinos": 0.22, "caballos": 2.19, "mulas_asnos": 1.20}
NOMBRE_ESPECIE = {"vacas_leche": "vacas de ordeño", "otros_vacunos": "otros vacunos", "porcinos": "porcinos",
                  "ovinos": "ovinos", "caprinos": "caprinos", "caballos": "caballos", "mulas_asnos": "mulas y asnos"}
# Arroz: factor de referencia 1,30 kg CH4/ha/día (IPCC 2006 v4 c5, cuadro 5.11) y factores de
# escala por régimen de agua (cuadro 5.12).
ARROZ_EF = 1.30
ARROZ_REGIMEN = {"inundación continua": 1.0, "inundación intermitente (un drenaje)": 0.60,
                 "inundación intermitente (varios drenajes)": 0.52, "secano (lluvia)": 0.28}
# N2O de suelos por fertilizante sintético: EF1 = 0,01; volatilización 10 % con EF4 = 0,01;
# lixiviación 30 % con EF5 = 0,0075 (IPCC 2006 v4 c11, cuadros 11.1 y 11.3).
EF1, FRAC_GASF, EF4, FRAC_LEACH, EF5 = 0.01, 0.10, 0.01, 0.30, 0.0075

# ---------------------------------------------------------------- 4. Residuos
# Residuos sólidos: método por defecto (balance de masa) de las Directrices de 1996, explicado
# en IPCC 2006 v5 c3 como alternativa simple; da la emisión potencial del residuo dispuesto en el año.
SITIO_MCF = {"relleno sanitario gestionado": 1.0, "botadero profundo (> 5 m)": 0.8,
             "botadero poco profundo (< 5 m)": 0.4, "sitio no clasificado": 0.6}
DOC_DEF, DOCF, F_CH4 = 0.14, 0.5, 0.5
# Aguas residuales domésticas: DBO por persona en América Latina 40 g/día y Bo = 0,6 kg CH4/kg DBO
# (IPCC 2006 v5 c6, cuadros 6.2 y 6.4); MCF por vía (cuadro 6.3).
DBO_G_DIA, BO = 40.0, 0.6
AGUAS_MCF = {"alcantarillado con planta aerobia": 0.0, "alcantarillado con laguna anaerobia": 0.8,
             "alcantarillado sin tratamiento (a río o mar)": 0.1, "pozo séptico": 0.5, "letrina": 0.1,
             "sin servicio (a campo abierto)": 0.1}
# N2O del efluente: FNPR 0,16; F_NON-CON 1,1; F_IND-COM 1,25; EF 0,005 kg N2O-N/kg N (cuadro 6.11).
FNPR, FNONCON, FINDCOM, EF_EFLUENTE = 0.16, 1.1, 1.25, 0.005

# Incertidumbre combinada por defecto (± %, dato de actividad y factor), orientativa a partir de
# los rangos de las Directrices de 2006. Sirve para el enfoque 1 (propagación del error).
INCERT = {"comb_CO2": 7, "comb_noCO2": 150, "red": 10, "enterica": 45, "estiercol": 55, "arroz": 60,
          "suelos": 150, "deforestacion": 50, "residuos": 60, "aguas": 70}


def _fila(sector, cat, gas, act, unidad, fe, fe_unidad, t_gas, fuente, inc, nota=""):
    return {"sector": sector, "categoria": cat, "gas": gas, "dato_actividad": act, "unidad_actividad": unidad,
            "factor": fe, "unidad_factor": fe_unidad, "emision_t_gas": t_gas,
            "emision_tCO2e": t_gas * PCG.get(gas, 1.0), "fuente_factor": fuente, "incertidumbre_pct": inc,
            "nota": nota}


def energia(gasolina_gal=0.0, diesel_gal=0.0, glp_kg=0.0, electricidad_mwh=0.0):
    """Combustión de combustibles y electricidad consumida.

    gasolina_gal y diesel_gal: ventas anuales en la provincia (galones), asignadas al transporte.
    glp_kg: GLP de uso doméstico (kg). electricidad_mwh: consumo facturado en la provincia (MWh),
    que se reporta aparte como alcance 2 (no se suma: las centrales ya están en el inventario nacional).
    """
    filas = []
    for nombre, cantidad in (("gasolina", gasolina_gal), ("diesel", diesel_gal), ("glp", glp_kg)):
        if not cantidad:
            continue
        c = COMBUSTIBLES[nombre]
        masa_t = cantidad if nombre == "glp" else cantidad * GALON_L * c["densidad"] / 1000
        masa_t = masa_t / 1000 if nombre == "glp" else masa_t
        tj = masa_t / 1000 * c["pcn"]  # Gg × TJ/Gg
        unidad = "kg" if nombre == "glp" else "galones"
        for gas in ("CO2", "CH4", "N2O"):
            t = tj * c[gas] / 1000
            filas.append(_fila("1. Energía", c["cat"], gas, cantidad, unidad, c[gas], "kg/TJ", t, c["fuente"],
                               INCERT["comb_CO2" if gas == "CO2" else "comb_noCO2"],
                               f"{nombre}: {tj:,.0f} TJ"))
    if electricidad_mwh:
        filas.append(_fila("Memo: electricidad (alcance 2)", "Consumo de electricidad del SNI", "CO2",
                           electricidad_mwh, "MWh", FE_RED, "t CO2-eq/MWh", electricidad_mwh * FE_RED,
                           FE_RED_FUENTE, INCERT["red"], "No se suma al total provincial"))
    return filas


def agricultura(arroz_ha=0.0, arroz_dias=120, arroz_regimen="inundación continua", n_sintetico_t=0.0, **animales):
    """Ganado (cabezas), arroz (ha cosechadas al año) y nitrógeno sintético aplicado (t de N)."""
    filas = []
    for esp, cab in animales.items():
        if esp not in ENTERICA:
            raise ValueError(f"Especie desconocida: {esp}. Use {sorted(ENTERICA)}")
        if not cab:
            continue
        filas.append(_fila("3. Agricultura", "3A1 Fermentación entérica", "CH4", cab, f"cabezas ({NOMBRE_ESPECIE[esp]})",
                           ENTERICA[esp], "kg CH4/cabeza/año", cab * ENTERICA[esp] / 1000,
                           "IPCC 2006 v4 c10 t10.10/10.11", INCERT["enterica"]))
        filas.append(_fila("3. Agricultura", "3A2 Gestión del estiércol", "CH4", cab, f"cabezas ({NOMBRE_ESPECIE[esp]})",
                           ESTIERCOL[esp], "kg CH4/cabeza/año", cab * ESTIERCOL[esp] / 1000,
                           "IPCC 2006 v4 c10 t10.14-10.16 (cálido)", INCERT["estiercol"]))
    if arroz_ha:
        sf = ARROZ_REGIMEN[arroz_regimen]
        ef = ARROZ_EF * sf * arroz_dias
        filas.append(_fila("3. Agricultura", "3C7 Cultivo de arroz", "CH4", arroz_ha, "ha cosechadas", ef,
                           "kg CH4/ha", arroz_ha * ef / 1000, "IPCC 2006 v4 c5 t5.11/5.12", INCERT["arroz"],
                           f"{arroz_regimen}, {arroz_dias} días"))
    if n_sintetico_t:
        directo = n_sintetico_t * EF1 * 44 / 28
        indirecto = n_sintetico_t * (FRAC_GASF * EF4 + FRAC_LEACH * EF5) * 44 / 28
        filas.append(_fila("3. Agricultura", "3C4 N2O directo de suelos gestionados", "N2O", n_sintetico_t, "t N",
                           EF1, "kg N2O-N/kg N", directo, "IPCC 2006 v4 c11 t11.1", INCERT["suelos"]))
        filas.append(_fila("3. Agricultura", "3C5 N2O indirecto de suelos gestionados", "N2O", n_sintetico_t, "t N",
                           FRAC_GASF * EF4 + FRAC_LEACH * EF5, "kg N2O-N/kg N", indirecto,
                           "IPCC 2006 v4 c11 t11.3", INCERT["suelos"]))
    return filas


def uscuss(deforestacion_ha=0.0, carbono_tC_ha=0.0):
    """Pérdida de bosque: área deforestada en el año (ha) por el carbono del estrato (t C/ha)."""
    if not deforestacion_ha or not carbono_tC_ha:
        return []
    t = deforestacion_ha * carbono_tC_ha * 44 / 12
    return [_fila("4. USCUSS", "3B1b Tierras forestales convertidas", "CO2", deforestacion_ha, "ha/año",
                  carbono_tC_ha, "t C/ha", t, "Carbono del estrato según el NREF del Ecuador (lo cita el estudiante)",
                  INCERT["deforestacion"], "Emisión bruta; no descuenta regeneración")]


def residuos(poblacion, gen_kg_hab_dia=0.0, frac_dispuesta=0.9, sitio="sitio no clasificado", doc=DOC_DEF,
             aguas=None, proteina_kg_hab_anio=25.0):
    """Residuos sólidos dispuestos y aguas residuales domésticas.

    aguas: dict {vía: fracción de la población} con las claves de AGUAS_MCF; las fracciones deben sumar 1.
    """
    filas = []
    if gen_kg_hab_dia:
        msw_t = poblacion * gen_kg_hab_dia * 365 / 1000 * frac_dispuesta
        mcf = SITIO_MCF[sitio]
        ch4 = msw_t * mcf * doc * DOCF * F_CH4 * 16 / 12
        filas.append(_fila("5. Residuos", "4A Eliminación de residuos sólidos", "CH4", msw_t, "t de residuo dispuesto",
                           mcf * doc * DOCF * F_CH4 * 16 / 12 * 1000, "kg CH4/t", ch4,
                           "IPCC 1996 por defecto (IPCC 2006 v5 c3)", INCERT["residuos"], f"{sitio}, DOC {doc}"))
    if aguas:
        tot = sum(aguas.values())
        if abs(tot - 1) > 0.01:
            raise ValueError(f"Las fracciones de aguas residuales suman {tot:.2f}; deben sumar 1")
        tow = poblacion * DBO_G_DIA / 1000 * 365 / 1000  # t DBO/año
        mcf = sum(AGUAS_MCF[k] * f for k, f in aguas.items())
        ch4 = tow * BO * mcf
        filas.append(_fila("5. Residuos", "4D1 Aguas residuales domésticas", "CH4", tow, "t DBO/año", BO * mcf,
                           "t CH4/t DBO", ch4, "IPCC 2006 v5 c6 t6.2-6.4", INCERT["aguas"], f"MCF ponderado {mcf:.2f}"))
        n_t = poblacion * proteina_kg_hab_anio * FNPR * FNONCON * FINDCOM / 1000
        filas.append(_fila("5. Residuos", "4D1 Aguas residuales domésticas", "N2O", n_t, "t N en el efluente",
                           EF_EFLUENTE, "kg N2O-N/kg N", n_t * EF_EFLUENTE * 44 / 28, "IPCC 2006 v5 c6 t6.11",
                           INCERT["aguas"], f"proteína {proteina_kg_hab_anio} kg/hab/año"))
    return filas


def tabla(filas) -> pd.DataFrame:
    df = pd.DataFrame(filas)
    if df.empty:
        raise ValueError("No hay datos de actividad: complete al menos un sector")
    return df


def total(df: pd.DataFrame) -> float:
    """Total provincial en t CO2-eq (sin las partidas informativas de alcance 2)."""
    return float(df.loc[~df.sector.str.startswith("Memo"), "emision_tCO2e"].sum())


def resumen(df: pd.DataFrame, por="sector") -> pd.DataFrame:
    d = df[~df.sector.str.startswith("Memo")]
    r = d.groupby(por, sort=True)["emision_tCO2e"].sum().to_frame("t CO2-eq")
    r["%"] = 100 * r["t CO2-eq"] / r["t CO2-eq"].sum()
    return r.sort_values("t CO2-eq", ascending=False)


def incertidumbre(df: pd.DataFrame) -> float:
    """Enfoque 1 del IPCC: propagación del error para una suma, en ± % del total."""
    d = df[~df.sector.str.startswith("Memo")]
    tot = d.emision_tCO2e.sum()
    return math.sqrt(((d.incertidumbre_pct * d.emision_tCO2e) ** 2).sum()) / tot if tot else float("nan")


def categorias_principales(df: pd.DataFrame, umbral=95.0) -> pd.DataFrame:
    """Análisis de nivel: categorías que juntas suman el umbral (%) del total, de mayor a menor."""
    d = df[~df.sector.str.startswith("Memo")].groupby(["categoria", "gas"])["emision_tCO2e"].sum()
    d = d.sort_values(ascending=False).to_frame("t CO2-eq")
    d["%"] = 100 * d["t CO2-eq"] / d["t CO2-eq"].sum()
    d["% acumulado"] = d["%"].cumsum()
    d["principal"] = (d["% acumulado"] - d["%"]) < umbral
    return d


def poblacion(provincia: str) -> int:
    p = pd.read_csv(RAIZ / "datos" / "inventario" / "poblacion_censo2022.csv").set_index("provincia")
    return int(p.loc[provincia, "poblacion_2022"])


# Inventario nacional de referencia: año 2022, Segunda NDC del Ecuador (2025), figura 2.
NACIONAL_2022 = {"1. Energía": 41674.68, "2. PIUP": 4245.78, "3. Agricultura": 11728.67,
                 "4. USCUSS": 25823.20, "5. Residuos": 4790.54}  # kt CO2-eq
NACIONAL_FUENTE = "MAATE (2025), Segunda NDC del Ecuador; INGEI 2022 (Quinta Comunicación Nacional y BTR1)"
POBLACION_NACIONAL = 16938986
