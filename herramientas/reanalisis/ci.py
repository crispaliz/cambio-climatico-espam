"""(Docente) Pasos del release de datos para GitHub Actions (`.github/workflows/datos-release.yml`).

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Hace lo mismo que `preparar_releases.py`, pero repartido en trabajos que GitHub ejecuta en paralelo en
sus propios servidores: ERA5 una provincia por trabajo y CORe un año por trabajo. Los parámetros salen de
`datos/release.json`, de modo que cada versión del release queda registrada en el repositorio.

    python -m herramientas.reanalisis.ci plan                    # matrices de provincias y años (JSON)
    python -m herramientas.reanalisis.ci era5 --slug manabi      # una provincia: diario, mensual y terreno
    python -m herramientas.reanalisis.ci core-anio --anio 1998   # CORe diario de Ecuador, un año
    python -m herramientas.reanalisis.ci core-provincias         # reparte los años en archivos por provincia
    python -m herramientas.reanalisis.ci publicar                # manifiesto y subida al release

Credenciales (secretos del repositorio, nunca en el código): CDSAPI_KEY para ERA5; GITHUB_TOKEN lo pone
GitHub Actions con permiso de escritura en el propio repositorio.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
CONFIG = RAIZ / "datos" / "release.json"


def config() -> dict:
    c = json.loads(CONFIG.read_text(encoding="utf-8"))
    c.setdefault("fuentes", ["era5", "core"])
    c.setdefault("provincias", "todas")
    c.setdefault("inicio_dia", 0)
    c.setdefault("hilos_core", 2)
    return c


def anios(c) -> range:
    return range(int(c["periodo"][0]), int(c["periodo"][1]) + 1)


def plan(c) -> dict:
    from herramientas import limites
    from herramientas.reanalisis import preparar_releases as PR

    provs = PR.lista_provincias(c["provincias"])
    p = [{"nombre": n, "slug": limites.slug(n), "celdas": int(len(limites.celdas(limites.zona(n)["geom"])))} for n in provs]
    p.sort(key=lambda r: -r["celdas"])  # las provincias con más celdas primero: el total termina antes
    return {
        "provincias": p if "era5" in c["fuentes"] else [],
        "anios": list(anios(c)) if "core" in c["fuentes"] else [],
        "etiqueta": c["etiqueta"],
        "era5": "era5" in c["fuentes"],
        "core": "core" in c["fuentes"],
    }


def _salida(a) -> pathlib.Path:
    s = pathlib.Path(a.salida)
    s.mkdir(parents=True, exist_ok=True)
    return s


def era5_provincia(c, slug: str, salida, trabajo) -> list[pathlib.Path]:
    from herramientas import limites
    from herramientas.reanalisis import era5
    from herramientas.reanalisis import preparar_releases as PR

    if not os.environ.get("CDSAPI_KEY"):
        sys.exit("Falta el secreto CDSAPI_KEY del repositorio (Settings › Secrets and variables › Actions).")
    print("Credencial CDS:", era5.credenciales())
    nombre = next(n for n in PR.lista_provincias("todas") if limites.slug(n) == slug)
    return PR.era5_provincias([nombre], anios(c), salida, trabajo, int(c["inicio_dia"]))


def core_anio(c, anio: int, salida, trabajo) -> list[pathlib.Path]:
    from herramientas.reanalisis import core

    return core.preparar_diario([anio], trabajo, salida, hilos=int(c["hilos_core"]))


def core_provincias(c, entrada, salida) -> list[pathlib.Path]:
    from herramientas.reanalisis import core, release
    from herramientas.reanalisis import preparar_releases as PR

    anuales = sorted(pathlib.Path(entrada).glob("core_ecuador_diario_*.nc"))
    esperados = len(anios(c))
    if len(anuales) != esperados:
        hay = {int(f.stem.rsplit("_", 1)[1]) for f in anuales}
        sys.exit(f"CORe: hay {len(anuales)} años de {esperados}; faltan {sorted(set(anios(c)) - hay)}. "
                 "Vuelva a ejecutar los trabajos fallidos.")
    provs = None if c["provincias"] in ("todas", ["todas"]) else PR.lista_provincias(c["provincias"])
    return release.por_provincia("core", anuales, salida, mensual=core.mensual_desde_diario, provincias=provs)


def publicar(c, entrada, simular: bool = False) -> dict:
    from herramientas import publicar as P
    from herramientas.reanalisis import preparar_releases as PR
    from herramientas.reanalisis import release

    entrada = pathlib.Path(entrada)
    archivos = sorted(f for f in entrada.rglob("*.nc") if not f.name.startswith("core_ecuador_"))
    if not archivos:
        sys.exit("No hay archivos para publicar.")
    destino = entrada / "manifiesto.json"
    man = P.manifiesto(archivos, destino, {"etiqueta": c["etiqueta"], "periodo": c["periodo"],
                                           "fecha": dt.date.today().isoformat(),
                                           "generado_por": "GitHub Actions, .github/workflows/datos-release.yml"})
    esperados = {release.nombre(f, fr, p["slug"]) for p in plan(c)["provincias"] for f, fr in release.PRODUCTOS if f == "era5"}
    if c["provincias"] in ("todas", ["todas"]) and "core" in c["fuentes"]:
        from herramientas import limites
        esperados |= {release.nombre("core", fr, limites.slug(n)) for n in PR.lista_provincias("todas") for fr in ("diario", "mensual")}
    faltan = sorted(esperados - {f.name for f in archivos})
    print(f"{len(archivos)} archivos ({sum(f.stat().st_size for f in archivos) / 1e6:.0f} MB); faltan {len(faltan)}"
          + (f": {', '.join(faltan)}" if faltan else ""))
    if simular:
        return {"archivos": [f.name for f in archivos], "faltan": faltan}
    tok = os.environ.get("GITHUB_TOKEN") or sys.exit("Falta GITHUB_TOKEN")
    estado = P.publicar(archivos + [man], os.environ.get("GITHUB_REPOSITORY", release.REPO), c["etiqueta"], tok,
                        f"Datos de reanálisis por provincia ({c['etiqueta']})",
                        PR.notas(anios(c), c["fuentes"], c["etiqueta"]), bool(c.get("reemplazar", False)))
    if faltan:
        print("::warning::Release publicado incompleto; vuelva a ejecutar los trabajos fallidos y luego 'publicar'.")
    return estado


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="paso", required=True)
    sub.add_parser("plan")
    p = sub.add_parser("era5"); p.add_argument("--slug", required=True); p.add_argument("--salida", default="salida"); p.add_argument("--trabajo", default="trabajo")
    p = sub.add_parser("core-anio"); p.add_argument("--anio", type=int, required=True); p.add_argument("--salida", default="salida"); p.add_argument("--trabajo", default="trabajo")
    p = sub.add_parser("core-provincias"); p.add_argument("--entrada", default="anuales"); p.add_argument("--salida", default="salida")
    p = sub.add_parser("publicar"); p.add_argument("--entrada", default="salida"); p.add_argument("--simular", action="store_true")
    a = ap.parse_args()
    c = config()
    if a.paso == "plan":
        pl = plan(c)
        print(json.dumps(pl, ensure_ascii=False))
        gh = os.environ.get("GITHUB_OUTPUT")
        if gh:
            with open(gh, "a", encoding="utf-8") as fh:
                for k in ("provincias", "anios"):
                    fh.write(f"{k}={json.dumps(pl[k], ensure_ascii=False)}\n")
                fh.write(f"era5={str(pl['era5']).lower()}\ncore={str(pl['core']).lower()}\netiqueta={pl['etiqueta']}\n")
    elif a.paso == "era5":
        print([f.name for f in era5_provincia(c, a.slug, _salida(a), pathlib.Path(a.trabajo))])
    elif a.paso == "core-anio":
        print([f.name for f in core_anio(c, a.anio, _salida(a), pathlib.Path(a.trabajo))])
    elif a.paso == "core-provincias":
        print([f.name for f in core_provincias(c, a.entrada, _salida(a))])
    elif a.paso == "publicar":
        publicar(c, a.entrada, a.simular)


if __name__ == "__main__":
    main()
