# DEPLOY.md — Cómo instalar HW Collector en el celular (modo producción)

La app ya es un **PWA** (Progressive Web App): tiene manifest, iconos y service worker, funciona **sin conexión** y se instala como app nativa en Android, iPhone y escritorio.

## La regla que no se puede saltar

Los navegadores solo permiten **instalar un PWA y registrar el service worker en un *contexto seguro***: **HTTPS** o `localhost`.

- Abrir el archivo con doble clic (`file://`) → se usa, pero **no se instala**.
- Servir por HTTP en la red local (`http://192.168.x.x:8080`) → se usa, pero **no se instala**.
- Servir por **HTTPS** → **se instala de verdad**, con icono propio, pantalla completa y offline.

Por eso el modo producción es publicar la carpeta `web/` por HTTPS.

---

## IA gratis para preguntas abiertas (Groq) — sin depender de tu PC

La app puede responder **preguntas abiertas con IA** sin backend y sin que tu PC esté encendida: llama directo a **Groq** desde el navegador (Groq permite CORS desde cualquier origen).

**Cómo activarla (2 minutos, gratis, sin tarjeta):**

1. Entrá a **https://console.groq.com** y creá una cuenta (email o Google/GitHub).
2. En el menú lateral → **API Keys** → **Create API Key**. Copiala (empieza con `gsk_`; se muestra una sola vez).
3. En la app → pestaña **Asistente** → sección **“IA para preguntas abiertas”** → pegá la key → **Guardar**.

La key se guarda **solo en el navegador de ese dispositivo** (`localStorage`) y **nunca** se sube al repositorio. Cada dispositivo que uses necesita su propia key.

**Cómo funciona el flujo:**

```
Pregunta del usuario
   ↓
Motor local (embebido, sin internet)  →  responde el ~80%: precios, cajas,
   │                                       códigos, impuestos, tu colección
   ↓ (si no sabe)
IA Groq (gpt-oss-120b)                →  responde lo abierto, con contexto
                                          del auto del catálogo si lo menciona
```

**Límites del plan gratis de Groq (octubre 2026):** 30 req/min, **1.000 req/día**, 8.000 tokens/min en `openai/gpt-oss-120b`. Sin tarjeta de crédito.

**Si la cuota se agota:** la app lo dice explícitamente y el asistente sigue funcionando con el motor local (solo se pierden las preguntas abiertas hasta que se renueve la cuota al día siguiente).

**Alternativa (Gemini):** el free tier de Gemini en 2026 quedó muy limitado (~20 req/día para los modelos flash), por eso se eligió Groq. Si preferís Gemini, hay que cambiar el endpoint en `build/build_app.py` (`GROQ_URL`/`GROQ_MODEL`).

---

## Modo conectado — el celular conectado a tu agente (puente)
Esto es lo que la convierte en una app **conectada a tu PC y a tu asistente**, con **modo offline** si no hay red o el puente está caído.

```bash
python agent_bridge.py --port 8081
```

```
  Esta PC:   http://127.0.0.1:8081/
  En la red: http://192.168.x.x:8081/   <- abrí esto en el celular
```

**En el celular (misma red Wi-Fi):** abrí `http://<ip-pc>:8081/` → la app detecta el puente (badge **“asistente”** arriba), y:
- **Preguntar al asistente** → responde **al instante** desde el motor de datos local (`build/atender_cola.py`), sin LLM y sin internet.
- **Actualizar datos** → baja los archivos de datos nuevos y los aplica en el próximo arranque (el overlay `DATOS_FUENTE` reemplaza los datos embebidos por los que trajiste del puente).
- **Sin red o puente caído** → la pregunta **se guarda en cola en el teléfono** y se envía sola cuando vuelve la conexión. La app sigue andando offline (el service worker ya tiene todo).

**Endpoints del puente:**

| Endpoint | Qué hace |
|---|---|
| `GET /agent/status` | estado, cola pendiente, versión de datos |
| `GET /agent/ask?q=...` | el motor local responde al instante; si no sabe, queda en cola |
| `GET /agent/answers?desde=<id>` | respuestas nuevas (para bajar al recuperar red) |
| `POST /agent/push` | el celular sube las preguntas hechas offline |
| `GET /sync/manifest` / `GET /sync/file?name=` | versión y descarga de archivos de datos |
| `GET /sync/refresh` | corre el motor de mercado y devuelve las alertas |

**¿Y si no estás en tu casa?** El puente atiende en la red local. Para el celular **fuesta de casa** hace falta exponerlo por HTTPS: un túnel (`cloudflared`, `ngrok`) o una VPN como **Tailscale**. Sin eso, el celular no alcanza la IP local — la app se abre igual, funciona offline y sincroniza cuando volvés a tu red.

> **Aviso de seguridad:** si lo exponés a internet, agregá autenticación (el puente no la tiene). El puente da acceso a tus datos de colección. Y `hermes serve --insecure` **ya no desactiva la autenticación** (según la docs, hardening de junio 2026).

---

## Opción A — GitHub Pages (recomendada: gratis, HTTPS, 2 comandos)

Ya tenés `gh` autenticado en esta máquina (cuenta `foxnismone`). Desde la carpeta del proyecto:

```bash
cd web
git init -b main
git add .
git commit -m "HW Collector — PWA"
gh repo create hw-collector --public --source=. --push
gh api -X POST repos/foxnismone/hw-collector/pages \
  -f "source[branch]=main" -f "source[path]=/"
```

Esperá ~1 minuto y la app queda en:

```
https://foxnismone.github.io/hw-collector/
```

**En el celular:** abrí esa URL en Chrome (Android) → aparece el botón **“Instalar app”** (también en el menú ⋮ → *Instalar app* / *Agregar a pantalla de inicio*).
**En iPhone:** abrí la URL en Safari → botón **Compartir (□↑)** → **“Agregar a pantalla de inicio”**.

Notas:
- Repositorio **público** (Pages en repos privados requiere plan pago). Si no querés que sea público, usá la opción B.
- El manifest usa rutas **relativas**, así que funciona igual bajo el subdirectorio `/hw-collector/`.
- Para actualizar: `cd web && git add . && git commit -m "update" && git push`.

---

## Opción B — Cloudflare Pages o Netlify Drop (sin CLI, sin repo público)

1. Entrá a **https://app.netlify.com/drop** (o Cloudflare Pages → *Upload assets*).
2. Arrastrá **la carpeta `web/`** completa (incluye `img/`, `icons/`, `manifest.webmanifest`, `sw.js`).
3. Te da una URL **HTTPS** al instante (ej. `https://algo-random.netlify.app`).
4. En el celular: abrí esa URL → **Instalar app**.

Ventaja: no expone nada en tu GitHub. Desventaja: para actualizar hay que volver a arrastrar la carpeta (o conectar el repo).

---

## Opción C — APK de Android real (Capacitor)

Es la vía para tener un **archivo `.apk`** que se instala en el teléfono como cualquier app, y el único formato que acepta Google Play.

**Ya está todo automatizado:** `bash build/make_apk.sh` instala lo que falte y genera `dist/HWCollector-debug.apk`.

Qué instala ese script (no está en esta máquina todavía):
1. **JDK 17** (~180 MB) vía `winget`.
2. **Android SDK** — command-line tools + platform 34 + build-tools 34 (~1,5 GB).
3. **Capacitor** (npm) y compila con Gradle (la primera vez descarga Gradle, ~150 MB).

Tiempo total: **15–30 min** la primera vez. Espacio: ~2 GB. Después de eso, recompilar tarda ~1 minuto.

### APK de Capacitor vs APK de PWABuilder (TWA)

| | **Capacitor** (este script) | **PWABuilder / TWA** |
|---|---|---|
| Dónde vive la app | **dentro del APK** (19 MB) | en tu web (el APK es un marco de ~1 MB) |
| ¿Funciona sin internet desde el arranque? | **Sí** | No: la primera carga necesita la URL online |
| ¿Necesita publicar la PWA primero? | No | **Sí**, exige la URL HTTPS |
| ¿Necesita instalar herramientas? | Sí (JDK + Android SDK) | No: se hace en pwabuilder.com |
| Para Play Store | Sí (firmando el AAB) | Sí |

**Conclusión:** si querés el APK **ya**, sin instalar nada, publicá la PWA (opción A o B) y usá **https://www.pwabuilder.com** → *Package for stores* → *Android*: te devuelve un APK firmado. Si querés un APK **100% offline** y sin depender de ninguna web, usá Capacitor con el script de este repo.

### Limitación honesta del APK

Dentro del WebView de Android:
- **Voz (hablar):** funciona — usa el TTS del sistema.
- **Micrófono (reconocimiento de voz):** **no funciona**, porque el WebView no implementa Web Speech API. Se resuelve agregando `@capacitor-community/speech-recognition` y llamando al plugin cuando `window.Capacitor` exista.
- Todo lo demás (catálogo, colección, seguimiento, cajas, mercados, valoraciones) funciona igual, sin internet.

Para publicar en **Google Play** hace falta firmar (`keytool` + `gradlew bundleRelease`) y una cuenta de desarrollador (US$25 pago único).

---

## Opción D — Probarla ya, en la red local (sin instalar)

```bash
python serve.py
```

Imprime la dirección para el celular (`http://TU-IP:8080/`) y genera un **QR** (`qr-lan.png`) para escanear.

Funciona completo (catálogo, colección, seguimiento, cajas, mercados, asistente), pero **no se puede instalar** porque es HTTP: el navegador exige HTTPS para eso.

---

## Qué queda instalado en el celular

| | |
|---|---|
| **Icono** | propio (fondo oscuro + “HW” naranja), incluido maskable para Android |
| **Pantalla completa** | sí, sin barra del navegador (`display: standalone`) |
| **Offline** | sí — el service worker cachea la app y las imágenes |
| **Datos del usuario** | se guardan en el dispositivo (`localStorage`): colección, alertas, cajas identificadas |
| **Atajos** | mantener presionado el icono → *Catálogo* / *Mi colección* |
| **Actualizaciones** | automáticas al abrir con conexión (o `git push` en la opción A) |

## Verificación rápida (después de publicar)

1. Abrí la URL en el celular y confirmá que aparece el botón **Instalar app**.
2. Instalá, abrí la app desde el icono y comprobá que entra en pantalla completa.
3. Activá **modo avión** y abrí la app de nuevo: debe seguir funcionando (catálogo y colección).
4. En Chrome de escritorio: `F12 → Application → Manifest` (sin errores) y `Service Workers` (activado).
