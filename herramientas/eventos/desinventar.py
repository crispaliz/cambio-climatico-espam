"""DesInventar Ecuador (UNDRR): registro de desastres de origen hidrometeorológico, 1970–2007.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Fuente: DesInventar Sendai, base de datos de Ecuador (https://db.desinventar.org, exportación XML
DI_export_ecu.zip). Los derechos de la información son de las instituciones que la compilaron; se cita en
cada fila. El curso usa una versión procesada, `datos/eventos/desinventar_ecu_hidromet.csv.gz`:

  - solo eventos de origen hidrometeorológico (tabla TIPOS);
  - fecha exacta (las fichas sin día quedan fuera: no se pueden cruzar con lluvia diaria);
  - provincia y cantón con su código DPA (level0, level1 de DesInventar);
  - cifras de daños: 0 de DesInventar = no reportado → celda vacía, como pide el registro del curso.

(Docente) Para regenerarla:  python -m herramientas.eventos.desinventar DI_export_ecu.xml datos/eventos/desinventar_ecu_hidromet.csv.gz
"""
from __future__ import annotations

import pathlib
import re
import sys

import numpy as np
import pandas as pd

URL = "https://db.desinventar.org/DesInventar/download_base.jsp?countrycode=ecu"
CITA = "DesInventar Sendai (UNDRR), base de datos de Ecuador"

# evento de DesInventar -> tipo del registro de eventos del curso
TIPOS = {
    "Inundación": "inundación",
    "Deslizamiento": "deslizamiento",
    "Aluvión": "aluvión",
    "Avenida torrencial": "aluvión",
    "Lluvias": "lluvia intensa",
    "Sequía": "sequía",
    "Incendio forestal": "incendio forestal",
    "Vendaval": "vendaval",
    "Tempestad": "vendaval",
    "Marejada": "oleaje",
    "Granizada": "otro",
    "Helada": "otro",
    "Ola de calor": "otro",
    "Tormenta eléctrica": "otro",
}
CAMPOS = ["fecha_inicio", "fecha_fin", "tipo", "canton", "parroquia", "descripcion", "fallecidos", "afectados",
          "viviendas_afectadas", "fuente", "url"]


def preparar(xml, salida) -> pd.DataFrame:
    """(Docente) Lee la exportación XML de DesInventar y guarda los eventos hidrometeorológicos con fecha exacta."""
    t = pathlib.Path(xml).read_text(encoding="utf-8")
    bloque = t[t.index("<fichas>"):t.index("</fichas>")]
    filas = [dict(re.findall(r"<(\w+)>(.*?)</\1>", r, re.S)) for r in re.findall(r"<TR>(.*?)</TR>", bloque, re.S)]
    d = pd.DataFrame(filas)
    d = d[d["evento"].isin(TIPOS)].copy()
    for c in ("fechano", "fechames", "fechadia", "muertos", "afectados", "damnificados", "vivdest", "vivafec"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[(d.fechadia > 0) & (d.fechames > 0)]
    fecha = pd.to_datetime(dict(year=d.fechano, month=d.fechames, day=d.fechadia), errors="coerce")
    d = d[fecha.notna()].assign(fecha=fecha[fecha.notna()])
    vacio = lambda s: s.where(s > 0)      # 0 en DesInventar = no reportado
    texto = (d["lugar"].fillna("").str.strip() + " · " + d["descausa"].fillna("").str.strip()).str.strip(" ·")
    out = pd.DataFrame({
        "fecha_inicio": d.fecha.dt.strftime("%Y-%m-%d"),
        "fecha_fin": d.fecha.dt.strftime("%Y-%m-%d"),
        "tipo": d.evento.map(TIPOS),
        "evento_desinventar": d.evento,
        "cod_provincia": d.level0.str.zfill(2),
        "cod_canton": d.level1.where(d.level1.str.len() == 4, ""),
        "provincia": d.name0.str.title(),
        "canton": d.name1.str.title(),
        "parroquia": d.name2.str.title().replace("", np.nan),
        "descripcion": texto.str.slice(0, 300),
        "fallecidos": vacio(d.muertos),
        "afectados": vacio(d.afectados.fillna(0) + d.damnificados.fillna(0)),
        "viviendas_afectadas": vacio(d.vivafec.fillna(0) + d.vivdest.fillna(0)),
        "fuente": CITA + np.where(d.fuentes.fillna("").str.strip() != "", " · " + d.fuentes.str.strip(), ""),
        "url": URL,
        "serial": d.serial,
    }).sort_values("fecha_inicio")
    out.to_csv(salida, index=False, encoding="utf-8")
    return out


def de_zona(ruta, codigo_dpa: str) -> pd.DataFrame:
    """Eventos de la zona en el formato del registro del curso. `codigo_dpa`: 2 dígitos (provincia) o 4 (cantón)."""
    d = pd.read_csv(ruta, dtype={"cod_provincia": str, "cod_canton": str})
    c = str(codigo_dpa)
    d = d[d.cod_provincia == c] if len(c) <= 2 else d[d.cod_canton == c.zfill(4)]
    return d[CAMPOS + ["evento_desinventar"]].reset_index(drop=True)


if __name__ == "__main__":
    r = preparar(sys.argv[1], sys.argv[2])
    print(f"{len(r)} eventos hidrometeorológicos con fecha exacta, {r.fecha_inicio.min()} a {r.fecha_inicio.max()}")
    print(r.tipo.value_counts().to_string())
