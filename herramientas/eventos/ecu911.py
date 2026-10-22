"""Incidentes de gestión de riesgos del ECU 911 (datos abiertos del Ecuador).

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Fuente: SIS ECU 911, «Base de Emergencias», portal de Datos Abiertos del Ecuador:
    https://www.datosabiertos.gob.ec/dataset/base-de-emergencias
Un archivo por mes desde julio de 2021, con una fila por incidente coordinado: fecha, provincia,
cantón, código y nombre de la parroquia, servicio y subtipo. Aquí se conservan solo los del servicio
«Gestión de Riesgos» y, de ellos, los de origen hidrometeorológico o climático (inundación,
deslizamiento, vendaval, incendio forestal, etc.).

Qué es y qué no es:
  - Es un registro diario y por parroquia de CUÁNDO y DÓNDE se pidió o coordinó atención: sirve para
    fechar eventos y contrastarlos con la lluvia.
  - No trae fallecidos, afectados ni viviendas: esos datos vienen de los informes de situación de la
    Secretaría Nacional de Gestión de Riesgos (SitRep) o de los GAD.
  - Un mismo evento genera varios incidentes; por eso se agrupan por día, cantón y tipo.

Uso en un cuaderno:
    from herramientas.eventos import ecu911
    inc = ecu911.incidentes(carpeta=BASE / "CC_datos" / "_ecu911")   # nacional, con caché por mes
    zona = ecu911.de_zona(inc, Z["codigo"])                          # su provincia o cantón (código DPA)
    reg = ecu911.a_registro(zona)                                    # formato de registro_eventos.csv
"""
from __future__ import annotations

import io
import json
import pathlib
import re
import urllib.request

import pandas as pd

DATASET = "https://www.datosabiertos.gob.ec/dataset/base-de-emergencias"
API = "https://www.datosabiertos.gob.ec/api/3/action/package_show?id=base-de-emergencias"
FUENTE = "SIS ECU 911, Base de Emergencias (Datos Abiertos Ecuador)"
COLUMNAS = ["fecha", "provincia", "canton", "cod_parroquia", "parroquia", "servicio", "subtipo"]

# Subtipo del ECU 911 (minúsculas, sin tildes) -> tipo del registro de eventos del curso
TIPOS = [
    (r"inund|desbord|anegam", "inundación"),
    (r"desliz|derrumbe|movimiento en masa|aluvi|flujo de lodo", "deslizamiento"),
    (r"vendaval|viento", "vendaval"),
    (r"incendio forestal|incendio de cobertura|quema", "incendio forestal"),
    (r"oleaje|aguaje|marejada", "oleaje"),
    (r"sequ|deficit hidrico", "sequía"),
    (r"tormenta|granizo|lluvia|hidrometeor", "lluvia intensa o tormenta"),
    (r"hundimiento|subsidencia|socavon", "hundimiento"),
    (r"amenazas? natural", "amenaza natural sin detalle"),
]
# «Amenazas naturales» es un subtipo genérico del ECU 911 que puede incluir sismos u otros eventos no
# climáticos: se conserva porque en la época lluviosa suele ser la mayoría, pero hay que verificarlo.


def _sin_tildes(t: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", str(t)) if unicodedata.category(c) != "Mn").lower().strip()


def tipo_curso(subtipo: str) -> str | None:
    """Tipo del registro del curso para un subtipo del ECU 911, o None si no es de origen climático."""
    s = _sin_tildes(subtipo)
    for patron, tipo in TIPOS:
        if re.search(patron, s):
            return tipo
    return None


def _abrir(url: str, timeout: int = 300) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "cambio-climatico-espam (docencia ESPAM MFL)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def recursos() -> pd.DataFrame:
    """Archivos mensuales publicados: mes (AAAAMM) y URL, según la API del portal."""
    datos = json.loads(_abrir(API, 60).decode("utf-8"))
    filas = []
    for r in datos["result"]["resources"]:
        m = re.search(r"(20\d{2})(0[1-9]|1[0-2])", r.get("name", ""))
        if m and re.search(r"emergencias", r.get("name", ""), re.I):
            filas.append({"mes": m.group(0), "url": r["url"]})
    return pd.DataFrame(filas).drop_duplicates("mes").sort_values("mes").reset_index(drop=True)


def leer_mes(contenido: bytes) -> pd.DataFrame:
    """Lee un archivo mensual (CSV con ';' o XLSX) y deja las 7 columnas normalizadas, como texto."""
    if contenido[:2] == b"PK":
        df = pd.read_excel(io.BytesIO(contenido), dtype=str)
    else:
        for enc in ("utf-8-sig", "latin-1"):
            try:
                df = pd.read_csv(io.BytesIO(contenido), sep=";", dtype=str, encoding=enc, on_bad_lines="skip")
                break
            except UnicodeDecodeError:
                continue
    df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed")].iloc[:, :7]
    df.columns = COLUMNAS
    return df


def filtrar(df: pd.DataFrame) -> pd.DataFrame:
    """Solo «Gestión de Riesgos» de origen climático, con fecha, código DPA de 6 dígitos y tipo del curso."""
    df = df[df["servicio"].map(_sin_tildes).str.contains("riesgo", na=False)].copy()
    df["tipo"] = df["subtipo"].map(tipo_curso)
    df = df[df["tipo"].notna()]
    df["fecha"] = pd.to_datetime(df["fecha"].str.strip().str[:10], dayfirst=True, errors="coerce")
    df["cod_parroquia"] = df["cod_parroquia"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(6)
    for c in ("provincia", "canton", "parroquia", "subtipo"):
        df[c] = df[c].astype(str).str.strip()
    return df.dropna(subset=["fecha"])


def incidentes(carpeta=None, desde: str = "2021-07", hasta: str | None = None, nacional=None,
               verbose: bool = True) -> pd.DataFrame:
    """Incidentes climáticos de gestión de riesgos de todo el país, de `desde` a `hasta` (AAAA-MM).

    Orden de búsqueda:
      1. `nacional`: un CSV ya compilado (por ejemplo, el que publica el docente en el repositorio).
      2. La caché por mes en `carpeta` (cada mes se descarga una sola vez).
      3. El portal de Datos Abiertos (unos 30–40 MB por mes; solo se guardan las filas útiles).
    """
    d0 = pd.Period(desde, "M")
    d1 = pd.Period(hasta, "M") if hasta else pd.Period(pd.Timestamp.today(), "M")
    if nacional and pathlib.Path(nacional).exists():
        df = pd.read_csv(nacional, dtype=str, parse_dates=["fecha"])
        if verbose: print(f"ECU 911: compilado {pathlib.Path(nacional).name}, {df['fecha'].min():%Y-%m} a {df['fecha'].max():%Y-%m}")
        return df[(df["fecha"].dt.to_period("M") >= d0) & (df["fecha"].dt.to_period("M") <= d1)]
    carpeta = pathlib.Path(carpeta) if carpeta else None
    if carpeta: carpeta.mkdir(parents=True, exist_ok=True)
    rec = recursos()
    rec = rec[(rec["mes"] >= d0.strftime("%Y%m")) & (rec["mes"] <= d1.strftime("%Y%m"))]
    partes, fallidos = [], []
    for _, r in rec.iterrows():
        cache = carpeta / f"ecu911_riesgos_{r['mes']}.csv" if carpeta else None
        if cache and cache.exists():
            partes.append(pd.read_csv(cache, dtype=str, parse_dates=["fecha"])); continue
        try:
            df = filtrar(leer_mes(_abrir(r["url"])))
        except Exception as err:
            fallidos.append(r["mes"])
            if verbose: print(f"  {r['mes']}: no se pudo leer ({err}); vuelva a ejecutar más tarde")
            continue
        if cache: df.to_csv(cache, index=False, encoding="utf-8")
        partes.append(df)
        if verbose: print(f"  {r['mes']}: {len(df)} incidentes climáticos de gestión de riesgos")
    if not partes:
        return pd.DataFrame(columns=COLUMNAS + ["tipo"])
    out = pd.concat(partes, ignore_index=True)
    out["fecha"] = pd.to_datetime(out["fecha"])
    out.attrs["meses_fallidos"] = fallidos
    return out.sort_values("fecha").reset_index(drop=True)


def de_zona(inc: pd.DataFrame, codigo_dpa: str) -> pd.DataFrame:
    """Incidentes de una provincia (código DPA de 2 dígitos) o de un cantón (4 dígitos)."""
    return inc[inc["cod_parroquia"].astype(str).str.zfill(6).str.startswith(str(codigo_dpa))].copy()


def a_registro(inc: pd.DataFrame, por: str = "canton") -> pd.DataFrame:
    """Agrupa los incidentes por día, cantón (o parroquia) y tipo, con las columnas de registro_eventos.csv.

    Cada fila es un «día con incidentes» del ECU 911, no un evento con daños verificados: el equipo
    decide cuáles son el mismo evento, completa daños desde los SitRep y conserva la fuente.
    """
    campos = ["fecha_inicio", "fecha_fin", "tipo", "canton", "parroquia", "descripcion", "fallecidos",
              "afectados", "viviendas_afectadas", "fuente", "url"]
    if inc.empty:
        return pd.DataFrame(columns=campos)
    claves = ["fecha", "canton", "tipo"] + (["parroquia"] if por == "parroquia" else [])
    g = inc.groupby(claves).agg(n=("subtipo", "size"), subtipos=("subtipo", lambda s: ", ".join(sorted(set(s)))),
                                parroquias=("parroquia", lambda s: "; ".join(sorted(set(s))[:5]) + (" …" if s.nunique() > 5 else "")))
    g = g.reset_index()
    return pd.DataFrame({
        "fecha_inicio": g["fecha"].dt.date, "fecha_fin": g["fecha"].dt.date, "tipo": g["tipo"],
        "canton": g["canton"].str.title(),
        "parroquia": (g["parroquia"] if por == "parroquia" else g["parroquias"]).str.title(),
        "descripcion": [f"{n} incidente(s) ECU 911: {s}" for n, s in zip(g["n"], g["subtipos"])],
        "fallecidos": pd.NA, "afectados": pd.NA, "viviendas_afectadas": pd.NA,
        "fuente": FUENTE, "url": DATASET})[campos]
