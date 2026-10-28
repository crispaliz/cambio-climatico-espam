"""Estaciones del curso: catálogo de `datos/estaciones/` y resolución del archivo de estación.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

En los cuadernos, `ARCHIVO_ESTACION` puede ser:
  - el nombre de un archivo del catálogo (columna `archivo` de `indice_estaciones.csv`),
    por ejemplo "manabi_calceta_espam.csv" o "synop/guayas_milagro_84202.csv";
  - la ruta de un CSV propio en Drive, por ejemplo "/content/drive/MyDrive/CC_Ambiental/estaciones/mi_estacion.csv";
  - una URL a un CSV con el formato del curso.
"""
from __future__ import annotations

import pathlib
import unicodedata

import pandas as pd

CARPETA = pathlib.Path("datos") / "estaciones"
INDICE = "indice_estaciones.csv"


def _norm(texto) -> str:
    t = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return t.strip().lower()


def tabla(repo_dir) -> pd.DataFrame:
    """Índice de las estaciones del curso."""
    return pd.read_csv(pathlib.Path(repo_dir) / CARPETA / INDICE)


def de_provincia(provincia: str, repo_dir) -> pd.DataFrame:
    """Estaciones del curso en una provincia, de la más completa a la menos completa."""
    t = tabla(repo_dir)
    t = t[t["provincia"].map(_norm) == _norm(provincia)]
    return t.sort_values("meses_tmax", ascending=False)


def resolver(archivo: str, repo_dir, provincia: str | None = None):
    """Devuelve (ruta, ficha). `ficha` es la fila del índice si el archivo es del catálogo; si no, None.

    Si no encuentra el archivo, lanza FileNotFoundError con las estaciones del curso de la provincia
    y los CSV que haya en la carpeta de Drive del curso.
    """
    archivo = str(archivo or "").strip()
    if archivo.startswith(("http://", "https://")):
        return archivo, None
    if archivo and pathlib.Path(archivo).exists():
        return pathlib.Path(archivo), None
    t = tabla(repo_dir)
    nombre = archivo.split("/datos/estaciones/")[-1]
    fila = t[(t["archivo"] == nombre) | (t["archivo"].map(lambda a: pathlib.Path(a).name) == pathlib.Path(nombre).name)]
    if archivo and len(fila):
        f = fila.iloc[0]
        return pathlib.Path(repo_dir) / CARPETA / f["archivo"], f
    lineas = [f"No se encontró el archivo de estación «{archivo}».", ""]
    if provincia:
        p = de_provincia(provincia, repo_dir)
        if len(p):
            lineas.append(f"Estaciones del curso en {provincia} (escriba el nombre de la columna «archivo» en ARCHIVO_ESTACION):")
            for _, r in p.iterrows():
                lineas.append(f"  {r['archivo']:55s} {r['estacion']} · Tmáx {r['meses_tmax']} meses · lluvia {r['meses_precip']} meses")
        else:
            lineas.append(f"El curso no tiene estaciones en {provincia}: use la estación que le indique el docente.")
    drive = pathlib.Path("/content/drive/MyDrive")
    propios = sorted(drive.glob("CC_*/**/*.csv"))[:20] if drive.exists() else []
    propios = [p for p in propios if "practica-1" not in p.parts]
    if propios:
        lineas += ["", "CSV encontrados en su Drive (copie la ruta completa):"] + [f"  {p}" for p in propios]
    lineas += ["", "Si usa un CSV propio, escriba la ruta completa, empezando por /content/drive/MyDrive/."]
    raise FileNotFoundError("\n".join(lineas))
