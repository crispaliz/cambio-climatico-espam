"""(Docente) Descarga ERA5 y CORe para todas las provincias y genera el release de datos (opción B).

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Uso en Colab: cuaderno `herramientas/reanalisis/preparar_releases.ipynb`.
Uso en una terminal (equipo propio o servidor, con el repositorio clonado):

    export CDSAPI_KEY=<su token del CDS>     GITHUB_TOKEN=<token del repositorio>
    python -m herramientas.reanalisis.preparar_releases --salida ./releases --trabajo ./trabajo \
        --anios 1981 2024 --provincias todas --fuentes era5 core --publicar --etiqueta datos-v1

Todo es reanudable: si se corta, vuelva a ejecutar lo mismo y seguirá donde quedó.
  - ERA5: una solicitud por celda de 0,25° (≈ 450 celdas para Ecuador con Galápagos). Las celdas de borde
    compartidas por dos provincias se descargan una sola vez (`trabajo/celdas_era5`).
  - CORe: un año diario de Ecuador por vez (1 460 archivos de 6 h, solo 8 campos de cada uno).
"""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import time

from herramientas import limites
from herramientas.reanalisis import core, era5, release


def lista_provincias(provincias="todas") -> list[str]:
    provs = limites.cargar("provincias")
    provs = provs[provs["region"] != "Zona no delimitada"]
    todas = list(provs["nombre"])
    if provincias in (None, "todas", ["todas"]):
        return todas
    return [limites.zona(p)["nombre"] for p in provincias]  # valida el nombre y lo devuelve como en la capa


def era5_provincias(provincias, anios, salida, trabajo, inicio_dia: int = 0) -> list[pathlib.Path]:
    """era5_diario, era5_mensual y era5_terreno de cada provincia."""
    import xarray as xr

    salida, trabajo = pathlib.Path(salida), pathlib.Path(trabajo)
    salida.mkdir(parents=True, exist_ok=True)
    celdas_dir = trabajo / "celdas_era5"
    zonas = [limites.zona(p) for p in provincias]

    # terreno: una sola solicitud para el recuadro que contiene todas las provincias pedidas
    cajas = [limites.recuadro(z["geom"], 0.25, 1) for z in zonas]
    grande = [max(c[0] for c in cajas), min(c[1] for c in cajas), min(c[2] for c in cajas), max(c[3] for c in cajas)]
    crudo = era5.descargar_terreno(grande, trabajo / f"era5_terreno_{'_'.join(f'{x:g}' for x in grande)}.nc")
    terr = era5.abrir_ds(crudo)
    terr = (terr.isel(time=0, drop=True) if "time" in terr.dims else terr)[["z"]].sortby("lat").sortby("lon")

    hechos = []
    t0 = time.time()
    for k, (z, (n, o, s, e)) in enumerate(zip(zonas, cajas), 1):
        f_t = salida / release.nombre("era5", "terreno", z["slug"])
        f_d = salida / release.nombre("era5", "diario", z["slug"])
        f_m = salida / release.nombre("era5", "mensual", z["slug"])
        if not (f_d.exists() and f_m.exists()):
            print(f"[{k}/{len(zonas)}] ERA5 {z['nombre']} · {len(limites.celdas(z['geom']))} celdas")
            era5.descargar_zona(z["geom"], anios, salida, z["slug"], inicio_dia, avance=False, carpeta_celdas=celdas_dir)
        if not f_t.exists():
            sub = terr.sel(lat=slice(s, n), lon=slice(o, e))
            sub.attrs = {"title": f"ERA5, geopotencial del terreno del modelo, {z['nombre']}",
                         "source": f"C3S CDS, {era5.MENSUAL}"}
            sub.to_netcdf(f_t)
        hechos += [f_d, f_m, f_t]
        print(f"   {z['nombre']} listo · {(time.time() - t0) / 60:.0f} min acumulados")
    return hechos


def core_provincias(provincias, anios, salida, trabajo, hilos: int = 4) -> list[pathlib.Path]:
    """core_diario y core_mensual de cada provincia, a partir de los años diarios de Ecuador."""
    trabajo = pathlib.Path(trabajo)
    anuales = core.preparar_diario(anios, trabajo / "grib_core", trabajo / "core_anual", hilos=hilos)
    return release.por_provincia("core", anuales, salida, mensual=core.mensual_desde_diario, provincias=provincias)


def generar(fuentes, anios, provincias, salida, trabajo, inicio_dia: int = 0, hilos_core: int = 4) -> list[pathlib.Path]:
    provincias = lista_provincias(provincias)
    archivos = []
    if "era5" in fuentes:
        archivos += era5_provincias(provincias, anios, salida, trabajo, inicio_dia)
    if "core" in fuentes:
        archivos += core_provincias(provincias, anios, salida, trabajo, hilos_core)
    return archivos


def notas(anios, fuentes, etiqueta) -> str:
    a0, a1 = min(anios), max(anios)
    filas = "\n".join(f"| `{f}_{fr}_<provincia>.nc` |" for f, fr in release.PRODUCTOS if f in fuentes)
    return f"""Datos de reanálisis por provincia de Ecuador, {a0}–{a1}, para las prácticas de Cambio Climático (ESPAM MFL).

Generado el {dt.date.today().isoformat()} con `herramientas/reanalisis/preparar_releases.py`. Detalle de cada archivo en `manifiesto.json`.

| Archivo |
|---|
{filas}

- ERA5: series horarias por punto del Climate Data Store, día local UTC-5 (00–24 h), celdas de 0,25° que tocan la provincia.
- CORe: NOAA/NCEP CPC, flujos de 6 h, día 06–06 UTC (01:00–01:00 hora local), recuadro de la provincia.
- Variables: tmed, tmax, tmin (°C), pr (mm/día; mm/mes en los mensuales), hr (%), q (g/kg), ps (hPa), u10, v10, ws (m/s).

Uso: cuaderno común `CR01_descarga_reanalisis` con `MODO_DATOS = "release"` y la etiqueta `{etiqueta}`.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL. ERA5: Hersbach et al. (2020), Copernicus C3S. CORe: NOAA/NCEP CPC.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--trabajo", required=True)
    ap.add_argument("--anios", nargs=2, type=int, default=[1981, 2024])
    ap.add_argument("--provincias", nargs="+", default=["todas"])
    ap.add_argument("--fuentes", nargs="+", default=["era5", "core"], choices=["era5", "core"])
    ap.add_argument("--inicio-dia", type=int, default=0)
    ap.add_argument("--hilos-core", type=int, default=4)
    ap.add_argument("--publicar", action="store_true")
    ap.add_argument("--etiqueta", default=release.ETIQUETA)
    ap.add_argument("--reemplazar", action="store_true")
    a = ap.parse_args()

    from herramientas import publicar

    anios = range(a.anios[0], a.anios[1] + 1)
    if "era5" in a.fuentes:
        print("Credencial CDS:", era5.credenciales())
    archivos = generar(a.fuentes, anios, a.provincias, a.salida, a.trabajo, a.inicio_dia, a.hilos_core)
    man = publicar.manifiesto(archivos, pathlib.Path(a.salida) / "manifiesto.json",
                              {"etiqueta": a.etiqueta, "periodo": [a.anios[0], a.anios[1]], "fecha": dt.date.today().isoformat()})
    if a.publicar:
        publicar.publicar(archivos + [man], release.REPO, a.etiqueta, publicar.token(),
                          f"Datos de reanálisis por provincia ({a.etiqueta})", notas(anios, a.fuentes, a.etiqueta), a.reemplazar)


if __name__ == "__main__":
    main()
