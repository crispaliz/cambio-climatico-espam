"""(Docente) Publica archivos como assets de un release de GitHub.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Necesita un token personal de GitHub del DUEÑO del repositorio (solo el docente):
  GitHub › Settings › Developer settings › Personal access tokens › Fine-grained tokens ›
  Generate new token › Repository access: solo `cambio-climatico-espam` ›
  Permissions › Repository › Contents: Read and write.
En Colab, guárdelo en Secrets con el nombre GITHUB_TOKEN. Nunca lo escriba en un cuaderno compartido.

Los estudiantes no necesitan token: los assets de un repositorio público se descargan sin cuenta.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import time

API = "https://api.github.com"
SUBIDAS = "https://uploads.github.com"


def token(valor: str | None = None, nombre_secreto: str = "GITHUB_TOKEN") -> str:
    """Token de GitHub: argumento, Secrets de Colab, variable de entorno o se pide sin mostrarlo."""
    if not valor:
        try:
            from google.colab import userdata
            valor = userdata.get(nombre_secreto)
        except Exception:
            valor = None
    valor = valor or os.environ.get(nombre_secreto)
    if not valor:
        import getpass
        valor = getpass.getpass("Token de GitHub (no se mostrará): ")
    return valor.strip()


class Release:
    """Crea u obtiene un release por etiqueta y gestiona sus assets."""

    def __init__(self, repo: str, etiqueta: str, tok: str, titulo: str | None = None, notas: str = ""):
        import requests

        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json",
                               "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "cambio-climatico-espam"})
        self.repo, self.etiqueta = repo, etiqueta
        r = self.s.get(f"{API}/repos/{repo}/releases/tags/{etiqueta}")
        if r.status_code == 404:
            r = self.s.post(f"{API}/repos/{repo}/releases", json={
                "tag_name": etiqueta, "name": titulo or etiqueta, "body": notas, "draft": False, "prerelease": False})
            print(f"Release {etiqueta} creado")
        r.raise_for_status()
        self.datos = r.json()
        self.id = self.datos["id"]

    def assets(self) -> dict:
        out, pagina = {}, 1
        while True:
            r = self.s.get(f"{API}/repos/{self.repo}/releases/{self.id}/assets", params={"per_page": 100, "page": pagina})
            r.raise_for_status()
            lote = r.json()
            out.update({a["name"]: a for a in lote})
            if len(lote) < 100:
                return out
            pagina += 1

    def notas(self, texto: str):
        self.s.patch(f"{API}/repos/{self.repo}/releases/{self.id}", json={"body": texto}).raise_for_status()

    def subir(self, ruta, reemplazar: bool = False, existentes: dict | None = None, intentos: int = 3) -> str:
        """Sube un archivo. Si ya existe uno con el mismo nombre y tamaño, lo salta (salvo `reemplazar`)."""
        ruta = pathlib.Path(ruta)
        existentes = self.assets() if existentes is None else existentes
        previo = existentes.get(ruta.name)
        if previo:
            if previo["size"] == ruta.stat().st_size and not reemplazar:
                return "igual, se mantiene"
            self.s.delete(f"{API}/repos/{self.repo}/releases/assets/{previo['id']}").raise_for_status()
        for k in range(intentos):
            try:
                with open(ruta, "rb") as fh:
                    r = self.s.post(f"{SUBIDAS}/repos/{self.repo}/releases/{self.id}/assets", params={"name": ruta.name},
                                    data=fh, headers={"Content-Type": "application/octet-stream"}, timeout=600)
                r.raise_for_status()
                return "reemplazado" if previo else "subido"
            except Exception as err:
                if k == intentos - 1:
                    raise
                print(f"  {ruta.name}: {err}; reintento en {30 * 2 ** k} s")
                time.sleep(30 * 2 ** k)


def sha256(ruta) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as fh:
        for bloque in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def manifiesto(archivos, destino, extra: dict | None = None) -> pathlib.Path:
    """Tamaño, SHA-256, variables y periodo de cada archivo, para documentar el release."""
    import xarray as xr

    filas = []
    for f in sorted(map(pathlib.Path, archivos)):
        fila = {"archivo": f.name, "bytes": f.stat().st_size, "sha256": sha256(f)}
        try:
            with xr.open_dataset(f) as ds:
                fila["variables"] = list(ds.data_vars)
                fila["malla"] = {k: int(ds.sizes[k]) for k in ("lat", "lon") if k in ds.sizes}
                if "time" in ds.dims:
                    fila["desde"], fila["hasta"] = str(ds["time"].values[0])[:10], str(ds["time"].values[-1])[:10]
        except Exception:
            pass
        filas.append(fila)
    destino = pathlib.Path(destino)
    destino.write_text(json.dumps({**(extra or {}), "archivos": filas}, ensure_ascii=False, indent=2), encoding="utf-8")
    return destino


def publicar(archivos, repo: str, etiqueta: str, tok: str, titulo: str | None = None, notas: str = "",
             reemplazar: bool = False) -> dict:
    """Sube todos los archivos al release `etiqueta` (lo crea si no existe). Devuelve {archivo: estado}."""
    rel = Release(repo, etiqueta, tok, titulo, notas)
    if notas:
        rel.notas(notas)
    existentes = rel.assets()
    estado = {}
    archivos = sorted(map(pathlib.Path, archivos))
    for k, f in enumerate(archivos, 1):
        estado[f.name] = rel.subir(f, reemplazar, existentes)
        print(f"  [{k}/{len(archivos)}] {f.name} ({f.stat().st_size / 1e6:.1f} MB): {estado[f.name]}")
    print(f"Listo: https://github.com/{repo}/releases/tag/{etiqueta}")
    return estado
