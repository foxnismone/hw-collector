# EGM Inventive-Catalyst Audit — SISTEMA.md

**Target:** `C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/SISTEMA.md`
**Reviewer lens:** `egm-inventive-catalyst` (Elephant-Goldfish; TRIZ catalog)
**Audit date:** 2026-11-10

## Reviewer status
`egm-inventive-catalyst`: **completed** · grounded by real execution (cat.js/catalog_web.json sizes & entry counts, index.html/web/index.html asset references, serve.py content, sw.js fetch contract, git-tracked files).

## Method
Read SISTEMA.md at full length; cross-checked its static claims against the repo's tracked files and code (sizes, entry counts, asset references, endpoints, service-worker contract). Grouped findings by the three audit targets:
- **False compromise** — a declared "trade-off" that is actually a premature resolution which gave up a bigger benefit.
- **Technical contradiction** — two declared requirements/claims that cannot both hold; the doc picks one and sacrifices the other without flagging the conflict.
- **Unexamined trade-off** — a decision or divergence presented without analysis.

Findings below are ordered Blocker-free Major → Nit.

---

## Finding 1 — Publish block: served artifact ≠ the published PWA made in §1
**Severity:** Major
**Affected scope:** §1 (published URL, PWA claim), §2 (bug #1), §4 (catalog flow), §5.1, §7 (Bloque), §8 (bug #6), §9 (rec #1)
**Discrepancy (contradiction):** §1 describes the service at `foxnismone.github.io/hw-collector/` as the PWA whose catalog is "4.214 en `web/`". §7's Bloque states the opposite fact: GitHub Pages serves `root/index.html` (352 KB), **not** `web/index.html` (4.1 MB). The repo's tracked files confirm GitHub Pages would serve `index.html` (root) plus a **tracked** `data/cat.js` (21,619,414 B). So the live published app serves the **dev index that loads the full 12,587-model script over the network** — the mirror image of the §1 "authentic, lightweight, 4.214-embedded" claim.
**False compromise:** the doc "chose" the dev root as the published entry (§2 bug #1, §7) and kept it open as a "Bloque"; this sacrifices the claimed lightweight autonomous PWA in favor of publishing the slow, full-catalog dev build.
**TRIZ resolution:** **Merger (Unificación)** + **Preparation (Anticipation)** — fold `root/index.html` and `web/index.html` into a single entry artifact and pre-place the published build at the Pages root (or commit to `/web/` with redirects). Choose one publication path; do not leave both open.
**Secondary liabilities:** (1) live public PWA is not offline-capable — §5.4 note says LAN/HTTP already blocks PWA install; the published root also drags the 21.6 MB script over the wire; (2) the public catalog (12,587) ≠ the §1 claim (4,214), so §1's "4.214 en web/" is inaccurate for the live site; (3) §9 rec #1 ("web/index.html must be the entry") has never been executed, so the block persists.

## Finding 2 — "autónomo + liviana" conflates independence with lightness
**Severity:** Major
**Affected scope:** §1, §2 (bug #1), §5.1, §7
**Discrepancy (contradiction):** web/index.html is 4.1 MB and **does NOT** reference `data/cat.js` (verified: grep 0). But the same file **fetchies ≈10 runtime `web/data/*.json` files** (catalog_web.json 4,214, cajas.json, tendencias.json ×2, mercados.json ×5, …). So "autónomo" (no `cat.js` reference) and "liviana" (§7) are presented as one state when they are opposite ends of a weight/independence trade-off: the lightweight entry is the dev root (352 KB), the autonomous-ish entry is the heavy web build (4.1 MB) plus ~10 external-ish data fetches.
**False compromise:** §7 declares the published fix "autónoma + liviana" as though these are one goal; they are not. The "trade-off" is real and named as a free win.
**TRIZ resolution:** **Cost/Quality trade-off** + **Segmentation** — separate the two axes explicitly (packaging/weight vs external-data dependency vs autonomy); declare which is which and which is 'prod' vs 'dev' before publishing.
**Secondary liabilities:** (1) the public web PWA still depends on live `web/data/*.json` fetches (~10 files), violating the offline-first principle the doc implies; (2) embedded `const CAT` (4,214) duplicates `web/data/catalog_web.json` (4,214) — redundant storage in the 4.1 MB embed; (3) the public only gets 4,214 of the 12,587 extracted models — a data-subset trade-off that §1/§4 never quantify.

## Finding 3 — Feature/spec overclaim: "market values / tendencias" and "chatbot" advertised while their endpoints 404
**Severity:** Major
**Affected scope:** §1 (features), §5.4 (serve.py table), §9 (rec #2), sw.js (fetch handler "API del puente")
**Discrepancy (contradiction):** §1 lists "mercado de valores (market values), tendencias" and "chatbot/voz" as system features. §5.4 shows `/trends`, `/sync/*`, `/agent/*` → **404**, "no implementado; `agent_bridge.py` NO existe". §5.4's own fix text says create those "solo si se implementa agent_bridge.py", yet nothing implements the bridge or the endpoints. Voz is real (`serve.py` Piper/edge-tts `/tts`), but §1's "chatbot" is not evidenced by any chatbot code. sw.js's fetch handler also proxies `/agent|/sync|/tts` to "API del puente" — a runtime contract that implies a live bridge, which `serve.py` does not implement.
**False compromise:** the doc publishes a system whose declared trending/agent features silently 404, while labeling the absence as "no implementado" without demoting those features from delivered-status to roadmap.
**TRIZ resolution:** **Prior counteraction / Elimination of the harmful action** + **Request** — either implement the backends with reproducible endpoints (trends, agent, sync, Groq) or demote the claims to roadmap and remove them from the delivered-feature list.
**Secondary liabilities:** (1) the public PWA advertises features users click on, then get 404s on, worsening perceived quality; (2) sw.js's "always-red bridge" contract is contradicted by serve.py's lack of a bridge → broken/agnostic runtime behavior in the published app; (3) §1's "IA Groq opcional" has no callable backend (serve.py has no Groq call) — same overclaim family as chatbot/tendencias.

## Finding 4 — Two publish fixes proposed, never resolved (unexamined trade-off)
**Severity:** Nit
**Affected scope:** §7, §9 (rec #1)
**Discrepancy (unexamined trade-off):** §7 offers two publish fixes — "cambiar la configuración de Pages a servir `/web/` **o** reemplazar `root/index.html` por `web/index.html`" — while §9 rec #1 unilaterally picks only "web/index.html debe ser la entrada". Neither option is evaluated against its real costs, and the §7 blocked state is retained.
**False compromise:** presenting two alternatives without a decision defers the fundamental layout/publication contradiction instead of resolving it.
**TRIZ resolution:** **Decision matrix / Preparation** — weigh both options (URL-path change + redirects vs. repo-root artifact swap + CI/Pages config + build_app.py coordination) and pick one, documenting the trade-off.
**Secondary liabilities:** `/web/` serving changes the public URL path (needs redirects/alt links); replacing root changes the repo-root artifact and breaks the §9 claim that `root/index.html` is dev-only; either choice must be coordinated with `build/build_app.py`, git, and GitHub Pages rebuild.

## Finding 5 — "21.6 MB" size claim vs actual 20.6 MB (measurement inconsistency)
**Severity:** Nit
**Affected scope:** §2, §4, §5.2, §8 (bug #6)
**Discrepancy:** SISTEMA.md states `data/cat.js` as 21.6 MB across §2, §4, §5.2, §8; the actual tracked bytes are 21,619,414 B ≈ **20.6 MB** (verified by `ls`/`head -c` and entry count 12,587 matches §1's "12.587").
**False compromise:** the doc uses an imprecise size in the load-performance narrative (§5.2 "visita lenta", §8 bug #6), which would mis-set any future CI size gate or perf budget.
**TRIZ resolution:** **Parameter change (measurement normalization)** — report bytes and MB consistently (21,619,414 B / 20.6 MB).
**Secondary:** none blocking, but a perf/CI "data/cat.js size" test would be calibrated to the wrong threshold.

## Finding 6 — §4 flow diagram hides web/index.html's runtime data fetches (layering omission)
**Severity:** Nit
**Affected scope:** §4 (flow), §5.1
**Discrepancy:** §4 shows `regenerar_datos.py → data/cat.js → root/index.html` and web/index.html "embebe CAT (4.214)", implying web/index.html is self-contained. In fact web/index.html also fetches `web/data/{catalog_web,cajas,tendencias,mercados}.json` at runtime (≈10 files), per asset references in the file.
**Unexamined trade-off:** the diagram's single "embed" arrow makes the published build look fully offline while the live file still pulls data JSONs.
**TRIZ resolution:** **Indexing / Segmentation** — add a "runtime data layer" row to the §4 flow (embedded CAT + web/data/*.json fetches) so build outputs and offline expectations match reality.
**Secondary:** a future maintainer may drop `web/data` files believing the build is autónomo, breaking the published app.

## Finding 7 — §3 taxonomy: FastAPI claimed but serve.py is standalone http.server; "Sku sku" header broken; Groq only CDN
**Severity:** Nit
**Affected scope:** §3 (lang/versions table), §5.1, §5.4
**Discrepancy:** §3 lists the backend as "Python 3.14 (FastAPI/standalone http.server)" — no uvicorn/FastAPI import exists anywhere (serve.py uses `http.server`). The §3 column header "Sku sku" is a template artifact. Groq appears as a CDN dependency in §5.1 but there is no server-side Groq call.
**Unexamined trade-off:** §3's framework claim overstates the backend stack; the Groq dependency mirrors the chatbot/tendencias overclaim (Finding 3).
**TRIZ resolution:** **Conversion of Exness / Parameter change** — correct the §3 stack entry to "Python 3.14, standalone http.server (serve.py); Groq absent server-side (optional CDN only)".
**Secondary:** staging a "FastAPI" backend that doesn't exist misleads any architect navigating the repo.

---

## Summary
| # | Severity | Type | Focal issue |
|---|----------|------|-------------|
| 1 | Major | Contradiction + false compromise | Published PWA ≠ §1 claim; §7 serves dev root + 21.6MB script |
| 2 | Major | Contradiction + false compromise | "autónomo + liviana" conflates independence with lightness |
| 3 | Major | Contradiction + false compromise | Trends/chatbot advertised; endpoints 404, bridge absent |
| 4 | Nit | Unexamined trade-off | Two publish fixes proposed, never decided |
| 5 | Nit | Measurement inconsistency | "21.6 MB" vs actual 20.6 MB |
| 6 | Nit | Layering omission | §4 flow hides web/data runtime fetches |
| 7 | Nit | Taxonomy / claim overstatement | FastAPI claimed, absent; Groq overclaimed |

**Backbone action (all three Major findings share one root):** the repository ships two distributions (root dev + web publish) that GitHub Pages actually merges inconsistently, and three declared features (tendencias, chatbot/agent, Groq) have no implemented backend. Resolve by consolidating the artifact entry (Merger) and implementing/demoting the missing backends — then re-verify §1–§7 and the live publish.
