# Informe Técnico: Stack de IA Gratuito/Bajo Costo para Asistente con Voz y Visión — Hot Wheels Collector

**Fecha:** 2026-10-11  
**Autor:** Investigación Hermes Agent  
**Estado:** Documento de investigación técnica  
**Contexto:** App de coleccionistas Hot Wheels (móvil Android/iOS + escritorio Windows) que debe: (a) tomar/recibir una FOTO de un auto y reconocerlo contra un catálogo, (b) mostrar una BARRA DE ÍNDICE DE COLECCIONABILIDAD y un VALOR ESTIMADO, (c) tener un ASISTENTE CON VOZ que hable y escuche, (d) actualizarse con información de la red. Todo en español.

---

## Tabla de Contenidos

1. [Visión por Computadora para Reconocer el Auto](#1-visión-por-computadora-para-reconocer-el-auto)
2. [Voz: TTS y STT](#2-voz-tts-y-stt)
3. [Motor de Recomendación / Índice de Coleccionabilidad](#3-motor-de-recomendación--índice-de-coleccionabilidad)
4. [Estimación de Valor Automática](#4-estimación-de-valor-automática)
5. [Arquitectura Técnica Concreta](#5-arquitectura-técnica-concreta)
6. [Límites y Riesgos](#6-límites-y-riesgos)
7. [Fuentes y Referencias](#7-fuentes-y-referencias)

---

## 1. Visión por Computadora para Reconocer el Auto

### 1.1 APIs Gratuitas con Capa Gratuita

#### Google Gemini API (AI Studio)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Modelos con visión gratuitos** | Gemini 2.5 Flash, 2.5 Flash-Lite, 2.0 Flash, 2.0 Flash-Lite, 2.5 Pro (limitado) | [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| **RPM Free (2.5 Flash)** | 10 RPM | [ai.google.dev/gemini-api/docs/rate-limits](https://ai.google.dev/gemini-api/docs/rate-limits) |
| **RPD Free (2.5 Flash)** | 250 RPD | idem |
| **RPM Free (2.5 Flash-Lite)** | 15 RPM | idem |
| **RPD Free (2.5 Flash-Lite)** | 1,000 RPD | idem |
| **RPM Free (2.5 Pro)** | 2 RPM (diciembre 2025: ajuste a 5 RPM) | [aifreeapi.com](https://www.aifreeapi.com/en/posts/gemini-advanced-rate-limit) |
| **RPD Free (2.5 Pro)** | 50 RPD | idem |
| **Requiere tarjeta** | No para Free Tier | [ai.google.dev](https://ai.google.dev/gemini-api/docs/billing) |
| **Uso comercial** | Sí (sujeto a ToS) | idem |
| **EU/EEA/UK/CH** | No disponible en Free Tier | [spurnow.com](https://www.spurnow.com/en/posts/is-gemini-api-free) |
| **Licencia** | Google ToS; output es de tu propiedad (verificar ToS actual) | idem |

**Nota:** Las cuotas de Gemini han cambiado frecuentemente. En diciembre 2025 hubo ajustes significativos. Verificar siempre la documentación oficial vigente.

#### Groq API

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Modelos con visión** | Llama 3.2 11B Vision, Llama 3.2 90B Vision | [artificial-intelligence-wiki.com](https://artificial-intelligence-wiki.com/generative-ai/large-language-models/groq-api-guide/) |
| **Whisper Large v3** | STT gratuito: 20 RPM, 2K RPD, 28.8K ASD (audio segundos/día) | [console.groq.com/docs/rate-limits](https://console.groq.com/docs/rate-limits) |
| **Whisper Large v3 Turbo** | 20 RPM, 2K RPD | idem |
| **Free Tier general** | Sin tarjeta, límites por modelo (~14K RPD en modelos comunes) | [console.groq.com](https://console.groq.com/settings/billing/plans) |
| **Uso comercial** | Sí (plan free para testing; Developer plan para producción) | idem |
| **Licencia** | Variada por modelo (Llama Community License, Apache 2.0) | idem |

#### OpenRouter

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Modelos :free con visión** | Multiples (ver openrouter.ai/models?max_price=0) | [openrouter.ai/docs](https://openrouter.ai/docs/api_reference/limits) |
| **RPM free (modelos :free)** | 20 RPM | idem |
| **RPD free (sin créditos comprados)** | 50 RPD | idem |
| **RPD free (con ≥$10 en créditos)** | 1,000 RPD | idem |
| **Uso comercial** | Sujeto a ToS de cada modelo y de OpenRouter | idem |
| **NOTA** | Los modelos :free tienen "low rate limits" y "usually not suitable for production" | [openrouter.ai/docs/faq](https://openrouter.ai/docs/faq) |

#### Hugging Face Inference Providers

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Créditos mensuales free** | $0.10/mes (Free), $2.00/mes (PRO) | [huggingface.co/docs/inference-providers](https://huggingface.co/docs/inference-providers/pricing) |
| **Enfoque (julio 2025)** | hf-inference: CPU (embeddings, text-classification). GPU: vía partners (Groq, Together, Fireworks, Cerebras) | idem |
| **Modelos con visión** | Miles (CLIP, LLaVA, Qwen2-VL, Pixtral, etc.) vía Hub | idem |
| **Uso comercial** | Depende de la licencia del modelo | idem |
| **NOTA** | $0.10/mes es extremadamente bajo para producción | idem |

#### Mistral AI (Pixtral)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Pixtral 12B** | Open weights Apache 2.0, 12B params, visión + texto | [playground.roboflow.com](https://playground.roboflow.com/models/mistral) |
| **API gratuita (La Plateforme)** | Existió free tier; Pixtral deprecated 2 Dic 2025, API retirement 31 Dic 2025 | [ai-tldr.dev](https://ai-tldr.dev/models/pixtral-12b/) |
| **Self-hosting** | Gratis (Apache 2.0) vía vLLM o mistral-inference | idem |
| **Uso comercial** | Sí (licencia Apache 2.0) | idem |
| **NOTA** | La API gratuita de Pixtral ya NO está disponible (retirada dic 2025). Solo self-hosting | idem |

#### Cloudflare Workers AI

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Neuronas gratis/día** | 10,000 Neuronas/día | [developers.cloudflare.com](https://developers.cloudflare.com/workers-ai/platform/pricing/) |
| **Precio** | $0.011 / 1,000 Neuronas (sobre free tier) | idem |
| **Modelos con visión** | Limitados (text generation, embeddings, some image models) | idem |
| **Requests Workers Free** | 100,000/día | [developers.cloudflare.com/workers](https://developers.cloudflare.com/workers/platform/limits/) |
| **Uso comercial** | Sí | idem |

#### Together AI

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Free trial** | $1 credit en signup (julio 2025: discontinued free trial, min $5 prepaid) | [chiri.ai](https://chiri.ai/chiri-atlas/together-ai) |
| **Modelos con visión** | Llama 4 Scout, Llama 4 Maverick, Llama 3.2 Vision | [support.together.ai](https://support.together.ai/articles/2644979080-what-models-does-together-ai-support) |
| **Uso comercial** | Sí | idem |
| **NOTA** | Ya NO hay free tier permanente (julio 2025) | idem |

#### Fireworks AI

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Free credits** | $1 en signup | [similarlabs.com](https://similarlabs.com/p/fireworks-ai) |
| **Modelos con visión** | Qwen3 VL, Llama 4, visión-language models | [chatforest.com](https://chatforest.com/reviews/fireworks-ai-inference-fine-tuning-platform/) |
| **Uso comercial** | Sí | idem |
| **NOTA** | $1 es muy poco para producción | idem |

#### Cerebras AI

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Free trial** | $5 credits, expira 30 días | [cerebras.ai/pricing](https://www.cerebras.ai/pricing) |
| **Requiere tarjeta** | Sí (para activar el trial) | [freellm.net](https://freellm.net/providers/cerebras) |
| **Uso comercial** | No (solo trial 30 días) | idem |
| **NOTA** | Cerebras eliminó su free tier sin tarjeta el 17 Ago 2026 | [prompthacker.ai](https://prompthacker.ai/free-llm) |

#### NVIDIA NIM

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Free tier** | ~40 RPM, sin facturación por token | [aihola.com](https://aihola.com/article/nvidia-nim-free-api-models) |
| **Acceso** | NVIDIA Developer Program (gratis) | [docs.api.nvidia.com](https://docs.api.nvidia.com/nim/docs/run-anywhere) |
| **Uso comercial** | NO (solo prototyping; producción requiere NVIDIA AI Enterprise desde $4,500/GPU/año) | idem |
| **Modelos con vision** | Varios (Llama, Mistral, etc.) | idem |

### 1.2 Alternativas On-Device (Sin Internet)

#### Ollama + Modelos de Visión

| Modelo | Tamaño | Uso recomendado | Fuente |
|--------|--------|-----------------|--------|
| **LLaVA (1.6)** | 7B, 13B, 34B | Descripción general de imágenes, VQA | [ollama.com/blog/vision-models](https://ollama.com/blog/vision-models) |
| **Qwen2.5-VL** | 3B, 7B, 32B, 72B | OCR, análisis de texto en imágenes, razonamiento visual | [ollama.com/library/qwen2.5vl](https://ollama.com/library/qwen2.5vl) |
| **Llama 3.2 Vision** | 11B, 90B | Razonamiento visual avanzado | [ollama.com/library](https://ollama.com/library?c=vision) |
| **moondream2** | ~2B | Edge devices, móviles de gama baja | idem |

**Requisitos de hardware:**
- **7B (FP16):** ~8 GB VRAM / ~10 GB RAM
- **7B (INT4):** ~5 GB VRAM / ~6 GB RAM
- **3B (INT4):** ~3 GB VRAM / ~4 GB RAM
- **CPU only:** Usable pero lento (1-5 tokens/seg para 7B)

#### Frameworks On-Device

| Framework | Uso | Plataformas | Fuente |
|-----------|-----|-------------|--------|
| **Google ML Kit** | OCR, barcode, image labeling, object detection | Android, iOS | [developer.android.com/ai](https://developer.android.com/ai/overview) |
| **MediaPipe** | Image classification, embedding, object detection | Android, iOS, Python, Web | [developers.google.com/edge/mediapipe](https://developers.google.com/edge/mediapipe/solutions/guide) |
| **TensorFlow Lite (LiteRT)** | Custom models on-device | Android, iOS, embedded | idem |
| **ONNX Runtime Mobile** | Modelos ONNX on-device | Android, iOS | idem |
| **Core ML (Apple)** | Modelos convertidos a Core ML | iOS/macOS | idem |

#### CLIP / Sentence-Transformers para Matching Imagen-Texto

**Enfoque práctico:** En vez de intentar que un VLM clasifique directamente el modelo Hot Wheels (decenas de miles de variantes), usar CLIP para generar un embedding de la foto del auto y compararlo contra embeddings de texto descriptivos de cada modelo en el catálogo.

**Cómo funciona:**
1. **Catálogo:** Para cada auto, generar texto descriptivo: "1969 Hot Wheels Custom Camaro rojo con rayas negras, base de vidrio, ruedas Redline"
2. **Embeddings de texto:** Codificar cada descripción con `sentence-transformers/clip-ViT-B-32` → vector 512-dim
3. **Embedding de imagen:** Codificar la foto del usuario con el mismo modelo → vector 512-dim
4. **Similitud:** Producto punto (cosine similarity) entre embedding de foto y cada embedding de texto → ranking

**Límites de CLIP:**
- CLIP fue entrenado en imágenes generales, no en juguetes específicos
- No distingue detalles finos (color exacto, tipo de rueda, variante de carrocería)
- Funciona mejor para "categoría general" que para "modelo exacto"
- Puede fine-tunearse con imágenes del catálogo (recomendado para producción)

**Implementación Python:**
```python
from sentence_transformers import SentenceTransformer
from PIL import Image

model = SentenceTransformer("sentence-transformers/clip-ViT-B-32")
img_emb = model.encode(Image.open("hotwheel.jpg"))
text_emb = model.encode(["1969 Custom Camaro rojo Redline", "1970 Chevelle verde", ...])
scores = model.similarity(img_emb, text_emb)
```

Fuente: [sbert.net](https://www.sbert.net/examples/sentence_transformer/applications/image-search/README.html)

### 1.3 OCR de la Tarjeta/Blister

#### Tesseract OCR (Gratuito, Local)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Costo** | Gratis (Apache 2.0) | [github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract) |
| **Idiomas** | 100+ (incluye español) | idem |
| **Precisión en blister** | Moderada (depende de calidad de foto, iluminación, resolución) | NO VERIFICADO (depende del caso) |
| **Uso** | `pytesseract.image_to_string(img, lang='spa+eng')` | idem |

#### IA de Visión para OCR Mejorado

Los VLMs modernos (Qwen2.5-VL, Gemini Flash) pueden leer texto en imágenes con mejor precisión que Tesseract tradicional:
- Leen el nombre del modelo en la tarjeta
- Extraen el año
- Identifican la serie (mainline, premium, etc.)

**Recomendación:** Usar VLM como método principal de OCR + Tesseract como fallback/validación cruzada.

### 1.4 Estrategia Híbrida Recomendada

```
FOTO DEL AUTO
     │
     ▼
┌─────────────────────────┐
│ 1. VISIÓN (VLM/CLIP)   │ → Descripción textual + candidatos top-5
│    (Gemini Flash o      │
│     Qwen2.5-VL local)   │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 2. BÚSQUEDA TEXTO EN    │ → Filtrar catálogo por nombre/keywords
│    CATÁLOGO PROPIO      │
│    (SQLite + FTS5 o     │
│     embeddings)         │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 3. MATCHING FINOS       │ → CLIP embeddings para ranking
│    (embedding foto vs   │    + validación de detalles
│     embedding texto)    │    (color, serie, año)
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 4. CONFIRMACIÓN         │ → Mostrar top-3 candidatos con
│    (Usuario elige o     │    fotos de referencia; usuario
│     confirma auto)      │    confirma o corrige
└─────────────────────────┘
```

**Cómo mejorar precisión:**
- **Fondo neutro:** Fondo blanco/gris uniforme mejora CLIP y OCR
- **Varias fotos:** Frente, lateral, trasera, blister completo → promedio de embeddings
- **UPC/EAN del blister:** Código de barras → búsqueda directa en catálogo (método más fiable)
- **Luz uniforme:** Evitar sombras y reflejos en el blister

---

## 2. Voz: TTS y STT

### 2.1 Texto a Voz (TTS) Gratis

#### Edge TTS (Recomendado — Gratis, Sin API Key)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Costo** | $0 (gratis ilimitado) | [github.com/rany2/edge-tts](https://github.com/rany2/edge-tts) |
| **API key** | No requiere | idem |
| **Voces** | 400+ voces neuronales en 100+ idiomas | idem |
| **Voces español** | Múltiples (es-ES, es-MX, es-AR, etc.) | [pub.dev/packages/edge_tts](https://pub.dev/packages/edge_tts) |
| **Plataformas** | Python (edge-tts), Flutter (edge_tts), Web (directo) | idem |
| **Uso comercial** | No es API oficial de Microsoft; uso a propio riesgo. No hay ToS explícito que lo prohíba | [echora.audio](https://echora.audio/models/edge-tts) |
| **Calidad** | Neuronal, alta calidad | idem |
| **NOTA** | Es un wrapper no oficial del servicio "Read Aloud" de Edge | idem |

**Integración Python:**
```python
import edge_tts
import asyncio

async def hablar(texto, voz="es-ES-AlvaroNeural"):
    communicate = edge_tts.Communicate(texto, voz)
    await communicate.save("output.mp3")
```

#### Piper TTS (Local, Gratis)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Costo** | $0 (código abierto) | [github.com/rhasspy/piper](https://github.com/rhasspy/piper) |
| **Voces español** | es_ES (male/female), es_MX, es_AR | [piperhub.org](https://piperhub.org/voices/) |
| **Calidad** | Buena (neural, pero inferior a Edge TTS) | idem |
| **Latencia** | Baja (local, ~200-500ms) | idem |
| **Plataformas** | Windows, Linux, macOS, Raspberry Pi, contenedores | idem |
| **Uso comercial** | Sí (licencia MIT) | idem |
| **Ideal para** | Uso 100% offline, embedded | idem |

**Voces Piper en español:**
- `es_ES-male-medium`, `es_ES-female-medium`
- `es_MX-ald-medium` (México)
- `es_ES-davefx-medium` (España)

#### Kokoro TTS (Local, Gratis, Calidad Alta)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Costo** | $0 (Apache 2.0) | [kompozy.io](https://kompozy.io/reviews/kokoro-tts) |
| **Modelo** | Kokoro-82M (82M parámetros, ~80MB ONNX) | idem |
| **Calidad** | Muy alta para su tamaño (comparable a APIs de pago hace 2 años) | idem |
| **Idiomas** | Inglés, Japonés, Francés, Coreano, Chino, **Español**, Hindi, Italiano, PT-BR | idem |
| **Latencia** | <200ms en CPU, <50ms en GPU (WebGPU) | idem |
| **Plataformas** | Python (kokoro-onnx), Navegador (WebGPU/WASM), Docker | idem |
| **Uso comercial** | Sí (Apache 2.0) | idem |

#### Otras Opciones TTS

| Opción | Costo | Calidad | Notas | Fuente |
|--------|-------|---------|-------|--------|
| **gTTS** | Gratis | Baja (síntesis estadística) | API no oficial de Google Translate | NO VERIFICADO |
| **espeak-ng** | Gratis | Muy baja (robótica) | Último recurso, offline | NO VERIFICADO |
| **Coqui TTS** | Gratis (open source) | Alta (XTTS v2) | Proyecto archivado (enero 2024) | [coqui.ai](https://coqui.ai) |
| **ElevenLabs Free** | 10,000 caracteres/mes | Muy alta | No comercial sin pago | [elevenlabs.io](https://elevenlabs.io) |
| **Google Cloud TTS Free** | 1 millón caracteres/mes | Alta (WaveNet) | Requiere billing account | [cloud.google.com/text-to-speech](https://cloud.google.com/text-to-speech/pricing) |

### 2.2 Voz a Texto (STT) Gratis

#### Whisper (Local, Gratis, Open Source)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Costo** | $0 (MIT license) | [github.com/openai/whisper](https://github.com/openai/whisper) |
| **Modelos** | tiny (39M), base (74M), small (244M), medium (769M), large-v3 (1.5B) | idem |
| **Precisión** | ~10-15% WER en inglés limpio; español similar | [localaimaster.com](https://localaimaster.com/blog/whisper-local-setup) |
| **Hardware** | tiny/base: CPU usable. small/medium: GPU recomendado. large-v3: GPU required | idem |
| **Latencia** | ~4x más rápido que implementación original con faster-whisper | idem |
| **Plataformas** | Python (faster-whisper), C++ (whisper.cpp), móvil (whisper.cpp compilado) | idem |
| **Uso comercial** | Sí (MIT) | idem |

#### faster-whisper (Python, Rápido)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Velocidad** | 4x más rápido que whisper original | [promptquorum.com](https://www.promptquorum.com/power-local-llm/faster-whisper-review) |
| **Memoria** | Menos RAM que original (INT8) | idem |
| **Ideal para** | Servidor Python con GPU NVIDIA | idem |

#### whisper.cpp (C/C++, Ultra Ligero)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Velocidad** | Muy rápido (AVX2/NEON, Metal, CUDA) | [promptquorum.com](https://www.promptquorum.com/power-local-llm/whisper-cpp-review) |
| **Plataformas** | CPU, Apple Silicon, NVIDIA, ARM, WebAssembly | idem |
| **Ideal para** | Móvil (iOS/Android), Raspberry Pi, embedded | idem |
| **Uso comercial** | Sí (MIT) | idem |

#### Vosk (Local, Ligero, Streaming)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Costo** | $0 (Apache 2.0) | [alphacephei.com/vosk](https://alphacephei.com/vosk) |
| **Tamaño modelo** | ~50MB por idioma (small model) | idem |
| **Idiomas** | 20+ (incluye español) | idem |
| **Streaming API** | Sí (tiempo real) | idem |
| **Plataformas** | Python, Java, Node, C#, Android, iOS, Raspberry Pi | [github.com/alphacep/vosk](https://github.com/alphacep/vosk) |
| **Precisión** | ~12% WER estándar | [stt.ai](https://stt.ai/models/vosk/) |
| **Uso comercial** | Sí (Apache 2.0) | idem |

#### Google Cloud Speech-to-Text

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Free tier** | 60 minutos/mes (V1 y V2) | [cloud.google.com/speech-to-text](https://cloud.google.com/speech-to-text/pricing) |
| **Precisión** | Alta (modelos Chirp) | idem |
| **Streaming** | Sí | idem |
| **Uso comercial** | Sí (sobre free tier pagado) | idem |
| **NOTA** | 60 min/mes es muy bajo para producción | idem |

#### Groq Whisper (Cloud, Gratis)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Free tier** | Whisper Large v3: 20 RPM, 2K RPD, 28.8K ASD | [console.groq.com/docs/rate-limits](https://console.groq.com/docs/rate-limits) |
| **Precisión** | Alta (Large v3) | idem |
| **Uso comercial** | Sí (Developer plan) | idem |
| **NOTA** | Los límites de audio/día (28.8K ASD = ~8 horas) son generosos para testing | idem |

#### Deepgram

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Free credit** | $200 en signup | [deepgram.com/pricing](https://deepgram.com/pricing) |
| **Precisión** | Alta (Nova-3) | idem |
| **Streaming** | Sí (WSS) | idem |
| **Uso comercial** | Sí | idem |

#### Web Speech API (Navegador)

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Costo** | $0 (built-in en navegadores) | NO VERIFICADO |
| **Plataformas** | Chrome, Edge, Safari (parcial) | idem |
| **Streaming** | Sí (con `continuous: true`) | idem |
| **Uso comercial** | Sujeto a ToS del navegador | idem |
| **Ideal para** | PWA, apps web, prototipos | idem |

### 2.3 Cómo Hacer un Asistente Conversacional Completo

#### Opción A: Pipeline STT → LLM → TTS (Más Flexible, Mayor Latencia)

```
Usuario habla → STT (Whisper/Vosk/Groq) → Texto → LLM (Gemini/Groq/OpenRouter) → Respuesta texto → TTS (Edge/Piper/Kokoro) → Audio → Usuario escucha
```

| Métrica | Valor |
|---------|-------|
| **Latencia total estimada** | 1.5 - 3.5 segundos (depende de modelos y hardware) |
| **Costo mensual (1 usuario)** | $0 (todo local) o ~$0.50 (nube gratuita) |
| **Costo mensual (1,000 usuarios)** | ~$50-200 (APIs gratuitas no escalan; pasar a paid o self-hosted) |
| **Ventaja** | Máxima flexibilidad, cada componente es interchangeable |
| **Desventaja** | Alta latencia, mala experiencia conversacional |

#### Opción B: Live API (Gemini Live / OpenAI Realtime) (Menor Latencia, Menor Flexibilidad)

**Gemini Live API:**

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Latencia** | 300-600ms (primer chunk de audio) | [mindstudio.ai](https://www.mindstudio.ai/blog/real-time-ai-voice-models-compared-2025) |
| **Free tier** | Existe (rate-limited) | [rywalker.com](https://rywalker.com/research/gemini-live-api) |
| **Modelo** | gemini-2.5-flash-native-audio | [ai.google.dev/gemini-api/docs/live](https://ai.google.dev/gemini-api/docs/live) |
| **Protocolo** | WebSocket (WSS) | idem |
| **Input** | Audio 16-bit PCM 16kHz, imágenes JPEG 1FPS, texto | idem |
| **Output** | Audio 24kHz | idem |
| **Idiomas** | 70+ (multilingüe seamless) | [docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/live-api) |

**OpenAI Realtime API:**

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Latencia** | 300-600ms | [mindstudio.ai](https://www.mindstudio.ai/blog/real-time-ai-voice-models-compared-2025) |
| **Free tier** | NO | [openai.com/api/pricing](https://openai.com/api/pricing/) |
| **Precio** | gpt-realtime-2.1: $32/1M audio input, $64/1M audio output | idem |
| **Precio (mini)** | gpt-realtime-2.1-mini: $10/1M audio input, $20/1M audio output | idem |
| **Uso comercial** | Sí | idem |

**Recomendación:** Gemini Live API para prototipo (free tier). OpenAI Realtime solo si ya se paga OpenAI. Para producción con voz en español, Gemini Live es mejor relación costo/calidad.

---

## 3. Motor de Recomendación / Índice de Coleccionabilidad

### 3.1 Fórmula Propuesta

El índice de coleccionabilidad (0-100) combina 5 factores con pesos justificados:

```
Índice = (R × 0.30) + (D × 0.25) + (C × 0.20) + (A × 0.15) + (M × 0.10)
```

| Factor | Descripción | Peso | Justificación |
|--------|-------------|------|---------------|
| **R (Rareza)** | Basada en tirada/serie estimada | 30% | Es el factor más determinante en coleccionabilidad. Autos de tirada limitada o series especiales son más buscados. |
| **D (Demanda)** | Frecuencia de ventas y búsquedas | 25% | Un auto que se vende mucho tiene más demanda real. Se mide por frecuencia de aparición en ventas eBay/PriceCharting. |
| **C (Condición)** | Estado del item (CIB, loose, etc.) | 20% | En coleccionismo, condición es crítica. CIB (Complete In Box) vale significativamente más que loose. |
| **A (Antigüedad)** | Año de fabricación | 15% | Los autos más viejos (pre-1970s "Redline") son más coleccionables. |
| **M (Mercado)** | Estado de mercado (tendencia) | 10% | Si el modelo está "trending" ahora (por película, aniversario, etc.), sube su valor temporalmente. |

### 3.2 Escalas de Cada Factor

**R (Rareza) — 0 a 100:**
| Tirada/Serie | Score |
|-------------|-------|
| Mainline masiva (millones) | 0-20 |
| Mainline estándar | 20-40 |
| Premium/Treasure Hunt | 40-60 |
| Super Treasure Hunt | 60-80 |
| Edición limitada (<1,000) | 80-95 |
| Prototipo/Pre-producción | 95-100 |

**D (Demanda) — 0 a 100:**
| Ventas último mes (eBay) | Score |
|--------------------------|-------|
| 0-5 ventas | 0-20 |
| 5-20 ventas | 20-40 |
| 20-50 ventas | 40-60 |
| 50-100 ventas | 60-80 |
| 100+ ventas | 80-100 |

**C (Condición) — 0 a 100:**
| Condición | Score |
|-----------|-------|
| CIB (Complete In Box) | 100 |
| Caja dañada, auto perfecto | 70-80 |
| Loose, perfecto estado | 50-60 |
| Loose, desgaste leve | 30-40 |
| Loose, dañado | 0-20 |

**A (Antigüedad) — 0 a 100:**
| Año | Score |
|-----|-------|
| 2020+ | 0-20 |
| 2010-2019 | 20-35 |
| 2000-2009 | 35-50 |
| 1990-1999 | 50-65 |
| 1980-1989 | 65-80 |
| 1970-1979 | 80-95 |
| Pre-1970 (Redline) | 95-100 |

**M (Mercado) — 0 a 100:**
| Indicador | Score |
|-----------|-------|
| Sin tendencia | 30-40 |
| Mencionado en redes/foros | 40-60 |
| Aniversario/relanzamiento | 60-80 |
| Película/serie/media buzz | 80-100 |

### 3.3 Cómo Evitar que el Índice Sea Arbitrario

1. **Transparencia total:** Mostrar cada sub-score y su justificación al usuario
2. **Calibración con datos reales:** Los pesos deben ajustarse retroactivamente comparando score vs. precio real de venta (regresión lineal sobre datos de eBay)
3. **Actualización periódica:** Recalcular D y M mensualmente con datos frescos
4. **Validación cruzada:** Comparar índice contra precios reales de venta; si R² < 0.6, revisar pesos
5. **No usar ML oscuro:** Una fórmula explícita es defendible; una caja negra no lo es

### 3.4 Calibración con Datos Reales

```python
# Pseudo-código de calibración
import pandas as pd
from sklearn.linear_model import LinearRegression

# Datos: [R, D, C, A, M] -> precio_real
df = pd.read_csv("ventas_reales.csv")
X = df[["R", "D", "C", "A", "M"]]
y = df["precio_real"]

model = LinearRegression().fit(X, y)
print("Pesos óptimos:", model.coef_)  # Ajustar pesos de la fórmula
print("R²:", model.score(X, y))       # Si < 0.6, revisar
```

---

## 4. Estimación de Valor Automática

### 4.1 Fuentes de Comparables de Venta

#### eBay Browse API

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **Free tier** | 5,000 calls/día (desarrollador) | [developer.ebay.com](https://developer.ebay.com/develop/api/buy/browse_api.md) |
| **Datos** | Solo listados activos (NO ventas completadas) | [sold-comps.com](https://sold-comps.com/use-cases/developer-integration) |
| **Sold items** | `findCompletedItems` fue descontinuado en febrero 2025 | idem |
| **Marketplace Insights** | Requiere aprobación Business (casi nunca otorgada) | idem |
| **Uso comercial** | Sí (con paid tier) | idem |
| **Alternativa gratuita** | Scraping manual de eBay.com (sujeto a ToS, frágil) | NO VERIFICADO |

#### PriceCharting

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **API** | Solo con suscripción paga (Legendary tier) | [pricecharting.com](https://www.pricecharting.com/api-documentation) |
| **Free** | No hay API gratuita | idem |
| **Web scraping** | pricecharting.com tiene datos de precios de juegos, TCG, comics, y Hot Wheels | [pricecharting.com](https://www.pricecharting.com) |
| **Uso comercial** | Sujeto a suscripción | idem |
| **NOTA** | La web pública muestra precios por juego/consola; Hot Wheels puede estar cubierto | NO VERIFICADO (verificar cobertura) |

#### HobbyDB

| Aspecto | Detalle | Fuente |
|---------|---------|--------|
| **API** | Existe API | [hobbydb.com](https://hobbydb.com) |
| **Free tier** | NO VERIFICADO | idem |
| **Cobertura** | Juguetes, coleccionables, modelos | idem |

#### Otras Fuentes Gratuitas

| Fuente | Tipo | Notas |
|--------|------|-------|
| **eBay manual** | Scraping manual | Frágil, pero gratis |
| **MercadoLibre API** | API pública | Solo LATAM, puede tener Hot Wheels |
| **Facebook Marketplace** | Scraping manual | Precios de venta |
| **Reddit r/HotWheels** | Comunidad | Tendencias, no precios estructurados |

### 4.2 Limpieza de Datos

```python
# Pipeline de limpieza de comparables
def limpiar_comparables(items):
    # 1. Filtrar por condición equivalente
    items = [i for i in items if condicion_equivalente(i, "CIB")]
    
    # 2. Remover outliers (precios > 3 desviaciones estándar)
    precios = [i.price for i in items]
    media = np.median(precios)
    std = np.std(precios)
    items = [i for i in items if abs(i.price - media) < 3 * std]
    
    # 3. Normalizar por inflación si el dato es antiguo
    items = [ajustar_inflacion(i) for i in items]
    
    # 4. Eliminar duplicados (mismo vendedor, mismo auto)
    items = deduplicar_por_vendedor(items)
    
    return items
```

### 4.3 Estimación de Rango con Percentiles

En vez de dar un solo precio, dar un rango estadístico:

```python
def estimar_valor(comparables):
    precios = sorted([c.precio for c in comparables])
    
    return {
        "p10": np.percentile(precios, 10),   # Precio bajo (auto en mal estado o venta rápida)
        "p25": np.percentile(precios, 25),   # Q1
        "p50": np.percentile(precios, 50),   # Mediana (mejor estimación)
        "p75": np.percentile(precios, 75),   # Q3
        "p90": np.percentile(precios, 90),   # Precio alto (auto perfecto o vendedor paciente)
        "confianza": "alta" if len(comparables) >= 10 else "media" if len(comparables) >= 5 else "baja"
    }
```

**Regla de oro:** Mínimo 5 comparables para estimar. Con menos, marcar como "confianza baja" y dar rango amplio.

---

## 5. Arquitectura Técnica Concreta

### 5.1 Stack Recomendado

| Capa | Tecnología | Justificación |
|------|------------|---------------|
| **Móvil (Android/iOS)** | Flutter + Dart | Un solo codebase, soporte para cámara, micrófono, Edge TTS, Piper (vía FFI) |
| **Escritorio (Windows)** | Flutter Desktop o Tauri | Flutter comparte código con móvil; Tauri es más ligero |
| **PWA de respaldo** | React + Vite | Respaldo web, Web Speech API para STT/TTS nativo |
| **Backend API** | Python + FastAPI | Rápido, async, easy de desplegar |
| **Motor de IA (backend)** | Python + FastAPI | Acceso a Gemini/Groq/OpenRouter APIs |
| **DB local (móvil/escritorio)** | SQLite + sqlcipher | Ligero, cifrado, sync offline-first |
| **DB servidor** | PostgreSQL + pgvector | Para catálogo global, embeddings, datos de mercado |
| **Catálogo** | JSON + SQLite (local) + PostgreSQL (server) | Catálogo Hot Wheels descargable como JSON comprimido |
| **Embeddings** | CLIP (sentence-transformers) + pgvector | Matching imagen-texto |
| **Voz (móvil)** | Edge TTS + whisper.cpp | Edge TTS gratis; whisper.cpp compilado para móvil |
| **Voz (escritorio)** | Piper TTS + faster-whisper | Piper local, faster-whisper en GPU |
| **Voz (backend)** | Gemini Live API | Para asistente conversacional en tiempo real |

### 5.2 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Cámara      │  │  Micrófono   │  │  Pantalla táctil     │  │
│  │  (foto auto) │  │  (voz)       │  │  (app Flutter)       │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                  │                     │               │
│         ▼                  ▼                     ▼               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              APP FLUTTER (móvil/escritorio)             │    │
│  │  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │    │
│  │  │ Camera      │  │ whisper.cpp  │  │ Edge TTS /    │  │    │
│  │  │ Plugin      │  │ (STT local)  │  │ Piper (TTS)   │  │    │
│  │  └─────────────┘  └──────────────┘  └───────────────┘  │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │ SQLite local (catálogo, colección, embeddings)  │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │ HTTP/HTTPS (solo si online)         │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI + Python)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ /api/vision  │  │ /api/voice   │  │ /api/catalog         │  │
│  │ (Gemini/     │  │ (Gemini Live │  │ (búsqueda texto,    │  │
│  │  Groq)       │  │  WebSocket)  │  │  embeddings)         │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ /api/value   │  │ /api/collect │  │ /api/sync            │  │
│  │ (estimación  │  │ (índice      │  │ (sincronización      │  │
│  │  valor)      │  │  colecc.)    │  │  catálogo)           │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ PostgreSQL + pgvector (catálogo, ventas, embeddings)    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Gemini API   │  │ Groq API     │  │ eBay API /           │  │
│  │ (Visión +    │  │ (Whisper +   │  │ PriceCharting        │  │
│  │  Live)       │  │  Llama)      │  │ (precios)            │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Endpoints de API Sugeridos

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/vision/identify` | POST | Recibe imagen JSON base64 → devuelve top-5 candidatos |
| `/api/vision/describe` | POST | Recibe imagen → devuelve descripción textual (color, tipo, etc.) |
| `/api/voice/stt` | POST | Recibe audio → devuelve texto (fallback si no usa Gemini Live) |
| `/api/voice/tts` | POST | Recibe texto → devuelve audio MP3 (fallback) |
| `/api/voice/live` | WebSocket | Gemini Live API streaming bidireccional |
| `/api/catalog/search` | GET | Búsqueda por texto (nombre, serie, año) |
| `/api/catalog/embeddings` | GET | Lista de embeddings (para matching local) |
| `/api/value/estimate` | POST | Recibe model_id + condición → devuelve rango de valor |
| `/api/collect/index` | GET | Calcula índice de coleccionabilidad para un model_id |
| `/api/sync/catalog` | GET | Descarga catálogo actualizado (JSON comprimido) |
| `/api/sync/prices` | GET | Descarga precios de mercado actualizados |

### 5.4 Modelo de Datos

```sql
-- Catálogo Hot Wheels
CREATE TABLE hotwheels (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,                    -- "1969 Custom Camaro"
    year INTEGER,                          -- 1969
    series TEXT,                           -- "Mainline", "Premium", "TH", "STH"
    sub_series TEXT,                       -- "Muscle Mania", "HW Race"
    color TEXT,                            -- "Spectraflame Red"
    wheel_type TEXT,                       -- "Redline", "PR5", "5SP"
    base_type TEXT,                        -- "Chrome", "Plastic"
    tampo TEXT,                            -- Descripción de tampografía
    photo_url TEXT,                        -- URL de foto de referencia
    rarity_score REAL,                     -- 0-100 (precalculado)
    category TEXT,                          -- "Car", "Truck", "Motorcycle"
    castings_id TEXT,                      -- ID interno de casting
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices de búsqueda
CREATE INDEX idx_hotwheels_name ON hotwheels(name);
CREATE INDEX idx_hotwheels_year ON hotwheels(year);
CREATE INDEX idx_hotwheels_series ON hotwheels(series);

-- FTS5 para búsqueda de texto
CREATE VIRTUAL TABLE hotwheels_fts USING fts5(name, series, sub_series, color, content='hotwheels', content_rowid='id');

-- Embeddings (pgvector)
CREATE TABLE hotwheels_embeddings (
    hotwheels_id INTEGER REFERENCES hotwheels(id) ON DELETE CASCADE,
    embedding vector(512),                  -- CLIP embedding
    PRIMARY KEY (hotwheels_id)
);

-- Colección del usuario
CREATE TABLE user_collection (
    id INTEGER PRIMARY KEY,
    hotwheels_id INTEGER REFERENCES hotwheels(id),
    user_id INTEGER NOT NULL,
    condition TEXT,                        -- "CIB", "Loose-Mint", "Loose-Good"
    purchase_price REAL,
    purchase_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ventas de mercado (comparables)
CREATE TABLE market_sales (
    id INTEGER PRIMARY KEY,
    hotwheels_id INTEGER REFERENCES hotwheels(id),
    sale_price REAL NOT NULL,
    condition TEXT,
    sale_date DATE,
    source TEXT,                           -- "eBay", "PriceCharting", "MercadoLibre"
    listing_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cache de embeddings de usuario (para matching local)
CREATE TABLE user_photo_embeddings (
    id INTEGER PRIMARY KEY,
    photo_path TEXT,                       -- Ruta local a la foto
    embedding vector(512),                  -- CLIP embedding de la foto
    hotwheels_id INTEGER,                  -- Si ya fue identificado
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5.5 Cómo se Ejecuta el Asistente de Voz en Cada Plataforma

| Plataforma | STT | TTS | Notas |
|------------|-----|-----|-------|
| **Android** | whisper.cpp (NDK) | Edge TTS o Piper (JNI) | whisper.cpp compilado con NDK; Edge TTS vía plugin Flutter |
| **iOS** | whisper.cpp (Swift bridging) | Edge TTS o Piper (Core ML) | whisper.cpp compilado con Core ML para Neural Engine |
| **Windows Desktop** | faster-whisper (GPU) o Vosk | Piper (local) o Edge TTS | faster-whisper aprovecha CUDA si hay GPU |
| **PWA (Web)** | Web Speech API (Chrome) | Web Speech API o Edge TTS | Nativo, sin instalación; limitado a navegadores compatibles |
| **Backend (Gemini Live)** | Gemini Live (WebSocket) | Gemini Live (nativo) | Latencia 300-600ms; free tier rate-limited |

### 5.6 Costos Mensuales Estimados

#### Escenario 1: Usuario Único (Desarrollo/Prototipo)

| Servicio | Costo/mes | Notas |
|----------|-----------|-------|
| Gemini API Free | $0 | 250 RPD Flash (suficiente para testing) |
| Groq Free | $0 | Whisper + Llama Vision |
| Edge TTS | $0 | Gratis ilimitado |
| Piper TTS (local) | $0 | Gratis |
| whisper.cpp (local) | $0 | Gratis |
| Hosting backend | $0 | Local (localhost) |
| **TOTAL** | **$0** | |

#### Escenario 2: 1,000 Usuarios (Producción)

| Servicio | Costo/mes | Notas |
|----------|-----------|-------|
| Gemini API (Flash) | ~$10-30 | Si superan free tier (pago por uso: $0.30/1M input, $2.50/1M output) |
| Groq (Developer) | ~$20-50 | Límites 10x free; por uso si supera |
| Edge TTS | $0 | Gratis (pero no es API oficial) |
| whisper.cpp (local) | $0 | Cada usuario corre en su dispositivo |
| Hosting (VPS o Cloud) | ~$10-50 | VPS básico ($5-10/mes) o Cloud Run/ Lambda |
| **TOTAL** | **~$40-130** | Con capas gratuitas + VPS |

**NOTA IMPORTANTE:** Los Edge TTS, Piper, whisper.cpp, Kokoro son GRATIS ILIMITADOS (no hay límite de caracteres/minutos). Los APIs de cloud (Gemini, Groq) tienen free tiers pero se agotan con uso intensivo.

#### Escenario 3: 1,000 Usuarios (Todo Local, Sin Nube)

| Servicio | Costo/mes | Notas |
|----------|-----------|-------|
| Ollama Qwen2.5-VL 7B (servidor) | ~$20-40 | Un solo servidor con GPU comparte entre usuarios |
| whisper.cpp (local en cada dispositivo) | $0 | Corre en el móvil/PC del usuario |
| Edge TTS (local en cada dispositivo) | $0 | Gratis |
| Hosting mínimo (API relay) | ~$5-10 | VPS solo para relay |
| **TOTAL** | **~$25-50** | |

---

## 6. Límites y Riesgos

### 6.1 Precisión Real del Reconocimiento por Foto

**SÉ HOTESTO:** Los Hot Wheels se parecen MUCHO entre sí. Diferenciar un modelo de otro solo por foto es extremadamente difícil incluso para humanos expertos.

| Aspecto | Realidad |
|---------|---------|
| **Mismo casting, diferentes colores** | Un 1969 Camaro puede tener 20+ variantes de color. La foto puede no distinguir el color exacto (depende de iluminación, cámara, pantalla). |
| **Mismo casting, diferentes años** | Un modelo fabricado 1975 y 1985 puede ser idéntico excepto por el stamp en la base. |
| **Redlines vs post-Redlines** | La diferencia clave (rueda Redline) es pequeña y puede no verse en la foto. |
| **Treasure Hunts vs normales** | Los TH tienen sticker especial; si no se ve el sticker, es indistinguible. |
| **Prototipos vs producción** | Casi imposible sin experticia. |

**Precisión esperada (NO VERIFICADO — depende de calidad de foto y modelo):**
- **Identificar casting correcto (ej. "Custom Camaro"):** 60-80% con VLM + buena foto
- **Identificar variante exacta (color + año + serie):** 30-50% solo con foto
- **Identificar con UPC/barcode:** 95%+ (si el código es legible)
- **Identificar con OCR de tarjeta:** 70-85% (depende de calidad de foto y VLM)

**Conclusión:** El reconocimiento por foto solo es un FILTRADOR, no un identificador definitivo. El flujo debe ser: foto → candidatos top-5 → usuario confirma.

### 6.2 Alucinaciones del Modelo

| Riesgo | Mitigación |
|--------|------------|
| VLM inventa detalles del auto | Pedir que responda "NO SÉ" si no está seguro; no forzar respuesta |
| VLM confunde con otro modelo similar | Mostrar top-5 candidatos, no solo 1 |
| VLM inventa valor de mercado | Nunca preguntar al VLM por precios; siempre usar datos reales de ventas |
| VLM inventa datos del catálogo | El catálogo es la fuente de verdad; el VLM solo describe la foto |

### 6.3 Dependencia de Proveedores Gratuitos

| Riesgo | Mitigación |
|--------|------------|
| Gemini cambia cuotas sin aviso | Implementar fallback a Groq/OpenRouter |
| Edge TTS cambia o desaparece | Tener Piper como backup local |
| Groq discontinua modelo | Llama 3.2 Vision → Qwen2.5-VL → Pixtral (todos open weights, se auto-hostean) |
| OpenRouter cambia políticas | No depender de un solo proveedor; abstracción en código |

**Recomendación de arquitectura:** Usar capa de abstracción `VisionProvider` y `VoiceProvider` para que sea trivial cambiar de proveedor.

### 6.4 Privacidad de las Fotos

| Riesgo | Mitigación |
|--------|------------|
| Fotos enviadas a APIs de cloud | Para usuarios preocupados por privacidad: modo 100% local (Ollama + CLIP) |
| Fotos de menores (coleccionistas infantiles) | No enviar fotos a cloud sin consentimiento parental |
| Metadatos GPS en fotos | Limpiar EXIF antes de enviar a cualquier API |
| Datos de ventas de eBay | Usar solo datos agregados/anonimizados |

### 6.5 Qué NO se Puede Lograr Gratis

| Capacidad | Por qué no es gratis |
|-----------|---------------------|
| **Voz en tiempo real con calidad Gemini Live** | Free tier es rate-limited; producción requiere pago |
| **Reconocimiento 100% preciso de variantes** | Requiere dataset etiquetado fino + fine-tuning (costo de entrenamiento) |
| **Datos de ventas completos de eBay** | eBay cerró `findCompletedItems`; Marketplace Insights es Business-only |
| **API de PriceCharting** | Solo suscripción paga |
| **1,000 usuarios concurrentes con APIs gratuitas** | Los free tiers no escalan; requiere self-hosting o pago |
| **Fine-tuning de CLIP para Hot Wheels** | Requiere GPU + dataset + tiempo de ingeniería (no es "gratis" en tiempo) |

---

## 7. Fuentes y Referencias

### Documentación Oficial

1. **Google Gemini API Pricing** — https://ai.google.dev/gemini-api/docs/pricing (accedido 2026-10-11)
2. **Google Gemini API Rate Limits** — https://ai.google.dev/gemini-api/docs/rate-limits (accedido 2026-10-11)
3. **Google Gemini Billing** — https://ai.google.dev/gemini-api/docs/billing (accedido 2026-10-11)
4. **Google Gemini Live API** — https://ai.google.dev/gemini-api/docs/live (accedido 2026-10-11)
5. **Groq Rate Limits** — https://console.groq.com/docs/rate-limits (accedido 2026-10-11)
6. **Groq Billing Plans** — https://console.groq.com/settings/billing/plans (accedido 2026-10-11)
7. **OpenRouter Limits** — https://openrouter.ai/docs/api_reference/limits (accedido 2026-10-11)
8. **OpenRouter FAQ** — https://openrouter.ai/docs/faq (accedido 2026-10-11)
9. **Hugging Face Inference Providers Pricing** — https://huggingface.co/docs/inference-providers/pricing (accedido 2026-10-11)
10. **Cloudflare Workers AI Pricing** — https://developers.cloudflare.com/workers-ai/platform/pricing/ (accedido 2026-10-11)
11. **Cloudflare Workers Limits** — https://developers.cloudflare.com/workers/platform/limits/ (accedido 2026-10-11)
12. **Together AI Supported Models** — https://support.together.ai/articles/2644979080-what-models-does-together-ai-support (accedido 2026-10-11)
13. **Cerebras Pricing** — https://www.cerebras.ai/pricing (accedido 2026-10-11)
14. **Cerebras Rate Limits** — https://inference-docs.cerebras.ai/support/rate-limits (accedido 2026-10-11)
15. **NVIDIA NIM Run Anywhere** — https://docs.api.nvidia.com/nim/docs/run-anywhere (accedido 2026-10-11)
16. **eBay Browse API** — https://developer.ebay.com/develop/api/buy/browse_api.md (accedido 2026-10-11)
17. **PriceCharting API Documentation** — https://www.pricecharting.com/api-documentation (accedido 2026-10-11)
18. **Google Cloud Speech-to-Text Pricing** — https://cloud.google.com/speech-to-text/pricing (accedido 2026-10-11)
19. **Google Cloud Free Tier** — https://cloud.google.com/free (accedido 2026-10-11)
20. **OpenAI API Pricing** — https://openai.com/api/pricing/ (accedido 2026-10-11)
21. **Deepgram Pricing** — https://deepgram.com/pricing (accedido 2026-10-11)

### Herramientas Open Source

22. **Edge TTS (GitHub)** — https://github.com/rany2/edge-tts (accedido 2026-10-11)
23. **Edge TTS Flutter Package** — https://pub.dev/packages/edge_tts (accedido 2026-10-11)
24. **Piper TTS (GitHub)** — https://github.com/rhasspy/piper (accedido 2026-10-11)
25. **Piper Voices Hub** — https://piperhub.org/voices/ (accedido 2026-10-11)
26. **Ollama Vision Models** — https://ollama.com/blog/vision-models (accedido 2026-10-11)
27. **Ollama Qwen2.5-VL** — https://ollama.com/library/qwen2.5vl (accedido 2026-10-11)
28. **Whisper (OpenAI GitHub)** — https://github.com/openai/whisper (accedido 2026-10-11)
29. **whisper.cpp (GitHub)** — https://github.com/ggml-org/whisper.cpp (accedido 2026-10-11)
30. **faster-whisper** — https://github.com/SYSTRAN/faster-whisper (accedido 2026-10-11)
31. **Vosk** — https://alphacephei.com/vosk (accedido 2026-10-11)
32. **Kokoro TTS Review** — https://kompozy.io/reviews/kokoro-tts (accedido 2026-10-11)
33. **Kokoro Voice Studio** — https://github.com/dilshan916/kokoro-voice-studio (accedido 2026-10-11)
34. **Google ML Kit** — https://developer.android.com/ai/overview (accedido 2026-10-11)
35. **MediaPipe Solutions** — https://developers.google.com/edge/mediapipe/solutions/guide (accedido 2026-10-11)
36. **CLIP (Hugging Face Docs)** — https://huggingface.co/docs/transformers/model_doc/clip (accedido 2026-10-11)
37. **Sentence-Transformers Image Search** — https://www.sbert.net/examples/sentence_transformer/applications/image-search/README.html (accedido 2026-10-11)

### Análisis y Comparativas

38. **Gemini Advanced Rate Limit Guide (Dec 2025)** — https://www.aifreeapi.com/en/posts/gemini-advanced-rate-limit (accedido 2026-10-11)
39. **Is Gemini API Free? (2025)** — https://www.spurnow.com/en/posts/is-gemini-api-free (accedido 2026-10-11)
40. **Groq API Guide** — https://artificial-intelligence-wiki.com/generative-ai/large-language-models/groq-api-guide/ (accedido 2026-10-11)
41. **Real-Time AI Voice Models Compared** — https://www.mindstudio.ai/blog/real-time-ai-voice-models-compared-2025 (accedido 2026-10-11)
42. **Gemini Live API Research** — https://rywalker.com/research/gemini-live-api (accedido 2026-10-11)
43. **eBay Sold Items API (SoldComps)** — https://sold-comps.com/use-cases/developer-integration (accedido 2026-10-11)
44. **Mistral Pixtral 12B Specs** — https://ai-tldr.dev/models/pixtral-12b/ (accedido 2026-10-11)
45. **Mistral Vision Models (Roboflow)** — https://playground.roboflow.com/models/mistral (accedido 2026-10-11)
46. **Together AI Review** — https://chiri.ai/chiri-atlas/together-ai (accedido 2026-10-11)
47. **Fireworks AI Review** — https://chatforest.com/reviews/fireworks-ai-inference-fine-tuning-platform/ (accedido 2026-10-11)
48. **Cerebras Free Tier Analysis** — https://prompthacker.ai/free-llm (accedido 2026-10-11)
49. **NVIDIA NIM Free API** — https://aihola.com/article/nvidia-nim-free-api-models (accedido 2026-10-11)
50. **faster-whisper Review** — https://www.promptquorum.com/power-local-llm/faster-whisper-review (accedido 2026-10-11)
51. **whisper.cpp Review** — https://www.promptquorum.com/power-local-llm/whisper-cpp-review (accedido 2026-10-11)
52. **Run Whisper Locally** — https://localaimaster.com/blog/whisper-local-setup (accedido 2026-10-11)
53. **Whisper Local on Raspberry Pi** — https://fast.io/resources/openclaw-raspberry-pi-speech-recognition-offline-voice-agent/ (accedido 2026-10-11)
54. **Home Assistant Voice Chapter 11** — https://www.home-assistant.io/blog/2025/10/22/voice-chapter-11/ (accedido 2026-10-11)
55. **Social Stream Ninja TTS Guide** — https://socialstream.ninja/docs/tts (accedido 2026-10-11)
56. **Hermes Agent TTS Providers** — https://www.hermify.io/en/blog/hermes-agent-tts-providers (accedido 2026-10-11)

---

## Resumen Ejecutivo

| Pregunta | Respuesta |
|----------|-----------|
| **¿Qué VLM gratis usar para visión?** | Gemini 2.5 Flash (250 RPD free) como primario; Groq Llama 3.2 Vision como fallback; Qwen2.5-VL 7B local (Ollama) para offline |
| **¿Qué TTS gratis en español?** | Edge TTS (gratis ilimitado, voces neuronales); Piper TTS (local, calidad media); Kokoro TTS (local, calidad alta) |
| **¿Qué STT gratis en español?** | whisper.cpp (local, MIT, gratis ilimitado); Groq Whisper Large v3 (cloud, 28.8K ASD free); Google Cloud STT (60 min/mes free) |
| **¿Voz en tiempo real gratis?** | Gemini Live API (free tier rate-limited); si no, pipeline STT→LLM→TTS (1.5-3.5s latencia, gratis) |
| **¿Precisión de reconocimiento?** | 60-80% casting, 30-50% variante exacta solo con foto. UPC/barcode es el método más fiable (95%+) |
| **¿Costo para 1 usuario?** | $0/mes (todo local + free tiers) |
| **¿Costo para 1,000 usuarios?** | ~$40-130/mes (APIs gratuitas + VPS) o ~$25-50/mes (self-hosted) |
| **¿Mayor riesgo?** | Hot Wheels son muy parecidos entre sí; el reconocimiento por foto es un filtro, no un identificador. El usuario siempre debe confirmar. |

---

**Documento generado:** 2026-10-11  
**Última verificación de fuentes:** 2026-10-11  
**Nota:** Las cuotas y precios de APIs cloud pueden cambiar sin aviso. Verificar siempre la documentación oficial antes de comprometerse en producción.
