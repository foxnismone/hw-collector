# -*- coding: utf-8 -*-
"""
Motor de respuestas del asistente — corre sobre los datos locales, sin LLM.

Uso como biblioteca:
    from atender_cola import responder
    responder("cuánto vale el Skyline en pesos")

Uso como script (atiende la cola de preguntas del celular):
    python build/atender_cola.py            # procesa data/cola_agente.json
    python build/atender_cola.py --pregunta "qué trae la caja A de 2026"

Por qué existe: el puente del celular necesita responder al instante y sin
depender de un modelo de lenguaje ni de internet. Todo lo que responde sale de
los archivos de data/ con su fuente. Lo que no sabe responder queda EN COLA
para que lo conteste el agente.
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def load(nombre, default=None):
    p = os.path.join(DATA, nombre)
    if not os.path.exists(p):
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)


CAT = load("catalog_web.json", [])
CAJ = load("cajas.json", {})
TEND = load("tendencias.json", {})
MKT = load("mercados.json", {})
PRE = load("precios_referencia.json", {})
SEG = load("seguimiento.json", {})
OWN = load("owned_collection.json", {})
IDXI = load("indice.json", {})
IDX = {c["i"]: c for c in CAT}

MON = (MKT.get("monedas") or {})
CLP = (MON.get("CLP") or {}).get("por_usd", 981.61)


def sin_acentos(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def plata(usd: float, moneda: str = "CLP") -> str:
    m = MON.get(moneda) or {"simbolo": "$", "por_usd": 1, "decimales": 0}
    v = usd * m["por_usd"]
    if m.get("decimales", 0) == 0:
        return f"{m['simbolo']}{round(v):,.0f}".replace(",", ".")
    return f"{m['simbolo']}{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def base_nombre(m: str) -> str:
    m = re.sub(r"\s*\(\s*(2nd|3rd|4th)\s*Color[^)]*\)", "", m, flags=re.I)
    return re.sub(r"\s*\(\s*Zamac\s*\)", "", m, flags=re.I).strip()


def buscar(texto: str, max_n: int = 3):
    """Busca el auto más parecido en el catálogo por coincidencia de palabras."""
    q = sin_acentos(texto)
    stop = {"cuanto", "vale", "cuesta", "precio", "valor", "busca", "buscar", "dime", "sobre", "del", "los",
            "las", "una", "unos", "autos", "auto", "hot", "wheels", "tengo", "hay", "esta", "este", "para",
            "pesos", "dolares", "euros", "chile", "puedo", "vender", "cuantos", "que", "cual", "como", "mio",
            "coleccion", "indice", "caja", "cajas", "trae", "traen", "contiene", "tiene"}
    palabras = [p for p in re.split(r"[^a-z0-9']+", q) if len(p) > 2 and p not in stop]
    if not palabras:
        return []
    punt = {}
    for c in CAT:
        nombre = sin_acentos(c["m"])
        s = 0
        for p in palabras:
            if p in nombre:
                s += len(p) + (3 if nombre.startswith(p) else 0)
        if s:
            punt[c["i"]] = s
    orden = sorted(punt.items(), key=lambda x: -x[1])[:max_n]
    return [IDX[i] for i, _ in orden if punt[i] >= 4]


def ficha(c) -> str:
    cb = None
    for anio, lista in (CAJ.get("cajas_por_anio") or {}).items():
        for caja in lista:
            for t in ("TH", "STH"):
                if caja.get(t) and caja[t].get("catalogo_id") == c["i"]:
                    cb = (caja["letra"], anio, t)
    p = [f"**{c['m']}** ({c['y']}, nº {c['c']}, toy {c['t']})",
         f"Serie: {c['s']} · clase {c['k']}",
         f"Índice de coleccionabilidad: **{c['x']}/100** (percentil {c.get('px','?')} del catálogo)",
         f"Valor de referencia: **{plata(c['v'])} – {plata(c['V'])}** (US${c['v']:.2f}–{c['V']:.2f})"]
    if cb:
        p.append(f"Caja: **{cb[0]}** del {cb[1]} ({'Super Treasure Hunt' if cb[2]=='STH' else 'Treasure Hunt'})")
    if c.get("imr"):
        p.append("_Imagen: referencia del casting (no necesariamente del año/color exacto)._")
    return "\n".join(p)


def demanda_rank(c):
    for mes in ("enero_2026", "febrero_2026"):
        for d in (TEND.get("demanda_coleccionistas") or {}).get(mes, []):
            if c["i"] in (d.get("catalogo_ids") or []):
                return f"#{d['rank']} de demanda real en {mes.replace('_',' ')} ({d['coleccionistas']} coleccionistas, HW Price Guide)"
    return None


def responder(texto: str):
    """Devuelve (respuesta, intencion) o (None, None) si no sabe."""
    t = sin_acentos(texto)
    fuente_general = "Fuente: catálogo Hot Wheels Wiki (2.177 registros 2016-2026) + data/"

    # --- caja de un año ---
    m = re.search(r"caja\s*([a-q])\b", t)
    if m and re.search(r"trae|contiene|sale|hay|tiene|viene|que", t):
        letra = m.group(1).upper()
        anios = re.findall(r"20\d\d", t)
        anio = anios[0] if anios else "2026"
        caja = next((c for c in (CAJ.get("cajas_por_anio") or {}).get(anio, []) if c["letra"] == letra), None)
        if caja:
            th = caja.get("TH")
            sth = caja.get("STH")
            p = [f"**Caja {letra} de {anio}**"]
            p.append(f"- Treasure Hunt: **{th['modelo']}** ({th['serie']} · {th['col']})" if th
                     else "- Treasure Hunt: sin dato publicado para ese año")
            p.append(f"- Super Treasure Hunt: **{sth['modelo']}** ({sth['serie']} · {sth['col']} · {sth.get('color','')})" if sth
                     else "- Super Treasure Hunt: sin dato")
            p.append("Cada caja trae ~72 autos con duplicados y **una sola TH**.")
            return "\n".join(p), "caja"
        return f"No tengo datos de la caja {letra} para {anio}. Letras publicadas: A B C D E F G H J K L M N P Q.", "caja"

    # --- código de base ---
    m = re.search(r"\b([a-z])\s*-?\s*(\d{1,2})\b", t)
    if m and re.search(r"codigo|base|fabricad|significa|anio", t):
        tabla = (CAJ.get("codigos_base") or {}).get("letra_a_anio", {})
        anio = tabla.get(m.group(1).upper())
        sem = int(m.group(2))
        if anio and 1 <= sem <= 53:
            return (f"El código **{m.group(1).upper()}{sem}** indica fabricación en **{anio}**, semana **{sem}** "
                    f"(≈ {date(anio,1,1).isoformat()}).\n_Fuente: Hot Wheels Wiki — Base codes._"), "codigo"

    # --- impuestos / importación ---
    if re.search(r"impuesto|aduana|importar|arancel|traer de", t):
        cl = next((m_ for m_ in MKT.get("mercados", []) if m_["id"] == "CL"), {}).get("importacion", {})
        return (f"**Traer autos a Chile:** hasta US$500 pagás **solo IVA 19%** (sin arancel). "
                f"Sobre US$500: **6% de arancel + 19% de IVA** sobre el CIF. "
                f"Envíos **entre personas (C2C)** de hasta US$500 son **exentos** si son ocasionales y no comerciales.\n"
                f"En la UE, desde el 1-jul-2026 hay un **arancel fijo de €3 por ítem** en envíos de hasta €150, más IVA.\n"
                f"_Fuente: {cl.get('fuente','aduana.cl / sii.cl')}._"), "impuestos"

    # --- dónde vender / mejor canal ---
    if re.search(r"donde vendo|mejor mercado|donde vender|conviene vender|que canal|vender", t):
        canales = sorted(MKT.get("calculadora_canales", []), key=lambda c: -(1 - c["pct"] - c["fijo_usd"] / 50))[:4]
        p = ["**Mejores canales (para una pieza de US$50):**"]
        for c in canales:
            neto = 50 - (50 * c["pct"] + c["fijo_usd"])
            p.append(f"- {c['canal']}: comisión {c['pct']*100:.1f}% → neto **{plata(neto)}**")
        p.append("Los autos de menos de US$10 conviene venderlos **en lote**; más de US$20, individuales.")
        p.append("_Fuente: comisiones oficiales en data/mercados.json._")
        return "\n".join(p), "venta"

    # --- mi colección ---
    if re.search(r"cuantos tengo|mi coleccion|valor de mi coleccion|cuanto vale mi", t):
        items = OWN.get("items", [])
        unidades = sum(i.get("cantidad", 0) for i in items)
        tot_min = tot_max = 0.0
        for i in items:
            c = IDX.get(i["catalog_id"])
            if not c:
                continue
            k = {"carded-nuevo": 1.0, "carded-dañado": .7, "loose-mint": .55, "loose-bueno": .4, "loose-jugado": .25}.get(i.get("condicion"), 1.0)
            tot_min += c["v"] * k * i["cantidad"]
            tot_max += c["V"] * k * i["cantidad"]
        return (f"Tu colección tiene **{unidades} autos** en {len(items)} modelos distintos "
                f"(cargada en data/owned_collection.json — hoy con datos de ejemplo).\n"
                f"Valor de referencia: **{plata(tot_min)} – {plata(tot_max)}** (US${tot_min:.2f}–{tot_max:.2f}) pieza por pieza. "
                f"En lote completo aplicá 50–70% de descuento."), "coleccion"

    # --- comparación de mercados ---
    if re.search(r"mercado|comparacion|precio en chile|chile vs|europa|estados unidos", t) and not buscar(texto):
        return ("**Comparación de mercados (mainline):**\n"
                f"- EE.UU.: US$1,25 retail · US$1–5 reventa\n"
                f"- Chile: $1.990–$2.450 retail (littletoys.cl, isatoyschile.cl) → **1,6–2× sobre EE.UU.**\n"
                f"- Europa: €2–3 retail\n"
                f"- Reino Unido: los **lotes** se pagan mejor por unidad (£1,19–£1,70 por auto)\n"
                f"Tipo de cambio cargado: 1 USD = ${CLP:,.0f} CLP (mindicador.cl, dólar observado).".replace(",", ".")), "mercados"

    # --- top de demanda ---
    if re.search(r"mas coleccionado|top de demanda|top demanda|trending|mas buscado|ranking|demanda", t):
        d = (TEND.get("demanda_coleccionistas") or {}).get("febrero_2026", [])[:5]
        p = ["**Top 5 de demanda real de coleccionistas (febrero 2026, HW Price Guide):**"]
        p += [f"{x['rank']}. {x['modelo']} — {x['coleccionistas']} coleccionistas" for x in d]
        p.append("_Mide demanda de colección, no precio de mercado secundario._")
        return "\n".join(p), "demanda"

    # --- ficha / valor de un modelo ---
    cs = buscar(texto)
    if cs:
        c = cs[0]
        extra = ""
        if re.search(r"peso|chil|clp", t):
            extra = f"\nEn pesos chilenos: **{plata(c['v'])} – {plata(c['V'])}** (1 USD = ${CLP:,.0f}).".replace(",", ".")
        if re.search(r"euro|eur", t):
            extra = f"\nEn euros: **{plata(c['v'],'EUR')} – {plata(c['V'],'EUR')}**."
        r = ficha(c) + extra
        dr = demanda_rank(c)
        if dr:
            r += f"\nDemanda: {dr}"
        otros = [x["m"] for x in cs[1:]]
        if otros:
            r += f"\n_Otros parecidos: {', '.join(otros)}_"
        r += f"\n{fuente_general}"
        return r, "ficha"

    # --- índice ---
    if re.search(r"indice|coleccionabilidad", t):
        e = IDXI.get("estadisticas_catalogo", {})
        return (f"**Índice de coleccionabilidad** = 0,30·R + 0,25·D + 0,20·C + 0,15·A + 0,10·M.\n"
                f"D (demanda) y M (mercado) usan datos reales (HW Price Guide ene/feb 2026); "
                f"cuando no hay medición, la ficha lo marca como proxi.\n"
                f"Catálogo: mediana **{e.get('mediana')}**, p90 {e.get('p90')}, máximo {e.get('max')}."), "indice"

    return None, None


# ---------------------------------------------------------------- cola

def procesar_cola(cola_path=None, resp_path=None, verbose=True):
    cola_path = cola_path or os.path.join(DATA, "cola_agente.json")
    resp_path = resp_path or os.path.join(DATA, "respuestas_agente.json")
    cola = load("cola_agente.json", []) or []
    respuestas = load("respuestas_agente.json", []) or []
    ya = {r["id"] for r in respuestas}
    atendidas = 0
    for item in cola:
        if item["id"] in ya:
            continue
        r, intencion = responder(item.get("pregunta", ""))
        if r:
            respuestas.append({"id": item["id"], "pregunta": item["pregunta"], "respuesta": r,
                               "intencion": intencion, "fecha": date.today().isoformat(), "origen": "motor local"})
            atendidas += 1
    with open(resp_path, "w", encoding="utf-8") as f:
        json.dump(respuestas, f, ensure_ascii=False, indent=1)
    pendientes = [c for c in cola if c["id"] not in {r["id"] for r in respuestas}]
    if verbose:
        print(f"atendidas: {atendidas} | pendientes para el agente: {len(pendientes)}")
        for p in pendientes:
            print(f"   · {p['pregunta']}")
    return atendidas, pendientes


if __name__ == "__main__":
    if "--pregunta" in sys.argv:
        q = sys.argv[sys.argv.index("--pregunta") + 1]
        r, i = responder(q)
        print(r if r else "(el motor local no supo responder: quedaría en cola para el agente)")
    else:
        procesar_cola()
