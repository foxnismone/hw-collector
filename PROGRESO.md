# Progreso — Proyecto HW Collector

## Hecho (verificado con datos reales)
- `data/catalog_raw_fandom.json` — **2.177 registros** de la línea Mainline, años **2016–2026** (233 en 2026, 231 en 2025), extraídos del wikitext real de la Hot Wheels Wiki vía API MediaWiki (`hotwheels.fandom.com/api.php`). Campos: `year, toy_number, collector_number, model, series, series_number, image_file, image_url, new_model, is_variant`.
- **1.718 registros con URL de imagen real** (`Special:FilePath/<archivo>`).
- `data/treasure_hunts.json` — Treasure Hunts por año 2022–2026 desde las páginas "YYYY Treasure Hunts Series" (wiki).
- `research/raw/*.wiki.txt` — wikitext crudo de: Super Treasure Hunt, Red Line Club, Car Culture, Treasure Hunts 2022–2026.
- `research/raw/*.txt` — texto extraído de las listas anuales y de la página oficial de Hot Wheels Collectors.
- Hallazgo propio: la app oficial de Mattel se llama **Hot Wheels Showcase™** (`com.mattel.hwcollector`), tiene buscador de 30.000+ autos, colección, wishlist, **Showcase Lens™ (identificación por foto)** y suscripción **Showcase Unlimited™**.

## En curso (5 subagentes de investigación en paralelo)
1. `research/01_lineas_y_coleccionismo.md`
2. `research/02_mercado_y_valores.md`
3. `research/03_bases_de_datos_y_foros.md`
4. `research/04_apps_analisis.md`
5. `research/05_ia_asistente_voz_vision.md`

## Pendiente
- Consolidar los 5 informes + datos propios en el MD maestro de desarrollo.
- `data/catalog.json` (catálogo normalizado + índice de coleccionabilidad + rangos de valor).
- `data/owned_collection.json` (plantilla de colección del usuario).
- Galerías HTML: `web/galeria_catalogo.html` y `web/galeria_coleccion.html`.
