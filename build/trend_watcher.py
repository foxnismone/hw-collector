# -*- coding: utf-8 -*-
"""
Trend Watcher — herramienta especializada en análisis de tendencias activas de Hot Wheels.

Recolecta datos de múltiples fuentes, calcula un índice de tendencia compuesto (0-100),
detecta momentum y genera alertas cuando un modelo de tu colección está subiendo.

Fuentes:
  • Google Trends (pytrends)  → interés relativo 0-100, series temporales
  • Reddit RSS (r/HotWheels)  → menciones de modelos en la comunidad
  • Datos internos             → demanda de coleccionistas, precios de referencia
  • Mercado Libre / eBay      → scraping con navegador (opcional, vía --browser)

Uso:
  python build/trend_watcher.py              # recolección + análisis + alertas
  python build/trend_watcher.py --alertas    # solo mostrar alertas
  python build/trend_watcher.py --sync       # integrar al puente (data/tendencias_activas.json)
  python build/trend_watcher.py --browser    # incluir fuentes con navegador (playwright)
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def load_json(name, default=None):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_json(name, obj):
    p = os.path.join(DATA, name)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)


def get_catalog():
    return load_json("catalog_web.json", [])


def get_tendencias():
    return load_json("tendencias.json", {})


def get_owned():
    return load_json("owned_collection.json", {})


def normalizar_nombre(nombre):
    """Normaliza un nombre para comparar (sin acentos, minúsinas)."""
    nombre = nombre.lower()
    nombre = re.sub(r"[^a-z0-9\s]", "", nombre)
    nombre = re.sub(r"\s+", " ", nombre).strip()
    return nombre


# ──────────────────────────────────────────────────────────────────────────────
# 1. GOOGLE TRENDS (pytrends)
# ──────────────────────────────────────────────────────────────────────────────

def fetch_google_trends(termos, timeframe="today 3-m", batch_size=3):
    """Obtiene series de interés de Google Trends para una lista de términos.

    • Elimina duplicados (el mismo modelo aparece varios años).
    • Batches chicos + pausas largas para no chocar con 429.
    Returns: dict {termino: {"max": float, "ultimo": float, "momentum": float}}
    """
    try:
        from pytrends.request import TrendReq
    except ImportError:
        return {}

    # Limpiar y DEDUPLICAR (clave: pytrends falla si un término se repite)
    vistos = set()
    terminos_limpios = []
    for t in termos:
        t_limpio = re.sub(r"[^a-zA-Z0-9\s\-/]", "", t).strip().lower()
        t_limpio = re.sub(r"\s+", " ", t_limpio)
        if len(t_limpio) >= 3 and len(t_limpio) <= 50 and t_limpio not in vistos:
            vistos.add(t_limpio)
            terminos_limpios.append(t_limpio)

    resultado = {}
    for i in range(0, len(terminos_limpios), batch_size):
        batch = terminos_limpios[i:i + batch_size]
        for intento in range(3):
            try:
                pytrends = TrendReq(hl="es-419", tz=-180, timeout=(20, 35))
                pytrends.build_payload(batch, cat=0, timeframe=timeframe, geo="", gprop="")
                df = pytrends.interest_over_time()
                if not df.empty:
                    for term in batch:
                        if term in df.columns:
                            serie = df[term].dropna()
                            if len(serie) >= 2:
                                maximo = float(serie.max())
                                ultimo = float(serie.iloc[-1])
                                anteriores = serie.iloc[:-1]
                                media = float(anteriores.mean()) if len(anteriores) else 0
                                momentum = round(((ultimo - media) / media) * 100, 1) if media > 0 else 0.0
                                resultado[term] = {"max": round(maximo, 1), "ultimo": round(ultimo, 1),
                                                    "momentum": momentum, "puntos": len(serie)}
                break
            except Exception as e:
                if "429" in str(e) or "TooManyRequests" in str(e):
                    # Rate limit: espera más
                    espera = 30 * (intento + 1)
                    print(f"  [trends] 429 → esperando {espera}s...")
                    time.sleep(espera)
                elif intento < 2:
                    time.sleep(15 * (intento + 1))
                else:
                    print(f"  [trends] batch {i//batch_size+1} falló: {str(e)[:70]}")
        time.sleep(12)  # Pausa generosa entre batches
    return resultado


# ──────────────────────────────────────────────────────────────────────────────
# 2. REDDIT RSS (r/HotWheels)
# ──────────────────────────────────────────────────────────────────────────────

def _extraer_variantes(nombre_norm):
    """Genera variantes de búsqueda de un nombre de modelo.

    Ej: "'59 chevrolet impala" → ["'59 chevrolet impala", "chevrolet impala", "impala"]
    """
    variantes = [nombre_norm]
    # Sin año al inicio ('59, 1967, etc.)
    sin_anio = re.sub(r"^['\"]?\d{2,4}\s+", "", nombre_norm)
    if sin_anio != nombre_norm:
        variantes.append(sin_anio)
    # Últimas 2 palabras (modelo propiamente dicho)
    palabras = sin_anio.split()
    if len(palabras) >= 2:
        variantes.append(" ".join(palabras[-2:]))
    # Última palabra si es distintiva (4+ chars)
    if palabras and len(palabras[-1]) >= 4:
        variantes.append(palabras[-1])
    # Deduplicar manteniendo orden
    vistas = set()
    unicas = []
    for v in variantes:
        if v not in vistas and len(v) >= 3:
            vistas.add(v)
            unicas.append(v)
    return unicas


def fetch_reddit_mentions(modelos, subreddit="HotWheels", limite=100):
    """Obtiene menciones de modelos en Reddit RSS con matching inteligente.

    Usa variantes del nombre (sin año, últimas palabras) para encontrar menciones
    aunque el título no tenga el nombre completo.

    Returns: dict {modelo_normalizado: {"menciones": int, "titulos": [str]}}
    """
    url = f"https://www.reddit.com/r/{subreddit}/new/.rss?limit={limite}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [reddit] falló: {e}")
        return {}

    # Extraer títulos del RSS
    entradas = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)
    titulos = []
    for entrada in entradas:
        m = re.search(r"<title>(.*?)</title>", entrada, re.DOTALL)
        if m:
            titulo = m.group(1)
            titulo = titulo.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').strip()
            if titulo and len(titulo) > 5:
                titulos.append(titulo)

    print(f"      → {len(titulos)} posts encontrados en RSS")

    # Pre-computar variantes para cada modelo
    modelos_con_variantes = []
    for modelo, nombre_norm in modelos:
        variantes = _extraer_variantes(nombre_norm)
        modelos_con_variantes.append((modelo, nombre_norm, variantes))

    # Contar menciones por modelo
    menciones = defaultdict(lambda: {"menciones": 0, "titulos": []})
    for titulo in titulos:
        titulo_lower = titulo.lower()
        for modelo, nombre_norm, variantes in modelos_con_variantes:
            # Probar variantes de más específica a menos específica
            for variante in variantes:
                if variante in titulo_lower:
                    menciones[nombre_norm]["menciones"] += 1
                    if len(menciones[nombre_norm]["titulos"]) < 3:
                        menciones[nombre_norm]["titulos"].append(titulo)
                    break  # Un título cuenta una sola vez
            else:
                continue
            break  # Ya encontró match para este título

    return dict(menciones)


# ──────────────────────────────────────────────────────────────────────────────
# 3. ANÁLISIS DE TENDENCIAS
# ──────────────────────────────────────────────────────────────────────────────

def calcular_indice_tendencia(google, reddit, demanda_interna=None):
    """Calcula un índice de tendencia compuesto (0-100) por modelo.

    Componentes:
      • Google Trends (40%): interés relativo normalizado
      • Reddit (30%): menciones normalizadas
      • Demanda interna (30%): coleccionistas (si hay datos)
    """
    # Normalizar Google Trends
    google_norm = {}
    if google:
        max_valor = max(v["max"] for v in google.values()) if google else 1
        for term, datos in google.items():
            google_norm[term] = (datos["max"] / max_valor * 100) if max_valor > 0 else 0

    # Normalizar Reddit
    reddit_norm = {}
    if reddit:
        max_menc = max(v["menciones"] for v in reddit.values()) if reddit else 1
        for modelo, datos in reddit.items():
            reddit_norm[modelo] = (datos["menciones"] / max_menc * 100) if max_menc > 0 else 0

    # Demanda interna
    demanda_norm = {}
    if demanda_interna:
        max_dem = max(demanda_interna.values()) if demanda_interna else 1
        for modelo, valor in demanda_interna.items():
            demanda_norm[modelo] = (valor / max_dem * 100) if max_dem > 0 else 0

    # Combinar
    todos_modelos = set(google_norm.keys()) | set(reddit_norm.keys()) | set(demanda_norm.keys())
    indice = {}
    for modelo in todos_modelos:
        g = google_norm.get(modelo, 0)
        r = reddit_norm.get(modelo, 0)
        d = demanda_norm.get(modelo, 0)
        # Pesos
        peso_g = 0.4 if google_norm else 0
        peso_r = 0.3 if reddit_norm else 0
        peso_d = 0.3 if demanda_norm else 0
        total_peso = peso_g + peso_r + peso_d
        if total_peso == 0:
            continue
        indice[modelo] = round((g * peso_g + r * peso_r + d * peso_d) / total_peso, 1)

    return indice


def detectar_momentum(google, reddit, indice_anterior=None):
    """Detecta momentum: qué modelos están subiendo respecto a la medición anterior."""
    momentum = {}
    for modelo, datos in google.items():
        mom = datos.get("momentum", 0)
        if mom != 0:
            momentum[modelo] = mom
    for modelo, datos in reddit.items():
        menc = datos.get("menciones", 0)
        if menc > 0:
            momentum[modelo] = momentum.get(modelo, 0) + menc * 5  # Ponderar menciones
    return momentum


def generar_alertas(indice, momentum, owned, umbral_indice=60, umbral_momentum=50):
    """Genera alertas para modelos de la colección que están subiendo."""
    owned_items = owned.get("items", []) if owned else []
    owned_ids = {item.get("catalog_id") for item in owned_items}
    catalogo = get_catalog()
    owned_models = [c for c in catalogo if c["i"] in owned_ids]

    alertas = []
    for c in owned_models:
        nombre_norm = normalizar_nombre(c["m"])
        # Buscar en el índice
        idx = None
        for modelo, val in indice.items():
            if nombre_norm in modelo or modelo in nombre_norm:
                idx = val
                break
        if idx is None:
            continue
        mom = 0
        for modelo, val in momentum.items():
            if nombre_norm in modelo or modelo in nombre_norm:
                mom = val
                break
        if idx >= umbral_indice or mom >= umbral_momentum:
            alertas.append({
                "modelo": c["m"],
                "indice_tendencia": idx,
                "momentum": mom,
                "nivel": "alta" if idx >= 75 or mom >= 80 else "media",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
    return sorted(alertas, key=lambda a: a["indice_tendencia"], reverse=True)


# ──────────────────────────────────────────────────────────────────────────────
# 4. SCRAPING CON NAVEGADOR (Mercado Libre, eBay)
# ──────────────────────────────────────────────────────────────────────────────

def fetch_with_browser(url, wait_for=None, timeout=30):
    """Scraping con navegador headless (playwright) para sitios que bloquean curl."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [browser] playwright no instalado. Ejecutá: pip install playwright && playwright install chromium")
        return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent=UA)
            page.goto(url, timeout=timeout * 1000, wait_until="networkidle")
            if wait_for:
                page.wait_for_selector(wait_for, timeout=timeout * 1000)
            html = page.content()
            browser.close()
            return html
    except Exception as e:
        print(f"  [browser] falló: {e}")
        return None


def parse_mercadolibre(html):
    """Parsea resultados de búsqueda de Mercado Libre."""
    if not html:
        return []
    # Buscar patrones de precio en el HTML
    resultados = []
    # ML usa JSON embebido en el HTML (.__NEXT_DATA__)
    import re
    json_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            items = data.get("props", {}).get("pageProps", {}).get("results", [])
            for item in items[:20]:
                resultados.append({
                    "titulo": item.get("title", ""),
                    "precio": item.get("price", {}).get("amount", 0),
                    "moneda": item.get("price", {}).get("currency", "CLP"),
                    "url": item.get("permalink", ""),
                    "imagen": item.get("thumbnail", ""),
                })
        except (json.JSONDecodeError, KeyError):
            pass
    return resultados


def parse_ebay(html):
    """Parsea resultados de eBay sold listings."""
    if not html:
        return []
    resultados = []
    # eBay usa clases s-item
    items = re.findall(r'<li class="s-item[^"]*".*?</li>', html, re.DOTALL)
    for item in items[:20]:
        titulo_m = re.search(r'<span role="heading"[^>]*>(.*?)</span>', item)
        precio_m = re.search(r'<span class="s-item__price">(.*?)</span>', item)
        if titulo_m and precio_m:
            titulo = re.sub(r"<[^>]+>", "", titulo_m.group(1))
            precio = re.sub(r"<[^>]+>", "", precio_m.group(1))
            resultados.append({"titulo": titulo, "precio": precio})
    return resultados


# ──────────────────────────────────────────────────────────────────────────────
# 5. INTEGRACIÓN CON EL PUENTE
# ──────────────────────────────────────────────────────────────────────────────

def sync_to_bridge(indice, momentum, alertas, google, reddit):
    """Guarda los resultados en data/tendencias_activas.json para que el puente los sirva."""
    datos = {
        "meta": {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fuentes": ["google_trends", "reddit_rss", "demanda_interna"],
            "total_modelos_analizados": len(indice),
            "metodo": "indice compuesto 0-100 (Google 40% + Reddit 30% + Demanda 30%)",
        },
        "indice_tendencia": dict(sorted(indice.items(), key=lambda x: x[1], reverse=True)[:100]),
        "momentum": dict(sorted(momentum.items(), key=lambda x: abs(x[1]), reverse=True)[:50]),
        "alertas": alertas,
        "google_trends_top": dict(sorted(google.items(), key=lambda x: x[1]["max"], reverse=True)[:30]),
        "reddit_top": dict(sorted(reddit.items(), key=lambda x: x[1]["menciones"], reverse=True)[:30]),
    }
    save_json("tendencias_activas.json", datos)
    print(f"\n  ✓ tendencias_activas.json actualizado ({len(datos['indice_tendencia'])} modelos, {len(alertas)} alertas)")
    return datos


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    solo_alertas = "--alertas" in args
    sync = "--sync" in args
    use_browser = "--browser" in args

    print("\n  ╔══════════════════════════════════════════════════════╗")
    print("  ║     TREND WATCHER — Análisis de tendencias activas   ║")
    print("  ╚══════════════════════════════════════════════════════╝")

    # Cargar datos
    catalogo = get_catalog()
    tendencias = get_tendencias()
    owned = get_owned()

    # Modelos a monitorear: STH + TH + top demanda
    modelos_monitorear = [c for c in catalogo if c["k"] in ("STH", "TH")]
    # Agregar top de demanda
    demanda_feb = tendencias.get("demanda_coleccionistas", {}).get("febrero_2026", [])
    demanda_mar = tendencias.get("demanda_coleccionistas", {}).get("marzo_2026", [])
    top_demanda = {d["modelo"]: d["coleccionistas"] for d in demanda_feb + demanda_mar}
    for modelo in list(top_demanda.keys())[:20]:
        if modelo not in [c["m"] for c in modelos_monitorear]:
            modelos_monitorear.append({"m": modelo, "k": "Mainline", "i": f"dem_{modelo}"})

    print(f"\n  Modelos a monitorear: {len(modelos_monitorear)}")

    # Términos para Google Trends
    terminos = [c["m"] for c in modelos_monitorear[:50]]  # Límite de pytrends

    # 1. Google Trends
    print("\n  [1/4] Google Trends...")
    google = fetch_google_trends(terminos) if terminos else {}
    print(f"      ✓ {len(google)} términos con datos")

    # 2. Reddit
    print("\n  [2/4] Reddit r/HotWheels...")
    modelos_norm = [(c["m"], normalizar_nombre(c["m"])) for c in modelos_monitorear[:100]]
    reddit = fetch_reddit_mentions(modelos_norm)
    print(f"      ✓ {len(reddit)} modelos mencionados")

    # 3. Demanda interna
    print("\n  [3/4] Demanda interna de coleccionistas...")
    demanda_interna = {}
    for d in demanda_feb + demanda_mar:
        nombre_norm = normalizar_nombre(d["modelo"])
        demanda_interna[nombre_norm] = max(demanda_interna.get(nombre_norm, 0), d["coleccionistas"])
    print(f"      ✓ {len(demanda_interna)} modelos con datos")

    # 4. Análisis
    print("\n  [4/4] Calculando índice de tendencia...")
    indice = calcular_indice_tendencia(google, reddit, demanda_interna)
    momentum = detectar_momentum(google, reddit)
    alertas = generar_alertas(indice, momentum, owned)

    # Mostrar resultados
    print(f"\n  ────────────────────────────────────────────────────")
    print(f"  TOP 15 TENDENCIA GLOBAL:")
    for i, (modelo, val) in enumerate(sorted(indice.items(), key=lambda x: x[1], reverse=True)[:15]):
        print(f"    {i+1:2d}. {modelo:40s} {val:5.1f}/100")

    print(f"\n  TOP 10 MOMENTUM (subiendo):")
    for i, (modelo, val) in enumerate(sorted(momentum.items(), key=lambda x: x[1], reverse=True)[:10]):
        print(f"    {i+1:2d}. {modelo:40s} {val:+.1f}%")

    if alertas:
        print(f"\n  ⚠ ALERTAS DE TU COLECCIÓN ({len(alertas)}):")
        for a in alertas:
            print(f"    • {a['modelo']}: índice {a['indice_tendencia']:.1f} | momentum {a['momentum']:+.1f}% | nivel {a['nivel']}")
    else:
        print(f"\n  Sin alertas por encima del umbral.")

    # 5. Scraping con navegador (opcional)
    if use_browser:
        print("\n  [+] Mercado Libre Chile (scraping)...")
        ml_html = fetch_with_browser("https://listado.mercadolibre.cl/hot-wheels")
        ml_items = parse_mercadolibre(ml_html)
        print(f"      ✓ {len(ml_items)} resultados de ML")

        print("\n  [+] eBay sold listings (scraping)...")
        ebay_html = fetch_with_browser("https://www.ebay.com/sch/i.html?_nkw=hot+wheels+treasure+hunt&LH_Sold=1")
        ebay_items = parse_ebay(ebay_html)
        print(f"      ✓ {len(ebay_items)} resultados de eBay")

    # 6. Sync al puente
    if sync or solo_alertas:
        sync_to_bridge(indice, momentum, alertas, google, reddit)

    print(f"\n  Listo. {datetime.now().strftime('%H:%M:%S')}\n")


if __name__ == "__main__":
    main()
