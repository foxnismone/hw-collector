#!/usr/bin/env python3
"""Validacion visual por similitud semantica (CLIP local).

Evita falsos positivos: una imagen solo se acepta si es visualmente coherente
con el nombre del modelo. Usa el modelo CLIP ya presente en tools/clip.

Si el modelo o onnxruntime no estan disponibles, el modulo degrada a None y el
resto del sistema sigue funcionando (sin filtro visual).
"""
from __future__ import annotations
import io, json, os, re, threading

from .config import Config, DEFAULT

_lock = threading.Lock()
_modelo = None
_tokenizador = None
_disponible = None


# ---------------------------------------------------------------- tokenizer
class TokenizerSimple:
    """Tokenizer compatible con CLIP (BPE en tokenizer.json) sin dependencias."""

    def __init__(self, path: str):
        with open(path, encoding='utf-8') as f:
            cfg = json.load(f)
        model = cfg.get('model') or {}
        self.vocab: dict[str, int] = {}
        for tok, idx in (model.get('vocab') or {}).items():
            self.vocab[tok] = int(idx)
        self.merges: list[tuple[str, str]] = []
        for m in (model.get('merges') or []):
            if isinstance(m, list) and len(m) == 2:
                self.merges.append((m[0], m[1]))
        # merges pueden venir como texto "a b" por linea
        if not self.merges and isinstance(model.get('merges'), str):
            for linea in model['merges'].splitlines():
                p = linea.split()
                if len(p) == 2:
                    self.merges.append((p[0], p[1]))
        self.bos = 49406
        self.eos = 49407
        self.ctx = 77
        self.cache: dict[str, list[str]] = {}
        self.byte_encoder = {b: chr(b) for b in range(256)}

    # CLIP usa GPT-2 BPE sobre bytes -> unicode
    def _bytes_to_unicode(self) -> dict[int, str]:
        bs = list(range(ord('!'), ord('~') + 1)) + list(range(ord('¡'), ord('¬') + 1)) + \
             list(range(ord('®'), ord('ÿ') + 1))
        cs = bs[:]
        n = 0
        for b in range(256):
            if b not in bs:
                bs.append(b)
                cs.append(256 + n)
                n += 1
        return dict(zip(bs, [chr(c) for c in cs]))

    def _get_pairs(self, palabra: tuple):
        return set(zip(palabra[:-1], palabra[1:]))

    def _bpe(self, token: str) -> list[str]:
        if token in self.cache:
            return self.cache[token]
        palabra = tuple(token)
        if len(palabra) == 1:
            return list(palabra)
        pares = self._get_pairs(palabra)
        if not pares:
            return list(palabra)
        merges = self._merge_dict()
        while True:
            bigrama = min(pares, key=lambda p: merges.get(p, float('inf')))
            if bigrama not in merges:
                break
            primero, segundo = bigrama
            nueva = []
            i = 0
            while i < len(palabra):
                try:
                    j = palabra.index(primero, i)
                except ValueError:
                    nueva.extend(palabra[i:])
                    break
                nueva.extend(palabra[i:j])
                i = j
                if i < len(palabra) - 1 and palabra[i + 1] == segundo:
                    nueva.append(primero + segundo)
                    i += 2
                else:
                    nueva.append(primero)
                    i += 1
            palabra = tuple(nueva)
            if len(palabra) == 1:
                break
            pares = self._get_pairs(palabra)
        self.cache[token] = list(palabra)
        return list(palabra)

    def _merge_dict(self) -> dict[tuple, int]:
        if not hasattr(self, '_md'):
            self._md = {m: i for i, m in enumerate(self.merges)}
        return self._md

    def encode(self, texto: str) -> list[int]:
        b2u = self._bytes_to_unicode()
        texto = texto.lower()
        texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
        out = [self.bos]
        for tok in re.findall(r'\S+', texto):
            if not tok:
                continue
            piece = ''.join(b2u[b] for b in tok.encode('utf-8'))
            for sub in self._bpe(piece):
                if sub in self.vocab:
                    out.append(self.vocab[sub])
        out.append(self.eos)
        return out[:self.ctx]


# ---------------------------------------------------------------- modelo
def _cargar(cfg: Config):
    global _modelo, _tokenizador, _disponible
    if _disponible is not None:
        return _modelo, _tokenizador
    try:
        import numpy as np
        import onnxruntime as ort
    except Exception:
        _disponible = False
        return None, None

    try:
        import PIL.Image as PILImage
        cache = os.path.join(cfg.clip_dir, 'cache')
        os.makedirs(cache, exist_ok=True)
        prov = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        vis = ort.InferenceSession(os.path.join(cfg.clip_dir, 'vision_model_quantized.onnx'),
                                   providers=[p for p in prov if p in ort.get_available_providers()])
        txt = ort.InferenceSession(os.path.join(cfg.clip_dir, 'text_model_quantized.onnx'),
                                   providers=[p for p in prov if p in ort.get_available_providers()])
        _modelo = (vis, txt, np, PILImage)
        _tokenizador = TokenizerSimple(os.path.join(cfg.clip_dir, 'tokenizer.json'))
        _disponible = True
    except Exception:
        _disponible = False
        _modelo = None
        _tokenizador = None
    return _modelo, _tokenizador


def disponible() -> bool:
    _cargar(DEFAULT)
    return bool(_disponible)


# ---------------------------------------------------------------- inferencia
def _preprocesar_imagen(datos: bytes, PILImage, np):
    """Preprocesa bytes crudos (o un path) al tensor 3x224x224 de CLIP."""
    try:
        img = PILImage.open(io.BytesIO(datos)).convert('RGB')
    except Exception:
        return None
    # centro crop cuadrado + resize 224
    w, h = img.size
    lado = min(w, h)
    img = img.crop(((w - lado) // 2, (h - lado) // 2, (w - lado) // 2 + lado, (h - lado) // 2 + lado))
    img = img.resize((224, 224), PILImage.BICUBIC)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    media = np.array([0.48145466, 0.4578275, 0.40821073], dtype=np.float32)
    std = np.array([0.26862954, 0.26130258, 0.27577711], dtype=np.float32)
    arr = (arr - media) / std
    return arr.transpose(2, 0, 1)[None, ...].astype(np.float32)


def _texto_a_tokens(texto: str, tok, np):
    ids = tok.encode(texto)
    arr = np.zeros((1, 77), dtype=np.int64)
    for i, v in enumerate(ids[:77]):
        arr[0, i] = v
    return arr


def score_visual(consulta: str, datos: bytes, cfg: Config = DEFAULT) -> float:
    """Similitud coseno CLIP entre la consulta y la imagen. 0 si no se puede."""
    modelo, tok = _cargar(cfg)
    if not modelo or not tok:
        return 0.0
    vis, txt, np, PILImage = modelo
    with _lock:
        try:
            img_t = _preprocesar_imagen(datos, PILImage, np)
            if img_t is None:
                return 0.0
            vname = vis.get_inputs()[0].name
            vin = vis.run(None, {vname: img_t})[0]
            tids = _texto_a_tokens(consulta, tok, np)
            tname = txt.get_inputs()[0].name
            tin = txt.run(None, {tname: tids})[0]
            a = vin[0].astype('float32')
            b = tin[0].astype('float32')
            na = (a * a).sum() ** 0.5 or 1.0
            nb = (b * b).sum() ** 0.5 or 1.0
            return float((a @ b) / (na * nb))
        except Exception:
            return 0.0


def score_visual_path(consulta: str, ruta: str, cfg: Config = DEFAULT) -> float:
    try:
        with open(ruta, 'rb') as f:
            return score_visual(consulta, f.read(), cfg)
    except Exception:
        return 0.0
