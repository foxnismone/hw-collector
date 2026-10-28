#!/usr/bin/env python3
"""Configuracion central de image-doctor.

Todo lo sensible (rutas, umbrales, timeouts) vive aca para que el resto de
modulos sea puro y testeable.
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field

# ---------------------------------------------------------------- paths
BASE = os.environ.get('HW_BASE', r'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector')
DATA = os.path.join(BASE, 'data')
IMG_DIR = os.path.join(BASE, 'img')
LOG_DIR = os.path.join(BASE, 'logs')
CACHE_DIR = os.path.join(BASE, 'cache', 'imadoctor')
# Raices donde resolver rutas locales relativas (el sitio las arma como 'img/'+f)
LOCAL_ROOTS = ('img', '')

# ---------------------------------------------------------------- red
TIMEOUT = 20
RETRIES = 3
RETRY_DELAY = 1.2
CONCURRENCY = 8

# ---------------------------------------------------------------- formatos
ALLOWED_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.avif'}
ALLOWED_MIME = {
    'image/png', 'image/jpeg', 'image/webp', 'image/gif',
    'image/svg+xml', 'image/avif', 'image/bmp',
}
MIN_BYTES = 800          # por debajo: probable placeholder/tracking pixel
MAX_BYTES = 40 * 1024 * 1024
MIN_DIM = 40             # px: por debajo es un icono, no una foto
MAX_DIM = 20000

# ---------------------------------------------------------------- fuentes
FANDOM_API = 'https://hotwheels.fandom.com/api.php'
WESERV = 'https://images.weserv.nl/?url='
UA = 'Mozilla/5.0 (hotwheels-collector-image-doctor; +https://github.com/foxnismone)'
# Wikia/Fandom devuelve 403 a user-agents que no parecen navegador. Para
# DESCARGAR imagenes hay que usar un UA de navegador real o el validador nunca
# podra confirmar que un candidato sirve.
UA_IMAGEN = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
             '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')


def headers_imagen(cfg: 'Config') -> dict:
    """Headers que Wikia/Fandom exige para servir una imagen.

    Sin 'Accept' y 'Referer' responde 403 aunque el UA sea de navegador: es la
    razon por la que el validador descartaba imagenes que si existen.
    """
    return {
        'User-Agent': cfg.ua_imagen,
        'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'https://hotwheels.fandom.com/',
        'Accept-Language': 'es-CL,es;q=0.9,en;q=0.8',
    }

# ---------------------------------------------------------------- validacion visual (CLIP)
CLIP_DIR = os.path.join(BASE, 'tools', 'clip')
CLIP_ENABLED = os.path.isdir(CLIP_DIR)
CLIP_MIN_SCORE = 0.115   # coseno minimo. Los nombres de producto puntuan bajo
                         # (0.16-0.19 es tipico); 0.18 descartaba imagenes validas


@dataclass
class Config:
    base: str = BASE
    data: str = DATA
    img_dir: str = IMG_DIR
    log_dir: str = LOG_DIR
    cache_dir: str = CACHE_DIR
    timeout: int = TIMEOUT
    retries: int = RETRIES
    concurrency: int = CONCURRENCY
    allowed_exts: frozenset = field(default_factory=lambda: frozenset(ALLOWED_EXTS))
    allowed_mime: frozenset = field(default_factory=lambda: frozenset(ALLOWED_MIME))
    min_bytes: int = MIN_BYTES
    max_bytes: int = MAX_BYTES
    min_dim: int = MIN_DIM
    max_dim: int = MAX_DIM
    fandom_api: str = FANDOM_API
    weserv: str = WESERV
    ua: str = UA
    ua_imagen: str = UA_IMAGEN
    local_roots: tuple = field(default_factory=lambda: tuple(LOCAL_ROOTS))
    clip_dir: str = CLIP_DIR
    clip_min_score: float = CLIP_MIN_SCORE
    dry_run: bool = False
    verbose: bool = True

    def ensure_dirs(self) -> None:
        for d in (self.img_dir, self.log_dir, self.cache_dir):
            os.makedirs(d, exist_ok=True)


DEFAULT = Config()
