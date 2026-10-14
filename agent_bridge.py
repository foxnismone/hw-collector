# -*- coding: utf-8 -*-
"""
Puente celular <-> asistente  (python agent_bridge.py --port 8080)

Sirve la app (web/) y expone el backend que el celular usa:

  GET  /agent/status          -> estado del puente, cola, versión de datos
  GET  /agent/ask?q=...       -> pregunta. El motor local responde al instante;
                                 si no sabe, queda en cola para el agente.
  GET  /agent/answers?desde=  -> respuestas nuevas (para bajar al recuperar red)
  POST /agent/push            -> el celular sube las preguntas que hizo offline
  GET  /sync/manifest         -> versión y hash de cada archivo de datos
  GET  /sync/file?name=...     -> descarga un archivo de datos
  GET  /sync/refresh          -> corre el motor de mercado y devuelve las alertas

Todo corre en la PC (donde están los datos y el asistente). El celular en la
misma red lo alcanza por http://<ip-pc>:8080/ . Fuera de casa hace falta un
túnel (ver DEPLOY.md).
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import http.server
import json
import os
import socket
import socketserver
import subprocess
import sys
import threading
import time
import urllib.parse
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "build"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atender_cola import responder  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
WEB = os.path.join(ROOT, "web")
BUILD = os.path.join(ROOT, "build")

DATOS_ARCHIVOS = ["catalog_web.json", "cajas.json", "tendencias.json", "mercados.json",
                   "precios_referencia.json", "owned_collection.json", "indice.json",
                   "seguimiento.json", "alertas.json", "tesoreros.json", "historias.json"]

COLA = os.path.join(DATA, "cola_agente.json")
RESP = os.path.join(DATA, "respuestas_agente.json")
_lock = threading.Lock()


def _load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _save(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def new_id(q: str) -> str:
    return hashlib.md5((q + str(time.time())).encode("utf-8")).hexdigest()[:12]


def encolar(pregunta: str):
    with _lock:
        cola = _load(COLA, [])
        item = {"id": new_id(pregunta), "pregunta": pregunta, "fecha": date.today().isoformat()}
        cola.append(item)
        _save(COLA, cola)
    return item


def responder_item(item):
    r, intencion = responder(item["pregunta"])
    with _lock:
        respuestas = _load(RESP, [])
        if r:
            respuestas.append({"id": item["id"], "pregunta": item["pregunta"], "respuesta": r,
                               "intencion": intencion, "fecha": date.today().isoformat(), "origen": "motor local"})
            _save(RESP, respuestas)
        return r, intencion


def manifest():
    archivos = []
    for n in DATOS_ARCHIVOS:
        p = os.path.join(DATA, n)
        if os.path.exists(p):
            b = open(p, "rb").read()
            archivos.append({"nombre": n, "bytes": len(b),
                             "hash": hashlib.md5(b).hexdigest()[:10], "mtime": int(os.path.getmtime(p))})
    version = hashlib.md5("".join(a["hash"] for a in archivos).encode()).hexdigest()[:10]
    return {"version": version, "actualizado": date.today().isoformat(), "archivos": archivos}


def correr_refresh():
    """Corre el motor de mercado y devuelve el resumen."""
    try:
        out = subprocess.run([sys.executable, os.path.join(BUILD, "refresh_market.py"), "--evaluate",
                              "--alertas-only"], capture_output=True, text=True, timeout=900)
        alertas = _load(os.path.join(DATA, "alertas.json"), []) or []
        seg = _load(os.path.join(DATA, "seguimiento.json"), {}) or {}
        return {"ok": True, "alertas": alertas[:60], "n_alertas": len(alertas),
                "mejores_alertas": [a for a in alertas if a.get("prioridad") == "alta"][:10],
                "salida": (out.stdout or "").strip().splitlines()[-12:], "n_modelos": len(seg.get("modelos", {}))}
    except Exception as e:
        return {"ok": False, "error": str(e)}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=WEB, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    # ------------------------------- agente
    def _ask(self, q):
        q = (q or "").strip()
        if not q or len(q) > 600:
            return self._json({"error": "pregunta vacía o demasiado larga"}, 400)
        item = encolar(q)
        r, intencion = responder_item(item)
        if r:
            return self._json({"id": item["id"], "estado": "respondida", "respuesta": r,
                              "intencion": intencion, "origen": "motor local"})
        return self._json({"id": item["id"], "estado": "en_cola",
                          "aviso": "El motor local no supo responder. El agente la contestará cuando pueda."})

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)

        if u.path == "/agent/status":
            cola = _load(COLA, [])
            respuestas = _load(RESP, [])
            ids_ok = {r["id"] for r in respuestas}
            pend = [c for c in cola if c["id"] not in ids_ok]
            return self._json({"ok": True, "agente": "puente local (motor de datos)",
                               "cola_pendientes": len(pend), "respuestas_totales": len(respuestas),
                               "datos": manifest(), "hora": time.strftime("%Y-%m-%d %H:%M:%S")})
        if u.path == "/agent/ask":
            return self._ask(q.get("q", [""])[0])
        if u.path == "/agent/answers":
            desde = q.get("desde", [""])[0]
            respuestas = _load(RESP, [])
            nuevas = [r for r in respuestas if r["id"] > desde] if desde else respuestas[-40:]
            return self._json({"respuestas": nuevas, "total": len(respuestas),
                               "ultima_id": respuestas[-1]["id"] if respuestas else ""})
        if u.path == "/sync/manifest":
            return self._json(manifest())
        if u.path == "/sync/file":
            nombre = (q.get("name", [""])[0] or "").strip()
            if nombre not in DATOS_ARCHIVOS:
                return self._json({"error": "archivo no permitido"}, 403)
            p = os.path.join(DATA, nombre)
            if not os.path.exists(p):
                return self._json({"error": "no existe"}, 404)
            with open(p, "rb") as f:
                datos = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(datos)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return self.wfile.write(datos)
        if u.path == "/sync/refresh":
            return self._json(correr_refresh())
        if u.path == "/trends":
            datos = _load(os.path.join(DATA, "tendencias_activas.json"), None)
            if not datos:
                return self._json({"error": "aún no hay datos de tendencias. Ejecutá: python build/trend_watcher.py --sync", "alertas": []})
            return self._json(datos)
        return super().do_GET()

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == "/agent/push":
            n = int(self.headers.get("Content-Length") or 0)
            try:
                payload = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
            except Exception:
                return self._json({"error": "JSON inválido"}, 400)
            preguntas = payload.get("preguntas") or []
            respondidas = 0
            encoladas = []
            for p in preguntas:
                item = encolar(str(p)[:600])
                r, intencion = responder_item(item)
                if r:
                    respondidas += 1
                else:
                    encoladas.append(item["id"])
            return self._json({"recibidas": len(preguntas), "respondidas": respondidas,
                              "en_cola": encoladas})
        return self._json({"error": "no encontrado"}, 404)

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--host", default="0.0.0.0")
    a = ap.parse_args()
    httpd = ThreadingServer((a.host, a.port), Handler)
    print()
    print("  Puente celular <-> asistente")
    print("  " + "─" * 52)
    print("  Esta PC:   http://127.0.0.1:%d/" % a.port)
    ip = local_ip()
    print(f"  En la red: http://{ip}:{a.port}/   <- abrí esto en el celular")
    print("  Endpoints: /agent/status · /agent/ask?q=... · /agent/answers")
    print("             /agent/push (POST) · /sync/manifest · /sync/file · /sync/refresh")
    print("  Ctrl+C para detener.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\npuente detenido")


if __name__ == "__main__":
    main()
