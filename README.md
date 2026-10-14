# HW Collector — investigación + app de coleccionismo Hot Wheels

Proyecto completo: investigación de mercado con fuentes, base de datos real del catálogo, galerías, seguimiento con alertas, análisis de cajas y prototipo funcional.

## Empezá por acá

| Archivo | Qué es |
|---|---|
| **`PLAN_DESARROLLO_APP_HOT_WHEELS.md`** | **Documento maestro**: plan completo de desarrollo (mercado, multi-moneda, IA, seguimiento, cajas, arquitectura, roadmap, riesgos). |
| `web/index.html` | **La app** (9 pestañas): Catálogo · Mi colección · Seguimiento · Tendencias · Cajas · Escanear · Valorar · Mercados · **Asistente con voz**. Abrir con doble clic. |
| `web/galeria_catalogo.html` | Galería del catálogo (2.177 autos) + cajas + tendencias. |
| `web/galeria_coleccion.html` | Mi colección con cantidades, seguimiento, valoración y mercados. |

Los tres HTML funcionan **sin internet y sin servidor** (imágenes locales incluidas). Todo lo que el usuario carga se guarda en el navegador (`localStorage`).

## Módulos de la app

| Pestaña | Qué hace |
|---|---|
| **Catálogo** | 2.177 autos 2016–2026 con imagen, filtros por año/serie/clase, búsqueda, insignia `TOP n` de demanda real y filtro “Solo trending”. |
| **Mi colección** | Galería de tus autos con **cantidad de cada uno**, condición, ubicación y valor. |
| **Seguimiento** | **Seguimiento uno a uno**: valor actual, sparkline de historial, semáforo de frescura (≤7 / ≤30 / >30 días), precio objetivo editable y **alertas** (VENTA, DEMANDA, SUBE, COMPRA, DATOS). |
| **Tendencias** | Ranking **real** de coleccionistas (HW Price Guide, ene/feb 2026), precios reales en **CLP** de tienda chilena, listados observados de eBay y matriz de qué se puede automatizar por marketplace. |
| **Cajas** | **Códigos de caja A–Q**: qué Treasure Hunt y qué Super Treasure Hunt trae cada una (2022–2026), contenido identificado por el usuario, y **decodificador de código de base** (letra=año, número=semana). |
| **Valorar** | Valor de la colección, distribución, plan de venta y descuento por lote. |
| **Ficha del auto** | **Índice de coleccionabilidad v2** con gauge circular, **radar de 5 ejes**, barras por factor con la fuente del dato e **histograma** de distribución del catálogo. |
| **Mercados** | Multi-moneda (**CLP / USD / EUR / GBP**), precios por mercado, calculadora de **importación a Chile** (IVA 19% / arancel 6%) y comparador de **neto por canal** con comisiones reales. |
| **Asistente** | Habla y escucha (español) con **3 personalidades**: Asistente (datos), **Pokédex** (formato de entrada de Pokédex) y **Clarkson** (humor cáustico latino con datos reales). Voz neuronal **local** con Piper (es-MX) o las voces del sistema. |
| **Puente celular** | `agent_bridge.py` conecta el celular con la PC: preguntas al asistente (motor local, al instante), **actualización de datos** y **cola offline** si no hay red. |
| **Tendencias activas** | `trend_watcher.py`: índice compuesto 0-100 (Google Trends 40% + Reddit 30% + demanda interna 30%). Alertas cuando un modelo de tu colección sube. |

## Datos

| Archivo | Contenido |
|---|---|
| `data/catalog.json` | 2.177 registros: año, toy #, nº de colección, modelo, serie, clase (Mainline/TH/STH), índice de coleccionabilidad, rango de valor, imagen. |
| `data/catalog_web.json` | Versión compacta para la app (con imágenes locales). |
| `data/cajas.json` | 15 cajas/año (2022–2026) con TH y STH por letra + decodificador de códigos de base (19 letras, 2008–2026). |
| `data/tendencias.json` | Demanda real de coleccionistas, precios en CLP, listados eBay, cobertura por marketplace. |
| `data/seguimiento.json` + `data/alertas.json` | Estado de seguimiento por auto y salida del motor de alertas. |
| `data/mercados.json` | Monedas y tipos de cambio con fuente/fecha, precios por mercado, comisiones, reglas de importación. |
| `data/treasure_hunts.json` | Treasure Hunts y Super Treasure Hunts 2022–2026 con caja, color, tampo, rueda y país. |
| `data/precios_referencia.json` | Rangos por clase, 34 modelos con precio verificado, tiempos de venta, comisiones, descuentos por lote. |
| `data/owned_collection.json` | **Plantilla** de tu colección (hoy con datos de EJEMPLO — reemplazalos). |
| `web/img/` | **1.814 imágenes WEBP** del catálogo (20 MB) — **2.177/2.177 registros con imagen** (500 son imagen de referencia del casting, marcadas en la app). |

## Instalarla en el celular (modo producción)

La app es un **PWA**: se instala con icono propio, pantalla completa y funciona sin conexión. **Requiere HTTPS** (los navegadores no permiten instalar desde `file://` ni desde HTTP local).

| Vía | Comando / acción | Resultado |
|---|---|---|
| **A. GitHub Pages** (recomendada) | `cd web && git init -b main && git add . && git commit -m "PWA" && gh repo create hw-collector --public --source=. --push && gh api -X POST repos/foxnismone/hw-collector/pages -f "source[branch]=main" -f "source[path]=/"` | URL HTTPS → “Instalar app” |
| **B. Netlify Drop** | Arrastrar la carpeta `web/` a app.netlify.com/drop | URL HTTPS al instante |
| **C. APK Android** | `bash build/make_apk.sh` (instala JDK + Android SDK, ~2 GB, 15-30 min) | `dist/HWCollector-debug.apk` |
| **C-bis. APK sin instalar nada** | Publicar (A o B) → pwabuilder.com → *Package for stores* → Android | APK firmado (TWA) |
| **D. Probar ya en la red local** | `python serve.py` → escanear el QR | Se usa, pero **no se instala** (es HTTP) |

Detalle completo, comparación Capacitor vs TWA y limitaciones del APK: **`DEPLOY.md`**.

## Herramientas

```bash
python agent_bridge.py --port 8081         # PUENTE: app + asistente + sync (celular en la red)
python build/build_app.py                  # regenera las 3 páginas HTML desde data/
python build/atender_cola.py               # procesa la cola de preguntas (motor local)
python build/trend_watcher.py --sync       # TENDENCIAS ACTIVAS: Google Trends + Reddit + demanda
python build/trend_scheduler.py --loop      # scheduler: corre el watcher cada 6 horas
python build/refresh_market.py --evaluate  # recalcula frescura y alertas (sin internet)
python build/refresh_market.py --api       # actualiza con APIs oficiales (config.json con tokens)
python build/refresh_market.py --browser   # colector con navegador real (playwright)
bash build/make_apk.sh                     # compila el APK de Android (Capacitor)
```

**Modo conectado (celular ↔ asistente):** corré `python agent_bridge.py --port 8081` y abrí `http://<ip-pc>:8081/` en el celular. La app detecta el puente (badge “asistente”), responde preguntas al instante, actualiza los datos y **queda en cola si no hay red**. Detalle completo en `DEPLOY.md`.

Para el modo `--api` hace falta un token gratuito de [MercadoLibre](https://developers.mercadolibre.cl) y/o un App ID de [eBay](https://developer.ebay.com), en `config.json` (no subir a git). El modo `--browser` no necesita credenciales pero sí `pip install playwright && playwright install chromium`.

## Investigación (con fuentes)

`research/01_lineas_y_coleccionismo.md` · `research/02_mercado_y_valores.md` · `research/03_bases_de_datos_y_foros.md` · `research/04_apps_analisis.md` · `research/05_ia_asistente_voz_vision.md` — 3.555 líneas con URL por cada dato.

## Cómo regenerar el catálogo

```bash
# La fuente es la API abierta de la Hot Wheels Wiki (MediaWiki, CC BY-SA 3.0)
curl -s -A "Mozilla/5.0 (hotwheels-research)" \
  "https://hotwheels.fandom.com/api.php?action=parse&page=List%20of%202026%20Hot%20Wheels&prop=wikitext&format=json&formatversion=2"
```

Para descargar imágenes de Fandom hace falta **User-Agent propio + `Referer: https://hotwheels.fandom.com/`** (sin eso devuelve 403), y la ruta de miniatura `…/revision/latest/scale-to-width-down/200`.

## Estado

- ✅ Investigación completa (5 informes, fuentes verificadas)
- ✅ Catálogo de 2.177 autos con **100 % de cobertura de imágenes** (1.814 archivos, 500 marcados como referencia del casting)
- ✅ App de 9 pestañas probada en navegador sin errores JS
- ✅ Multi-moneda (CLP/USD/EUR/GBP) y comparación entre mercados
- ✅ **Índice de coleccionabilidad v2** con demanda y tendencia reales + gauge, radar e histograma
- ✅ **Voz neuronal local** (Piper es-MX) + personalidades Pokédex y Clarkson (muestras en `muestras/`)
- ✅ Seguimiento por auto + motor de alertas funcionando (11 alertas generadas)
- ✅ Galería de códigos de caja 2022–2026 + decodificador de códigos de base
- ⏳ Tu colección real (pendiente de cargar)
- ⏳ Backend de IA para identificación por foto (especificado en el plan, §5 y §7)
- ⏳ Tokens de API para actualización en vivo (especificado en §14.4)
