#!/usr/bin/env python3
"""Flujo 3 — Validacion y filtrado de resultados candidatos.

Un candidato solo pasa si:
  - responde 200 (o 206) con MIME de imagen permitido
  - tiene un tamano razonable (ni pixel de rastreo ni HTML de error)
  - decodifica como imagen real y tiene dimensiones validas
  - (opcional) supera la validacion visual por CLIP contra la consulta
"""
from __future__ import annotations
import hashlib, os, tempfile
from dataclasses import dataclass
from typing import Callable
import urllib.request, urllib.error

from .config import Config, DEFAULT
from .scanner import _dims_from_bytes


@dataclass
class Verdict:
    url: str
    valid: bool
    score: float = 0.0
    reason: str = ''
    width: int = 0
    height: int = 0
    size: int = 0
    content_type: str = ''
    local_path: str = ''
    sha1: str = ''

    def to_dict(self):
        return self.__dict__


def _head(url: str, cfg: Config) -> tuple[int, dict]:
    info = {}
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', cfg.ua)
        req.add_header('Accept', 'image/*,*/*;q=0.8')
        with urllib.request.urlopen(req, timeout=cfg.timeout) as r:
            info['status'] = r.status
            info['ctype'] = (r.headers.get('Content-Type') or '').split(';')[0].strip()
            info['len'] = int(r.headers.get('Content-Length') or 0)
            return r.status, info
    except urllib.error.HTTPError as e:
        info['status'] = e.code
        info['ctype'] = ''
        info['len'] = 0
        return e.code, info
    except Exception as e:
        info['status'] = 0
        info['error'] = str(e)[:80]
        return 0, info


def _download(url: str, cfg: Config, max_bytes: int | None = None) -> bytes:
    """Descarga con tope de bytes (evita HTML infinitos o binarios enormes)."""
    limite = max_bytes or cfg.max_bytes
    req = urllib.request.Request(url)
    req.add_header('User-Agent', cfg.ua)
    req.add_header('Accept', 'image/*,*/*;q=0.8')
    with urllib.request.urlopen(req, timeout=cfg.timeout) as r:
        return r.read(limite)


def _dims_from_path(path: str) -> tuple[int, int]:
    try:
        from PIL import Image
        with Image.open(path) as im:
            w, h = im.size
            im.verify()
        return int(w), int(h)
    except Exception:
        return 0, 0


def validar(url: str, cfg: Config = DEFAULT,
            consulta_visual: str | None = None,
            score_fn: Callable[[str, str], float] | None = None) -> Verdict:
    """Valida un candidato de imagen. Nunca lanza: devuelve Verdict con reason."""
    v = Verdict(url=url, valid=False)

    # --- 1. existencia y MIME ---
    status, info = _head(url, cfg)
    v.content_type = info.get('ctype', '')
    if status and status >= 400:
        v.reason = f'HTTP {status}'
        return v
    if status == 0:
        v.reason = info.get('error', 'sin respuesta')
        return v
    if v.content_type and v.content_type not in cfg.allowed_mime:
        v.reason = f'MIME no permitido: {v.content_type}'
        return v

    # --- 2. descargar una muestra para inspeccionar bytes reales ---
    try:
        datos = _download(url, cfg, max_bytes=cfg.max_bytes)
    except Exception as e:
        v.reason = f'no descarga: {str(e)[:70]}'
        return v
    v.size = len(datos)
    if len(datos) < cfg.min_bytes:
        v.reason = f'{len(datos)} bytes < minimo {cfg.min_bytes} (posible pixel/HTML)'
        return v

    # --- 3. decodificar y medir ---
    if v.content_type == 'image/svg+xml' or url.lower().split('?')[0].endswith('.svg'):
        if b'<svg' not in datos[:2048].lower():
            v.reason = 'dice SVG pero no contiene <svg>'
            return v
        v.width, v.height = 0, 0
    else:
        w, h = _dims_from_bytes(datos)
        if w == 0:
            # fallback con PIL sobre el chunk (sirve para JPEG progresivo)
            try:
                from PIL import Image
                import io
                with Image.open(io.BytesIO(datos)) as im:
                    w, h = im.size
            except Exception:
                pass
        v.width, v.height = w, h
        if w and (w < cfg.min_dim or h < cfg.min_dim):
            v.reason = f'dimensiones degeneradas {w}x{h}'
            return v
        if w and w > cfg.max_dim:
            v.reason = f'imagen gigante {w}x{h}'
            return v

    # --- 4. validacion visual por CLIP (anti falsos positivos) ---
    if consulta_visual and score_fn is not None:
        try:
            score = float(score_fn(consulta_visual, datos))
        except Exception as e:
            v.reason = f'error en validacion visual: {str(e)[:60]}'
            return v
        v.score = score
        if score < cfg.clip_min_score:
            v.reason = f'score visual {score:.3f} < {cfg.clip_min_score} (irrelevante)'
            return v

    v.valid = True
    v.sha1 = hashlib.sha1(datos).hexdigest()
    return v


def elegir_mejor(candidatos: list[str], cfg: Config = DEFAULT,
                 consulta_visual: str | None = None,
                 score_fn=None) -> Verdict | None:
    """Recorre candidatos en orden y devuelve el primero que pasa todas las validaciones."""
    mejor: Verdict | None = None
    for url in candidatos:
        v = validar(url, cfg, consulta_visual=consulta_visual, score_fn=score_fn)
        if v.valid:
            if mejor is None or v.score > mejor.score:
                mejor = v
                if v.score >= 0.30:      # suficientemente bueno: no seguir buscando
                    break
        else:
            if cfg.verbose:
                print(f'      descartado: {v.reason[:70]}')
    return mejor
