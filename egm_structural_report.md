# Goldfish Review Report — EGM Structural (Stage 7)

**Target:** `C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/SISTEMA.md`
**Reviewer lens:** `egm-structural` (Structural Goldfish)
**Audit date:** 2026-11-10

## Reviewer status

| Reviewer | Status |
| --- | --- |
| egm-structural (Structural Goldfish) | completed — verified against tracked repo files, gh-pages branch, and live HEAD HTTP |

**Note on `feature-spec-standard`:** no file named `feature-spec-standard` exists in the repo or the Hermes profile, so the review was applied against the structural checklist named in the request (heading hierarchy, template compliance, formatting rules, missing required headers, link compliance). All scope/line references below are to the on-disk `SISTEMA.md`.

## Method

- Parsed `SISTEMA.md` for heading hierarchy, code fences, and markdown table cell counts.
- Diffed every static claim in the doc against tracked repo files (`git ls-tree`, `stat`, `grep`), gh-pages branch content, and live HEAD HTTP responses.
- Folded in the independently grounded `egm-inventive-catalyst` findings where they bear on structural consistency.

## Structural summary

**Heading hierarchy:** valid. H1 (line 1) → H2 (§1–§10, lines 8–172) → H3 (§5.1–5.5, lines 88–116). No skipped levels.

**Template / formatting:** 4 matched code-fence pairs (23–42, 66–75, 99–101, 117–121). 4 tables with internally consistent column counts: §3 (3), §5.4 (3), §6 (2), §8 (5). No unclosed fences.

**Link compliance:** external §1 URLs resolve 200 OK. One broken internal anchor: `[instalado](#5-antigravity)` (§6 table) → no such heading exists.

---

## Findings (Blocker → Major → Nit)

### [§2 tree: stale self-referential filename] — Severity: Blocker
- **Reviewer lens:** egm-structural
- **Affected scope:** §2 "Directorio de trabajo y estructura", line 41
- **Discrepancy:** The tree lists `└── system-arch.md (este archivo)` as the architectural summary file, but the on-disk artifact is `SISTEMA.md`. Two wrong references in the same tree: line 40 also points at `REPORTE_FALLOS_ACTUALIZADO.md`, which does not exist.
- **Rationale:** The tree is the single most-referred-to structural document in the repo; pointing the "this file" marker at a nonexistent name (`system-arch.md`) invalidates §2 as a navigation/structural contract and contradicts the header of the very file it describes.

### [§2 tree + §9: dangling bug-report deliverable] — Severity: Blocker
- **Reviewer lens:** egm-structural
- **Affected scope:** §2 "Directorio de trabajo y estructura" line 40; §9 recommendation #3 (line 165)
- **Discrepancy:** `REPORTE_FALLOS_ACTUALIZADO.md` is referenced as an existing tracked artifact (§2 tree) and as the required source to follow when registering errors (§9 rec #3). Verified: the file is absent from the working tree **and** from the `gh-pages` branch (which contains 1898 tracked files, none named `REPORTE_FALLOS_ACTUALIZADO.md`). §8's bug table (IDs 1–7) has no anchoring issue report.
- **Rationale:** The doc both requires and depends on a deliverable that is not part of the repo. A structural review requires the referenced artifacts to exist or be explicitly marked `TODO/VERIFICAR`; this one is neither. It also means the "Errores / anomalías" chapter and the "Registrar errores" workflow are orphans.

### [§8 bug index unanchored + out of order] — Severity: Major
- **Reviewer lens:** egm-structural
- **Affected scope:** §8 "Errores / anomalías actuales y estado" (lines 148–156)
- **Discrepancy:** The `#` column encodes bugs #1–#7, but the rows are listed in the order 6, 7, 5, 4, 3, 2, 1. There is no authoritative source (the `REPORTE_FALLOS_ACTUALIZADO.md` referenced elsewhere is missing) that defines a bug's ID, status, fix, or confirmation, so the table is not traceable.
- **Rationale:** An error ledger whose IDs are neither sorted nor anchored to a tracked report cannot serve as the system's state of record. Even though each row's content is individually correct, the ledger structure fails as a governance artifact.

### [§1 publication claim vs §7 + verified Pages behavior] — Severity: Major
- **Reviewer lens:** egm-structural
- **Affected scope:** §1 (line 17), §2 "bug #1" (line 44), §7 "Bloque" (lines 139–143), §9 rec #1
- **Discrepancy:** §1 describes the published service at `foxnismone.github.io/hw-collector/` as the autonomous PWA whose catalog is "4.214 en `web/`". §7's Bloque — confirmed against the `gh-pages` branch (which serves root `index.html`, 352 KB, and **not** `web/index.html`) — states the live published app is the slow dev root that loads the 21.6 MB script over the network. The doc's top-level "what it is" claim is therefore contradicted by its own §7 block and by verified head behavior.
- **Rationale:** The inconsistency is central: §1 sells the public URL as an embedded PWA; §7 says Pages serves the non-embedded dev root. Until the publication path is decided and executed, §1's claim is false for the live URL. §9 rec #1 ("`web/index.html` debe ser la entrada") has not been executed, which is consistent with the block but means the doc leaves its own headline claim unresolved.

### [§6 table: broken internal anchor] — Severity: Major
- **Reviewer lens:** egm-structural
- **Affected scope:** §6 "Skills / herramientas disponibles", line 132
- **Discrepancy:** The EGM row links `[instalado](#5-antigravity)`; no heading named `antigravity` (or `#5-antigravity`) exists anywhere in `SISTEMA.md`. Valid anchors are only `§1`–`§10` and `§5.1`–`§5.5`.
- **Rationale:** Markdown link references to non-existent anchors silently resolve to the top of the document, so the "instalado" badge leads nowhere. A reviewer cross-referencing this cell lands on the wrong place or the page top — a link-compliance failure.

### [§8 row ordering cosmetic] — Severity: Nit
- **Reviewer lens:** egm-structural
- **Affected scope:** §8 (line 148–156)
- **Discrepancy:** Row order 6, 7, 5, 4, 3, 2, 1 instead of ascending 1–7.
- **Rationale:** Cosmetic only; does not affect data correctness, but the order undermines the ledger's readability and traceability. Sorting ascending resolves it.

### [§2/§7 path-naming inconsistency] — Severity: Nit
- **Reviewer lens:** egm-structural
- **Affected scope:** §2 tree line 25 (`index.html` at root) vs §7 Bloque (`root/index.html`)
- **Discrepancy:** Only `index.html` exists at repo root; §7 writes `root/index.html`, implying a `root/` subdirectory.
- **Rationale:** Two sections use different path notations for the same artifact. Harmless to rendering but worth reconciling for CI/citation consistency.

### [§5.5/§4: generator script location convention] — Severity: Nit
- **Reviewer lens:** egm-structural
- **Affected scope:** §4 flow diagram (line 70); §5.5 (line 116)
- **Discrepancy:** `regenerar_datos.py` is referenced as a root-level step, but the file lives at `scripts/regenerar_datos.py` (BASE is hardcoded to the repo root, so it must be run from root; the path notation is ambiguous).
- **Rationale:** Readers copying the command `regenerar_datos.py → data/cat.js` will look for a root file and not find one. Specify `scripts/regenerar_datos.py` or a `python scripts/regenerar_datos.py` invocation.

---

## Compliance verdict

| Criterion | Result |
| --- | --- |
| Heading hierarchy | ✅ H1→H2→H3, no skipped levels |
| Template compliance | ✅ 10 H2 sections fully populated; 4 matched code fences; 4 tables with consistent column counts |
| Formatting rules | ✅ No unclosed fences; blockquotes/tables/HR consistent |
| Missing required headers | ✅ None structurally missing (H1 + §1–§10 present) |
| Link compliance | ⚠️ 1 broken internal anchor (`#5-antigravity`); external §1 URLs 200 OK |

**Blockers:** §2 tree stale filename; §2 tree + §9 dangling bug-report deliverable.
**Major:** §8 unanchored/out-of-order bug ledger; §1 vs §7 publication-claim contradiction; §6 broken internal anchor.
**Nit:** §8 ordering; §2/§7 path naming; §5.5 generator-script path convention.

## Recommended fixes (priority order)

1. Rename/align the §2 tree so `system-arch.md` → `SISTEMA.md`, and mark `REPORTE_FALLOS_ACTUALIZADO.md` as `TODO/VERIFICAR` (or create it).
2. Anchor §8's ledger: sort IDs 1–7 ascending and add a `TODO/VERIFICAR` note on the missing issue-report source, or create the report file.
3. Decide the publication path (Pages `/web/` with redirects **or** root-artifact swap) and execute; update §1 to match the verified live behaviour so the headline claim is no longer contradicted by §7.
4. Fix `[instalado](#5-antigravity)` to a valid anchor, e.g. `[instalado](#5)` (§5) — or reference `§5.1`.
5. Reconcile `index.html` vs `root/index.html` and script paths in §2/§5.5/§4.
