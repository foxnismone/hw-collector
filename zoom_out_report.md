# EGM Stage 5 — Initial Zoom-Out Review

- TargetFile: C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/SISTEMA.md (177 lines)
- Reviewer: egm-zoom-out (Skeptical Architect)
- Standard: Zoom-Out Standard (resources/document_standards/zoom-out-standard.md)
- Focus: root-problem focus, simplicity (YAGNI), existing-reuse, anti-premature-detail (altitude control), no architectural dead-ends.

## Overall

Context is sufficient. §1 defines the objective; §2/§4 diagnose the two-distribution root problem. The document passes context-sufficiency. Findings below target the simplicity/architecture quality of the content.

## Findings

### 1. Major — §2 (Directorio de trabajo), §4 (Flujo del catálogo), §5.5 (Build/publicación)
**Rationale:** No documented step produces the self-contained `web/index.html`. §5.5 names `build_app.py` (which §4 line 81 states does NOT embed the catalog — only 6 OCR/zxing patches) and `regenerar_datos.py` (which only writes `catalog_web.json`, `cat.js`, `ruedas.js`; verified on disk at `scripts/regenerar_datos.py`, but §4/§5.5 reference it without a path). The published 4.1 MB artifact is therefore an end-state that no documented command builds. This is why §2 can call the root-divergence "bug #1" but the documented flow never actually fixes it — the root problem is diagnosed but not solvable by the documented build.

### 2. Major — §5.4 (Servidor local), §9 Recomendación #2
**Rationale:** Recommends creating `/trends` and `/agent/*` "solo si se implementa agent_bridge.py" to remove 404s. Verified `agent_bridge.py` does not exist anywhere in the repo, and `/trends`, `/sync`, `/agent` currently do nothing. These endpoints serve no proven need; leaving them 404 is correct until a real client calls them. Proposing an interface plus a hypothetical bridge now is a YAGNI violation and a speculative interface that can harden into an architectural dead-end.

### 3. Nit — §1 (¿Qué es?)
**Rationale:** §0 requires the document to define *what* we achieve and *why*. §1 states the goal as a feature list (catalog, CRUD, market values, chatbot/voz, OCR, auth) but never names the root problem being solved (e.g., "tracking a personal Hot Wheels collection and its market values"). Without a problem statement, downstream sections risk optimizing symptoms rather than the root need.

### 4. Nit — §5.3 (Código clave — Imagedoctor), §8 (Errores/anomalías)
**Rationale:** Low-altitude weeds mixed into the architectural record. §5.3 lists the imadoctor internal pipeline files and a specific crash fix (KeyError('auditoria'), exit-1); §8 is a bug log carrying crash traces and exit codes. These are dev-status details that dilute the zoom-out view and belong in a run-log, not in the architecture record.

### 5. Nit — §7 (Publicación y bloques), §9 Recomendación #1
**Rationale:** §7 proposes two remedies for the published-file block (serve `/web/` OR replace root/index.html); §9 #1 gives a single "unificar" direction. Two candidate paths for one problem is avoidable branching. Reconcile to one committed fix.

## Positive observations (no action)

- §2/§4 correctly identify the two-distribution divergence as the root problem and point at unificación on `web/index.html` (§9 #1).
- §9 #1 and #3 (register errors with reproducibility/diff; CI over the idempotent build) are sensible, non-speculative.
- The frontend already leverages existing libraries via CDN/vendor (Supabase, Tesseract.js, ZXing, Groq) rather than inlining — aligns with the Leverage-Existing rule.

## Open items (already documented; not findings)

- §7's publication block (Pages serves root/index.html, not web/index.html) is identified and scoped; resolution depends on the §9 unificación direction.
