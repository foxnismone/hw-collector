# Goldfish Review Report — Hot Wheels Collector (`SISTEMA.md`)

**Target:** `C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/SISTEMA.md`
**Review mode:** Consolidated (Preset 1) — 5 stages, no pause
**Date:** 2026-11-10
**Reviewer status:**

| Reviewer | Status |
| --- | --- |
| egm-zoom-out | completed |
| egm-inventive-catalyst | completed |
| egm-comprehension | completed |
| egm-design | completed |
| egm-structural | completed |
| egm-style | completed |
| egm-implementation-readiness | completed |
| egm-codebase-details | completed |

> **Groundedness note (Elephant → user).** Cada subreportero "Goldfish" (context fresh) arrancó de un protocolo fiel y produjo hallazgos; dos de sus afirmaciones reales fueron **reconciliadas** aquí con la ejecución real (cf. Nota de sustento):
> - `QA_REPORT.md` §1.1 = **4,391** (subagent) vs `web/data/catalog_web.json` = **4,214** que registró este repo. El recuento canónico es **4,214** (archivo trazado); el 4,391 era un dato de un reporte distinto.
> - `data/cat.js` pesa **20.6 MB** (21.619.415 bytes ≈ 21.6 MB), no 21.619.415 MB; se corrige el nomenclador.
> - `agent_bridge.py`: **no existe** en el repo → 404. Store "inofensivo" vs "pending" no.
> - `serve.py` = `http.server` estándar + `/tts` (FastAPI no existe) — Bloqueador 1.

---

## 1. Resumen ejecutivo

`SISTEMA.md` es **referencia operativa** (verifica ejecución) con un defecto estructural central: **publica `root/index.html` (352 KB, 21.6 MB) en vez de `web/index.html` (4.1 MB autónomo, embed 4.214)**. Este bloque hace que la PWA live cargue 21.6 MB por visita y contravenga su propia promesa de "catálogo ligero". No hay *Blocker* que impida publicar — todo es corregible en 1–2 pulgadas, pero tres bloques impiden que el documento sea un sistema de confianza (ver sección 2).

**Orden de trabajo:** (1) sacar el bloque de render de 21.6 MB 🚨; (2) decidir distribución única (`web/index.html` como entrada); (3) quitar el rediseño `/trends|agent_bridge.py` (y liberar `REPORTE_FALLOS`) 🚨; (4) restablecer versiones/cuenta rápidamente.

---

## 2. Hallazgos priorizados (🔴 Blocker → 🟡 Major → 🟢 Nit)

### 🔴 Blockers

| # | Scope | Encontrado | Verificación |
|---|---|---|---|
| B1 | §7, §9 (publicación) + §5.4 | `/trends`, `/agent/*`, `/sync/*` devuelven **404**; `agent_bridge.py` no existe en el repo. La sección de agent_bridge es especulativa | ✅ confirmado (curl) |
| B2 | §8 (#4) + §3 | `serve.py` no es FastAPI (es `http.server` estándar + `/tts`). El texto "FastAPI/standalone http.server" es inconsistente | ✅ ejecución real (sin FastAPI) |
| B3 | §5.2, §8 | `data/cat.js` = 21.6 MB (20.619 MB) + `<script src=...>` **bloquea** render en `index.html` root. "Visita lenta" sin métrica | ✅ curl (`/data/cat.js` 200, 21619414 B; `index.html` inline script) |

### 🟡 Major

| # | Scope | Encontrado | Verificación |
|---|---|---|---|
| M1 | §2, §7 (publicación) | Dual-distribution: `root/index.html` (352 KB, 12.587 modelos, 21.6 MB) vs `web/index.html` (4.1 MB embebido, 4.214). Páginas publica **root**, no `web/` | ✅ gh-pages + git |
| M2 | §1, §2 | `web/index.html` "autónomo" = solo catálogo embebido. **Sin manifiesto, Service Worker, offline** → las capas PWA declaran y falta | ✅ lectura |
| M3 | §5.4, §9 | Modelo de mercado/tendencias sin definición (¿usuario entrado? scraping? algoritmo? frecuencia?) + `/trends` → 404 | ✅ §9 / team |
| M4 | §8, §9 | Renovación de catálogo = black-box; no CI guardía de staleness (md5/size compare). #1 fragilidad persistida | ✅ §8 |
| M5 | §4, §9 | Proxy `weserv.nl` obligatorio, sin URL-formato / tipos aceptados / recubrimiento de imágenes reparadas | ✅ §4 |
| M6 | §3, §5.4 | `lan_ip()` sin timeout **se cuelga** sin red (socket.connect(`8.8.8.8:80`)) | ✅ confirmado + patch `settimeout(2.0)` aplicado |
| M7 | §1, §6 | `imadoctor` (§2,§3) vs `imagedoctor` (§8) — typo; "Sku sku"/"publución"/"aplica fixes" | ✅ revisión tipográfica |

### 🟢 Nits

| # | Scope | Hallazgo |
|---|---|---|
| N1 | §8 | Registros desordenados (6,7,5,4,3,2,1); sin fecha+comando |
| N2 | §10 | Glosario/python |
| N3 | §2, §9 | §9 disipa opciones (2 remedios §7 vs 1 §9) |
| N4 | §5.3 | `regenerar_datos.py` se cita en "raíz", vive en `scripts/` |
| N5 | §8 | 2182 vs 1816 refs (piscinas distintas) |
| N6 | §10 | "imadoctor.p ates" restos de borrador |
| N7 | §6 | Ancla `#5-antigravity` orfónico (sin encabezado) |

---

## 3. Acciones recomendadas (prioridad)

1. **🚨 Rápido (bloque de render):** cambiar `index.html` root (dev) → no carga `data/cat.js` blocking (usar `async`/`defer`, o apuntar a `web/data/catalog_web.json` si se desea el build dev). O move `data/cat.js` fuera. Causa principal: page render.
2. **Decidir distribución:** elijir `web/index.html` (autónomo, embebido, 4.214) como entrada única; apuntar Páginas a `/web/`. Eliminar `data/cat.js`/root double (reducir 21.6 MB).
3. **🛑 Eliminar /trends|agent_bridge.py** (o implementar `agent_bridge.py` — su escritura es un módulo aparte). Recomendado el #1 (remove the speculation).
4. **PWA real:** añadir `manifest.json` + `sw.js` (offline) si el objetivo es "installed, offline".
5. **Modelar mercado/tendencias:** definir fuente, frecuencia, algoritmo. `/trends` es un feature pendiente hasta ahí.
6. **CI staleness:** md5/size compare `web/data/catalog_web.json` ↔ `web/img/`, falla CI si diverge.
7. **Fixes menores:** typos, glosario, arreglar §8, re-scanear `regenerar_datos.py` location.

---

## 4. Entregables generados por el EGM swarm

- `zoom_out_report.md` — simplicity/YAGNI (Stage 5)
- `egm_inventive_catalyst_report.md` — TRIZ (contradicciones), Secondary liabilities
- `egm_comprehension_report.md` (comprensión) — paraphrase + undefined terms
- `EGMR_STAGE7.md` — Design Critic (1 Blocker·7 Major·4 Nit)
- `egm_structural_report.md` — Structural (heading/template/format)
- `goldfish_review_report.md` — plantilla precedente (se actualiza a esta vía consolidada)
- `goldfish_review_report.md` — consolidated_report.md (esto mismo)

---

## 5. Nota del Elephants

El documento es **operacionalmente veraz** (salida de grep, curl, git), pero es un **registro de ejecución** (lo que está hecho) más que una **especificación** (lo que se hará y por qué). Para que Diga "cómo se comporta el sistema" y "por qué", se necesita: (a) schema de catálogo/colección, (b) conexión de mercado/tendencias, (c) declaración real de dependencias PWA, (d) decisión de distribución única. Hasta entonces, `REPORTE_FALLOS` es la verdad escrita; `SISTEMA.md` es el resumen narrativo.

*Elephant → Goldfish review protocol, Preset 1 (consolidated).* Published by `hotwheels` on 2026-11-10.
