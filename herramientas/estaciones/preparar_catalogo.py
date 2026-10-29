"""(Docente) Construye el catálogo de estaciones del curso (`datos/estaciones/`) desde las fuentes originales.

© 2026 Cristian Omar Paliz Acosta · ESPAM MFL · Todos los derechos reservados.

Uso:
    python -m herramientas.estaciones.preparar_catalogo --fuentes CARPETA --salida datos/estaciones --zips CARPETA_ZIPS

CARPETA debe contener:
    ogimet_pr_diaria.csv, ogimet_tmax_diaria.csv, ogimet_tmin_diaria.csv   SYNOP de OGIMET (tabla ancha)
    redes_pr_diaria.csv, redes_tmax_diaria.csv, redes_tmin_diaria.csv,
    redes_tmed_diaria.csv, redes_resumen.csv                                redes INAMHI, HIDRONACIÓN, CELEC, GYE, CCS
    correcciones_coordenadas.csv, coordenadas_pendientes.csv               ubicación verificada de estaciones
    altitud_dem.csv                                                         altitud del DEM para estaciones sin altitud
    rr_est_T_QC.csv, estaciones_QC_provincia.csv                           lluvia diaria INAMHI 1964–2018 (QC + Climatol/CHIRPS)
    metar_semt.csv, calceta_espam.csv                                       ya en el formato del curso

Reglas (se documentan en datos/estaciones/README.md):
  1. Las coordenadas se corrigen antes de cualquier cruce.
  2. La lluvia del INAMHI 1964–2018 se prolonga con la de las redes (2019–2024) solo si en 2016–2018 coinciden:
     ≥ 85 % de días idénticos, cociente de totales entre 0,9 y 1,1 y r ≥ 0,85.
  3. La temperatura de la red INAMHI (desde 2022) completa los días sin dato del SYNOP de la misma estación (código W)
     o se agrega a la estación INAMHI del mismo código (código M); si no hay ninguna, es una estación nueva.
  4. Una estación con temperatura toma la lluvia de la estación INAMHI más cercana si está a ≤ 5,5 km y con ≤ 100 m de
     diferencia de altitud.
  5. Todo termina el 31 de diciembre de 2024 (fin de los reanálisis del curso). Los meses válidos se cuentan desde 1981.
"""
from __future__ import annotations

import argparse
import io
import pathlib
import re
import sys
import unicodedata
import warnings
import zipfile

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
FIN = "2024-12-31"
RAMA = "https://raw.githubusercontent.com/crispaliz/cambio-climatico-espam/estaciones/"
MAIN = "https://raw.githubusercontent.com/crispaliz/cambio-climatico-espam/main/datos/estaciones/"
COLS = ["tmed", "tmax", "tmin", "precip", "hr", "pres", "vv", "dv"]
FUENTE_INAMHI = "INAMHI {c}: lluvia 1964–2018 con control de calidad y relleno Climatol (apoyo CHIRPS)"


def slug(s) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def km(lat1, lon1, lat2, lon2):
    return np.hypot(lat1 - lat2, (lon1 - lon2) * np.cos(np.radians(lat1))) * 111.2


def ancha(ruta, n_meta, clave):
    """Tabla ancha (una fila por estación, una columna por día) → (metadatos, DataFrame días × estaciones)."""
    d = pd.read_csv(ruta, low_memory=False)
    m = d.iloc[:, :n_meta].copy()
    m.index = m[clave].astype(str)
    x = d.iloc[:, n_meta:].apply(pd.to_numeric, errors="coerce")
    x.columns = pd.to_datetime(x.columns).normalize()
    x.index = m.index
    x = x[~x.index.duplicated()]
    return m[~m.index.duplicated()], x.T.sort_index().loc[:FIN]


def meses_validos(s: pd.Series, completo: bool) -> int:
    """Meses 1981–2024 que pasan la regla de los cuadernos (lluvia: mes completo; temperatura: ≤ 4 días faltantes)."""
    s = s.loc["1981":FIN].dropna()
    if s.empty:
        return 0
    g = s.groupby([s.index.year, s.index.month]).size()
    dim = np.array([pd.Period(f"{y}-{m:02d}").days_in_month for y, m in g.index])
    return int(((g.values == dim) if completo else (g.values >= dim - 4)).sum())


def provincia_de(lat, lon, prov):
    import geopandas as gpd
    pts = gpd.GeoDataFrame(geometry=gpd.points_from_xy(lon, lat), crs=4326)
    j = gpd.sjoin(pts, prov[["nombre", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated()]["nombre"]
    falta = j.isna()
    if falta.any():   # estaciones costeras que caen al mar por pocos metros: provincia más cercana (≤ 10 km)
        cerca = gpd.sjoin_nearest(pts[falta.values].to_crs(32717), prov[["nombre", "geometry"]].to_crs(32717),
                                  how="left", max_distance=10_000)
        cerca = cerca[~cerca.index.duplicated()]["nombre"]
        j.loc[cerca.index] = cerca.values
    return j.values


def main(fuentes, salida, zips):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    from herramientas import limites
    F, OUT, Z = pathlib.Path(fuentes), pathlib.Path(salida), pathlib.Path(zips)
    prov = limites.cargar("provincias").to_crs(4326)
    corr = pd.read_csv(F / "correcciones_coordenadas.csv").set_index("codigo")
    pend = set(pd.read_csv(F / "coordenadas_pendientes.csv")["codigo"].astype(str))

    def corregir(cod, lat, lon, z):
        base = re.sub(r"-\d$", "", str(cod))
        for k in (str(cod), base):
            if k in corr.index:
                r = corr.loc[k]
                return float(r.lat), float(r.lon), float(r.elev) if pd.notna(r.elev) else z, True
        return lat, lon, z, False

    # ---------------------------------------------------------------- INAMHI 1964–2018 (lluvia)
    q = pd.read_csv(F / "rr_est_T_QC.csv")
    qm = q.iloc[:, :5].set_index("Code")
    Q = q.iloc[:, 5:]
    Q.columns = pd.to_datetime(Q.columns).normalize()
    Q.index = qm.index
    Q = Q.T
    pq = pd.read_csv(F / "estaciones_QC_provincia.csv")
    pq = pq[pq.variable == "precipitacion"].set_index("codigo")
    est = {}   # código → dict(meta) ; series en SER[código] = DataFrame
    SER = {}
    for c, r in qm.iterrows():
        lat, lon, z, cor = corregir(c, r.Y, r.X, r.Z)
        est[c] = dict(codigo=c, estacion=str(r.Name).replace("_", " ").title(), lat=lat, lon=lon, altitud_m=z,
                      red="INAMHI", corregida=cor, fuente=FUENTE_INAMHI.format(c=c), omm=pd.NA)
        SER[c] = pd.DataFrame({"precip": Q[c].round(1)})

    # ---------------------------------------------------------------- redes: prolongación de la lluvia y estaciones nuevas
    rm, Rp = ancha(F / "redes_pr_diaria.csv", 6, "codigo_M")
    res = pd.read_csv(F / "redes_resumen.csv")
    red_de = res.drop_duplicates(["variable", "codigo"]).set_index(["variable", "codigo"])["red"]
    prolongadas, nuevas_pr = [], []
    qc_lat = np.array([est[k]["lat"] for k in SER]); qc_lon = np.array([est[k]["lon"] for k in SER]); qc_cod = list(SER)
    for c in Rp.columns:
        s = Rp[c]
        if s.loc[:FIN].notna().sum() == 0:
            continue
        destino = c if c in SER else None
        if destino is None:   # código de la red (p. ej. W84239) en el sitio de una estación INAMHI (≤ 1 km)
            r = rm.loc[c]
            d = km(qc_lat, qc_lon, float(r.lat), float(r.lon))
            if d.min() <= 1:
                destino = qc_cod[int(np.argmin(d))]
        if destino is not None:
            j = pd.concat([s, SER[destino].precip], axis=1, keys=["red", "qc"]).loc["2016":"2018"].dropna()
            if len(j) > 300:
                iden = (abs(j.red - j.qc) < 0.05).mean()
                cociente = j.red.sum() / max(j.qc.sum(), 1e-6)
                r = j.red.corr(j.qc)
                if iden >= 0.85 and 0.9 <= cociente <= 1.1 and r >= 0.85:
                    ext = s.loc["2019":FIN].round(1)
                    if destino not in prolongadas:
                        SER[destino] = pd.concat([SER[destino].loc[:"2018"], ext.rename("precip").to_frame()])
                        est[destino]["fuente"] += f"; 2019–2024 observada, red {red_de.get(('pr', c), 'INAMHI')}" + ("" if destino == c else f" ({c})")
                        prolongadas.append(destino)
                    continue
            if c in SER:
                continue
        if meses_validos(s, True) >= 24:
            r = rm.loc[c]
            lat, lon, z, cor = corregir(c, float(r.lat), float(r.lon), r.elev)
            red = red_de.get(("pr", c), "red")
            est[c] = dict(codigo=c, estacion=str(r.estacion).replace("_", " ").title(), lat=lat, lon=lon,
                          altitud_m=z, red=red, corregida=cor, fuente=f"{red}: lluvia diaria observada", omm=pd.NA)
            SER[c] = pd.DataFrame({"precip": s.round(1)})
            nuevas_pr.append(c)
    print(f"Lluvia INAMHI prolongada a 2024: {len(prolongadas)} · estaciones nuevas de lluvia: {len(nuevas_pr)}")

    # ---------------------------------------------------------------- SYNOP (OGIMET)
    syn = {}
    sm = None
    S = {}
    for v in ("tmax", "tmin", "pr"):
        m, X = ancha(F / f"ogimet_{v}_diaria.csv", 7, "codigo_OMM")
        sm = m if sm is None else pd.concat([sm, m[~m.index.isin(sm.index)]])
        S[v] = X
    for o, r in sm.iterrows():
        w = f"W{o}"
        df = pd.DataFrame({k: S[v].get(o) for k, v in (("tmax", "tmax"), ("tmin", "tmin"), ("precip", "pr"))})
        df = df.dropna(how="all")
        lat, lon, z, cor = corregir(w, r.lat, r.lon, r.elev)
        syn[w] = dict(codigo=str(r.codigo_M), estacion=str(r.estacion), lat=lat, lon=lon, altitud_m=z, omm=int(o),
                      red="OGIMET (SYNOP)", corregida=cor, fuente="OGIMET (SYNOP)", df=df)

    # ---------------------------------------------------------------- temperatura de la red INAMHI (desde 2022)
    T = {}
    for v in ("tmax", "tmin"):
        m, X = ancha(F / f"redes_{v}_diaria.csv", 6, "codigo_M")
        T[v] = (m, X)
    tm = T["tmax"][0]
    nuevas_t = []
    for c in tm.index:
        tx, tn = T["tmax"][1].get(c), T["tmin"][1].get(c)
        add = pd.DataFrame({"tmax": tx, "tmin": tn}).dropna(how="all").round(1)
        if add.empty:
            continue
        if c in syn:                                     # completa días sin dato del SYNOP
            syn[c]["df"] = syn[c]["df"].combine_first(add).sort_index()
            syn[c]["fuente"] = "OGIMET (SYNOP) + red INAMHI (2022–2024)"
        elif c in SER:                                    # estación INAMHI con lluvia
            SER[c] = SER[c].join(add, how="outer")
            est[c]["fuente"] += "; Tmáx y Tmín observadas 2022–2024, red INAMHI"
        else:                                             # estación nueva
            r = tm.loc[c]
            lat, lon, z, cor = corregir(c, float(r.lat), float(r.lon), r.elev)
            syn[c] = dict(codigo=c, estacion=str(r.estacion).replace("_", " ").title(), lat=lat, lon=lon, altitud_m=z,
                          omm=int(c[1:]) if c.startswith("W") and c[1:].isdigit() else pd.NA, red="INAMHI",
                          corregida=cor, fuente="Red INAMHI (2022–2024)", df=add)
            nuevas_t.append(c)
    print(f"Estaciones nuevas con temperatura de la red INAMHI: {len(nuevas_t)} {nuevas_t}")

    # ---------------------------------------------------------------- HIDRONACIÓN: temperatura media
    hm, Hx = ancha(F / "redes_tmed_diaria.csv", 6, "codigo_M")
    for c in hm.index:
        r = hm.loc[c]
        lat, lon, z, cor = corregir(c, float(r.lat), float(r.lon), r.elev)
        df = pd.DataFrame({"tmed": Hx[c].round(1)}).dropna()
        syn[c] = dict(codigo=c, estacion=str(r.estacion).replace("_", " ").title(), lat=lat, lon=lon, altitud_m=z,
                      omm=pd.NA, red="HIDRONACIÓN", corregida=cor, fuente="HIDRONACIÓN: temperatura media", df=df)

    # ---------------------------------------------------------------- cruce temperatura + lluvia del INAMHI
    E = pd.DataFrame(est.values()).set_index("codigo")
    con_lluvia = E[[SER[c].precip.notna().sum() > 0 for c in E.index]]
    filas = []
    for w, s in syn.items():
        df = s.pop("df")
        if df.empty:
            continue
        if pd.isna(s["altitud_m"]):
            s["altitud_m"] = np.nan
        d = km(con_lluvia.lat.values, con_lluvia.lon.values, s["lat"], s["lon"])
        dz = (con_lluvia.altitud_m - s["altitud_m"]).abs().fillna(0).values if pd.notna(s["altitud_m"]) else np.zeros(len(d))
        ok = np.where((d <= 5.5) & (dz <= 100))[0]
        if len(ok):
            # entre las del mismo sitio (≤ 0,5 km) o, si no hay, entre todas: la serie más larga y, a igualdad, la más cercana
            largo = np.array([SER[con_lluvia.index[i]].precip.notna().sum() for i in ok])
            mismo = d[ok] <= 0.5            # en el mismo sitio manda el sitio; si no, la serie más larga
            sel = ok[mismo] if mismo.any() else ok
            largo = largo[mismo] if mismo.any() else largo
            k = sel[np.lexsort((d[sel], -largo))[0]]
            c = con_lluvia.index[k]
            pr_ = SER[c].precip
            df = df.drop(columns=[x for x in ("precip",) if x in df]).join(pr_.rename("precip"), how="outer")
            s["fuente"] += f" Tmáx/Tmín + lluvia {E.loc[c, 'fuente']}" if "tmed" not in df else f" + lluvia {E.loc[c, 'fuente']}"
            s["lluvia_de"] = c
            if str(s["codigo"]).startswith("W"):
                s["codigo"] = c
        s["df"] = df
        filas.append(s)

    # ---------------------------------------------------------------- escritura
    OUT.mkdir(parents=True, exist_ok=True)
    for sub in ("synop", "redes"):
        (OUT / sub).mkdir(exist_ok=True)
        for f in (OUT / sub).glob("*.csv"):
            f.unlink()
    indice = []

    def registrar(archivo, s, df, url):
        df = df.loc[:FIN].dropna(how="all")
        df = df[[c for c in COLS if c in df]]
        if df.empty:
            return
        mm = {v: (meses_validos(df[v], v == "precip") if v in df else 0) for v in ("tmax", "tmin", "tmed", "precip")}
        if max(mm.values()) < 12:
            return
        indice.append(dict(archivo=archivo, provincia=None, estacion=s["estacion"], omm=s.get("omm"), codigo=s["codigo"],
                           lat=round(s["lat"], 5), lon=round(s["lon"], 5), altitud_m=s["altitud_m"],
                           desde=str(df.index.min().date()), hasta=str(df.index.max().date()),
                           meses_tmax=mm["tmax"], meses_tmin=mm["tmin"], meses_tmed=mm["tmed"], meses_precip=mm["precip"],
                           fuente=s["fuente"], variables=",".join(df.columns), url=url,
                           coordenadas_corregidas=bool(s.get("corregida")), coordenadas_revisar=str(s["codigo"]) in pend))
        return df

    E["provincia"] = provincia_de(E.lat.values, E.lon.values, prov)
    usadas = {s.get("lluvia_de") for s in filas} | {s["codigo"] for s in filas}
    otras = E[(E.red != "INAMHI") & ~E.index.isin(usadas)]   # lluvia de otras redes sin estación de temperatura: van en main
    for c, s in otras.iterrows():
        filas.append(dict(s, codigo=c, df=SER[c]))
    for s in filas:
        df = s.pop("df")
        sub = "synop" if "SYNOP" in s["red"] else "redes"
        pv = s.get("provincia") if pd.notna(s.get("provincia")) else provincia_de([s["lat"]], [s["lon"]], prov)[0]
        if pd.isna(pv):
            continue
        ident = s["omm"] if pd.notna(s.get("omm")) else s["codigo"]
        nombre = f"{sub}/{slug(pv)}_{slug(s['estacion'])[:30]}_{slug(ident)}.csv"
        dfo = registrar(nombre, s, df, MAIN + nombre)
        if dfo is not None:
            dfo.to_csv(OUT / nombre, index_label="fecha", date_format="%Y-%m-%d")
    for nombre, red in (("manabi_manta_aeropuerto_semt_metar.csv", "METAR"), ("manabi_calceta_espam.csv", "ESPAM")):
        src = F / ("metar_semt.csv" if red == "METAR" else "calceta_espam.csv")
        df = pd.read_csv(src, parse_dates=["fecha"]).set_index("fecha")
        s = (dict(estacion="Manta Aeropuerto Eloy Alfaro (METAR)", codigo="SEMT", omm=84117, lat=-0.946, lon=-80.679, altitud_m=15,
                  fuente="OGIMET (METAR)") if red == "METAR" else
             dict(estacion="ESPAM MFL Calceta", codigo="ESPAM", omm=pd.NA, lat=-0.83, lon=-80.18, altitud_m=15,
                  fuente="Estación meteorológica ESPAM MFL (coordenadas aproximadas)"))
        if red == "METAR" and "M0074" in SER:
            df = df.drop(columns=[c for c in ("precip",) if c in df]).join(SER["M0074"].precip.rename("precip"), how="outer")
            s["fuente"] += f" + lluvia {E.loc['M0074', 'fuente']}"
        dfo = registrar(nombre, s, df, MAIN + nombre)
        dfo.to_csv(OUT / nombre, index_label="fecha", date_format="%Y-%m-%d")

    # INAMHI: un ZIP por provincia en la rama `estaciones`
    E = E[E.red == "INAMHI"]
    Z.mkdir(parents=True, exist_ok=True)
    for f in Z.glob("inamhi_precip_*.zip"):
        f.unlink()
    por_prov = {}
    for c, s in E.iterrows():
        if pd.isna(s.provincia):
            continue
        p = slug(s.provincia)
        nombre = f"inamhi/{p}/{slug(c)}.csv"
        dfo = registrar(nombre, dict(s, codigo=c), SER[c], RAMA + f"inamhi_precip_{p}.zip")
        if dfo is not None:
            por_prov.setdefault(p, []).append((f"{slug(c)}.csv", dfo.to_csv(index_label="fecha", date_format="%Y-%m-%d")))
    for p, archivos in por_prov.items():
        with zipfile.ZipFile(Z / f"inamhi_precip_{p}.zip", "w", zipfile.ZIP_DEFLATED) as zf:
            for n, txt in archivos:
                zf.writestr(n, txt)

    I = pd.DataFrame(indice)
    # altitud que falta: la del modelo digital de elevación en las coordenadas de la estación (altitud_dem.csv)
    I["altitud_fuente"] = np.where(I.altitud_m.notna(), "declarada", "")
    if (F / "altitud_dem.csv").exists():
        dem = pd.read_csv(F / "altitud_dem.csv")
        dlat = dem.clave.str.split(",").str[0].astype(float).values
        dlon = dem.clave.str.split(",").str[1].astype(float).values
        for i in I.index[I.altitud_m.isna()]:
            d = km(dlat, dlon, I.at[i, "lat"], I.at[i, "lon"])
            k = int(np.argmin(d))
            if d[k] <= 1:
                I.at[i, "altitud_m"] = float(dem.elev_dem.iloc[k])
                I.at[i, "altitud_fuente"] = "DEM"
    I["provincia"] = provincia_de(I.lat.values, I.lon.values, prov)
    I = I[I.provincia.notna()]
    I["omm"] = pd.to_numeric(I["omm"], errors="coerce").astype("Int64")
    I = I.sort_values(["provincia", "archivo"])
    I.to_csv(OUT / "indice_estaciones.csv", index=False)
    print(f"Índice: {len(I)} estaciones · {I.provincia.nunique()} provincias · "
          f"con temperatura ≥ 60 meses: {(I[['meses_tmax', 'meses_tmin', 'meses_tmed']].max(axis=1) >= 60).sum()} · "
          f"coordenadas corregidas: {I.coordenadas_corregidas.sum()} · por revisar: {I.coordenadas_revisar.sum()}")


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--fuentes", required=True)
    a.add_argument("--salida", default="datos/estaciones")
    a.add_argument("--zips", required=True)
    o = a.parse_args()
    main(o.fuentes, o.salida, o.zips)
