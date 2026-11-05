"""(Docente / GitHub Actions) Tabla nacional de elementos expuestos por cantón.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Calcula, para los 224 cantones, la población y la infraestructura que están en el territorio y la parte
que está en zonas bajas (posible inundación costera o fluvial) o en laderas empinadas (posible movimiento
en masa). Se ejecuta en GitHub Actions (.github/workflows/exposicion.yml), que tiene acceso a internet, y
guarda `datos/exposicion/exposicion_cantones.csv` y `metadatos.json` en el repositorio. Los cuadernos solo
leen esa tabla: los estudiantes no descargan nada.

Fuentes (todas abiertas):
  - Población: WorldPop 2020, 1 km, sin restricción (UN-adjusted no), reescalada al total provincial del
    Censo 2022 (datos/inventario/poblacion_censo2022.csv).
  - Relieve: Copernicus DEM GLO-90 (ESA, © DLR e.V. 2010–2014 y © Airbus Defence and Space GmbH 2014–2018),
    teselas COG de 1° en el bucket público de AWS.
  - Infraestructura: OpenStreetMap (© colaboradores de OpenStreetMap, ODbL), extracto de Ecuador de Geofabrik.

Uso:  python -m herramientas.exposicion.preparar --salida datos/exposicion
      (pruebas sin internet: --worldpop, --dem-dir y --osm con archivos locales)
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import pathlib
import subprocess
import tempfile
import traceback

import numpy as np
import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[2]
URL_WORLDPOP = "https://data.worldpop.org/GIS/Population/Global_2000_2020_1km/2020/ECU/ecu_ppp_2020_1km_Aggregated.tif"
URL_DEM = "https://copernicus-dem-90m.s3.amazonaws.com/{n}/{n}.tif"
URL_OSM = "https://download.geofabrik.de/south-america/ecuador-latest.osm.pbf"

COTA_BAJA_M = 10.0          # zona baja: altitud < 10 m (zona costera de baja elevación, McGranahan et al., 2007)
PENDIENTE_GRADOS = 20.0     # ladera empinada: pendiente > 20° en el DEM de 90 m
PASO_VIA_M = 200.0          # las vías se muestrean cada 200 m para saber qué tramo cae en zona baja o ladera

# Teselas de 1°: Ecuador continental y Galápagos (las de solo mar no existen y se omiten)
TESELAS = [(la, lo) for la in range(-6, 2) for lo in range(-82, -74)] + \
          [(la, lo) for la in range(-2, 1) for lo in range(-92, -88)]

CLASES_OSM = {
    "escuelas": ("amenity", {"school", "kindergarten", "college", "university"}),
    "salud": ("amenity", {"hospital", "clinic", "doctors"}),
    "emergencia": ("amenity", {"fire_station", "police"}),
}
VIAS = {"motorway", "trunk", "primary", "secondary"}
VIAS_PUENTE = VIAS | {"tertiary"}


def nombre_tesela(la: int, lo: int) -> str:
    ns = f"N{la:02d}" if la >= 0 else f"S{-la:02d}"
    ew = f"E{lo:03d}" if lo >= 0 else f"W{-lo:03d}"
    return f"Copernicus_DSM_COG_30_{ns}_00_{ew}_00_DEM"


def descargar(url: str, destino: pathlib.Path, timeout=600) -> pathlib.Path | None:
    import requests

    r = requests.get(url, stream=True, timeout=timeout)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    with open(destino, "wb") as f:
        for b in r.iter_content(1 << 20):
            f.write(b)
    return destino


# ---------------------------------------------------------------- población
def poblacion(ruta_tif, cantones):
    """Lee WorldPop y rasteriza los cantones en su malla. Devuelve (pob, transform, codigos_por_celda, lista)."""
    import rasterio
    from rasterio import features

    with rasterio.open(ruta_tif) as src:
        pob = src.read(1).astype("float64")
        nd = src.nodata
        T, crs = src.transform, src.crs
    if nd is not None:
        pob[pob == nd] = 0
    pob[~np.isfinite(pob) | (pob < 0)] = 0
    c = cantones.to_crs(crs) if crs else cantones
    codigos = list(c["codigo"])
    ids = features.rasterize(((g, i + 1) for i, g in enumerate(c.geometry)), out_shape=pob.shape, transform=T,
                             fill=0, dtype="int32", all_touched=False)
    return pob, T, ids, codigos


# ---------------------------------------------------------------- relieve
def _pendiente(e, la_centro, paso_grados):
    dy = paso_grados * 111_320.0
    dx = dy * math.cos(math.radians(la_centro))
    gy, gx = np.gradient(e, dy, dx)
    return np.degrees(np.arctan(np.hypot(gx, gy)))


def relieve(dem_dir, malla_T, malla_shape, puntos=None, tmp=None, log=print):
    """Fracción de cada celda de población en zona baja y en ladera; altitud y pendiente en los puntos.

    puntos: GeoDataFrame en EPSG:4326 (se le agregan las columnas 'cota' y 'pendiente').
    Devuelve (frac_baja, frac_ladera, n_teselas).
    """
    import rasterio
    from rasterio.warp import reproject, Resampling

    frac_b = np.zeros(malla_shape, "float32"); frac_l = np.zeros(malla_shape, "float32")
    cubierto = np.zeros(malla_shape, "float32")
    if puntos is not None:
        puntos["cota"] = np.nan; puntos["pendiente"] = np.nan
        px, py = puntos.geometry.x.values, puntos.geometry.y.values
    n = 0
    for la, lo in TESELAS:
        nom = nombre_tesela(la, lo)
        ruta = pathlib.Path(dem_dir) / f"{nom}.tif" if dem_dir else None
        if ruta is None or not ruta.exists():
            if dem_dir:
                continue
            ruta = descargar(URL_DEM.format(n=nom), pathlib.Path(tmp) / f"{nom}.tif")
            if ruta is None:
                continue
        with rasterio.open(ruta) as src:
            e = src.read(1).astype("float32"); T = src.transform
        e[e < -100] = np.nan
        paso = abs(T.a)
        s = _pendiente(np.nan_to_num(e, nan=0.0), la + 0.5, paso)
        baja = ((e < COTA_BAJA_M) & np.isfinite(e)).astype("float32")
        ladera = (s > PENDIENTE_GRADOS).astype("float32")
        for capa, dst in ((baja, frac_b), (ladera, frac_l), (np.ones_like(baja), cubierto)):
            tmpd = np.zeros(malla_shape, "float32")
            reproject(capa, tmpd, src_transform=T, src_crs="EPSG:4326", dst_transform=malla_T, dst_crs="EPSG:4326",
                      resampling=Resampling.average, src_nodata=None, dst_nodata=None)
            dst += tmpd
        if puntos is not None:
            sel = (px >= lo) & (px < lo + 1) & (py >= la) & (py < la + 1)
            if sel.any():
                inv = ~T
                cols, filas = inv * (px[sel], py[sel])
                cols = np.clip(np.floor(cols).astype(int), 0, e.shape[1] - 1)
                filas = np.clip(np.floor(filas).astype(int), 0, e.shape[0] - 1)
                idx = np.where(sel)[0]
                puntos.iloc[idx, puntos.columns.get_loc("cota")] = e[filas, cols]
                puntos.iloc[idx, puntos.columns.get_loc("pendiente")] = s[filas, cols]
        n += 1
        if not dem_dir and ruta.exists():
            ruta.unlink()
        log(f"  DEM {nom}: listo")
    with np.errstate(invalid="ignore", divide="ignore"):
        frac_b = np.where(cubierto > 0, frac_b / np.maximum(cubierto, 1e-9), 0)
        frac_l = np.where(cubierto > 0, frac_l / np.maximum(cubierto, 1e-9), 0)
    return np.clip(frac_b, 0, 1), np.clip(frac_l, 0, 1), n


# ---------------------------------------------------------------- OpenStreetMap
def osm(ruta_pbf_o_geojsonseq, tmp):
    """Puntos de servicios y vías principales del extracto de OSM. Devuelve (puntos, vias) en EPSG:4326."""
    import geopandas as gpd

    ruta = pathlib.Path(ruta_pbf_o_geojsonseq)
    if ruta.suffix == ".pbf":
        filtrado = pathlib.Path(tmp) / "filtrado.osm.pbf"
        seq = pathlib.Path(tmp) / "osm.geojsonseq"
        expr = ["nwr/amenity=school,kindergarten,college,university,hospital,clinic,doctors,fire_station,police",
                "w/highway=motorway,trunk,primary,secondary,tertiary"]
        subprocess.run(["osmium", "tags-filter", str(ruta), *expr, "-o", str(filtrado), "--overwrite"], check=True)
        subprocess.run(["osmium", "export", str(filtrado), "-f", "geojsonseq", "-o", str(seq), "--overwrite",
                        "--geometry-types=point,linestring,polygon"], check=True)
        ruta = seq
    g = gpd.read_file(ruta)
    if g.crs is None:
        g = g.set_crs(4326)
    for col in ("amenity", "highway", "bridge"):
        if col not in g:
            g[col] = None
    pts = []
    for clase, (k, vals) in CLASES_OSM.items():
        s = g[g[k].isin(vals)].copy()
        if s.empty:
            continue
        s["geometry"] = s.geometry.representative_point()
        s["clase"] = clase
        pts.append(s[["clase", "geometry"]])
    puntos = gpd.GeoDataFrame(pd.concat(pts, ignore_index=True) if pts else pd.DataFrame(columns=["clase", "geometry"]),
                              geometry="geometry", crs=4326)
    lin = g[g.geometry.geom_type.isin(["LineString", "MultiLineString"]) & g["highway"].isin(VIAS_PUENTE)].copy()
    lin["principal"] = lin["highway"].isin(VIAS)
    lin["puente"] = lin["bridge"].fillna("no").astype(str).isin(["yes", "viaduct"])
    return puntos, lin[["highway", "principal", "puente", "geometry"]].reset_index(drop=True)


def muestrear_vias(vias):
    """Puntos cada PASO_VIA_M a lo largo de las vías principales, cada uno con su longitud representada (km)."""
    import geopandas as gpd

    v = vias[vias["principal"]].to_crs(32717)
    filas = []
    for geom in v.geometry:
        partes = getattr(geom, "geoms", [geom])
        for p in partes:
            L = p.length
            if L <= 0:
                continue
            k = max(1, int(round(L / PASO_VIA_M)))
            for d in (np.arange(k) + 0.5) * (L / k):
                filas.append((p.interpolate(d), L / k / 1000))
    if not filas:
        return gpd.GeoDataFrame({"km": []}, geometry=[], crs=4326)
    return gpd.GeoDataFrame({"km": [f[1] for f in filas]}, geometry=[f[0] for f in filas], crs=32717).to_crs(4326)


# ---------------------------------------------------------------- tabla
def tabla(cantones, censo, worldpop=None, dem_dir=None, osm_ruta=None, log=print):
    import geopandas as gpd

    errores, meta = {}, {}
    out = cantones[["codigo", "nombre_dpa", "codigo_provincia", "provincia"]].copy()
    out["area_km2"] = cantones.to_crs(32717).area.values / 1e6
    with tempfile.TemporaryDirectory() as tmp:
        # 1. población
        pob = None
        try:
            ruta = worldpop or descargar(URL_WORLDPOP, pathlib.Path(tmp) / "worldpop.tif")
            pob, T, ids, codigos = poblacion(ruta, cantones)
            log(f"WorldPop: {pob.sum():,.0f} habitantes en la malla")
        except Exception as e:
            errores["poblacion"] = f"{type(e).__name__}: {e}"; log(traceback.format_exc())
        # 2. OSM
        puntos = vias = muestras = None
        try:
            ruta = osm_ruta or descargar(URL_OSM, pathlib.Path(tmp) / "ecuador.osm.pbf", timeout=1800)
            puntos, vias = osm(ruta, tmp)
            muestras = muestrear_vias(vias)
            log(f"OSM: {len(puntos)} servicios, {len(vias)} tramos de vía, {len(muestras)} muestras de vía principal")
        except Exception as e:
            errores["osm"] = f"{type(e).__name__}: {e}"; log(traceback.format_exc())
        # 3. relieve
        fb = fl = None
        if pob is not None:
            try:
                todos = None
                if puntos is not None:
                    todos = gpd.GeoDataFrame(pd.concat([puntos.assign(km=np.nan), muestras.assign(clase="via")],
                                                       ignore_index=True), geometry="geometry", crs=4326)
                fb, fl, nt = relieve(dem_dir, T, pob.shape, todos, tmp, log)
                meta["teselas_dem"] = nt
                if todos is not None:
                    puntos = todos[todos.clase != "via"].copy(); muestras = todos[todos.clase == "via"].copy()
            except Exception as e:
                errores["relieve"] = f"{type(e).__name__}: {e}"; log(traceback.format_exc())

    # agregación por cantón
    if pob is not None:
        n = len(codigos)
        def suma(arr):
            return np.bincount(ids.ravel(), weights=arr.ravel(), minlength=n + 1)[1:]
        s_pob = suma(pob)
        out["poblacion_worldpop_2020"] = s_pob
        if fb is not None:
            out["_baja"] = suma(pob * fb); out["_ladera"] = suma(pob * fl)
        # reescalado al Censo 2022 por provincia
        fac = {}
        for prov, g in out.groupby("provincia"):
            tot = censo.get(prov)
            wp = g["poblacion_worldpop_2020"].sum()
            fac[prov] = tot / wp if tot and wp > 0 else np.nan
        out["factor_censo"] = out["provincia"].map(fac)
        out["poblacion_2022"] = (out["poblacion_worldpop_2020"] * out["factor_censo"]).round()
        out["densidad_hab_km2"] = out["poblacion_2022"] / out["area_km2"]
        if fb is not None:
            out["poblacion_cota_baja"] = (out.pop("_baja") * out["factor_censo"]).round()
            out["poblacion_ladera"] = (out.pop("_ladera") * out["factor_censo"]).round()
            out["pct_cota_baja"] = 100 * out["poblacion_cota_baja"] / out["poblacion_2022"]
            out["pct_ladera"] = 100 * out["poblacion_ladera"] / out["poblacion_2022"]
        meta["factor_censo_por_provincia"] = {k: (None if not np.isfinite(v) else round(float(v), 3)) for k, v in fac.items()}

    if puntos is not None:
        cj = cantones[["codigo", "geometry"]]
        p = gpd.sjoin(puntos, cj, predicate="within", how="inner")
        for clase in CLASES_OSM:
            sub = p[p.clase == clase]
            out[clase] = out["codigo"].map(sub.groupby("codigo").size()).fillna(0).astype(int)
            if "cota" in sub:
                out[f"{clase}_cota_baja"] = out["codigo"].map(sub[sub.cota < COTA_BAJA_M].groupby("codigo").size()).fillna(0).astype(int)
                out[f"{clase}_ladera"] = out["codigo"].map(sub[sub.pendiente > PENDIENTE_GRADOS].groupby("codigo").size()).fillna(0).astype(int)
        m = gpd.sjoin(muestras, cj, predicate="within", how="inner")
        out["km_vias_principales"] = out["codigo"].map(m.groupby("codigo")["km"].sum()).fillna(0).round(1)
        if "cota" in m:
            out["km_vias_cota_baja"] = out["codigo"].map(m[m.cota < COTA_BAJA_M].groupby("codigo")["km"].sum()).fillna(0).round(1)
            out["km_vias_ladera"] = out["codigo"].map(m[m.pendiente > PENDIENTE_GRADOS].groupby("codigo")["km"].sum()).fillna(0).round(1)
        pu = vias[vias["puente"]].copy(); pu["geometry"] = pu.geometry.representative_point()
        pu = gpd.sjoin(pu, cj, predicate="within", how="inner")
        out["puentes"] = out["codigo"].map(pu.groupby("codigo").size()).fillna(0).astype(int)

    out = out.rename(columns={"nombre_dpa": "canton"})
    for c in out.columns:
        if out[c].dtype.kind == "f":
            out[c] = out[c].round(2)
    return out, errores, meta


def main(argv=None):
    import geopandas as gpd

    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=str(RAIZ / "datos" / "exposicion"))
    ap.add_argument("--worldpop"); ap.add_argument("--dem-dir"); ap.add_argument("--osm")
    a = ap.parse_args(argv)
    sal = pathlib.Path(a.salida); sal.mkdir(parents=True, exist_ok=True)
    cantones = gpd.read_file(RAIZ / "datos" / "limites" / "ecuador_cantones.geojson")
    censo = pd.read_csv(RAIZ / "datos" / "inventario" / "poblacion_censo2022.csv").set_index("provincia")["poblacion_2022"].to_dict()
    t, errores, meta = tabla(cantones, censo, a.worldpop, a.dem_dir, a.osm)
    t.to_csv(sal / "exposicion_cantones.csv", index=False, encoding="utf-8")
    meta.update({
        "generado": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "cantones": len(t), "columnas": list(t.columns), "errores": errores,
        "umbrales": {"cota_baja_m": COTA_BAJA_M, "pendiente_grados": PENDIENTE_GRADOS, "paso_via_m": PASO_VIA_M},
        "fuentes": {"poblacion": URL_WORLDPOP, "censo": "datos/inventario/poblacion_censo2022.csv",
                    "relieve": URL_DEM.format(n="<tesela>"), "osm": URL_OSM},
    })
    (sal / "metadatos.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"errores": errores, "cantones": len(t)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
