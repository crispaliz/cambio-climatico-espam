"""(Docente) Compila los incidentes climáticos de gestión de riesgos del ECU 911 de todo el país.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Con este archivo en el repositorio, `RD1_02` no descarga nada del portal: cada equipo filtra su zona
del compilado. Sin él, cada estudiante baja unos 30–40 MB por mes desde Datos Abiertos.

En Colab (unos 10–20 minutos; reanudable, porque cada mes queda en la caché):
    !git clone -q https://github.com/crispaliz/cambio-climatico-espam
    %cd cambio-climatico-espam
    !python -m herramientas.eventos.preparar_ecu911
Luego suba `datos/eventos/ecu911_gestion_riesgos.csv.gz` al repositorio, en esa misma ruta
(Add file › Upload files). Repítalo cuando quiera incorporar los meses nuevos.
"""
from __future__ import annotations

import argparse
import pathlib

from herramientas.eventos import ecu911

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--desde", default="2021-07")
    ap.add_argument("--hasta", default=None)
    ap.add_argument("--cache", default="_cache_ecu911")
    ap.add_argument("--salida", default="datos/eventos/ecu911_gestion_riesgos.csv.gz")
    a = ap.parse_args()
    inc = ecu911.incidentes(carpeta=a.cache, desde=a.desde, hasta=a.hasta)
    salida = pathlib.Path(a.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    inc.to_csv(salida, index=False, encoding="utf-8")
    fallidos = inc.attrs.get("meses_fallidos", [])
    print(f"{len(inc)} incidentes, {inc['fecha'].min():%Y-%m} a {inc['fecha'].max():%Y-%m} → {salida} "
          f"({salida.stat().st_size / 1e6:.1f} MB)")
    print(inc.groupby("tipo").size().sort_values(ascending=False).to_string())
    if fallidos:
        print("Meses que no se pudieron leer (vuelva a ejecutar):", ", ".join(fallidos))
