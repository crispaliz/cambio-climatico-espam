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
RAMA = "https://raw.githubusercontent.com/crispaliz/cambio-climatico-espam/estaciones/"


def _local(archivo: str, repo_dir) -> pathlib.Path:
    """Ruta local de un archivo del catálogo. Las estaciones del INAMHI (inamhi/<provincia>/<código>.csv)
    no están en la rama main: se descarga una vez el ZIP de la provincia desde la rama `estaciones`."""
    import urllib.request
    import zipfile

    destino = pathlib.Path(repo_dir) / CARPETA / archivo
    if destino.exists() or not archivo.startswith("inamhi/"):
        return destino
    _, prov, nombre = archivo.split("/")
    zip_local = pathlib.Path(repo_dir) / CARPETA / "_cache" / f"inamhi_precip_{prov}.zip"
    if not zip_local.exists():
        zip_local.parent.mkdir(parents=True, exist_ok=True)
        print(f"Descargando la lluvia del INAMHI de {prov} (una sola vez)…")
        urllib.request.urlretrieve(RAMA + zip_local.name, zip_local)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_local) as z:
        destino.write_bytes(z.read(nombre))
    return destino


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


NINGUNA = ("ninguna", "ninguno", "no", "sin estacion", "sin estación")


def candidatas(zona: dict, repo_dir, recuadro=None) -> pd.DataFrame:
    """Estaciones del curso utilizables para la zona elegida, de la mejor a la peor.

    Para una provincia: las de la provincia. Para un cantón: las que caen dentro del recuadro
    descargado (`recuadro` = [N, O, S, E]); primero las que están dentro del cantón.
    Orden: primero las que están dentro de la zona; entre ellas, primero las que tienen temperatura y lluvia
    (60 meses válidos o más de lluvia y de Tmáx, Tmín o Tmed), luego las que solo tienen temperatura y al final las que
    solo tienen lluvia, cada grupo de más a menos meses válidos. Las de coordenadas por revisar van al final.
    Luego las de fuera, con el mismo criterio de grupos y de la más cercana a la más lejana.
    """
    import geopandas as gpd

    t = tabla(repo_dir)
    pts = gpd.GeoSeries(gpd.points_from_xy(t["lon"], t["lat"]), crs=4326)
    geom = zona["geom"]
    t["dentro"] = pts.within(geom).values
    c = geom.centroid
    t["dist_km"] = (((t["lat"] - c.y) ** 2 + ((t["lon"] - c.x) * 0.9998) ** 2) ** 0.5 * 111.2).round(1)
    if zona.get("tipo") == "provincia":
        t = t[t["provincia"].map(_norm) == _norm(zona["provincia"])]
    elif recuadro is not None:
        n, o, s, e = recuadro
        t = t[t["lat"].between(s, n) & t["lon"].between(o, e)]
    else:
        t = t[t["dentro"]]
    for col in ("meses_tmed", "coordenadas_revisar"):
        if col not in t:
            t[col] = 0 if col == "meses_tmed" else False
    mt = t[["meses_tmax", "meses_tmin", "meses_tmed"]].max(axis=1)
    t = t.assign(meses=mt * 2 + t["meses_precip"])
    t = t[t["meses"] > 0]
    # nivel 0: temperatura y lluvia (60 meses o más de cada una); 1: solo temperatura; 2: solo lluvia o pocos datos;
    # +3 si las coordenadas están por revisar (se usan solo si no hay otra)
    con_t = mt >= 60
    con_p = t["meses_precip"] >= 60
    t["nivel"] = (~(con_t & con_p)).astype(int) + (~con_t).astype(int) + 3 * t["coordenadas_revisar"].fillna(False).astype(bool)
    dentro = t[t["dentro"]].sort_values(["nivel", "meses", "dist_km"], ascending=[True, False, True])
    fuera = t[~t["dentro"]].assign(_corta=lambda d: d["meses"] < 60)   # fuera de la zona manda la cercanía,
    fuera = fuera.sort_values(["nivel", "_corta", "dist_km"]).drop(columns="_corta")  # entre las de 60 meses o más
    return pd.concat([dentro, fuera])


def elegir(archivo: str, zona: dict, repo_dir, recuadro=None):
    """Como `resolver`, pero si `archivo` está vacío elige sola la mejor estación del curso para la zona.

    Devuelve (ruta, ficha) o (None, None) si el usuario escribió «ninguna» o no hay estación del curso.
    """
    archivo = str(archivo or "").strip()
    if _norm(archivo) in NINGUNA:
        return None, None
    if archivo:
        return resolver(archivo, repo_dir, zona.get("provincia"))
    c = candidatas(zona, repo_dir, recuadro)
    if c.empty:
        return None, None
    print(f"Estaciones del curso para esta zona: {len(c)} (se usa la primera; para elegir otra, escriba su archivo en ARCHIVO_ESTACION):")
    for _, r in c.head(10).iterrows():
        tm = f" · Tmed {int(r['meses_tmed'])}" if r.get("meses_tmed", 0) else ""
        aviso = " · coordenadas por revisar" if bool(r.get("coordenadas_revisar", False)) else ""
        print(f"  {r['archivo']:55s} {r['estacion']} · Tmáx {r['meses_tmax']} · Tmín {r['meses_tmin']}{tm} · lluvia {r['meses_precip']} meses · {r['dist_km']:.0f} km del centro{aviso}")
    if len(c) > 10:
        print(f"  … y {len(c) - 10} más (lista completa: datos/estaciones/indice_estaciones.csv)")
    f = c.iloc[0]
    return _local(f["archivo"], repo_dir), f


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
        return _local(f["archivo"], repo_dir), f
    lineas = [f"No se encontró el archivo de estación «{archivo}».", ""]
    if provincia:
        p = de_provincia(provincia, repo_dir)
        if len(p):
            lineas.append(f"Estaciones del curso en {provincia} (escriba el nombre de la columna «archivo» en ARCHIVO_ESTACION):")
            for _, r in p.head(15).iterrows():
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
