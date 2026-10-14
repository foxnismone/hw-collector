#!/usr/bin/env bash
# make_apk.sh — genera un APK de Android real de HW Collector (Capacitor).
#
# Requisitos: Node (ya lo tenés). El script instala el resto si falta:
#   · JDK 17          (winget: Microsoft.OpenJDK.17)
#   · Android SDK     (command-line tools + platform 34 + build-tools 34)
#
# Uso:   bash build/make_apk.sh
# Salida: dist/HWCollector-debug.apk
#
# Por qué Capacitor y no una TWA (PWABuilder):
#   La TWA carga la app desde una URL: necesita internet la primera vez.
#   Capacitor mete los 19 MB de la app DENTRO del APK → funciona sin internet
#   desde el primer arranque, y es el formato que acepta Google Play.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo "== Proyecto: $ROOT"

# ---------- 1. JDK ----------
if ! command -v java >/dev/null 2>&1; then
  echo "== Instalando JDK 17 (winget)…"
  winget install --id Microsoft.OpenJDK.17 --accept-source-agreements --accept-package-agreements -h || \
  winget install --id EclipseAdoptium.Temurin.17.JDK --accept-source-agreements --accept-package-agreements -h
  export JAVA_HOME="$(ls -d '/c/Program Files/Microsoft/jdk-17'* 2>/dev/null | head -1)"
  export PATH="$JAVA_HOME/bin:$PATH"
fi
java -version 2>&1 | head -1 || { echo "!! Java no quedó disponible. Cerrá y reabrí la terminal, y volvé a correr el script."; exit 1; }

# ---------- 2. Android SDK ----------
export ANDROID_HOME="${ANDROID_HOME:-$LOCALAPPDATA/Android/Sdk}"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
if [ ! -d "$ANDROID_HOME/cmdline-tools/latest" ]; then
  echo "== Instalando Android command-line tools…"
  mkdir -p "$ANDROID_HOME/cmdline-tools"
  TMP="$(mktemp -d)"
  curl -sL -o "$TMP/tools.zip" "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"
  unzip -q -o "$TMP/tools.zip" -d "$TMP"
  mv "$TMP/cmdline-tools" "$ANDROID_HOME/cmdline-tools/latest" 2>/dev/null || \
    mv "$ANDROID_HOME/cmdline-tools" "$ANDROID_HOME/cmdline-tools-tmp" && mkdir -p "$ANDROID_HOME/cmdline-tools" && \
    mv "$ANDROID_HOME/cmdline-tools-tmp" "$ANDROID_HOME/cmdline-tools/latest"
fi
SDKM="$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager.bat"
[ -f "$SDKM" ] || SDKM="$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager"
echo "== Aceptando licencias e instalando platform 34 + build-tools…"
yes | "$SDKM" --licenses >/dev/null 2>&1 || true
"$SDKM" "platform-tools" "platforms;android-34" "build-tools;34.0.0" >/dev/null

# ---------- 3. Capacitor ----------
echo "== Preparando Capacitor…"
[ -f package.json ] || npm init -y >/dev/null
npm install --silent @capacitor/core @capacitor/cli @capacitor/android

cat > capacitor.config.json <<'JSON'
{
  "appId": "app.hwcollector",
  "appName": "HW Collector",
  "webDir": "web",
  "android": { "allowMixedContent": false, "backgroundColor": "#0c0e12" },
  "server": { "androidScheme": "https" }
}
JSON

[ -d android ] || npx cap add android
npx cap sync android

# ---------- 4. APK ----------
echo "== Compilando APK (la primera vez descarga Gradle, tarda unos minutos)…"
cd android
chmod +x ./gradlew 2>/dev/null || true
./gradlew assembleDebug
cd "$ROOT"

mkdir -p dist
cp android/app/build/outputs/apk/debug/app-debug.apk dist/HWCollector-debug.apk
echo
echo "== LISTO: $ROOT/dist/HWCollector-debug.apk  ($(du -h dist/HWCollector-debug.apk | cut -f1))"
echo
echo "Instalación en el celular:"
echo "  1) Pasá el APK al teléfono (cable, Google Drive, Telegram a vos mismo)."
echo "  2) Abrilo y permití 'Instalar apps de fuentes desconocidas' para ese gestor de archivos."
echo
echo "Nota: la VOZ funciona en el APK así: hablar (TTS) SÍ; micrófono (reconocimiento)"
echo "NO, porque el WebView de Android no implementa Web Speech API. Se resuelve con"
echo "un plugin nativo (@capacitor-community/speech-recognition) — ver DEPLOY.md."
