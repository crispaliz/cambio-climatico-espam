"""Bitácora del evento El Niño 2026–2027: una fila por consulta, en el Drive del estudiante.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Los cuadernos `IA1_03` (Ambiental) y `RD1_01` (Riesgos) llaman a `registrar` cada vez que se ejecutan:

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


def registrar(carpeta, zona_slug: str, icen: pd.Series, oni: pd.Series, categoria, hoy: datetime.date | None = None):
    """Agrega (o actualiza) la fila de hoy en la bitácora. Devuelve (ruta, tabla)."""
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
