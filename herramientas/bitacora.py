"""Bitácora del evento El Niño 2026–2027: una fila por consulta, en el Drive del estudiante.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

El cuaderno común `CB01_bitacora_el_nino` (semanal, menos de un minuto) y los cuadernos `IA1_03` (Ambiental) y
`RD1_01` (Riesgos) llaman a `registrar` cada vez que se ejecutan:

  - crea `bitacora_el_nino_<zona>.xlsx` en `Mi unidad/CC_<carrera>/bitacora/` la primera vez;
  - agrega una fila con la fecha de la consulta, el mes del índice, el ICEN (calculado por el curso con
    Niño 1+2 de NOAA) con su categoría y el ONI;
  - si ya hay una fila con la fecha de hoy, solo actualiza los índices de esa fila;
  - nunca borra lo que el estudiante escribió en las demás columnas (comunicado, alerta, incidentes,
    observación).

El estudiante completa esas columnas abriendo el .xlsx desde Drive (Hojas de cálculo de Google lo edita
sin convertirlo) o en Excel. Se usa .xlsx y no .csv porque Hojas de cálculo convierte un .csv en otro
archivo al editarlo y los cambios no volverían a la bitácora.
"""
from __future__ import annotations

import datetime
import pathlib

import pandas as pd

COLUMNAS = ["fecha_consulta", "mes_indice", "icen", "icen_categoria", "oni", "comunicado", "alerta_sngr",
            "incidentes_zona", "observacion_propia", "fuente", "url"]
A_COMPLETAR = ["comunicado", "alerta_sngr", "incidentes_zona", "observacion_propia"]
FUENTE = ("NOAA CPC, ERSSTv5: ONI e ICEN calculado por el curso con Niño 1+2 (contrastar con el ICEN oficial del IGP); "
          "completar: comunicado ERFEN/INAMHI, SNGR, ECU 911")
URL = "https://www.cpc.ncep.noaa.gov/data/indices/ · http://met.igp.gob.pe/datos/ICEN.txt"


def _ultimo(serie: pd.Series):
    s = serie.dropna()
    return s.index[-1], round(float(s.iloc[-1]), 2)


def registrar(carpeta, zona_slug: str, icen: pd.Series, oni: pd.Series, categoria, hoy: datetime.date | None = None,
              prellenar: dict | None = None):
    """Agrega (o actualiza) la fila de hoy en la bitácora. Devuelve (ruta, tabla).

    `prellenar`: valores para columnas del estudiante (p. ej. {"incidentes_zona": "..."}) que solo se escriben
    si la celda de hoy está vacía; nunca reemplazan lo que el estudiante ya escribió.
    """
    carpeta = pathlib.Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"bitacora_el_nino_{zona_slug}.xlsx"
    hoy = (hoy or datetime.date.today()).isoformat()
    (m_i, v_i), (m_o, v_o) = _ultimo(icen), _ultimo(oni)
    mes = f"{m_i:%Y-%m}" if f"{m_i:%Y-%m}" == f"{m_o:%Y-%m}" else f"ICEN {m_i:%Y-%m} · ONI {m_o:%Y-%m}"
    nuevos = {"fecha_consulta": hoy, "mes_indice": mes, "icen": v_i, "icen_categoria": categoria(v_i), "oni": v_o}

    if ruta.exists():
        tabla = pd.read_excel(ruta, dtype=object).reindex(columns=COLUMNAS).astype(object)
    else:
        tabla = pd.DataFrame(columns=COLUMNAS, dtype=object)
    tabla["fecha_consulta"] = tabla["fecha_consulta"].map(lambda x: str(x)[:10] if pd.notna(x) else "").astype(object)
    hay = tabla["fecha_consulta"] == hoy
    if hay.any():
        i = tabla.index[hay][-1]
        for k, v in nuevos.items():
            tabla.loc[i, k] = v
    else:
        fila = {c: "" for c in COLUMNAS} | nuevos | {"fuente": FUENTE, "url": URL}
        tabla = pd.concat([tabla, pd.DataFrame([fila])], ignore_index=True)
    tabla = tabla.fillna("")
    i = tabla.index[tabla["fecha_consulta"] == hoy][-1]
    for k, v in (prellenar or {}).items():
        if k in COLUMNAS and v and not str(tabla.loc[i, k]).strip():
            tabla.loc[i, k] = v
    for c in ("icen", "oni"):
        tabla[c] = pd.to_numeric(tabla[c], errors="coerce")

    with pd.ExcelWriter(ruta, engine="openpyxl") as w:
        tabla.to_excel(w, index=False, sheet_name="bitacora")
        hoja = w.sheets["bitacora"]
        anchos = {"A": 14, "B": 22, "C": 8, "D": 20, "E": 8, "F": 34, "G": 30, "H": 44, "I": 40, "J": 50, "K": 40}
        for col, a in anchos.items():
            hoja.column_dimensions[col].width = a
        hoja.freeze_panes = "A2"
    return ruta, tabla


def ultima_consulta(carpeta, zona_slug: str, antes_de: datetime.date | None = None):
    """Fecha de la última consulta registrada antes de hoy (o None si la bitácora no existe o está vacía)."""
    ruta = pathlib.Path(carpeta) / f"bitacora_el_nino_{zona_slug}.xlsx"
    if not ruta.exists():
        return None
    f = pd.to_datetime(pd.read_excel(ruta, dtype=object)["fecha_consulta"].astype(str).str.slice(0, 10), errors="coerce").dropna()
    hoy = pd.Timestamp(antes_de or datetime.date.today())
    f = f[f < hoy]
    return None if f.empty else f.max().date()


def mostrar(ruta, tabla, n: int = 5):
    """Resumen para el cuaderno: últimas filas y columnas que faltan por completar."""
    print(f"Bitácora actualizada: {ruta}")
    print(tabla.tail(n)[["fecha_consulta", "mes_indice", "icen", "icen_categoria", "oni"]].to_string(index=False))
    falta = tabla.iloc[-1][A_COMPLETAR]
    vacias = [c for c, v in falta.items() if not str(v).strip()]
    if vacias:
        print(f"\nComplete en la fila de hoy: {', '.join(vacias)}.")
        print("Abra el archivo desde Drive (doble clic: se edita en Hojas de cálculo sin convertirlo) o en Excel.")
    print("Una fila por semana como mínimo. Todo lo de la bitácora es preliminar y va en el anexo A del capítulo 1.")


def resumen_ecu911(inc_zona: pd.DataFrame, desde=None, max_cantones: int = 3) -> str:
    """Texto breve de los incidentes climáticos del ECU 911 en la zona desde `desde` (exclusive).

    Ejemplo: «ECU 911, 27/10–30/10: inundación 5 (Portoviejo 3, Chone 2); deslizamiento 1 (Pichincha 1)».
    Son días con atención coordinada, no desastres verificados.
    """
    if inc_zona is None or inc_zona.empty:
        return ""
    d = inc_zona.copy()
    d["fecha"] = pd.to_datetime(d["fecha"])
    if desde is not None:
        d = d[d["fecha"] > pd.Timestamp(desde)]
    if d.empty:
        return ""
    partes = []
    for tipo, g in d.groupby("tipo"):
        c = g["canton"].str.title().value_counts().head(max_cantones)
        partes.append(f"{tipo} {len(g)} (" + ", ".join(f"{k} {v}" for k, v in c.items()) + ")")
    return f"ECU 911, {d['fecha'].min():%d/%m}–{d['fecha'].max():%d/%m/%Y}: " + "; ".join(partes)
