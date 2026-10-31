# -*- coding: utf-8 -*-
"""
Servidor local para HW Collector.

Uso:
    python serve.py                # puerto 8080, accesible desde el celular en la misma Wi-Fi
    python serve.py --port 9000
    python serve.py --host 127.0.0.1

Imprime las direcciones de acceso y genera un código QR (PNG) para abrir la app
desde el teléfono sin tipear la IP.

OJO — límite real de los navegadores: por HTTP en red local la app funciona
(se ve, se usa, guarda datos), pero el navegador NO permite instalar un PWA ni
registrar el service worker porque exige un "contexto seguro" (HTTPS o localhost).
Para instalar en el celular hay que publicarla por HTTPS: ver DEPLOY.md
(opción A: GitHub Pages, gratis, 2 comandos).
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import os
import socket
import socketserver
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(ROOT, "web")


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
        ".webp": "image/webp",
        ".json": "application/json",
        ".js": "text/javascript",
        ".svg": "image/svg+xml",
    }

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Service-Worker-Allowed", "/")
        super().end_headers()

    # ---- voces ----
    # Piper: neuronal, LOCAL, gratis, sin API key ni internet (recomendado).
    # edge-tts: voces de Microsoft; su endpoint devuelve 403 cuando rotan el token.
    VOCES_EDGE = [
        {"id": "es-CL-LorenzoNeural", "nombre": "Lorenzo (Chile)", "genero": "M"},
        {"id": "es-CL-CatalinaNeural", "nombre": "Catalina (Chile)", "genero": "F"},
        {"id": "es-MX-JorgeNeural", "nombre": "Jorge (México)", "genero": "M"},
        {"id": "es-MX-DaliaNeural", "nombre": "Dalia (México)", "genero": "F"},
        {"id": "es-AR-TomasNeural", "nombre": "Tomás (Argentina)", "genero": "M"},
        {"id": "es-US-AlonsoNeural", "nombre": "Alonso (Latino EE.UU.)", "genero": "M"},
    ]
    _piper = {}

    @classmethod
    def voces_piper(cls):
        d = os.path.join(ROOT, "voices")
        out = []
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.endswith(".onnx"):
                    out.append({"id": f[:-5], "nombre": f[:-5].replace("-", " ").replace("_", " "), "archivo": f})
        return out

    @classmethod
    def cargar_piper(cls, voz):
        if voz in cls._piper:
            return cls._piper[voz]
        ruta = os.path.join(ROOT, "voices", voz + ".onnx")
        if not os.path.exists(ruta):
            return None
        try:
            from piper import PiperVoice
            v = PiperVoice.load(ruta)
            cls._piper[voz] = v
            return v
        except Exception as e:
            sys.stderr.write("  piper error: %s\n" % e)
            return None

    def _tts_piper(self, texto, voz):
        v = self.cargar_piper(voz)
        if not v:
            return None
        import io, wave
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            v.synthesize_wav(texto[:1200], wf)
        return buf.getvalue()

    def _tts_edge(self, texto, voz):
        try:
            import asyncio
            import edge_tts
        except ImportError:
            return None
        async def gen():
            com = edge_tts.Communicate(texto, voz)
            audio = b""
            async for chunk in com.stream():
                if chunk.get("type") == "audio":
                    audio += chunk["data"]
            return audio
        try:
            return asyncio.run(gen())
        except Exception:
            return None

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _audio(self, datos, tipo):
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(datos)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(datos)

    def do_GET(self):
        if self.path.startswith("/tts-voices"):
            return self._json({"piper": self.voces_piper(), "edge": self.VOCES_EDGE})
        if self.path.startswith("/tts"):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            texto = (q.get("text", [""])[0] or "").strip()[:1200]
            voz = q.get("voice", [""])[0]
            if not texto:
                return self._json({"error": "falta el texto"}, 400)
            piper_voces = self.voces_piper()
            if piper_voces:
                if not any(v["id"] == voz for v in piper_voces):
                    voz = piper_voces[0]["id"]
                datos = self._tts_piper(texto, voz)
                if datos:
                    return self._audio(datos, "audio/wav")
            datos = self._tts_edge(texto, voz if voz in [v["id"] for v in self.VOCES_EDGE] else "es-MX-JorgeNeural")
            if datos:
                return self._audio(datos, "audio/mpeg")
            return self._json({"error": "sin motor de voz disponible (revisá la carpeta voices/ o edge-tts)"}, 503)
        return super().do_GET()

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


def lan_ip() -> str:
    """IP local de la interfaz que sale a internet (no requiere conexión real)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(2.0)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--host", default="0.0.0.0")
    a = ap.parse_args()

    if not os.path.isdir(WEB):
        print("No encuentro la carpeta web/. Ejecutá este script desde la raíz del proyecto.")
        return 1

    handler = functools.partial(Handler, directory=WEB)
    socketserver.ThreadingTCPServer.allow_reuse_address = True

    ip = lan_ip()
    print("\n  HW Collector — servidor local")
    print("  " + "─" * 52)
    print(f"  En esta computadora :  http://127.0.0.1:{a.port}/")
    print(f"  Desde el celular    :  http://{ip}:{a.port}/   (misma red Wi-Fi)")
    print(f"  Catálogo            :  http://{ip}:{a.port}/galeria_catalogo.html")
    print(f"  Mi colección        :  http://{ip}:{a.port}/galeria_coleccion.html")
    print("  " + "─" * 52)
    print("  Voces neuronales:  /tts-voices  (edge-tts, gratis) — incluye es-CL y es-MX")
    print("  Nota: por HTTP local la app se usa pero NO se puede instalar como PWA.")
    print("  Para instalarla en el celular: publicá la carpeta web/ por HTTPS (ver DEPLOY.md).")
    print("  Ctrl+C para detener.\n")

    try:
        import qrcode  # opcional
        url = f"http://{ip}:{a.port}/"
        qr = qrcode.QRCode(border=1, box_size=1)
        qr.add_data(url)
        qr.make()
        qr.print_ascii(invert=True)
        out = os.path.join(ROOT, "qr-lan.png")
        qrcode.make(url).save(out)
        print(f"  QR guardado en {out} (escanealo con el celular)\n")
    except Exception:
        pass

    with socketserver.ThreadingTCPServer((a.host, a.port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Servidor detenido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
