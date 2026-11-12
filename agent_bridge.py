#!/usr/bin/env python3
"""Bridge de datos para Hot Wheels Collector.
Sirve los archivos JSON de data/ y los sincroniza al navegador.
"""
import json
import os
import time
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote, parse_qs

VERSION = "2.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
WEB_DIR = os.path.join(BASE_DIR, "web")

# Archivos que se pueden servir
ARCHIVOS = {
    "catalog_web.json": "CAT",
    "cajas.json": "CAJ",
    "tendencias.json": "TEND",
    "mercados.json": "MKT",
    "precios_referencia.json": "PRE",
    "indice.json": "IDXI",
    "owned_collection.json": "OWNED_DEMO",
    "seguimiento.json": "SEG",
    "historias.json": "HIST",
}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silencioso

    def _send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _send_file(self, filepath):
        if not os.path.exists(filepath):
            self.send_error(404)
            return
        with open(filepath, "rb") as f:
            data = f.read()
        ext = os.path.splitext(filepath)[1].lower()
        ct = {".json": "application/json; charset=utf-8",
              ".js": "application/javascript; charset=utf-8",
              ".html": "text/html; charset=utf-8",
              ".css": "text/css",
              ".webp": "image/webp", ".jpg": "image/jpeg", ".png": "image/png",
              ".svg": "image/svg+xml", ".ico": "image/x-icon"}.get(ext, "application/octet-stream")
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parsed.query

        # Endpoint de estado
        if path == "/agent/status":
            archivos = []
            for nombre in ARCHIVOS:
                fp = os.path.join(DATA_DIR, nombre)
                if os.path.exists(fp):
                    try:
                        with open(fp, "rb") as f:
                            content = f.read()
                        hash_val = hashlib.md5(content).hexdigest()[:12]
                    except Exception:
                        hash_val = str(int(os.path.getmtime(fp)))
                    archivos.append({
                        "nombre": nombre,
                        "hash": hash_val,
                        "size": os.path.getsize(fp)
                    })
            self._send_json({
                "vivo": True,
                "version": VERSION,
                "actualizado": time.strftime("%Y-%m-%d %H:%M:%S"),
                "archivos": archivos,
            })
            return

        # Endpoint de sincronización (formato ?name= y /sync/<archivo>)
        if path.startswith("/sync/"):
            if path == "/sync/file":
                qs = parse_qs(query)
                nombre = (qs.get("name") or [""])[0]
            else:
                nombre = unquote(path[6:])
            if nombre in ARCHIVOS:
                filepath = os.path.join(DATA_DIR, nombre)
                if os.path.exists(filepath):
                    self._send_file(filepath)
                    return
            self.send_error(404)
            return

        # Endpoint de tendencias
        if path == "/trends":
            try:
                with open(os.path.join(DATA_DIR, "tendencias.json"), encoding="utf-8") as f:
                    tend = json.load(f)
                self._send_json({
                    "alertas": [],
                    "indice_tendencia": {"valor": 68, "cambio_pct": 12.5},
                    "demanda": tend.get("demanda_coleccionistas", {}),
                })
            except Exception as e:
                self._send_json({"error": str(e)})
            return

        # Servir archivos estáticos de web/
        if path == "/" or path == "":
            self._send_file(os.path.join(WEB_DIR, "index.html"))
            return
        filepath = os.path.join(WEB_DIR, path.lstrip("/"))
        if os.path.isfile(filepath):
            self._send_file(filepath)
            return

        self.send_error(404)

    def do_POST(self):
        self.send_error(405)

if __name__ == "__main__":
    from http.server import ThreadingHTTPServer
    port = 8081
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    srv.daemon_threads = True
    print(f"Bridge de datos escuchando en http://localhost:{port}")
    print(f"  /agent/status - estado")
    print(f"  /sync/<archivo> - sincronizar datos")
    print(f"  /trends - tendencias")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nBridge detenido")
    finally:
        srv.server_close()
