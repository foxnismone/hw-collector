# ACTUALIZACION_OCR_SCRAPING.md — OCR con cámara, scraping global y actualización semanal

> Actualización de la app HW Collector: escaneo de códigos Hot Wheels con cámara, búsqueda automática en internet si el código no existe, y actualización semanal de la base de datos.
> Fecha: 12-oct-2026 · Estado: **propuesta de implementación**

---

## 1. Resumen ejecutivo

Se implementarán tres capacidades nuevas:

1. **OCR con cámara**: escanear códigos de Hot Wheels (asortación, modelo, case) usando la cámara del celular o PC
2. **Scraping de rescate**: si el código no existe en la base local, buscar automáticamente en internet (Reddit, catálogos comunitarios, Marketplaces) e integrar el dato a la base global
3. **Actualización semanal**: una tarea programada que actualiza todos los datos de la app (catálogo, precios, tendencias) para mantenerse al día

### Flujo completo

```
Usuario escanea código con cámara
        ↓
¿Existe en la base local?
   ├─ Sí → Mostrar ficha + opciones (agregar a colección / ver datos)
   └─ No → Scraping automático en internet
              ↓
         ¿Encontrado?
              ├─ Sí → Guardar en base global + mostrar ficha
              └─ No → Sugerir alternativas (nombre, año, foto)
                        ↓
                   Usuario confirma → Agregar manualmente

Actualización semanal (domingo 3am)
        ↓
Actualiza catálogo, precios, tendencias, nuevos lanzamientos
```

---

## 2. OCR con cámara — Especificación técnica

### 2.1 Qué código leer

Hot Wheels tiene tres tipos de códigos relevantes:

| Tipo de código | Ejemplo | Dónde está | Qué revela |
|---|---|---|---|
| **Asortación (Assortment)** | `L2593`, `C4982`, `5785` | Reverso del card, sobre el código de barras | Tipo de card (USA, internacional, corta) |
| **Número de modelo (Toy #)** | `FRN78`, `L2593` | Hang tab (lengüeta) | Identificador único del modelo |
| **Case code** | `L2593-976K PN` | Caja de cartón | Asortación + mix + fecha de producción |

### 2.2 Herramientas evaluadas

| Herramienta | Tipo | Offline | Formatos | Performance | Licencia |
|---|---|---|---|---|---|
| **Tesseract.js v5** | OCR | ✅ WASM | Texto | ~1-2s por imagen | Apache 2.0 |
| **ZXing** | Código de barras | ✅ | 1D (C128, EAN, UPC), 2D (QR, DataMatrix) | Rápido, en tiempo real | Apache 2.0 |
| **Quagga2** | Código de barras | ✅ | 1D (C128, EAN, UPC, Code 39) | Medio, en tiempo real | MIT |
| **Dynamsoft Barcode Reader** | Código de barras | ✅ | 1D/2D completo | Muy rápido | Comercial (pago) |
| **Scandit** | Código de barras | ✅ | 1D/2D completo | Muy rápido | Comercial (pago) |

### 2.3 Recomendación: Tesseract.js + ZXing

**Combinación óptima:**

| Capa | Herramienta | Por qué |
|---|---|---|
| **Lectura de código de barras** | ZXing | Más rápido, más confiable, nativo para barras |
| **OCR de texto** | Tesseract.js | Lee texto impreso (asortación, modelo, case) |

**¿Por qué ZXing para barcodes?**
- Soporta C128 (el código de barras de Hot Wheels), EAN, UPC, QR
- Funciona en tiempo real con video (no requiere foto fija)
- Apache 2.0 (libre)
- Funciona en Chrome, Firefox, Safari, Edge

**¿Por qué Tesseract.js para OCR?**
- Lee texto impreso en el card (ej: "L2593", "Asst. C4982", "FRN78")
- Usa WebAssembly (funciona offline en el navegador)
- Apache 2.0 (libre)
- Puede entrenarse con datos de Hot Wheels si es necesario

### 2.4 Arquitectura de escaneo

```javascript
// Flujo de escaneo
async function escanearCodigo() {
  // 1. Iniciar cámara
  const video = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: 'environment' }
  });
  
  // 2. Escanear con ZXing (barcodes)
  const zx = new ZXing.BrowserMultiFormatReader();
  zx.decodeFromVideoDevice(undefined, video, (result) => {
    if (result) {
      codigoDetectado = result.getText();
      procesarCodigo(codigoDetectado);
    }
  });
  
  // 3. Si no hay barcode, capturar frame para OCR
  // (usuario presiona botón de foto)
  const captura = await capturarFrame(video);
  const texto = await tesseract.recognize(captura, 'eng');
  procesarTextoOCR(texto.data.text);
}
```

### 2.5 Integración en la app

**Nueva pestaña o modal: "Escanear"**

```
┌─────────────────────────────────────┐
│  📷 Escanear Hot Wheels             │
│                                     │
│  ┌───────────────────────────────┐  │
│  │                               │  │
│  │     Vista previa de cámara    │  │
│  │                               │  │
│  └───────────────────────────────┘  │
│                                     │
│  Apuntá al código de barras o al    │
│  texto del card (asortación/modelo) │
│                                     │
│  [📷 Capturar]  [✕ Cerrar]         │
└─────────────────────────────────────┘
```

**Resultado del escaneo:**

```
┌─────────────────────────────────────┐
│  Código detectado: L2593            │
│                                     │
│  Modelo: FRN78 '18 Dodge Challenger │
│  Serie: Muscle Mania                │
│  Case: K                            │
│                                     │
│  [+ Agregar a mi colección]        │
│  [Ver ficha completa]               │
│  [Buscar en internet] ← si no existe │
└─────────────────────────────────────┘
```

---

## 3. Scraping de rescate — Cuando el código no existe

### 3.1 Cuándo se activa

Cuando el código escaneado **no existe** en la base local (`catalog_web.json`), se activa el scraping automático:

```
Código L2593-XXXX no encontrado
        ↓
¿Es un formato válido?
   ├─ No → "Código no válido, revisá que esté completo"
   └─ Sí → Scraping automático
```

### 3.2 Fuentes de scraping (ordenadas por prioridad)

| Prioridad | Fuente | Qué busca | URL |
|---|---|---|---|
| 1 | **SmartWheelers** | Modelo por asortación o código | https://www.smartwheelers.com |
| 2 | **Hot Wheels Wiki** | Modelo por nombre o año | https://hotwheels.fandom.com |
| 3 | **HW Price Guide** | Modelo + valor | https://www.hwpriceguide.com |
| 4 | **Reddit r/HotWheels** | Discusiones, fotos, valor | https://reddit.com/r/HotWheels |
| 5 | **eBay** | Ventas recientes (valor) | https://www.ebay.com |
| 6 | **Mercado Libre Chile** | Precios en CLP | https://www.mercadolibre.cl |
| 7 | **Diecast Direct** | Catálogo completo | https://www.diecastdirect.com |

### 3.3 Estrategia de scraping

```python
# Pseudocódigo del scraper de rescate
def buscar_en_internet(codigo):
    # 1. Buscar en SmartWheelers (comunidad de coleccionistas)
    resultado = scrapear_smartwheelers(codigo)
    if resultado:
        return normalizar(resultado)
    
    # 2. Buscar en Hot Wheels Wiki
    resultado = scrapear_hw_wiki(codigo)
    if resultado:
        return normalizar(resultado)
    
    # 3. Buscar en HW Price Guide
    resultado = scrapear_hwpriceguide(codigo)
    if resultado:
        return normalizar(resultado)
    
    # 4. Buscar en eBay
    resultado = scrapear_ebay(codigo)
    if resultado:
        return normalizar(resultado)
    
    # 5. Buscar en Mercado Libre
    resultado = scrapear_mercadolibre(codigo)
    if resultado:
        return normalizar(resultado)
    
    return None  # No encontrado en ninguna fuente
```

### 3.4 Herramientas de scraping (backend)

| Herramienta | Uso | Licencia |
|---|---|---|
| **Cheerio** | Parser HTML rápido (sitios estáticos) | MIT |
| **Puppeteer** | Sitios con JS (eBay, Mercado Libre) | Apache 2.0 |
| **Playwright** | Multi-browser, más robusto | Apache 2.0 |
| **node-fetch** | HTTP requests | MIT |

### 3.5 Estructura del scraper

```javascript
// build/scraper_rescate.js
const cheerio = require('cheerio');
const fetch = require('node-fetch');

async function buscarEnSmartWheelers(codigo) {
  const url = `https://www.smartwheelers.com/search?q=${encodeURIComponent(codigo)}`;
  const res = await fetch(url, { headers: { 'User-Agent': 'HWCollector/1.0' } });
  const html = await res.text();
  const $ = cheerio.load(html);
  
  // Extraer datos del primer resultado
  const nombre = $('.product-title').first().text().trim();
  const asortacion = $('.assortment-code').first().text().trim();
  const año = $('.year').first().text().trim();
  
  return { nombre, asortacion, año, fuente: 'SmartWheelers' };
}

async function buscarEnHWPriceGuide(codigo) {
  const url = `https://www.hwpriceguide.com/search?query=${encodeURIComponent(codigo)}`;
  const res = await fetch(url, { headers: { 'User-Agent': 'HWCollector/1.0' } });
  const html = await res.text();
  const $ = cheerio.load(html);
  
  // Extraer datos
  const nombre = $('.car-name').first().text().trim();
  const valor = $('.price').first().text().trim();
  
  return { nombre, valor, fuente: 'HW Price Guide' };
}

// ... más scrapers
```

### 3.6 Integración en la app

**Flujo de rescate:**

```
Código no encontrado
        ↓
Mostrando: "Buscando en internet..."
        ↓
┌─────────────────────────────────────┐
│  🔍 Buscando en internet...         │
│                                     │
│  [SmartWheelers] ✓                 │
│  [Hot Wheels Wiki] ✓               │
│  [HW Price Guide] ✓                │
│  [eBay] ⏳                          │
│  [Mercado Libre] ⏳                │
└─────────────────────────────────────┘
        ↓
Encontrado en SmartWheelers
        ↓
┌─────────────────────────────────────┐
│  ✅ Modelo encontrado               │
│                                     │
│  FRN78 '18 Dodge Challenger        │
│  Serie: Muscle Mania                │
│  Año: 2024                          │
│  Valor: $15 CLP                     │
│  Fuente: SmartWheelers              │
│                                     │
│  [+ Agregar a mi colección]        │
│  [Ver ficha completa]               │
│  [Guardar en base global]           │
└─────────────────────────────────────┘
```

---

## 4. Actualización semanal — Todos los datos de la app

### 4.1 Qué se actualiza

| Dato | Fuente | Frecuencia | Método |
|---|---|---|---|
| **Catálogo (nuevos modelos)** | Mattel, SmartWheelers, HW Wiki | Semanal | Scraping |
| **Precios (valor de mercado)** | eBay, Mercado Libre, HW Price Guide | Semanal | Scraping |
| **Tendencias** | Google Trends, Reddit, Twitter | Semanal | API + Scraping |
| **Cajas (assortments)** | HW Wiki, Reddit | Semanal | Scraping |
| **Índice de coleccionabilidad** | Interno (basado en datos) | Semanal | Cálculo |
| **Historias y datos** | HW Wiki, foros | Semanal | Scraping |

### 4.2 Arquitectura de actualización

```
┌─────────────────────────────────────────────────────────────┐
│                    ACTUALIZACIÓN SEMANAL                     │
│                      (Domingo 3:00 AM)                       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Scraper      │   │  Scraper      │   │  Scraper      │
│  Catálogo     │   │  Precios      │   │  Tendencias   │
│  (SmartWheelers)│   │  (eBay, ML)  │   │  (Google, Reddit)│
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ↓
                  ┌───────────────────┐
                  │  Base de datos    │
                  │  (catalog_web.json)│
                  └───────────────────┘
                              │
                              ↓
                  ┌───────────────────┐
                  │  Build app        │
                  │  (build_app.py)   │
                  └───────────────────┘
                              │
                              ↓
                  ┌───────────────────┐
                  │  Deploy           │
                  │  (GitHub Pages)   │
                  └───────────────────┘
```

### 4.3 Herramientas de actualización

| Herramienta | Uso |
|---|---|
| **node-cron** | Programar tarea semanal en Node.js |
| **GitHub Actions** | Ejecutar build + deploy automático |
| **Puppeteer/Playwright** | Scraping de sitios dinámicos |
| **Cheerio** | Scraping de sitios estáticos |
| **pytrends** | Google Trends API |

### 4.4 GitHub Actions workflow

```yaml
# .github/workflows/weekly-update.yml
name: Actualización Semanal
on:
  schedule:
    - cron: '0 3 * * 0'  # Domingo 3:00 AM
  workflow_dispatch:  # También manual

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Instalar dependencias
        run: |
          pip install -r requirements.txt
          pip install pytrends
      
      - name: Scrapear catálogo
        run: python build/scraper_catalogo.py
      
      - name: Scrapear precios
        run: python build/scraper_precios.py
      
      - name: Scrapear tendencias
        run: python build/trend_watcher.py
      
      - name: Actualizar índice
        run: python build/actualizar_indice.py
      
      - name: Reconstruir app
        run: python build/build_app.py
      
      - name: Commit y push
        run: |
          git add data/ web/
          git commit -m "Actualización semanal: $(date +%Y-%m-%d)"
          git push
```

### 4.5 Datos que se actualizan en cada build

| Archivo | Contenido | Tamaño actual |
|---|---|---|
| `data/catalog_web.json` | Catálogo completo de autos | ~2177 registros |
| `data/precios_referencia.json` | Valores de referencia | ~2177 registros |
| `data/tendencias.json` | Tendencias de búsqueda | ~50 términos |
| `data/mercados.json` | Precios en CLP/USD/EUR | ~2177 registros |
| `data/cajas.json` | Cajas y assortments | ~100 registros |
| `data/indice.json` | Índice de coleccionabilidad | ~2177 registros |
| `data/historias.json` | Historias y curiosidades | ~500 registros |
| `data/tendencias_activas.json` | Tendencias activas | ~20 registros |

---

## 5. Mejoras adicionales identificadas

### 5.1 De la investigación

| Mejora | Fuente | Impacto |
|---|---|---|
| **Escaneo de código de barras con ZXing** | Comparativa de scanners | Más rápido y confiable que OCR para barcodes |
| **OCR con Tesseract.js v5** | BestOfJS | Lee texto del card offline |
| **Scraping con Cheerio + Puppeteer** | Olostep, Oxylabs | Cheerio para estáticos, Puppeteer para dinámicos |
| **GitHub Actions para CI/CD** | GitHub | Automatiza build + deploy semanal |
| **DiceBear para avatares** | DiceBear | Avatares deterministas sin backend |
| **Hunt64 como referencia** | Hunt64 app | App competidora con IA scanner (julio 2026) |
| **HW Price Guide** | hwpriceguide.com | 22,000 autos con precios reales |
| **SmartWheelers** | smartwheelers.com | Base de conocimiento de Hot Wheels |

### 5.2 Funcionalidades futuras (no críticas)

| Funcionalidad | Descripción | Prioridad |
|---|---|---|
| **Escaneo de foto del auto** | Identificar el modelo por foto (no solo código) | Media |
| **Comparación de precios** | Mostrar precio en eBay, ML, HW Price Guide simultáneamente | Media |
| **Alertas de precio** | Notificar cuando un auto de tu colección baja de precio | Baja |
| **Marketplace integrado** | Vender autos directamente desde la app | Baja |
| **Reconocimiento de imagen** | Foto del auto → identificar modelo (ML) | Baja |

---

## 6. Plan de implementación

### Fase 1: OCR con cámara (semana 1)

| Tarea | Archivo | Horas |
|---|---|---|
| Integrar ZXing | `web/vendor/zxing.js` | 2 |
| Integrar Tesseract.js | `web/vendor/tesseract.js` | 2 |
| Crear modal de escaneo | `build/build_app.py` | 4 |
| Procesar código escaneado | `build/build_app.py` | 3 |
| Mostrar ficha o error | `build/build_app.py` | 2 |
| **Total** | | **13** |

### Fase 2: Scraping de rescate (semana 2)

| Tarea | Archivo | Horas |
|---|---|---|
| Crear scraper SmartWheelers | `build/scraper_rescate.py` | 3 |
| Crear scraper HW Wiki | `build/scraper_rescate.py` | 2 |
| Crear scraper HW Price Guide | `build/scraper_rescate.py` | 2 |
| Crear scraper eBay | `build/scraper_rescate.py` | 3 |
| Crear scraper Mercado Libre | `build/scraper_rescate.py` | 3 |
| Integrar en app | `build/build_app.py` | 4 |
| Guardar en base global | `build/build_app.py` | 2 |
| **Total** | | **19** |

### Fase 3: Actualización semanal (semana 3)

| Tarea | Archivo | Horas |
|---|---|---|
| Crear scraper de catálogo | `build/scraper_catalogo.py` | 4 |
| Crear scraper de precios | `build/scraper_precios.py` | 4 |
| Crear scraper de tendencias | `build/trend_watcher.py` | 3 |
| Crear GitHub Actions | `.github/workflows/weekly-update.yml` | 2 |
| Probar pipeline completo | | 3 |
| **Total** | | **16** |

### Fase 4: Perfil de coleccionista (semana 4)

| Tarea | Archivo | Horas |
|---|---|---|
| Agregar campos al esquema | `supabase/02_perfil_extension.sql` | 1 |
| Actualizar cliente Supabase | `web/js/supabase-client.js` | 2 |
| Actualizar UI del perfil | `build/build_app.py` | 4 |
| Avatar con DiceBear | `build/build_app.py` | 2 |
| Bio y tipo de coleccionista | `build/build_app.py` | 3 |
| **Total** | | **12** |

---

## 7. Verificación

### Tests de OCR

| # | Test | Esperado |
|---|---|---|
| 1 | Escanear código de barras L2593 | Detecta L2593 |
| 2 | Escanear texto "Asst. C4982" | Detecta C4982 |
| 3 | Escanear código no válido | "Código no válido" |
| 4 | Escanear sin cámara | "No se detectó cámara" |
| 5 | Escanear con luz baja | Sugerir mejor iluminación |

### Tests de scraping

| # | Test | Esperado |
|---|---|---|
| 1 | Código no existe → scraping | Busca en 3 fuentes |
| 2 | Encontrado en SmartWheelers | Muestra datos |
| 3 | No encontrado en ninguna | "No encontrado en internet" |
| 4 | Timeout de red | Reintentar con backoff |

### Tests de actualización

| # | Test | Esperado |
|---|---|---|
| 1 | Ejecutar scraper catálogo | Actualiza catalog_web.json |
| 2 | Ejecutar scraper precios | Actualiza precios_referencia.json |
| 3 | Ejecutar scraper tendencias | Actualiza tendencias.json |
| 4 | GitHub Actions semanal | Build + push automático |

---

## 8. Referencias

**OCR y escaneo**
- Tesseract.js · https://www.npmjs.com/package/tesseract.js
- ZXing · https://github.com/zxing-js/library
- Quagga2 · https://github.com/errerruelo/quagga2

**Scraping**
- Olostep — JavaScript Web Scraping Guide · https://www.olostep.com/blog/javascript-web-scraping
- Oxylabs — Node.js Web Scraping · https://oxylabs.io/blog/javascript-web-scraping
- Thunderbit — Best Practices · https://thunderbit.com/blog/nodejs-web-scraping-best-practices

**Fuentes de datos Hot Wheels**
- SmartWheelers · https://www.smartwheelers.com
- HW Price Guide · https://www.hwpriceguide.com
- Hot Wheels Wiki · https://hotwheels.fandom.com
- Diecast Direct · https://www.diecastdirect.com

**Competencia y referencia**
- Hunt64 — AI Scanner (julio 2026) · https://hunt64.app
- HW Showcase — Mattel's app · https://www.mattel.com

**Avatares**
- DiceBear · https://www.dicebear.com

---

*Parte del plan de desarrollo en `../PLAN_DESARROLLO_APP_HOT_WHEELS.md`*
