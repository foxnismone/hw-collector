#!/usr/bin/env python3
"""Flujo 1 — Auditoria y deteccion de enlaces rotos.

Escanea codigo fuente (JSON/HTML/JS/Markdown) y el directorio local de imagenes,
identifica cada referencia y valida su estado real (404, ruta vacia, archivo
inexistente, extension corrupta, MIME incorrecto, dimensiones degeneradas).
"""
from __future__ import annotations
import json, os, re, hashlib
from dataclasses import dataclass, field, asdict
from typing import Iterator
from urllib.parse import urlparse, unquote

from .config import Config, DEFAULT, headers_imagen

# --------------------------------------------------------------- cache de sondas
# Probar 12k URLs por HEAD tarda horas; el resultado casi no cambia entre
# corridas, asi que se persiste en disco y se reutiliza.
_cache_http: dict = {}
_cache_cargada = False


def _cache_path(cfg: Config) -> str:
    return os.path.join(cfg.cache_dir, 'sondas_http.json')


def cargar_cache(cfg: Config) -> None:
    global _cache_cargada
    if _cache_cargada:
        return
    try:
        with open(_cache_path(cfg), encoding='utf-8') as f:
            _cache_http.update(json.load(f))
    except Exception:
        pass
    _cache_cargada = True


def guardar_cache(cfg: Config) -> None:
    try:
        cfg.ensure_dirs()
        with open(_cache_path(cfg), 'w', encoding='utf-8') as f:
            json.dump(_cache_http, f)
    except Exception:
        pass

# ---------------------------------------------------------------- modelo
BROKEN = 'broken'        # existe la referencia pero no carga
MISSING = 'missing_file' # ruta local que no existe en disco
EMPTY = 'empty'          # referencia vacia o placeholder
CORRUPT = 'corrupt'      # archivo presente pero ilegible
OK = 'ok'

REF_HTTP = 'http_url'
REF_LOCAL = 'local_path'
REF_DATA = 'data_uri'
REF_EMPTY = 'empty'


@dataclass
class ImageRef:
    source_file: str          # archivo donde se encontro
    field_name: str           # campo JSON o selector HTML
    raw_value: str            # valor original tal cual
    ref_type: str = REF_EMPTY
    status: str = OK
    resolved: str = ''        # ruta absoluta local o URL normalizada
    error: str = ''
    # contexto (flujo 2)
    model_name: str = ''
    serie: str = ''
    alt: str = ''
    title: str = ''
    surrounding: str = ''
    # metadata exacta del vehiculo (marca/modelo/anio/version/color)
    marca: str = ''
    modelo: str = ''
    anio: int = 0
    version: str = ''
    color: str = ''
    toy_number: str = ''
    casting_code: str = ''
    http_status: int = 0
    content_type: str = ''
    size: int = 0
    width: int = 0
    height: int = 0
    sha1: str = ''
    candidates: list = field(default_factory=list)
    repaired_with: str = ''
    repaired: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------- deteccion
IMG_TAG_RE = re.compile(r'<img\b[^>]*>', re.I | re.S)
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


def _classify(value: str, cfg: Config) -> tuple[str, str]:
    """Devuelve (ref_type, resolved).

    Las rutas locales se resuelven contra `cfg.local_roots` en orden: el sitio
    las arma como 'img/'+nombre, asi que esa raiz va primero. Si ninguna existe
    en disco, se devuelve la primera para que el estado quede como missing_file.
    """
    v = (value or '').strip()
    if not v:
        return REF_EMPTY, ''
    if v.startswith('data:'):
        return REF_DATA, v[:60]
    if v.startswith('//'):
        return REF_HTTP, 'https:' + v
    if v.startswith('http://') or v.startswith('https://'):
        return REF_HTTP, v
    v = unquote(v.split('?')[0].split('#')[0])
    v = v.replace('\\', '/')
    if v.startswith('/'):
        v = v.lstrip('/')
    for root in cfg.local_roots:
        cand = os.path.join(cfg.base, root, v) if root else os.path.join(cfg.base, v)
        if os.path.isfile(cand):
            return REF_LOCAL, cand
    return REF_LOCAL, os.path.join(cfg.base, cfg.local_roots[0], v)


def _sha1_file(path: str) -> str:
    try:
        h = hashlib.sha1()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ''


def _probe_local(path: str, cfg: Config) -> tuple[str, dict]:
    """Valida un archivo local. Devuelve (status, info)."""
    info = {}
    if not os.path.exists(path):
        return MISSING, info
    if not os.path.isfile(path):
        return CORRUPT, info
    try:
        size = os.path.getsize(path)
    except OSError:
        return CORRUPT, info
    info['size'] = size
    ext = os.path.splitext(path)[1].lower()
    if ext and ext not in cfg.allowed_exts:
        info['error'] = f'extension no permitida: {ext}'
        return CORRUPT, info
    if size < 12:
        info['error'] = 'archivo demasiado chico (vacio/corrupto)'
        return CORRUPT, info
    # integridad real decodificando con PIL
    try:
        from PIL import Image
        with Image.open(path) as im:
            w, h = im.size
            im.verify()
        info['width'], info['height'] = int(w), int(h)
    except ImportError:
        pass
    except Exception as e:
        info['error'] = f'no decodifica: {str(e)[:80]}'
        return CORRUPT, info
    if size < cfg.min_bytes:
        info['error'] = f'{size} bytes < minimo {cfg.min_bytes}'
        return CORRUPT, info
    info['sha1'] = _sha1_file(path)
    return OK, info


def _probe_http(url: str, cfg: Config) -> tuple[str, dict]:
    """Valida una URL con HEAD (fallback GET). Devuelve (status, info).

    Lee la cache de sondas ANTES de tocar la red: el escaneo completo dispara
    ~50k HEADs a weserv/Fandom y cada uno tarda en resolver. Re-runs deben ser
    instantaneos (la cache persiste en disco). La cache es la regla del flujo
    image-asset-recovery, no la excepcion.
    """
    import urllib.request, urllib.error
    info = {}
    if not _cache_cargada:
        cargar_cache(cfg)
    clave = url.split('&v=')[0]
    cached = _cache_http.get(clave)
    if cached:
        info.update(cached.get('info', {}))
        return cached.get('status', BROKEN), info
    last = ''
    for intento in range(cfg.retries):
        try:
            req = urllib.request.Request(url, method='HEAD')
            for k, v in headers_imagen(cfg).items():
                req.add_header(k, v)
            with urllib.request.urlopen(req, timeout=cfg.timeout) as r:
                info['http_status'] = r.status
                info['content_type'] = (r.headers.get('Content-Type') or '').split(';')[0].strip()
                info['size'] = int(r.headers.get('Content-Length') or 0)
                st = OK if r.status < 400 else BROKEN
                _memorizar(url, cfg, st, info)
                return st, info
        except urllib.error.HTTPError as e:
            info['http_status'] = e.code
            if e.code in (403, 405, 501):     # algunos CDNs no soportan HEAD
                return _probe_http_get(url, cfg, info)
            return BROKEN, info
        except Exception as e:
            last = str(e)[:90]
        import time
        time.sleep(1.0 * (intento + 1))
    info['error'] = last or 'sin respuesta'
    _memorizar(url, cfg, BROKEN, info)
    return BROKEN, info


def _memorizar(url: str, cfg: Config, status: str, info: dict) -> None:
    if not cfg.cache_dir:
        return
    clave = url.split('&v=')[0]
    _cache_http[clave] = {'status': status, 'info': info}


def _probe_http_get(url: str, cfg: Config, info: dict) -> tuple[str, dict]:
    import urllib.request
    try:
        req = urllib.request.Request(url, method='GET')
        for k, v in headers_imagen(cfg).items():
            req.add_header(k, v)
        req.add_header('Range', 'bytes=0-2047')
        with urllib.request.urlopen(req, timeout=cfg.timeout) as r:
            data = r.read(2048)
            info['http_status'] = r.status
            info['content_type'] = (r.headers.get('Content-Type') or '').split(';')[0].strip()
            if info['size'] == 0:
                info['size'] = len(data)
            if len(data) >= 12:
                info['width'], info['height'] = _dims_from_bytes(data)
            return OK if r.status < 400 else BROKEN, info
    except Exception as e:
        info['error'] = str(e)[:90]
        return BROKEN, info


def _dims_from_bytes(data: bytes) -> tuple[int, int]:
    """Dimensiones desde la cabecera (JPEG/PNG/GIF/WebP) sin librerias."""
    try:
        if data[:8] == b'\x89PNG\r\n\x1a\n':
            import struct
            return struct.unpack('>II', data[16:24])
        if data[:8] == b'GIF87a' or data[:8] == b'GIF89a':
            import struct
            return struct.unpack('<HH', data[6:10])
        if data[:2] == b'\xff\xd8':
            import struct
            i = 2
            while i < len(data) - 9:
                if data[i] != 0xFF:
                    i += 1
                    continue
                m = data[i + 1]
                if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    h, w = struct.unpack('>HH', data[i + 5:i + 9])
                    return w, h
                if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
                    i += 2
                    continue
                seg = struct.unpack('>H', data[i + 2:i + 4])[0]
                i += 2 + seg
        if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
            if data[12:16] == b'VP8X':
                import struct
                w = 1 + int.from_bytes(data[24:27], 'little')
                h = 1 + int.from_bytes(data[27:30], 'little')
                return w, h
            if data[12:16] == b'VP8 ':
                import struct
                w, h = struct.unpack('<HH', data[26:30])
                return w & 0x3FFF, h & 0x3FFF
    except Exception:
        pass
    return 0, 0


def _ext_de_magic(datos: bytes) -> str | None:
    """Extension de imagen deducida de magic-bytes (no confiar en '.part' ni url)."""
    if not datos:
        return None
    if datos[:8] == bytes.fromhex('89504e470d0a1a0a'):
        return '.png'
    if datos[:3] == bytes.fromhex('ffd8ff'):
        return '.jpg'
    if datos[:6] in (b'GIF87a', b'GIF89a'):
        return '.gif'
    if datos[:4] == b'RIFF' and datos[8:12] == b'WEBP':
        return '.webp'
    if datos[:4] == b'RIFF' and datos[8:12] == b'AVIF':
        return '.avif'
    return None


# ---------------------------------------------------------------- escaneo
def scan_catalog_json(path: str, cfg: Config) -> Iterator[ImageRef]:
    """Recorre un JSON de catalogo (lista de modelos con 'im' y 'galeria')."""
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        yield ImageRef(source_file=path, field_name='$', raw_value='',
                       status=CORRUPT, error=f'JSON ilegible: {str(e)[:80]}')
        return

    items = data if isinstance(data, list) else [data]
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        nombre = str(item.get('m') or item.get('modelo') or item.get('nombre') or '')
        serie = str(item.get('s') or item.get('serie') or '')
        ctx = f"{nombre} {serie}".strip()

        for field in ('im', 'imagen', 'image', 'foto'):
            if field in item and item[field]:
                yield _make_ref(path, f'{field}[{idx}]', item[field], ctx, nombre, serie, cfg)

        gal = item.get('galeria') or item.get('images') or []
        if isinstance(gal, list):
            for j, u in enumerate(gal):
                if u:
                    yield _make_ref(path, f'galeria[{j}]', u, ctx, nombre, serie, cfg)


def _make_ref(path: str, field: str, value: str, ctx: str, nombre: str,
              serie: str, cfg: Config) -> ImageRef:
    """Clasifica una referencia SIN sondearla (el sondeo va en _probar_batch).

    Separar ambas cosas es lo que permite procesar 12k referencias en paralelo
    en vez de una por una.
    """
    ref = ImageRef(source_file=path, field_name=field, raw_value=value,
                   model_name=nombre, serie=serie, surrounding=ctx)
    ref.ref_type, ref.resolved = _classify(value, cfg)
    return ref


def scan_html(path: str, cfg: Config) -> Iterator[ImageRef]:
    """Extrae <img> de un HTML junto con su contexto (alt, title, parrafo)."""
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            html = f.read()
    except Exception as e:
        yield ImageRef(source_file=path, field_name='<img>', raw_value='',
                       status=CORRUPT, error=f'no se pudo leer: {str(e)[:80]}')
        return

    for m in IMG_TAG_RE.finditer(html):
        tag = m.group(0)
        attrs = {k.lower(): v for k, v in ATTR_RE.findall(tag)}
        src = attrs.get('src') or attrs.get('data-src') or ''
        if not src:
            continue
        # contexto: 220 caracteres alrededor
        ini = max(0, m.start() - 220)
        alrededor = re.sub(r'\s+', ' ', html[ini:m.end() + 220]).strip()
        alrededor = re.sub(r'<[^>]+>', ' ', alrededor)
        ref = _make_ref(path, '<img>.src', src, alrededor, '', '', cfg)
        ref.alt = attrs.get('alt', '')
        ref.title = attrs.get('title', '')
        yield ref


def scan_directory(dir_path: str, cfg: Config) -> Iterator[ImageRef]:
    """Audita los archivos de imagen del directorio local."""
    if not os.path.isdir(dir_path):
        return
    for root, _dirs, files in os.walk(dir_path):
        for fn in files:
            ruta = os.path.join(root, fn)
            rel = os.path.relpath(ruta, cfg.base).replace('\\', '/')
            ref = ImageRef(source_file='(directorio)', field_name='archivo', raw_value=rel)
            ref.ref_type, ref.resolved = REF_LOCAL, ruta
            st, info = _probe_local(ruta, cfg)
            ref.status = st
            ref.size = info.get('size', 0)
            ref.width = info.get('width', 0)
            ref.height = info.get('height', 0)
            ref.sha1 = info.get('sha1', '')
            ref.error = info.get('error', '')
            yield ref


def _probar_batch(refs: list[ImageRef], cfg: Config) -> list[ImageRef]:
    """Sondea en paralelo las referencias HTTP (la parte lenta del escaneo)."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def sondear(ref: ImageRef) -> None:
        try:
            if ref.ref_type == REF_LOCAL:
                st, info = _probe_local(ref.resolved, cfg)
            elif ref.ref_type == REF_HTTP:
                st, info = _probe_http(ref.resolved, cfg)
            else:
                return
            ref.status = st
            ref.http_status = info.get('http_status', ref.http_status)
            ref.content_type = info.get('content_type', ref.content_type)
            ref.size = info.get('size', ref.size)
            ref.width = info.get('width', ref.width)
            ref.height = info.get('height', ref.height)
            ref.sha1 = info.get('sha1', ref.sha1)
            ref.error = info.get('error', ref.error)
            if (ref.content_type and ref.content_type not in cfg.allowed_mime
                    and st == OK):
                ref.status = BROKEN
                ref.error = f'MIME no es imagen: {ref.content_type}'
        except Exception as e:
            ref.status = BROKEN
            ref.error = f'excepcion al sondear: {str(e)[:70]}'

    # las locales son instantaneas: solo paralelizar las remotas.
    # Los probes HTTP van a CDN (weserv / Fandom static), NO al API -> concurrencia
    # alta (24) es segura y no consume el rate-limit de Fandom. La fase de busqueda
    # (Fandom api.php, 200 req/5min) mantiene cfg.concurrency (8) aislada aqui.
    remotas = [r for r in refs if r.ref_type == REF_HTTP]
    for r in refs:
        if r.ref_type == REF_LOCAL:
            sondear(r)
    with ThreadPoolExecutor(max_workers=max(cfg.concurrency, 24)) as ex:
        futs = [ex.submit(sondear, r) for r in remotas]
        for f in futs:
            try:
                f.result()
            except Exception:
                pass
    return refs


def scan_all(cfg: Config = DEFAULT, limite: int | None = None,
             solo_http: bool = False) -> list[ImageRef]:
    """Punto de entrada del flujo 1: junta todas las fuentes.

    limite: corta el escaneo (util para pruebas rapidas).
    solo_http: omite el recorrido del directorio img/.
    """
    refs: list[ImageRef] = []
    # 1. catalogo principal
    cat = os.path.join(cfg.data, 'catalog_web.json')
    if os.path.exists(cat):
        refs.extend(scan_catalog_json(cat, cfg))
    if limite and len(refs) > limite:
        refs = refs[:limite]
    # 2. HTML del sitio
    if not limite:
        for name in ('index.html', 'galeria_catalogo.html', 'galeria_coleccion.html'):
            p = os.path.join(cfg.base, name)
            if os.path.exists(p):
                refs.extend(scan_html(p, cfg))
    # 3. sondear (locales + remotas en paralelo)
    refs = _probar_batch(refs, cfg)
    # 4. directorio local
    if not solo_http:
        refs.extend(scan_directory(cfg.img_dir, cfg))
    return refs


def resumen(refs: list[ImageRef]) -> dict:
    from collections import Counter
    c = Counter(r.status for r in refs)
    return {
        'total': len(refs),
        'ok': c.get(OK, 0),
        'broken': c.get(BROKEN, 0),
        'missing_file': c.get(MISSING, 0),
        'empty': c.get(EMPTY, 0),
        'corrupt': c.get(CORRUPT, 0),
    }
