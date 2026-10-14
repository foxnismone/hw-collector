# -*- coding: utf-8 -*-
"""
Motor de actualización de mercado, seguimiento y alertas de HW Collector.

Modos
-----
  python build/refresh_market.py --evaluate   # sin internet: recalcula frescura y alertas
  python build/refresh_market.py --api        # usa las APIs oficiales (requiere config.json)
  python build/refresh_market.py --browser    # colector con navegador real (requiere playwright)
  python build/refresh_market.py --all        # api + evaluate

Por qué hay dos modos online
----------------------------
MercadoLibre y eBay bloquean el acceso automatizado sin credenciales:
  * La API pública de MercadoLibre exige un token de aplicación (gratis):
    https://developers.mercadolibre.cl  → crear app → access_token
  * La API Browse de eBay exige App ID (gratis):
    https://developer.ebay.com  → crear app → Client ID / Client Secret
  * Las páginas de búsqueda de ambos bloquean bots desde IP de datacenter,
    pero responden bien desde una IP residencial con un navegador real
    (modo --browser, con Playwright). Esa es la vía sin credenciales.
  * Facebook Marketplace y TikTok no ofrecen API pública de búsqueda de
    productos: se cargan a mano desde la app.

Config (config.json, en la raíz del proyecto — NO subir a git)
-------------------------------------------------------------
{
  "mercadolibre": {"access_token": "APP_USR-..."},
  "ebay": {"client_id": "...", "client_secret": "...", "marketplace": "EBAY_US"},
  "queries": ["hot wheels super treasure hunt", "hot wheels premium car culture", "hot wheels 2026"]
}
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
import urllib.parse
import urllib.request
from datetime import datetime, date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
HOY = date.today().isoformat()


def load(name, default=None):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save(name, obj):
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def cfg():
    p = os.path.join(ROOT, "config.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}


def http_json(url, headers=None, timeout=25):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


# ---------------------------------------------------------------- proveedores

def ml_search(query, token, site="MLC", limit=50):
    """MercadoLibre: precio de listado + sold_quantity. Requiere token de app."""
    u = (f"https://api.mercadolibre.com/sites/{site}/search?"
         + urllib.parse.urlencode({"q": query, "limit": limit}))
    d = http_json(u, {"Authorization": f"Bearer {token}", "Accept": "application/json"})
    out = []
    for it in d.get("results", []):
        out.append({"titulo": it.get("title"), "precio": it.get("price"),
                    "moneda": it.get("currency_id"), "vendidos": it.get("sold_quantity"),
                    "condicion": it.get("condition"), "link": it.get("permalink")})
    return out


def ebay_search(query, client_id, client_secret, marketplace="EBAY_US", limit=50):
    """eBay Browse API: SOLO listados activos (las ventas cerradas se cerraron en feb-2025)."""
    tok = http_json  # noqa: F841  (referencia para legibilidad)
    import base64
    cred = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    req = urllib.request.Request(
        "https://api.ebay.com/identity/v1/oauth2/token",
        data=urllib.parse.urlencode({"grant_type": "client_credentials", "scope": "https://api.ebay.com/oauth/api_scope"}).encode(),
        headers={"Authorization": f"Basic {cred}", "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=25) as r:
        token = json.loads(r.read().decode())["access_token"]
    u = ("https://api.ebay.com/buy/browse/v1/item_summary/search?"
         + urllib.parse.urlencode({"q": query, "limit": limit}))
    d = http_json(u, {"Authorization": f"Bearer {token}",
                      "X-EBAY-C-MARKETPLACE-ID": marketplace, "Accept": "application/json"})
    out = []
    for it in d.get("itemSummaries", []):
        pr = it.get("price") or {}
        out.append({"titulo": it.get("title"), "precio": float(pr.get("value", 0) or 0),
                    "moneda": pr.get("currency"), "condicion": it.get("condition"),
                    "link": it.get("itemWebUrl")})
    return out


def browser_collect(queries, sites=("mercadolibre", "ebay")):
    """Colector con navegador real. Requiere: pip install playwright && playwright install chromium."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [!] Playwright no está instalado:  pip install playwright && playwright install chromium")
        return {}
    res = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        ctx = b.new_context(locale="es-CL", user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"))
        page = ctx.new_page()
        for q in queries:
            if "mercadolibre" in sites:
                try:
                    page.goto("https://listado.mercadolibre.cl/" + urllib.parse.quote(q.replace(" ", "-")),
                              wait_until="domcontentloaded", timeout=45000)
                    page.wait_for_timeout(3500)
                    rows = page.eval_on_selector_all(
                        "li.ui-search-layout__item, .poly-card",
                        """els => els.map(e => {
                             const t = e.querySelector('.poly-component__title, .ui-search-item__title, h2');
                             const p = e.querySelector('.andes-money-amount__fraction, .price-tag-fraction');
                             const s = e.innerText.match(/(\\d[\\d.]*)\\s*vendidos?/i);
                             return {titulo: t ? t.innerText.trim() : null,
                                     precio: p ? parseInt(p.innerText.replace(/\\./g,''),10) : null,
                                     vendidos: s ? parseInt(s[1].replace(/\\./g,''),10) : null};
                           })""")
                    res.setdefault("mercadolibre", {})[q] = [r for r in rows if r.get("titulo")][:50]
                    print(f"  ML Chile  '{q}': {len(res['mercadolibre'][q])} listados")
                except Exception as e:
                    print(f"  ML Chile  '{q}': ERROR {e}")
            if "ebay" in sites:
                try:
                    page.goto("https://www.ebay.com/sch/i.html?_nkw=" + urllib.parse.quote(q),
                              wait_until="domcontentloaded", timeout=45000)
                    page.wait_for_timeout(3000)
                    rows = page.eval_on_selector_all(
                        "li.s-item, li.s-card",
                        """els => els.map(e => {
                             const t = e.querySelector('.s-item__title, .s-card__title');
                             const p = e.querySelector('.s-item__price, .s-card__price');
                             const sold = e.querySelector('.s-item__quantitySold, .s-card__quantitySold');
                             return {titulo: t ? t.innerText.trim() : null,
                                     precio_txt: p ? p.innerText.trim() : null,
                                     vendidos_txt: sold ? sold.innerText.trim() : null};
                           })""")
                    res.setdefault("ebay", {})[q] = [r for r in rows if r.get("titulo")][:50]
                    print(f"  eBay      '{q}': {len(res['ebay'][q])} listados")
                except Exception as e:
                    print(f"  eBay      '{q}': ERROR {e}")
        b.close()
    return res


# ---------------------------------------------------------------- agregación

def precio_a_usd(txt, clp=981.61):
    if not txt:
        return None
    n = re.sub(r"[^\d.,]", "", txt)
    if not n:
        return None
    if "," in n and "." in n:
        n = n.replace(".", "").replace(",", ".")
    elif n.count(",") == 1 and len(n.split(",")[-1]) == 2:
        n = n.replace(",", ".")
    else:
        n = n.replace(",", "").replace(".", "")
    try:
        v = float(n)
    except ValueError:
        return None
    return round(v / clp, 2) if "CLP" in (txt or "").upper() or v > 500 else v


def agregar(rows):
    """Mediana, percentiles y cantidad de muestras de una lista de precios."""
    precios = sorted(r["precio"] for r in rows if r.get("precio"))
    if not precios:
        return None
    def pct(p):
        if len(precios) == 1:
            return precios[0]
        k = (len(precios) - 1) * p
        lo, hi = int(k), min(int(k) + 1, len(precios) - 1)
        return round(precios[lo] + (precios[hi] - precios[lo]) * (k - lo), 2)
    return {"n": len(precios), "min": precios[0], "p25": pct(.25), "mediana": pct(.5),
            "p75": pct(.75), "max": precios[-1],
            "vendidos_total": sum(r.get("vendidos") or 0 for r in rows),
            "confianza": "alta" if len(precios) >= 10 else "media" if len(precios) >= 5 else "baja"}


# ---------------------------------------------------------------- alertas

def evaluar_alertas(seg, tend):
    """Recalcula frescura y genera alertas por item. Sin internet."""
    fre = seg["meta"].get("frescura_dias", {"fresco": 7, "aceptable": 30})
    alertas = []
    for cid, it in seg["items"].items():
        try:
            dias = (date.fromisoformat(HOY) - date.fromisoformat(it["fecha_actualizacion"])).days
        except Exception:
            dias = 999
        it["frescura"] = "fresco" if dias <= fre["fresco"] else ("aceptable" if dias <= fre["aceptable"] else "viejo")
        if it["frescura"] == "viejo":
            alertas.append({"id": cid, "tipo": "DATOS", "severidad": "media",
                            "mensaje": f"{it['modelo']}: datos de hace {dias} días. Actualizá para no vender a ciegas.",
                            "accion": "Actualizar"})
        va, vant = it.get("valor_actual_usd"), it.get("valor_anterior_usd")
        obj = (it.get("alertas") or {}).get("precio_objetivo_usd")
        cpct = (it.get("alertas") or {}).get("cambio_pct") or 20
        if obj and va and va >= obj:
            alertas.append({"id": cid, "tipo": "VENTA", "severidad": "alta",
                            "mensaje": f"{it['modelo']}: llegó a US${va:.2f} y tu objetivo era US${obj:.2f}. Buen momento para publicar.",
                            "accion": "Publicar en " + ((it.get("alertas") or {}).get("canal_preferido") or "MercadoLibre Chile")})
        if va and vant:
            chg = (va - vant) / vant * 100
            if chg >= cpct:
                alertas.append({"id": cid, "tipo": "SUBE", "severidad": "media",
                                "mensaje": f"{it['modelo']}: subió {chg:.0f}% (US${vant:.2f} → US${va:.2f}).",
                                "accion": "Revisar precio"})
            elif chg <= -cpct:
                alertas.append({"id": cid, "tipo": "COMPRA", "severidad": "media",
                                "mensaje": f"{it['modelo']}: bajó {abs(chg):.0f}%. Oportunidad para completar la serie.",
                                "accion": "Buscar compra"})
        if it.get("confianza") == "baja":
            alertas.append({"id": cid, "tipo": "DATOS", "severidad": "baja",
                            "mensaje": f"{it['modelo']}: valor por clase (confianza baja), no comparable del modelo exacto.",
                            "accion": "Cargar comparables"})
        rank = (it.get("senales") or {}).get("demanda_coleccionistas_rank")
        if rank and rank <= 10:
            alertas.append({"id": cid, "tipo": "DEMANDA", "severidad": "alta",
                            "mensaje": f"{it['modelo']}: está en el top {rank} de demanda de coleccionistas (HW Price Guide).",
                            "accion": "Priorizar venta individual"})
    return alertas


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Actualización de mercado, seguimiento y alertas")
    ap.add_argument("--evaluate", action="store_true", help="solo recalcula frescura y alertas (sin internet)")
    ap.add_argument("--api", action="store_true", help="usa las APIs oficiales (config.json)")
    ap.add_argument("--browser", action="store_true", help="colector con navegador (playwright)")
    ap.add_argument("--all", action="store_true", help="api + evaluate")
    a = ap.parse_args()
    if not any([a.evaluate, a.api, a.browser, a.all]):
        ap.print_help()
        return 1

    seg = load("seguimiento.json")
    tend = load("tendencias.json")
    if seg is None:
        print("Falta data/seguimiento.json"); return 1

    if a.api or a.browser:
        c = cfg()
        queries = c.get("queries") or ["hot wheels super treasure hunt", "hot wheels premium car culture"]
        obs = {}
        if a.api:
            ml = (c.get("mercadolibre") or {}).get("access_token")
            eb = c.get("ebay") or {}
            if not ml and not eb.get("client_id"):
                print("Sin credenciales en config.json.\n"
                      "  · MercadoLibre: https://developers.mercadolibre.cl (token gratuito)\n"
                      "  · eBay: https://developer.ebay.com (App ID gratuito)\n"
                      "  Alternativa sin credenciales:  python build/refresh_market.py --browser")
            for q in queries:
                if ml:
                    try:
                        rows = ml_search(q, ml)
                        agg = agregar([{"precio": r["precio"], "vendidos": r.get("vendidos")} for r in rows])
                        obs.setdefault("mercadolibre_cl", {})[q] = {"agregado": agg, "muestras": rows[:20]}
                        print(f"ML Chile '{q}': {agg['n'] if agg else 0} precios, mediana "
                              f"{agg['mediana'] if agg else '-'} CLP")
                    except Exception as e:
                        print(f"ML Chile '{q}': ERROR {e}")
                if eb.get("client_id"):
                    try:
                        rows = ebay_search(q, eb["client_id"], eb["client_secret"])
                        agg = agregar(rows)
                        obs.setdefault("ebay", {})[q] = {"agregado": agg, "muestras": rows[:20]}
                        print(f"eBay '{q}': {agg['n'] if agg else 0} precios, mediana {agg['mediana'] if agg else '-'} USD")
                    except Exception as e:
                        print(f"eBay '{q}': ERROR {e}")
        if a.browser:
            obs.update(browser_collect(queries))
        if obs:
            tend["observaciones_ultima_corrida"] = {"fecha": HOY, "datos": obs}
            tend["meta"]["generado"] = HOY
            save("tendencias.json", tend)
            print(f"→ data/tendencias.json actualizado ({HOY})")

    alertas = evaluar_alertas(seg, tend)
    seg["meta"]["actualizado"] = HOY
    save("seguimiento.json", seg)
    save("alertas.json", {"generado": HOY, "total": len(alertas),
                          "por_tipo": {t: sum(1 for x in alertas if x["tipo"] == t)
                                       for t in sorted({x["tipo"] for x in alertas})},
                          "alertas": alertas})
    print(f"→ data/seguimiento.json y data/alertas.json actualizados · {len(alertas)} alertas "
          f"({', '.join(sorted({x['tipo'] for x in alertas})) or 'ninguna'})")
    for x in sorted(alertas, key=lambda z: {"alta": 0, "media": 1, "baja": 2}[z["severidad"]])[:8]:
        print(f"   [{x['severidad']:5}] {x['tipo']:7} {x['mensaje']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
