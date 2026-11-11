# Hot Wheels Collector — Sistema, Arquitectura y Estado

> Estado actual verificado a partir de ejecución real (no fichas). Repo: `foxnismone/hw-collector`.  
> Si un dato no está confirmado por ejecución, el marcado `TODO/VERIFICAR` indica lo pendiente.

---

## 1. ¿Qué es?

**Hot Wheels Collector** — PWA (Progressive Web App) para:
- Listado del catálogo de modelos (4.214 en `web/`, 12.587 extraídos en `root/data/`).
- CRUD de la colección personal.
- Mercado de valores (market values), tendencias → *pendiente* (endpoint `/trends` → 404); chatbot/voz (TTS Piper + Edge); escáner OCR/barrido (ZXing + Tesseract.js); Auth Supabase multiusuario, IA Groq opcional.
- Escáner OCR/barrido (ZXing + Tesseract.js) para capturar códigos.
- Auth Supabase multiusuario, IA Groq opcional.

Servicio web: <https://foxnismone.github.io/hw-collector/> · Repositorio: <https://github.com/foxnismone/hw-collector>.

---

## 2. Directorio de trabajo y estructura

```
hotwheels_collector/                      ← raíz del repo (dev)
├── index.html                            ← index dev (root) 352 KB
├── web/                                  ← PWA publicada (build)
│   ├── index.html                        ← 4.1 MB, catálogo EMBEBIDO (self-contained)
│   ├── data/catalog_web.json             ← 4.214 modelos (subset publicado)
│   └── img/                              ← imágenes (reparadas 2182)
├── data/                                 ← catálogo RAW/dev (root)
│   ├── catalog_web.json                  ← 12.587 modelos (extracción completa)
│   ├── cat.js                            ← 21.6 MB, const CAT=[…] (carga externa)
│   ├── disenadores.js · ruedas.js · series.js
│   └── …
├── img/                                  ← imágenes root (dev)
├── tools/image-doctor/                   ← suite imadoctor (repair/audit)
├── build/
│   └── build_app.py                      ← aplica fixes OCR/zxing a HTML
├── serve.py                              ← server local 8080 (TTS + static) ⚠ root vs web
├── REPORTE_FALLOS_ACTUALIZADO.md
└── SISTEMA.md (este archivo) ← resumen arquitectónico
```

> El repo tiene **dos** distribuciones: `root/index.html` (dev, 352 KB) y `web/index.html` (publicada, 4.1 MB). **¡No son lo mismo!** Esto es el bug #1 del sistema.

---

## 3. Lenguajes y versiones (verificados)

| Componente | Lenguaje | Versión/estado |
|---|---|---|
| Frontend PWA | HTML / CSS / vanilla JS | ES2020+, sin bundler, `<script>` inline |
|| Backend local | Python 3.14 + `serve.py` (`http.server` + /tts) | 8080 |
|| Raspage/repair | Python 3.14 | `tools/image-doctor/` (imadoctor) |
|| Frontend PWA | JS CDN | Tesseract.js 5, ZXing 0.21.3, Supabase, Groq |
| Publicación | GitHub + GitHub Pages | `foxnismone.github.io/hw-collector` |
| DB (POS_2026_V3, separado) | SQLite/WAL | `cache.db` (no confundir con este repo) |

- Python: `python 3.14.9` (alias `python3` roto; usar `python`). `pip` ausente; usar `uv`.
- Node: 20.x+ disponible (solo para herramientas, el sitio no requiere bundler).

---

## 4. Flujo del catálogo (cómo se obtiene y se publica)

```
Fandom Wiki (api.php) ──► wikitext VACÍO para List_of, pero web_extract SÍ ──► data/*.json
       │
       ▼
regenerar_datos.py  ──►  `data/cat.js` (20.6 MB, const CAT=[…])
       │                                                       │
       ▼                                                       ▼
web/index.html embebe CAT=[{…}] (4.214)                /data/cat.js (root, 12.587) ──► root/index.html
(4.1 MB autónomo)                                          (publución root, 12.587 modelos)
```

**Puntos críticos (verificados):**
- **Proxy de imágenes OBLIGATORIO**: `images.weserv.nl` vía `IMG()` para toda URL de `static.wikia.nocookie.net`. Sin proxy, las tarjetas muestran 🚫.
- `api.php` del Fandom **devuelve wikitext vacío** para `List_of`; `web_extract` SÍ funciona. Si te pierdes, el proxy fuerza a usar `web_extract`.
- Limpiar wikitext antes de integrar: `{{…}}`, `[[File:…]]`, `[[x|y]]`.
- `build_app.py` **no genera/embede** catálogo; **solo parchea 6 fixes OCR/zxing** (idempotente). `web/index.html` es el artifact con el catálogo embebido.
- Si se edita `catalog_web.json` sin correr `regenerar_datos.py`, `cat.js` queda desactualizado.

---

## 5. Código clave

### 5.1 Frontend publicado — `web/index.html` (≈4.1 MB, autónomo)
- No referencia `data/cat.js`: **embebe** `CAT=[{…}]` (4214 modelos).
- JS: `js/supabase-client.js`, `vendor/supabase.js` + CDN (Tesseract.js, ZXing, Groq).
- La mayoría del catálogo está compilado en el HTML; imagenes `data:image/webp` / `<hash>.webp` en `img/`.
- `src` JS: `js/supabase-client.js`, `vendor/supabase.js`, `tesseract.js@5`, `@zxing/library@0.21.3`.

### 5.2 Index dev — `index.html` (root, 352 KB)
- Carga **externamente**: `src="data/cat.js"` (20.6 MB, const CAT) + `data/disenadores.js` + `data/ruedas.js` + `data/series.js`.
- Bloquea render hasta descargar 20.6 MB → **visita lenta** (ver `#6`).

### 5.3 Imagedoctor — `tools/image-doctor/`
```
imadoctor.py (entry) ──► pipeline.py ──► repair.py ──► scanner.py ──► sources.py
```
- Audit: reclama imágenes rotas/sin-archivo/vacías/corruptas (`auditoria` dict).
- Fix: reintento de descarga, `webp` (no jpg), `md5`-stable filename.
- **Bug arreglado**: `KeyError('auditoria')` crashea exit-1 en happy-path → ahora exit 0.
- Artefactos: `diagnosticar_sin_imagen.py` (sin imagen), `repair.py`, `pipeline.py`.

### 5.4 Servidor local — `serve.py` (port 8080)
| Endpoint | Método | Respuesta |
|---|---|---|
| `/tts-voices` | GET | 200 JSON (voces Piper + Edge) |
| `/tts?text=` | GET | 200 audio/mpeg (Piper→edge-tts) |
| `/img/` | static | 200 image/webp |
| `/trends` / `/sync/*` / `/agent/*` | — | **404** (no implementado; `agent_bridge.py` NO existe) |
- `lan_ip()`: `socket.connect(("8.8.8.8",80))` **sin timeout** → cuelga sin red. ⚠ PATCHED (settimeout 2.0).

### 5.5 Build / publicación
```
python build/build_app.py  → aplica fixes OCR/zxing (idempotente, 0 cambios si ya aplicados)
regenerar_datos.py        → data/cat.js (y web/data/catalog_web.json)
git commit + push + GitHub Pages rebuild
```

---

## 6. Skills / herramientas disponibles

| Skill | Uso |
|---|---|
| `imadoctor` (image-doctor) | Audit/repair de imágenes (detectar, reintentar, md5, `auditoria`) |
| `scanner` / `sources` | Fuente de datos Fandom / fallback |
| `diagnosticar_sin_imagen` | Diagnosticar fichas sin imagen |
|| EGM (Elephant-Goldfish) | instalado (sección 6) — diseño + review con subagents fresh (brainstorm/draft/resolve/bootstrap/drift-report) |
| `build_app.py` | Aplica fixes OCR/zxing a todos los HTML |
| `serve.py` | Server local TTS + static 8080 |

---

## 7. Publicación y bloques (verificados)

1. `git add -A && git commit && git push` a `foxnismone/hw-collector`.
2. GitHub Pages rebuild → `foxnismone.github.io/hw-collector`.
3. **⚠ Bloque**: Pages sirve `root/index.html` (352 KB), **NO** `web/index.html` (4.1 MB embebido). Para que la PWA publicada sea autónoma + liviana, cambiar la configuración de Pages a servir `/web/` o reemplazar `root/index.html` por `web/index.html`.

---

## 8. Errores / anomalías actuales y estado

|| # | Error / anomalía | Estado | Fix aplicado | Confirmación |
||---|---|---|---|---|
|| 1 | 3 imágenes sin archivo | ⚠️ Missing asset (no Fandom) | N/A | 3/1816 refs, faltan en img/ y root |
|| 2 | `web/data/cat.js` 404 en serve.py | ✅ Inofensivo | web/index.html embebe | 200 ≠ 404 → inofensivo |
|| 3 | `python -m serve.py` (invocación) → ModuleNotFoundError | ✅ Corregido | `python serve.py` | EOF |
|| 4 | `scanner.py` sugerido como "dead code" | ✅ Falso positivo | Quedó como núcleo (cadena real) | No cambiado |
|| 5 | `imadoctor` crachea `KeyError('auditoria')` exit-1 | ✅ Arreglado | exit-0 en happy-path | Re-run OK |
|| 6 | Live carga **20.6 MB cat.js** (root dev) | ⚠️ Pendiente decisión distribución | N/A (config Páginas) | Curl live: `/data/cat.js` 200, 21619414 B |
|| 7 | `serve.py` `lan_ip()` colgó sin red | Stalled al inicio | Añadido `s.settimeout(2.0)` | Start OK; endpoints 200 |

**Health**: `imagedoctor` 2182 reparadas, 1813/1816 refs en `web/img/` OK (99.8%), 3 faltan (sin asset en Fandom — issue de datos, no de build). E2E: 2182 refs | 200=2182 | bad=0.

---

## 9. Recomendaciones arquitectónicas

1. **Unificar la PWA**: `web/index.html` (autónomo, embebido, 4.214) debe ser la entrada publicada; `root/index.html` solo es dev/dev debug.
2. **Servidor**: no implementar `/trends` ni `/agent/*` (404 actuales; `agent_bridge.py` no existe); solo `/tts?text=` completa `/tts-voices`. `serve.py` queda TTL para /tts.
3. **Registrar** errores siguiendo `REPORTE_FALLOS_ACTUALIZADO.md` con reproducibilidad + diff.
4. **CI**: `python build/build_app.py` idempotente + test E2E de `/tts-voices`, `/img`, y verificación de `data/cat.js` size.
5. **Imágenes**: proxy obligatorio `weserv.nl`; script para migrar 112 ruedas sin imagen.

---

## 10. Notas de trabajo

- `data/cat.js` (root, 20.6 MB, 12.587) y `web/data/catalog_web.json` (4.214) son distintos; **no confundirlos**.
- \`imadoctor\` modifica \`web/index.html\` y \`web/data/catalog_web.json\` en la misma corrida (refs se propagan).
- Repositorio: https://github.com/foxnismone/hw-collector
- Publicación: https://foxnismone.github.io/hw-collector/
