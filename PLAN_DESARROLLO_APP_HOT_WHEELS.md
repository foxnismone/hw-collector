# HW COLLECTOR — Plan completo de desarrollo de una app de coleccionismo Hot Wheels
### Catálogo · Colección · Valoración de reventa · Asistente con IA de visión y voz (móvil + escritorio)

**Versión:** 1.0 · **Fecha:** 11 de octubre de 2026
**Autor:** investigación y especificación técnica (agente Hotwheels)
**Idioma del producto:** español (multi-idioma previsto)
**Estado del proyecto:** investigación completa + base de datos construida + prototipo funcional verificado

---

## 0. Cómo leer este documento

Este MD es el documento maestro de desarrollo. Cada afirmación de mercado, precio o cuota de API lleva su fuente: los cinco informes de investigación que lo respaldan están en `research/` y las URL se citan al pie de cada sección.

**Lo que ya está construido y verificado** (no es una promesa, es código que corre):

| Artefacto | Ruta | Estado verificado |
|---|---|---|
| Base de datos de catálogo | `data/catalog.json` | **2.177 registros** reales de la línea Mainline 2016–2026 (102 STH, 28 TH, 2.047 mainline) |
| Catálogo compacto para la app | `data/catalog_web.json` | 380 KB, campos cortos, con **imágenes locales** |
| Imágenes del catálogo | `web/img/` | **1.814 imágenes WEBP** (20 MB) — **2.177/2.177 registros con imagen** (100 %), 500 marcadas como *imagen de referencia del casting* |
| Treasure Hunts / Super TH | `data/treasure_hunts.json` | 2022–2026, con **código de caja**, color, rueda, tampo, país |
| **Galería de códigos de caja** | `data/cajas.json` | **15 cajas/año 2022–2026** con TH y STH por letra + decodificador de códigos de base (19 letras, 2008–2026) |
| **Señales de demanda y tendencias** | `data/tendencias.json` | ranking real de coleccionistas (ene/feb 2026), precios en CLP de tienda chilena, listados eBay, matriz de automatización |
| **Índice de coleccionabilidad v2** | `data/indice.json` | fórmula con **datos reales** en D (demanda medida) y M (momentum ene→feb 2026), con fuente declarada por factor |
| **Seguimiento y alertas** | `data/seguimiento.json`, `data/alertas.json`, `build/refresh_market.py` | motor probado: **11 alertas** generadas (2 altas por demanda, 9 por datos) |
| **Voz neuronal local** | `serve.py` (`/tts`, `/tts-voices`), `voices/`, `muestras/` | **Piper es_MX-claude-high funcionando** (100 KB de WAV por frase, sin internet) + 3 personalidades (Asistente, Pokédex, Clarkson) |
| **Multi-moneda y mercados** | `data/mercados.json` | USD/CLP/EUR/GBP con fuente y fecha, precios por mercado, comisiones e importación |
| Precios de referencia con fuente | `data/precios_referencia.json` | rangos por clase + 34 modelos con precio verificado + tiempos + comisiones |
| Galería del catálogo | `web/galeria_catalogo.html` | probada: 2.177 autos, filtros, búsqueda, fichas, imágenes, cajas, tendencias |
| Galería de mi colección | `web/galeria_coleccion.html` | probada: cantidades, valor, distribución, plan de venta, seguimiento |
| App completa | `web/index.html` | probada: **9 pestañas** (catálogo, colección, seguimiento, tendencias, cajas, escanear, valorar, mercados, asistente) sin errores JS |
| Informes de investigación | `research/01…05_*.md` | 3.555 líneas / 211 KB con URLs verificadas |

Los tres HTML **no necesitan internet ni servidor**: se abren con doble clic (la colección se guarda en `localStorage`).

---

## 1. Resumen ejecutivo

### 1.1 La idea

Una app de coleccionismo de diecast que corre en **celular y computadora**, donde el usuario:

1. **Cataloga** sus autos con una foto, un código de barras o búsqueda por nombre.
2. **Ve su colección** como galería, con cantidades por modelo y por variante.
3. **Conoce el valor** de cada pieza y de la colección completa, con rango y nivel de confianza explícitos.
4. **Recibe un plan de venta**: cuánto pedir, en qué canal, cuánto tarda y cuánto queda neto después de comisiones.
5. **Habla con un asistente** que le contesta en voz alta sobre el auto que tiene en la mano.

### 1.2 Por qué hay lugar para otra app

El análisis competitivo de `research/04_apps_analisis.md` muestra que **ninguna app existente combina todo**:

| App | Escaneo | Valores | Multi-marca | Social | Export | Puntaje tiendas |
|---|---|---|---|---|---|---|
| Hot Wheels Showcase™ (oficial, Mattel) | Solo foto IA (por suscripción) | **NO** | NO | Sí | **NO** | 4.8 / 4.7 |
| Die Carz | Foto IA (gratis) | NO | Sí (11 marcas) | Sí | Limitado | 4.8 |
| Hunt64 | Foto IA (gratis ilimitado) | Sí (comunidad) | HW + manual | Sí | CSV | 4.8–4.9 |
| iCollect Toy Cars | UPC + OCR + AI | Sí | Sí (barcode) | NO | CSV | 4.5 |
| Carlect | Foto IA | Sí | Sí | NO | CSV | 4.5–4.7 |
| HW Price Guide | NO | Sí (ventas reales) | Solo HW | NO | NO | — |
| CollectHW (web) | NO | NO | Solo HW | NO | NO | — |

Los cinco motivos documentados de fracaso de estas apps (research/04 §5): abandono por dependencia de hardware (Hot Wheels **id** murió en 2023 con sus chips NFC), datos incompletos, **ausencia de valores de mercado**, escaneo poco fiable y **paywalls que destruyen la confianza** (Carlect: USD 4,99/semana).

**Los diez diferenciadores que nuestra app debe cumplir** (research/04 §6.1):
escaneo híbrido (foto + UPC + número de base) · precios de ventas reales, no *asking* · multi-marca real · export abierto (CSV/JSON/Sheets) · condición y fotos propias del usuario · gamificación con logros reales · monetización justa (catalogación **siempre** gratis) · comunidad con privacidad granular · **sin hardware propietario** · escritorio y móvil sincronizados.

### 1.3 La verdad incómoda (leer antes de prometer nada)

Los Hot Wheels se parecen muchísimo entre sí. Identificar la **variante exacta** por foto es difícil incluso para un experto humano. Precisión esperada y honesta:

| Método | Precisión esperada | Comentario |
|---|---|---|
| Foto con IA de visión → *casting* (p. ej. "Custom Camaro") | **60–80 %** | sirve como filtro, no como identificador |
| Foto → variante exacta (color + año + serie) | **30–50 %** | casi imposible sin ver la base o la tarjeta |
| OCR del blister / texto de la tarjeta | 70–85 % | depende de la calidad de la foto |
| **Código de barras (UPC) del blister** | **95 %+** | el método más fiable, cuando el auto está en su tarjeta |
| Número de *casting* grabado en la base | alto | requiere foto macro de la base |

Conclusión de diseño: **el reconocimiento por foto propone candidatos, el usuario confirma**. Nunca al revés. (research/05 §6.1)

---

## 2. El producto Hot Wheels: qué se colecciona y cómo funciona

### 2.1 Línea básica (Mainline)

- La **mainline** es la línea de producción masiva: **250 modelos numerados por año** (numeración 1–250; las variantes de color **no** reciben número nuevo, y los Treasure Hunts y los exclusivos de tienda **sí** están numerados). Confirmado para 2025 y 2026 en la Hot Wheels Wiki.
- Cada modelo tiene un **Toy #** (código de 5 caracteres, p. ej. `HYW18`) y un **número de colección** (`001`…`250`).
- Precio de referencia en EE. UU.: del orden de **USD 1,25–1,50** por unidad suelta en tienda; los modelos nuevos de 2025 aparecen en hobbyDB entre **USD 2,00 y USD 5,00** ya en el mercado secundario.
- **Case codes**: los surtidos se embalan en cajas identificadas con letras (A, B, C… sin usar I/O). Cada caja trae una mezcla conocida de modelos; los coleccionistas "cazan" cajas concretas porque la probabilidad de Treasure Hunt cambia por caja.
- **Series temáticas** dentro de la mainline 2025 (42 series distintas en el catálogo construido): HW Dream Garage, HW Metro, HW EV, HW Art Cars, Factory Fresh, HW Screen Time, HW J-Imports, HW Dirt, HW Hot Trucks, HW Modified, Track Aces, Rod Squad, Compact Kings, Safari Mode, Wild Widebody, Batman, Hot Wheels Let's Race, HW Celebration Racers (Cinco de Mayo, Day of the Dead, Chinese New Year, Movember, 80.º aniversario de Mattel)… etc.

### 2.2 Líneas para coleccionistas (el dinero está acá)

| Línea | Qué es | Rango de precio real |
|---|---|---|
| **Premium / Car Culture / Boulevard** | adultas, ruedas Real Riders, metal/metal, tarjeta premium | unidad **USD 6,95–12,50**; set de 5 **USD 29,95–64,99** |
| **Team Transport** | auto + camión de transporte a escala | premium |
| **Pop Culture / Retro Entertainment** | temas de cine, TV, anime | premium |
| **Fast & Furious Premium** | licencia de la saga | set de 5 ≈ **USD 44,99** |
| **RLC (Red Line Club)** | club de pago de Mattel; ediciones limitadas numeradas | **USD 29,99–84,99** |
| **Convention / Nationals** | exclusivos de convención | **USD 42,99–140** |
| **Colaboraciones** | Fórmula 1 (acuerdo multianual), Ferrari (regreso tras 10 años), BAPE, etc. | variable |
| **Mattel Creations** | drops directos al consumidor | variable |
| **NFT Garage** | pausado/discontinuado por Mattel | — |
| **Hot Wheels id** | app + chips NFC: **descontinuado en 2023**; sus autos ahora son raros | USD 135–340 en el mercado |
| **Hot Wheels Unleashed** | videojuego (no producto físico) | — |
| **Legends Tour** | concurso anual de autos reales → se convierte en diecast | — |

### 2.3 Treasure Hunts (TH) y Super Treasure Hunts (STH)

- Se identifican por el **logo "circle flame"** estampado en el auto y/o la tarjeta.
- Los **STH** suman **pintura Spectraflame** y **ruedas Real Riders**, y son la pieza más buscada de la mainline.
- La wiki publica por año la lista completa con **color de carrocería, tampo, color de base, ventanas, interior, tipo de rueda, país y caja** — es exactamente la estructura que ya parseamos en `data/treasure_hunts.json` (15 TH + 15 STH por año).
- Precios de reventa observados: TH carded **USD 5–20**; STH **USD 85–250** típico en 2024–2025, con extremos: `'83 Chevy Silverado` STH USD 250, `Mazda 787B` STH USD 200, `'87 Audi Quattro` STH USD 20–252. Un **set completo de 15 STH 2025** se ha visto entre **USD 396 y 2.751**.

### 2.4 Qué hace valioso a un auto (factores ordenados por impacto)

1. **Rareza / tirada** — series cortas, exclusivos, RLC numerado.
2. **TH vs STH vs Chase** — el escalón de rareza dentro de la mainline.
3. **Error cars** — autos con fallas de fábrica (rueda equivocada, tampo invertido, ventana faltante). Pueden multiplicar el valor.
4. **Variaciones** — rueda, tampo, color, base (cromada vs plástica), país de fabricación.
5. **Condición** — carded (en tarjeta) > loose (suelto). `short card` vs `long card`; blister dañado baja el valor.
6. **Autenticidad** — el mercado está lleno de **re-cards** (auto genuino en tarjeta falsa), repintados y STH con ruedas cambiadas.
7. **Antigüedad** — la era **Redline (1968–1977)** es el santo grial: `Custom Camaro` 1968 común jugado **USD 150–400**, rose/pink **USD 400–1.500**; `Beach Bomb` side-loader común **USD 200–3.500**; el **Pink Rear-Loading Beach Bomb** (1969) alcanza **USD 100.000–175.000**.
8. **Firma de diseñador** (p. ej. Larry Wood) y **edición de convención**.

### 2.5 Glosario mínimo (versión completa en `research/01`, §6)

**Mainline** línea masiva · **Premium** línea adulta · **RLC** Red Line Club · **TH / STH** Treasure Hunt / Super Treasure Hunt · **Chase** variante rara dentro de un set · **Carded / Loose** en tarjeta / suelto · **Short / Long card** formatos de tarjeta · **Real Riders** ruedas de goma con llanta cromada · **Spectraflame** pintura metálica translúcida histórica · **ZAMAC** aleación de zinc sin pintar · **Error car** falla de fábrica · **Re-card** auto genuino en tarjeta falsa · **Grail** la pieza soñada · **Case** caja de surtido · **Assortment** mezcla de modelos de una caja.

---

## 3. Mercado, valoración y tiempos de venta

### 3.1 Cómo se forma el precio (y por qué las guías mienten)

- **Sold comps vs asking prices**: lo único que vale es el **precio de ventas realizadas**, no lo que el vendedor pide. Muchas guías publican *asking*, que infla el valor percibido.
- **Subastas**: el formato de 7 días descubre el precio real de mercado; "Buy It Now" fija un techo.
- **Liquidez**: los mainlines comunes son líquidos pero de valor ínfimo; los Redlines son valiosos pero ilíquidos.
- **Estacionalidad**: sube antes de Navidad y alrededor de las convenciones.
- **Manipulación**: existe *shill bidding* (pujas falsas del propio vendedor) y lotes vendidos "a precio de guía" sin ventas reales que lo respalden.

### 3.2 Fuentes de precio: qué sirve y qué no

| Fuente | Cobertura | API | Límite |
|---|---|---|---|
| **eBay** (filtro *Sold Items*) | la referencia del mercado | **Browse API** free tier: 5.000 llamadas/día — pero **solo listados activos**; `findCompletedItems` fue **descontinuado en febrero de 2025**; *Marketplace Insights* (ventas reales) requiere aprobación Business, casi nunca otorgada | crítico para el motor de valor |
| **hobbyDB** | base de datos + guía de precios + marketplace; absorbió la mítica **South Texas Diecast** | existe API, **acceso pago (desde ~USD 1.200 de setup según el proveedor)** | buena calidad, costo alto |
| **PriceCharting** | precios por ítem | **solo con suscripción paga** (Legendary) | sin capa gratuita |
| **CollectHW** | **61.298 modelos** catalogados | sin API pública | scraping frágil |
| **Hot Wheels Wiki (Fandom)** | el catálogo histórico más completo y **gratuito** | **API MediaWiki abierta, sin auth** | CC BY-SA 3.0 (atribución obligatoria) |
| **Beckett, Mercari, Whatnot, Etsy, Facebook** | canales de venta y datos dispersos | — | manual |
| **Reddit r/HotWheels** | sentimiento y tendencias, **no precios estructurados** | JSON público | usar como señal, no como dato |

### 3.3 Rangos de precio reales (con fuente y fecha — tabla completa en `data/precios_referencia.json`)

| Categoría | Rango USD | Fuente | Fecha |
|---|---|---|---|
| Mainline común loose | 0,50 – 3,00 | hobbyDB / allhotwheels | 2025 |
| Mainline carded | 1,00 – 5,00 | hobbyDB listings | 2025 |
| Treasure Hunt carded | 5 – 20 | iCollectEverything | 2026 |
| Super Treasure Hunt | 85 – 250 (extremos 19,50 – 252) | resellcalendar / autoevolution | 2024–2025 |
| Set completo 15 STH | 396 – 2.751 | autoevolution | 2025 |
| Premium / Car Culture (unidad) | 6,95 – 12,50 | eBay | 2024–2025 |
| Premium (set de 5) | 29,95 – 64,99 | eBay | 2023–2025 |
| RLC | 29,99 – 84,99 | 99diecast / WheelCollectors / Colorado Diecast | 2024–2025 |
| Convention Exclusive | 42,99 – 140 | hobbyDB Blog | 2022–2025 |
| Redline 1968–77 (jugado → NM) | 50 – 3.500 | Yonkers Times / RarityFinder (PSA) | 2026 |
| Grail / prototipo | 5.000 – 175.000 | iCollectEverything / UnderpricedAI | 2024–2026 |

Modelos con precio puntual verificado (35 en total): `Porsche 935 Toy Fair` 690 · `Twin Mill Mobil 1` 620 · `'99 Civic Type R EK9 STH` 270 · `Pininfarina Battista (id)` 340 · `'83 Silverado STH` 250 · `Porsche 959 RLC Gulf` 84,99 · `Honda Motocompo` 2,99–3,99 · `'67 Firebird 400` 4,00 …

### 3.4 Tiempo para vender y neto por canal

| Tramo de precio | Tiempo típico | Canal recomendado |
|---|---|---|
| 0,50 – 3 | semanas/meses individual; **días en lotes** | lotes en eBay o Facebook Marketplace |
| 3 – 15 | 1–4 semanas | eBay Buy It Now |
| 15 – 50 | 1–2 semanas | eBay subasta o BIN |
| 50 – 200 | 1–4 semanas | eBay subasta |
| 200 – 1.000 | 1–6 meses | eBay subasta / casas de subastas |
| 1.000+ | meses a años | casas de subastas especializadas |

**Comisiones y neto sobre un ítem de USD 50:** eBay **13,25 % + USD 0,40** → ~42,98 · Mercari 10 % → ~45,00 · Whatnot 8 % + 2,9 % + 0,30 → ~44,60 · Etsy 6,5 % + fees → ~45,00 · **Facebook Marketplace y hobbyDB: 0 %** → 50,00.
**Descuento por volumen:** lote pequeño (2–6) 10–20 % · lote mediano (20–50) 30–50 % · colección completa (100+) **50–70 %** · venta a revendedor 50–70 %.
**Regla operativa:** si un auto vale menos de USD 10 → lote; si vale más de USD 20 → individual.

### 3.5 Riesgos de mercado a mitigar en el producto

*Shill bidding*, falsificaciones (auto falso, **re-card**, STH con ruedas cambiadas, error fabricado, repintado) y lotes sobrevalorados. Mitigaciones del producto: mostrar siempre el **rango + confianza**, exigir **mínimo 5 comparables** para dar un precio puntual, separar visualmente "precio pedido" de "precio vendido", y publicar una **guía de verificación** (fotos de la base, luz UV, señales de re-card).

---

## 4. Fuentes de datos y base legal

### 4.1 La fuente gratuita que sí funciona: la API de la Hot Wheels Wiki

`https://hotwheels.fandom.com/api.php` — MediaWiki abierta, **sin autenticación**, licencia **CC BY-SA 3.0** (atribución obligatoria). Comandos probados realmente (research/03):

```bash
# Lista anual completa en wikitext (la usamos para construir el catálogo)
curl -s -A "Mozilla/5.0 (hotwheels-research)" \
 "https://hotwheels.fandom.com/api.php?action=parse&page=List%20of%202025%20Hot%20Wheels&prop=wikitext&format=json&formatversion=2"

# Ficha de un modelo (infobox estructurado)
curl -s -A "Mozilla/5.0 (hotwheels-research)" \
 "https://hotwheels.fandom.com/api.php?action=query&prop=revisions&titles=Punk%20Rod&rvslots=*&rvprop=content&format=json"

# Miembros de una categoría por año
curl -s -A "Mozilla/5.0 (hotwheels-research)" \
 "https://hotwheels.fandom.com/api.php?action=query&list=categorymembers&cmtitle=Category:2024%20Hot%20Wheels&cmlimit=50&format=json"

# Búsqueda
curl -s -A "Mozilla/5.0 (hotwheels-research)" \
 "https://hotwheels.fandom.com/api.php?action=query&list=search&srsearch=2024+Mainline&srlimit=5&format=json"
```

**Truco crítico verificado:** las **imágenes** de Fandom devuelven **403** con un User-Agent genérico o desde `urllib`. Funcionan con `User-Agent: Mozilla/5.0 (hotwheels-research)` **+ `Referer: https://hotwheels.fandom.com/`** y usando la ruta de miniatura `…/revision/latest/scale-to-width-down/200`. Así se descargaron las **1.673 imágenes** del proyecto.

### 4.2 Otras fuentes y su rol

- **South Texas Diecast** (`southtexasdiecast.com`): catálogo histórico clásico, hoy migrado a hobbyDB; sigue siendo consultable por año.
- **CollectHW**: 61.298 modelos — referencia de cobertura a alcanzar.
- **hwcollectorsnews.com**, **Lamley Group**, **Orange Track Diecast**, **164custom**, **hwheadline**: checklists, reportes de caja y novedades; ideales para un pipeline de noticias.
- **Mattel Creations / Hot Wheels Collectors**: catálogo oficial, drops RLC, reglas de membresía.
- **Comunidades**: Reddit (`r/HotWheels` y afines), foros de Mattel Creations, **The Toy Peddler**, Discord de diecast, grupos de Facebook (incluidos varios en español: HWCA `hwcaforum.mforos.com`, grupos LATAM).
- **GitHub**: `joedots1/fast_wheels` (MIT) — API FastAPI de datos Hot Wheels 2010–2020, útil como referencia de estructura.
- **Hugging Face / Kaggle**: **no hay datasets relevantes** de Hot Wheels (verificado).

### 4.3 Base legal

- "Hot Wheels" y "Mattel" son **marcas registradas**: la app debe declararse **no oficial** y no usar el logotipo de Mattel.
- Las **imágenes de la Wiki son CC BY-SA 3.0**: requieren atribución y compartir-igual; para un producto comercial conviene **fotografiar los autos propios** o usar imágenes propias, y usar la wiki solo como dato de referencia interno.
- Los datos de eBay se usan vía **API oficial**, no scraping.
- Cumplir GDPR/ley local con las fotos del usuario: **limpiar EXIF**, pedir consentimiento antes de enviar cualquier imagen a un servicio en la nube, y ofrecer **modo 100 % local**.

---

## 5. El asistente con IA: qué se puede hacer gratis y cómo

### 5.1 Visión (identificar el auto desde una foto)

| Proveedor | Modelo | Capa gratuita | Uso comercial |
|---|---|---|---|
| **Google Gemini (AI Studio)** | 2.5 Flash (visión) | **250 peticiones/día** | sí, con condiciones |
| **Groq** | Llama 3.2 Vision | límites por minuto/día | sí |
| **OpenRouter** | modelos `:free` con visión | 50–1.000 req/día | según modelo |
| **Hugging Face Inference Providers** | varios VLM | crédito gratuito (~USD 0,10/mes de cómputo) | sí |
| **Cloudflare Workers AI** | modelos de visión | 10.000 neuronas/día | sí |
| **Mistral (Pixtral)**, Together, Fireworks, Cerebras, NVIDIA NIM | VLM | capas gratuitas variables | revisar |
| **Ollama local** | Qwen2.5-VL 7B / LLaVA | **ilimitado, offline** | sí (open weights) |
| **CLIP / sentence-transformers** | embeddings imagen-texto | ilimitado, local | sí |

**Estrategia híbrida recomendada (research/05 §1.4):**
1. La foto se describe con un VLM (Gemini Flash; fallback Groq; offline Ollama).
2. En paralelo, se calcula un **embedding CLIP** de la foto y se compara contra los embeddings del catálogo (pgvector/SQLite-vec) → **top-5 candidatos**.
3. Si hay **código de barras** o **OCR del blister**, ese resultado tiene prioridad (95 %+).
4. El usuario confirma o corrige. Cada corrección se guarda como dato de entrenamiento futuro.

### 5.2 Voz (el asistente que habla y escucha)

**TTS gratis:** **Edge TTS** (gratis, sin API key, voces neuronales en español — recomendado), **Piper** (local), **Kokoro-82M** (local, calidad alta, Apache 2.0), gTTS, espeak-ng. Capas gratuitas de ElevenLabs/Google/Azure/OpenAI existen pero con cuota.

**STT gratis:** **whisper.cpp** (local, MIT, ilimitado), **faster-whisper** (Python, GPU), **Vosk** (ligero, streaming), **Groq Whisper Large v3** (nube, capa gratuita amplia), Google Cloud STT (60 min/mes), Web Speech API del navegador.

**Dos arquitecturas:**
- **Pipeline STT → LLM → TTS**: latencia 1,5–3,5 s, máxima flexibilidad, todo gratis. *Es lo que usa el prototipo.*
- **Live API** (Gemini Live): latencia 300–600 ms, conversación natural, capa gratuita limitada.

En el prototipo ya implementado se usa **`speechSynthesis`** (TTS del sistema, con voz en español) y **Web Speech API** (STT) — funcionan sin backend y sin costo.

### 5.3 Índice de coleccionabilidad v2 (con datos reales, no constantes)

```
Índice (0–100) = (R × 0,30) + (D × 0,25) + (C × 0,20) + (A × 0,15) + (M × 0,10)
```

| Factor | Qué mide y **de dónde sale el dato** |
|---|---|
| **R** Rareza (30%) | clase (STH 72 · TH 55 · Mainline 25) − penalización por re-ediciones del casting (máx. −12) + bonus si es modelo nuevo (+4) y variante (+1,5). Fuente: clase + **conteo de apariciones del casting en el catálogo 2016–2026**. |
| **D** Demanda (25%) | `35 + 65 × (coleccionistas ÷ máximo)`. Fuente: **conteos reales de coleccionistas de HW Price Guide (enero y febrero 2026)**. Cuando no hay medición, se usa un **proxi declarado** por re-ediciones (`18 + 5 × apariciones`). La ficha marca `medido` cuando el dato es real. |
| **C** Condición (20%) | 100 = nuevo en tarjeta · 70 tarjeta dañada · 55 suelto impecable · 40 suelto bueno · 25 jugado. En el catálogo se asume “nuevo en tarjeta”; en la colección del usuario se ajusta con su condición real. |
| **A** Antigüedad (15%) | curva ajustada al rango del catálogo: `(2026 − año) × 5,5`, tope 60. |
| **M** Mercado (10%) | **momentum real enero→febrero 2026** de la demanda (`55 + Δ% × 45`) + 12 si el modelo tiene precio en tienda chilena + 8 si aparece en listados de eBay. Sin señal específica: 40. |

**Qué cambió respecto de la v1:** la v1 dejaba **D vacía** (el índice se renormalizaba sin demanda) y usaba **M = 35 fijo**. La v2 usa datos reales en los dos factores que antes eran constantes y **elimina la renormalización**.

**Estadísticas del catálogo (2.177 registros):** mínimo 37,2 · p10 39,6 · p25 41,3 · **mediana 43,7** · p75 46,1 · p90 47,8 · máximo 63,0 · media 44,0. Por clase: Mainline 43,3 · TH 48,9 · **STH 55,4**.
Como el rango es estrecho por construcción (C aporta 20 puntos fijos), cada ficha muestra además el **percentil** del auto dentro del catálogo, que es lo que da lectura real (“índice 54,9 · percentil 97”).

**Visualizaciones implementadas** (todas en la ficha del auto):
1. **Gauge circular** con el índice y el percentil.
2. **Radar de 5 ejes** (R, D, C, A, M) con grilla de referencia.
3. **Barras por factor** con color por nivel, peso de cada factor y **la fuente del dato** debajo (`medido` cuando es dato real).
4. **Histograma de distribución** del catálogo con una línea marcando dónde cae ese auto.
5. **Barra de la tarjeta** en el catálogo coloreada por nivel (verde ≥58 · ámbar ≥44 · gris por debajo).

**Anti-arbitrariedad:** la fórmula es explícita, cada factor muestra su origen, y la calibración pendiente es la regresión contra precios reales de venta (si R² < 0,6 se revisan los pesos).

### 5.7 Voces y personalidades del asistente

**Motor de voz implementado en `serve.py` (endpoint `/tts`):**

| Motor | Estado verificado | Notas |
|---|---|---|
| **Piper** (neuronal, **local**) | ✅ **funcionando** — voz `es_MX-claude-high` (México, masculina, calidad alta), 63 MB | Gratis, sin API key, **sin internet**, ~1 s por frase (más rápido que tiempo real). Las voces se agregan dejando archivos `.onnx` en `voices/`. |
| **edge-tts** (nube, Microsoft) | ❌ **403 en este entorno** — el endpoint de síntesis rechaza el token (`Sec-MS-GEC`); el reloj está correcto (±3 s) y no hay bloqueo de red: es la rotación de token del servicio | La lista de voces sí responde. Se dejan **es-CL (Lorenzo, Catalina)**, es-MX, es-AR y es-US listas para cuando el servicio lo acepte. |
| **Voces del sistema** (navegador) | ✅ 4 voces en español en esta máquina (es-MX Raúl y Sabina, es-US, es-ES) | Respaldo automático cuando no hay servidor local (por ejemplo, en la PWA publicada en GitHub Pages). |

**Tres personalidades** (cambian el guion, la velocidad y el tono; se guardan en el dispositivo):

1. **Asistente** — neutral, solo datos con fuente.
2. **Pokédex** — formato de entrada de Pokédex (“X, el Super Treasure Hunt legendario… Se le ha visto en la caja A del año 2026… Datos completados”), voz más grave y pausada.
3. **Clarkson** — humor cáustico estilo Jeremy Clarkson **en español latino**, siempre sobre datos reales del auto (“Es un Treasure Hunt, o sea que Mattel escondió uno por caja para que vos compres diez cajas. Astuto.”).

**Sobre las voces originales:** la voz del Pokédex latino y la de Jeremy Clarkson son interpretaciones con derechos de autor y **no se pueden usar ni clonar sin licencia**. Lo que sí está implementado es el **formato y el humor** con una voz neuronal libre. Para clonar una voz propia hace falta un servicio de voz (ElevenLabs y similares) con clave del usuario.

**Muestras de audio reales** generadas con Piper en `muestras/`: `voz_pokedex.wav` (33 s), `voz_clarkson.wav` (28 s), `voz_asistente.wav` (24 s).

### 5.9 Arquitectura celular ↔ asistente (puente + offline)

**Problema:** el celular tiene que consultar al asistente y a los datos, pero a veces no hay red, o la PC (donde viven los datos) está apagada.

**Solución en 3 capas (todas verificadas):**

1. **`agent_bridge.py` — el puente** (donde corre la app y el agente):
   - Sirve la app (`web/`) **y** los endpoints del agente: `/agent/status`, `/agent/ask`, `/agent/answers`, `/agent/push`, `/sync/manifest`, `/sync/file`, `/sync/refresh`.
   - El celular en la misma red abre `http://<ip-pc>:8081/`. La app detecta el puente (badge “asistente”).
   - **El servicio no toca la API del puente** (`sw.js` deja pasar `/agent`, `/sync`, `/tts`), así que las llamadas van directo a la red y no a la caché.

2. **`build/atender_cola.py` — el cerebro local** (sin LLM, sin internet):
   - 10 intenciones implementadas y probadas: ficha/valor de un modelo (en CLP/USD/EUR), caja de un año, código de base, impuestos de importación a Chile, dónde vender (neto por canal), valor de tu colección, top de demanda real, comparación de mercados, qué es el índice.
   - Todo sale de `data/` **con su fuente**; lo que no sabe, **queda en cola** para el agente.

3. **Cola + overlay en la app** (offline de verdad):
   - **Preguntas:** si el puente no responde, la pregunta se guarda en `localStorage` (`hw_cola_local`) y se envía sola (`/agent/push`) cuando vuelve la red. Las respuestas se bajan con `/agent/answers` y se deduplican por ID.
   - **Datos:** al arrancar, la app pregunta por el manifiesto; si la versión cambió, baja los archivos nuevos y los aplica **sobre los embebidos** con el overlay `DATOS_FUENTE` (versión visible en el header). Así las actualizaciones no requieren volver a descargar la app.

**Manejo de errores verificado:** los 3 bugs críticos encontrados en la integración (reesignación de `const CASEBY`/`DEM` en el overlay, `PUENTE="."` que generaba `.agent/status` en vez de `./agent/status`, y el service worker que interceptaba la API) están corregidos y el flujo completo probado en navegador: pregunta → respuesta instantánea → sync de 9 archivos → recarga con datos actualizados → simulación de red caída → pregunta en cola → recuperación.

### 5.10 Herramienta de tendencias activas (`trend_watcher.py`)

**Qué hace:** recolecta datos de múltiples fuentes, calcula un **índice de tendencia compuesto (0-100)**, detecta momentum y genera alertas cuando un modelo de tu colección está subiendo.

**Fuentes y pesos:**

| Fuente | Qué aporta | Peso | Estado verificado |
|---|---|---|---|
| **Google Trends** (pytrends) | Interés relativo 0-100, series temporales 3 meses | 40% | ⚠️ 429 rate limit desde esta IP; la herramienta reintenta con backoff (30s) y si falla, recalcula el índice sin este peso |
| **Reddit RSS** (r/HotWheels) | Menciones de modelos en títulos de posts | 30% | ✅ **funciona** — 5 modelos detectados (Honda Civic Custom ×6, Toyota Supra ×3, Honda S800 Racing ×1, BMW M3 Wagon ×1, Batmobile ×1) |
| **Demanda interna** | Coleccionistas por modelo (HW Price Guide) | 30% | ✅ **funciona** — 20 modelos con datos reales ene+feb 2026 |

**Matching inteligente de Reddit:** genera variantes de cada nombre de modelo (sin año `'59`, últimas 2 palabras, última palabra distintiva) y busca coincidencias en los títulos. Esto detecta menciones como "Finished the Supra" para el modelo `Toyota Supra`.

**Manejo de errores de Google Trends:** batches de 3 términos, 6s entre batches, 3 intentos con backoff de 30s en 429. Si un batch falla, no detiene la ejecución.

**Índice compuesto:** pondera las 3 fuentes. Si una no hay dato, renormaliza con las disponibles. Así el índice siempre es útil aunque Google Trends esté caído.

**Scheduler** (`trend_scheduler.py`): ejecuta el watcher periódicamente (cada 6h por defecto, configurable con `--interval`).

**Integración:**
- Guarda en `data/tendencias_activas.json` con fecha, fuentes y top de cada una.
- Endpoint `/trends` en el puente lo sirve al celular.
- Vista "Tendencias activas" en la app (pestaña Tendencias) carga automáticamente cada 60s con `_cargar_trends_activas()`.
- Alertas cuando un modelo de tu colección supera umbral (índice ≥60 o momentum ≥50).

**Resultado verificado (12-oct-2026 11:10):** 25 modelos analizados, top tendencia global liderado por Ferrari SF90 Stradale (50.0) y Honda Civic Custom (50.0), 94 Toyota Supra detectado por Reddit (25.0). Sin alertas por encima del umbral (la colección de ejemplo no tiene modelos en alta tendencia).

**Limitaciones honestas:**
- Google Trends puede fallar por rate limit; la herramienta lo maneja pero no puede forzarlo.
- Reddit RSS solo ve los últimos ~100 posts de r/HotWheels; menciones de modelos menos populares pueden perderse.
- ML API bloqueada (403 desde curl); se puede agregar vía scraping con navegador (`--browser`).

**Para usar:**
```bash
python build/trend_watcher.py --sync       # recolección + análisis + guardado
python build/trend_scheduler.py --loop      # corre cada 6 horas automáticamente
```

### 5.8 Estimación de valor automática

- **Nunca** preguntarle el precio a un modelo de lenguaje: el precio sale **solo** de datos de ventas.
- **Percentiles**, no un número único: p10 / p25 / p50 / p75 / p90, con mediana como estimación central.
- **Confianza declarada**: alta con ≥10 comparables, media con ≥5, baja con menos. **Regla de oro: mínimo 5 comparables**; con menos, rango amplio y advertencia visible.
- **Limpieza**: filtrar por condición equivalente, descartar outliers (>3 σ), deduplicar por vendedor, normalizar por inflación.
- Mitigación de alucinaciones: el VLM **describe la foto**; el catálogo y las ventas son la **fuente de verdad**.

### 5.5 Costos reales

| Escenario | Costo/mes |
|---|---|
| Usuario único (prototipo, todo local + capas gratuitas) | **USD 0** |
| 1.000 usuarios (capas gratuitas + VPS) | **USD 40–130** |
| 1.000 usuarios (self-hosted con Ollama + whisper local) | **USD 25–50** |

### 5.6 Qué **no** se puede lograr gratis (prometer en consecuencia)

Voz en tiempo real con calidad Gemini Live en producción · reconocimiento 100 % preciso de variantes · **ventas completadas de eBay** (cerrado en febrero de 2025; Marketplace Insights es Business-only) · API de PriceCharting · 1.000 usuarios concurrentes con capas gratuitas · *fine-tuning* de CLIP para Hot Wheels (requiere GPU y dataset etiquetado).

---

## 6. Especificación funcional de la app

### 6.1 Plataformas y superficies

| Superficie | Uso principal | Requisitos |
|---|---|---|
| **Móvil (Android/iOS)** | cazar en la tienda, escanear, consultar valor en el pasillo | cámara, micrófono, offline, sincronización |
| **Escritorio (Windows/macOS/Linux)** | catalogación seria con teclado, gestión de lotes, exportación, análisis | importar CSV, edición masiva, informes |
| **PWA (respaldo web)** | acceso rápido sin instalar, demo, compartir | Web Speech API |

### 6.2 Módulos

**M1 · Catálogo (galería de todos los autos que existen)**
Explorar y filtrar 2.177 registros (hoy) sobre una arquitectura preparada para 61.000+. Filtros por año, serie, clase (Mainline/TH/STH), texto libre; orden por índice, valor o año; ficha con desglose del índice, rango de valor con fuente y estado de la colección. → **ya implementado en `web/galeria_catalogo.html`**.

**M2 · Mi colección (galería de los autos que tengo, con cantidad de cada uno)**
Alta por escaneo o búsqueda; cantidad por modelo/variante; condición; ubicación física; precio de compra y fecha; notas; fotos propias (hasta 6: frente, dorso, base, blister, detalle). Totales: unidades, modelos distintos, valor de referencia, distribución por año y clase. → **ya implementado en `web/galeria_coleccion.html`**.

**M3 · Escáner**
Flujo: foto → candidatos → confirmación → alta con condición. Tres métodos en cascada: **UPC del blister → OCR de la tarjeta → IA de visión + CLIP**. Siempre con porcentaje de confianza y corrección manual. → **flujo maquetado en `web/index.html` (pestaña Escanear); la IA real requiere el backend del §7**.

**M4 · Valoración y plan de venta**
Valor por pieza y de la colección completa; neto después de comisiones por canal; tiempo estimado de venta por tramo; recomendación lote vs individual con el descuento aplicable; simulador "¿cuánto saco si vendo todo hoy?".

**M5 · Asistente con voz**
Preguntas en lenguaje natural sobre el auto en la mano o sobre la colección, respondidas en voz alta y **siempre con la fuente citada**. Comandos ya funcionales en el prototipo: *"cuántos autos tengo"*, *"cuánto vale el Skyline"*, *"cómo vendo mi colección"*.

**M6 · Actualización continua**
Catálogo (nuevos años, nuevos modelos), precios (comparables), checklists TH/STH y noticias. Pipelines programados + versionado + aviso al usuario de "catálogo actualizado a la fecha X".

**M7 · Comunidad (fase 3)**
Perfil público opcional, wishlist compartible, seguimiento, intercambios. Privacidad granular: nada público por defecto.

### 6.3 Flujo de escaneo ideal (research/04 §6.3)

1. El usuario apunta la cámara al paquete o al auto.
2. La IA identifica casting + año + serie + rareza (TH/STH/Chase).
3. La app muestra el match con **% de confianza**.
4. Confianza > 90 % → autocompleta y sugiere "agregar a mi garaje".
5. Confianza < 90 % → **top 3 candidatos**, el usuario elige.
6. Corrección manual de cualquier campo.
7. Detección automática de duplicados.
8. Al guardar, el valor estimado se actualiza en segundo plano.

### 6.4 Estructura de datos de un ítem de colección

```
casting_name · brand · year · series · series_number · assortment
color · wheel_type · rarity (normal|TH|STH|Chase) · variant
condition (MOC|CIB|loose|played) · quantity_owned
purchase_price · purchase_date · current_estimated_value · value_last_updated
storage_location · notes · photos[≤6] · wishlist · traded_away · custom_tags[]
```

---

## 7. Arquitectura técnica

### 7.1 Stack recomendado

| Capa | Tecnología | Por qué |
|---|---|---|
| Móvil | **Flutter** (Android/iOS) | un solo código, cámara/micrófono, Edge TTS, whisper.cpp vía FFI |
| Escritorio | **Flutter Desktop** (o Tauri) | comparte código con móvil; Tauri si se prioriza peso |
| PWA de respaldo | React + Vite | sin instalación; Web Speech API |
| Backend / motor de IA | **Python + FastAPI** | async, rápido de desplegar, ecosistema de IA |
| DB local | **SQLite (+ sqlcipher)** | offline-first, cifrado |
| DB servidor | **PostgreSQL + pgvector** | catálogo global, embeddings, datos de mercado |
| Catálogo distribuido | JSON comprimido versionado | descarga y sync incremental |
| Embeddings | **CLIP** (sentence-transformers) | matching imagen ↔ texto |
| Voz móvil | Edge TTS + whisper.cpp | gratis / local |
| Voz escritorio | Piper + faster-whisper | local, aprovecha GPU |
| Voz tiempo real | Gemini Live API | 300–600 ms |

### 7.2 Diagrama

```
┌──────────────── USUARIO ────────────────┐
│ cámara · micrófono · pantalla táctil    │
└───────────────┬─────────────────────────┘
                ▼
┌──────── APP FLUTTER (móvil / escritorio) ────────┐
│ cámara · whisper.cpp (STT) · Edge TTS/Piper (TTS)│
│ SQLite local: catálogo + colección + embeddings  │
└───────────────┬──────────────────────────────────┘
                │ HTTPS (solo si hay red)
                ▼
┌──────────── BACKEND FastAPI ─────────────┐
│ /vision/identify · /vision/describe      │
│ /voice/stt · /voice/tts · /voice/live    │
│ /catalog/search · /catalog/embeddings    │
│ /value/estimate · /collect/index         │
│ /sync/catalog · /sync/prices             │
│ PostgreSQL + pgvector                    │
└──┬─────────┬─────────┬───────────────────┘
   ▼         ▼         ▼
Gemini    Groq     eBay Browse API /
(vision+  (Whisper hobbyDB / fuentes
 Live)    + Llama) de precios
```

### 7.3 Modelo de datos (SQL)

```sql
CREATE TABLE hotwheels (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, year INTEGER,
  series TEXT, sub_series TEXT, color TEXT, wheel_type TEXT, base_type TEXT,
  tampo TEXT, photo_url TEXT, rarity_score REAL, category TEXT,
  castings_id TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_hw_name ON hotwheels(name);
CREATE INDEX idx_hw_year ON hotwheels(year);
CREATE VIRTUAL TABLE hotwheels_fts USING fts5(name, series, color, content='hotwheels', content_rowid='id');

CREATE TABLE hotwheels_embeddings (
  hotwheels_id INTEGER REFERENCES hotwheels(id) ON DELETE CASCADE,
  embedding vector(512), PRIMARY KEY (hotwheels_id)
);
CREATE TABLE user_collection (
  id INTEGER PRIMARY KEY, hotwheels_id INTEGER REFERENCES hotwheels(id),
  user_id INTEGER NOT NULL, quantity INTEGER DEFAULT 1,
  condition TEXT, purchase_price REAL, purchase_date DATE,
  storage_location TEXT, notes TEXT, photos TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE market_sales (
  id INTEGER PRIMARY KEY, hotwheels_id INTEGER REFERENCES hotwheels(id),
  sale_price REAL NOT NULL, condition TEXT, sale_date DATE,
  source TEXT, listing_url TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE user_photo_embeddings (
  id INTEGER PRIMARY KEY, photo_path TEXT, embedding vector(512),
  hotwheels_id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

> Nota de implementación: `vector(512)` es de pgvector (servidor). En el SQLite local usar **sqlite-vec** con el mismo esquema lógico, y `FTS5` para la búsqueda por texto.

### 7.4 Endpoints

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/vision/identify` | POST | imagen → top-5 candidatos con % de confianza |
| `/api/vision/describe` | POST | imagen → descripción textual (color, tipo, detalles) |
| `/api/voice/stt` | POST | audio → texto |
| `/api/voice/tts` | POST | texto → audio MP3 |
| `/api/voice/live` | WS | conversación en tiempo real (Gemini Live) |
| `/api/catalog/search` | GET | búsqueda por nombre/serie/año |
| `/api/catalog/embeddings` | GET | embeddings para matching local |
| `/api/value/estimate` | POST | model_id + condición → rango con percentiles y confianza |
| `/api/collect/index` | GET | índice de coleccionabilidad con desglose |
| `/api/sync/catalog` | GET | catálogo actualizado (JSON comprimido) |
| `/api/sync/prices` | GET | precios de mercado actualizados |

### 7.5 Capa de abstracción de proveedores

Interfaz `VisionProvider` / `VoiceProvider` con implementaciones intercambiables (Gemini, Groq, OpenRouter, Ollama, whisper.cpp, Piper, Edge TTS). Motivo concreto: las capas gratuitas **cambian sin aviso** — si un proveedor cambia cuotas o desaparece, el reemplazo debe ser una línea de configuración, no una reescritura.

### 7.6 Offline-first

Toda la operación crítica (catálogo, colección, valoración con datos cacheados, TTS, STT) funciona **sin red**. La red solo mejora: comparables frescos, identificación por VLM, sincronización entre dispositivos. Resolución de conflictos: *last-write-wins* por campo, con registro de cambios.

---

## 8. Motor de valoración y tiempos de venta (especificación)

**Entrada:** `model_id`, `condición`, `cantidad`, `estado de tarjeta`.
**Salida:** `{min, p25, mediana, p75, max, confianza, n_comparables, fuente, fecha_dato, tiempo_venta_dias, canal_recomendado, neto_estimado}`.

**Algoritmo:**
1. Buscar comparables: primero por modelo+variante+año; si hay <5, ampliar a la clase (Mainline/TH/STH) y **marcar confianza baja**.
2. Filtrar por condición equivalente y descartar outliers >3 σ.
3. Calcular percentiles. **Mediana = estimación central.**
4. Aplicar el multiplicador de condición: nuevo en tarjeta ×1,00 · tarjeta dañada ×0,70 · loose impecable ×0,55 · loose bueno ×0,40 · loose jugado ×0,25.
5. Calcular el neto por canal con las comisiones reales del §3.4.
6. Devolver el tiempo de venta del tramo correspondiente.
7. Para la colección completa: sumar piezas y aplicar el descuento por volumen del §3.4, mostrando **siempre** las dos cifras (pieza por pieza y en lote).

**Regla anti-fraude interna:** si el rango resultante es más amplio que 3× entre p10 y p90, la app dice *"datos insuficientes"* en lugar de mostrar un número que parezca preciso.

---

## 9. Actualización continua de datos

| Pipeline | Frecuencia | Fuente | Salida |
|---|---|---|---|
| Catálogo anual | semanal (en temporada de anuncios) | API Fandom: `List of YYYY Hot Wheels` | `catalog.json` + imágenes nuevas |
| Treasure Hunts / STH | mensual y al anunciarse cada caja | Fandom: `YYYY Treasure Hunts Series` | `treasure_hunts.json` |
| Precios y comparables | diario | eBay Browse API (5.000 llamadas/día) + hobbyDB | `market_sales` |
| Precios de referencia por clase | semanal | research + guías públicas | `precios_referencia.json` |
| Noticias y checklists | diario | hwcollectorsnews, Lamley, Orange Track Diecast (RSS) | feed interno |
| Calibración del índice | mensual | regresión sobre `market_sales` | pesos del índice |

**Versionado:** el catálogo lleva `version` y `fecha`; la app muestra "Catálogo actualizado al 11/10/2026" y avisa cuando hay una versión nueva. **Salud de fuentes:** si una fuente falla 3 veces seguidas, se marca como degradada y se avisa en el panel de administración (nunca se silencia).

---

## 10. Roadmap

| Fase | Alcance | Entregable | Criterio de aceptación |
|---|---|---|---|
| **F0 — Hecho** | Investigación + catálogo + galerías + prototipo | `research/`, `data/`, `web/*.html` | 2.177 registros cargando con imágenes, filtros y fichas funcionando ✔ |
| **F1 — MVP móvil+escritorio** | Flutter, catálogo offline, colección con cantidades, valoración por clase, TTS/STT del sistema | App instalable | catalogar 50 autos sin red; valor de colección con confianza declarada |
| **F2 — IA real** | Backend FastAPI, Gemini Flash + CLIP + OCR + UPC, top-5 con confianza | Escaneo funcional | ≥60 % de acierto de casting con foto; 95 %+ con UPC |
| **F3 — Mercado** | eBay Browse API, comparables, percentiles, plan de venta, export CSV/JSON | Valoración con datos reales | precio con ≥5 comparables y confianza media/alta |
| **F4 — Social y escala** | cuentas, sync multi-dispositivo, wishlist pública, comunidad | Backend productivo | sync sin pérdida de datos; privacidad por defecto |
| **F5 — Multi-marca** | Matchbox, Mini GT, Tarmac Works, Greenlight, M2, Inno64 | Catálogo ampliado | misma UX en 7 marcas |

---

## 11. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| El reconocimiento por foto es impreciso | alto | top-5 + confirmación del usuario + priorizar UPC/OCR |
| eBay cerró las ventas completadas | alto | combinar Browse API (activos) + hobbyDB + reportes de la comunidad, y **declarar la limitación** |
| Proveedores gratuitos cambian cuotas | medio | capa de abstracción + fallback local (Ollama/CLIP/whisper) |
| Datos de la wiki incompletos o erróneos | medio | validación cruzada con CollectHW/hobbyDB; campo "verificado por la comunidad" |
| Copyright de imágenes y marcas | medio | app no oficial, imágenes propias, atribución CC BY-SA donde corresponda |
| El índice parece arbitrario | medio | desglose visible + calibración por regresión + R² publicado |
| Privacidad de fotos | medio | EXIF fuera, consentimiento explícito, modo 100 % local |
| Falsificaciones en el mercado | medio | guía de verificación + señales de alerta en la ficha |

---

## 12. QA y validación

- **Datos:** contar registros contra la fuente (hoy: 2.177 = 102 STH + 28 TH + 2.047 mainline, con 1.716 imágenes locales verificadas como WEBP válido).
- **UI:** probar en navegador real que la galería renderiza, filtra por clase (STH = 102), busca ("skyline" = 2 resultados) y abre la ficha con desglose del índice — *ya ejecutado*.
- **Valoración:** tests con casos conocidos (mainline común ≈ USD 1–5; STH 2025 ≈ USD 85–250) y verificación de que **nunca** se devuelve un precio sin comparables sin marcarlo como confianza baja.
- **Voz:** comprobar que el TTS elige una voz en español y que el asistente cita la fuente en cada respuesta.
- **Regresión de datos:** cada corrida de los pipelines debe reportar altas/bajas y fallar ruidosamente si un año pierde >10 % de registros.

---

## 13. Multi-moneda y comparación entre mercados

### 13.1 Tipos de cambio cargados (con fuente y fecha)

| Moneda | Valor | Fuente | Fecha |
|---|---|---|---|
| **USD** | base | — | — |
| **CLP** | **1 USD = 981,61 CLP** | mindicador.cl `/api/dolar` (dólar observado, fuente oficial chilena) | 2026-10-09 |
| **EUR** | 1 EUR = 1,13440 USD | exchangerate-api.com (EUR/USD 0,88152) | 2026-09-30 |
| **GBP** | 1 GBP = 1,32312 USD | exchangerate-api.com (GBP/USD 0,755961) | 2026-09-30 |

EUR/CLP (≈1.113,5) y GBP/CLP (≈1.298,5) son **tipos cruzados** calculados, no cotizaciones directas: está declarado así en la app. El selector de moneda convierte **todo** el catálogo, la colección y las calculadoras, y la tasa se muestra siempre con su fuente y su fecha. En el plan: refresco diario del tipo de cambio y caché del último valor conocido para funcionar offline.

### 13.2 Precios reales observados por mercado (asking, no ventas cerradas)

| Mercado | Mainline | Premium / Car Culture | STH |
|---|---|---|---|
| **EE.UU.** | US$1,25 retail · US$1–5 reventa | US$6,95–12,50 unidad · US$29,95–64,99 set de 5 | US$85–250 |
| **Chile** | $1.990–$2.450 (littletoys.cl, isatoyschile.cl) | $6.290 (Car Culture, Lider) · $7.990 (Boulevard) · $12.990 (Premium) | **$15.000–$100.000 CLP** en tienda especializada (minidiecast.cl) |
| **Europa (eBay DE)** | €2–3 retail | ~€8–15 unidad | €80–200 |
| **Reino Unido (eBay UK)** | £4,92 listado típico | £31,58 set de 5 (≈US$41,8) | £38,82 (STH 2026) |

**Lecturas verificadas:** Chile está **1,6–2× sobre el precio de EE.UU.** (un auto de US$1,25 se vende a $1.990–$2.450); Europa 1,8–2,7×; en el Reino Unido los **lotes** se pagan mejor por unidad que en EE.UU. (£1,19–£1,70 por auto en lotes de 30 y 50).

**Por qué difieren** (factores con fuente): aranceles e IVA (19% Chile, 19–21% UE, 20% UK) · logística · tipo de cambio · margen del retail local · oferta y demanda local.

### 13.3 Reglas de importación (calculadora implementada)

- **Chile** — hasta US$500: **solo IVA 19%**, sin arancel. Sobre US$500: **6% de arancel + 19% de IVA sobre el CIF**. Envíos **entre personas naturales (C2C)** de hasta US$500: **exentos** si son ocasionales y no comerciales. Fuente: aduana.cl y sii.cl (Ley N°21.713, vigente desde el 25-oct-2025; antes existía la exención de US$41).
- **Unión Europea** — desde el **1-jul-2026** se eliminó la exención de arancel de €150: se aplica un **arancel fijo temporal de €3 por ítem** en envíos de hasta €150 (hasta el 1-jul-2028), más el IVA de importación que aplica a **todo** bien (19–21% según país). Fuente: taxation-customs.ec.europa.eu (Reglamento (UE) 2026/382), zoll.de.

### 13.4 Comisiones por canal y mercado (usadas por la calculadora de neto)

| Mercado | Canal | Comisión |
|---|---|---|
| EE.UU. | eBay | 13,25% + US$0,40 |
| EE.UU. | Mercari / Whatnot / Facebook / hobbyDB | 10% / 8%+2,9%+US$0,30 / 0% / 0% |
| **Chile** | **MercadoLibre (Clásica)** | **8–17%** + cargo fijo (~$700 hasta $9.990; ~$1.000 hasta $19.990) + envío + IVA 19% sobre la comisión |
| **Chile** | **MercadoLibre (Premium)** | **11–21%** |
| Chile | Facebook Marketplace / feria | 0% |
| Reino Unido | eBay **particular** | **0%** (desde oct-2024) + 2,5% de conversión de moneda (2,75% desde dic-2026) |
| Reino Unido | eBay business | 12,8% + £0,30/£0,40 · categoría Collectables 10,9% |
| Europa | eBay DE business | 10,9% + €0,30 |

---

## 14. Seguimiento uno a uno, alertas y señales de demanda

### 14.1 Modelo de seguimiento (`data/seguimiento.json`)

Cada auto de la colección tiene su propia ficha de seguimiento:

```
modelo · anio · clase · cantidad
valor_actual_usd · valor_anterior_usd
fecha_actualizacion · fuente · confianza · frescura
historial[]  → {fecha, usd, fuente}          ← crece en cada actualización
senales{}    → demanda_coleccionistas_rank, precio_chile_clp, ebay_usd, mercadolibre_clp
alertas{}    → precio_objetivo_usd, cambio_pct, canal_preferido
```

**Frescura** (semáforo visible en la app): verde ≤7 días · ámbar ≤30 · rojo >30 (hay que actualizar antes de vender a ciegas).

### 14.2 Tipos de alerta (implementados y evaluados por `build/refresh_market.py`)

| Tipo | Severidad | Se dispara cuando | Acción sugerida |
|---|---|---|---|
| **VENTA** | alta | el valor alcanza tu precio objetivo | publicar en el canal preferido |
| **DEMANDA** | alta | el modelo está en el top 10 de demanda de coleccionistas | vender individual, no en lote |
| **SUBE / COMPRA** | media | el valor cambió más que tu umbral % | revisar precio / buscar compra |
| **DATOS** | media/baja | datos de más de 30 días, o valor por clase (confianza baja) | actualizar / cargar comparables |

Las reglas son configurables por auto (precio objetivo, % de cambio, canal) y se guardan en el dispositivo.

### 14.3 Señales de demanda reales (no estimadas)

- **Ranking de coleccionistas (HW Price Guide)**, enero y febrero 2026, con el número exacto de coleccionistas que agregaron cada casting. Metodología declarada por la fuente: **mide demanda de colección, no precio de mercado secundario**. Ejemplos: `Ferrari SF90 Stradale` 263 coleccionistas (feb-2026, rank 1), `'83 Chevy Silverado Black Widow` 211, `Ford Mustang GTD` 164.
- **Estos rankings se muestran como insignia `TOP n` en las tarjetas del catálogo**, con un filtro "Solo trending".
- **Precios reales en Chile (CLP)** de tienda especializada, **listados observados en eBay** y **precios retail locales**: todo con fuente y fecha, en la pestaña Tendencias.

### 14.4 Pipeline de actualización (`build/refresh_market.py`)

```
python build/refresh_market.py --evaluate   # sin internet: recalcula frescura y alertas
python build/refresh_market.py --api        # APIs oficiales (config.json con tokens)
python build/refresh_market.py --browser    # colector con navegador real (playwright)
```

- **Modo API:** MercadoLibre (`/sites/MLC/search`, requiere **token gratuito** de developers.mercadolibre.cl) y eBay Browse API (requiere **App ID gratuito** de developer.ebay.com). Agrega **mediana, percentiles, cantidad de muestras, total vendido y confianza** (alta ≥10 comparables, media ≥5, baja <5).
- **Modo navegador:** Playwright sobre la conexión del usuario — es la vía sin credenciales, porque ambos sitios bloquean IP de datacenter pero responden bien desde una IP residencial.
- **Regla de oro heredada:** nunca mostrar un precio puntual sin declarar fuente, fecha y confianza.

### 14.5 Matriz de automatización por marketplace (honesta)

| Marketplace | ¿Automatizable? | Qué se obtuvo | Bloqueo real |
|---|---|---|---|
| MercadoLibre Chile | Solo con token o navegador con sesión | términos más buscados + precios retail locales | **muro de login** para accesos automatizados |
| eBay | API con clave gratuita (solo listados activos) | listados observados de STH/TH y lotes | búsqueda bloqueada a bots; sin ventas cerradas desde feb-2025 |
| Facebook Marketplace | **No** (sin API pública de búsqueda) | — | login obligatorio |
| TikTok (Shop/videos) | **No** (sin API pública de productos) | — | contenido dinámico, sin API |
| hwpriceguide.com | Parcial (artículos públicos) | ranking real de demanda | — |
| Tiendas chilenas especializadas | Sí (HTML simple) | precios reales en CLP de STH/RLC/Car Culture | — |

---

## 15. Códigos de caja (case codes): contenido posible e identificado

### 15.1 Cómo funcionan

- El **código de caja** es una letra (A, B, C… **Q**) impresa en la caja de surtido y en la tarjeta.
- Hay **15 cajas por año**; se **omiten las letras I y O** para no confundirlas con 1 y 0.
- Cada caja trae **~72 autos con duplicados** de los modelos comunes (no son 72 modelos distintos).
- Cada caja incluye **una Treasure Hunt regular** (los coleccionistas estiman ~1 por caja de 72; **no es cifra oficial de Mattel**).
- La **Super Treasure Hunt** es mucho más rara: puede haber una por caja o ninguna.
- **Master Case / Factory Sealed Set:** un ejemplar de todos los modelos del año + recolors + exclusivos + STH, con sello holográfico, solo en Mattel Creations para miembros RLC (~US$600, numerado).

### 15.2 Mapa real caja → TH → STH (2026, dato verificado)

| Caja | Treasure Hunt | Serie · Nº | Super Treasure Hunt en la misma caja |
|---|---|---|---|
| A | '87 Buick Regal GNX | Nightspeed · 9/250 | Drift-Ender |
| B | '92 Dodge Viper RT/10 | Drop Tops · 29/250 | Ford Mustang GTD |
| C | Electro Silhouette | HW EV · 58/250 | Ferrari F40 Competizione |
| D | Hot Wheengs | X-Raycers · 81/250 | '64 Impala |
| E | Cone Shaker | HW Starting Grid · 122/250 | '87 Ford Sierra Cosworth |
| F | 2016 Ford GT Race | Exoticars · 124/250 | Honda Civic Custom |
| G | 2 Jet Z | HW Dream Garage · 147/250 | Custom Otto |
| H | Total Disposal | HW Heavyweights · 162/250 | Lotus Sport Elise |
| J | Amaru GTC | HW Mods · 186/250 | Subaru Impreza |
| K | Sweet Driver | Sweet Rides · 196/250 | '94 Toyota Supra |
| L | Mad Manga | Hot Wheels Let's Race · 217/250 | Nissan Maxima Drift Car |
| M | Ford Model A Custom '31 | Rod Squad · 229/250 | Porsche 911 Carrera RS 2.7 |
| N | Fast Fish | Team Wheels · 238/250 | '23 Ram 1500 |
| P | Nissan Skyline HT 2000GT-X | Screen Time · 244/250 | '70 Plymouth AAR Cuda |
| Q | Gazella GT | Trophy Case · 247/250 | '67 Pontiac Firebird 400 |

Fuente: Hot Wheels Wiki (columna *Case/Wave* de las tablas de Treasure Hunts y Super Treasure Hunts) cruzada con hotwheelstreasure.com (tabla TH↔STH, verificada el 29-sep-2026). La app ya trae **2022–2026** con color de carrocería, tipo de rueda, país y número de colección de cada pieza.

### 15.3 Decodificador de código de base

El código grabado en la **base** del auto (date code) se compone de **una letra = año de fabricación** y **dos dígitos = semana del año**. La tabla publicada cubre **19 letras (2008–2026)**: A=2008 … V=2026. Ejemplo: `M36` → 2019, semana 36 → fabricado entre el 2 y el 8 de septiembre de 2019. Sirve para datar un auto suelto sin tarjeta y detectar variantes de producción entre lotes. La app lo decodifica y el asistente lo responde por voz.

### 15.4 Contenido posible vs contenido identificado

- **Contenido posible** = lo que la fuente pública garantiza: la TH y la STH de cada letra, con su serie, número de colección, color y rueda.
- **Contenido identificado** = lo que el usuario confirma en la app ("marcar identificado") y sus notas por caja; se guarda en el dispositivo y alimenta su propio historial de cacería.
- **Límite declarado:** la composición completa de los 72 autos de cada caja **solo se conoce por reportes de apertura** (canales de unboxing y foros). El producto no la inventa: la pide como dato a la comunidad o la toma de reportes citados.

---

## 16. Apéndices

### 16.1 Estructura del proyecto

```
hotwheels_collector/
├── PLAN_DESARROLLO_APP_HOT_WHEELS.md   ← este documento
├── README.md
├── PROGRESO.md
├── research/
│   ├── 01_lineas_y_coleccionismo.md    (515 líneas)
│   ├── 02_mercado_y_valores.md         (537 líneas)
│   ├── 03_bases_de_datos_y_foros.md    (944 líneas)
│   ├── 04_apps_analisis.md             (582 líneas)
│   ├── 05_ia_asistente_voz_vision.md   (977 líneas)
│   └── raw/                            (wikitext y HTML crudos)
├── data/
│   ├── catalog.json                    (2.177 registros completos)
│   ├── catalog_web.json                (compacto para la app, con imágenes locales)
│   ├── treasure_hunts.json             (TH/STH 2022–2026 con caja, color, rueda, país)
│   ├── cajas.json                      (15 cajas/año 2022–2026: TH y STH por letra + decodificador de códigos base)
│   ├── tendencias.json                 (demanda real de coleccionistas, precios Chile/eBay, cobertura por marketplace)
│   ├── seguimiento.json                (seguimiento uno a uno: valor, historial, señales, alertas)
│   ├── alertas.json                    (salida del motor de alertas)
│   ├── mercados.json                   (monedas, tipos de cambio, precios y comisiones por mercado, importación)
│   ├── precios_referencia.json         (rangos + 34 modelos + comisiones + tiempos)
│   ├── owned_collection.json           (plantilla de colección — EJEMPLO)
│   ├── image_urls.json / image_local.json
│   └── catalog_raw_fandom.json
├── build/
│   ├── build_app.py                    (generador reproducible de las 3 páginas)
│   └── refresh_market.py               (motor de actualización y alertas: --evaluate | --api | --browser)
└── web/
    ├── index.html                      (app: 9 pestañas)
    ├── galeria_catalogo.html           (galería del catálogo + cajas + tendencias)
    ├── galeria_coleccion.html          (colección + seguimiento + valoración + mercados)
    └── img/                            (1.673 imágenes WEBP)
```

### 13.2 Fuentes principales (listado completo en cada informe)

Hot Wheels Wiki / Fandom (`hotwheels.fandom.com`, CC BY-SA 3.0) · hobbyDB (`hobbydb.com`) · eBay Seller Center (`ebay.com/sellercenter/selling/seller-fees`) · autoevolution (`autoevolution.com/news/hot-wheels-super-treasure-hunt-prices-2025-vs-2024-253713.html`) · resellcalendar · blog.hobbydb.com · iCollectEverything · RarityFinder · Yonkers Times · UnderpricedAI · PriceCharting API docs · Mattel Creations · Google AI (Gemini) pricing y rate limits · Groq rate limits · OpenRouter limits · Hugging Face Inference Providers · Cloudflare Workers AI · Ollama · whisper.cpp · faster-whisper · Vosk · Edge TTS · Piper · Kokoro · App Store y Google Play (fichas y reseñas de las apps competidoras) · Reddit r/HotWheels.

### 13.3 Próximo paso concreto

1. **Cargar tu colección real** en `data/owned_collection.json` (o directamente en la app) para que la galería de colección y la valoración reflejen lo que realmente tenés.
2. Elegir la plataforma de la F1 (Flutter es la recomendación) y arrancar el MVP.
3. Conectar el backend de IA de la F2 (Gemini Flash + CLIP) sobre el catálogo que ya existe.

---

**Advertencia de precisión:** los rangos de valor por clase son **referenciales** (confianza baja) hasta que el motor cargue comparables de ventas del modelo exacto. Toda cifra de este documento proviene de las fuentes citadas en los informes de `research/`; las cuotas de las APIs gratuitas pueden cambiar sin aviso — verificar la documentación oficial antes de comprometerse en producción.
