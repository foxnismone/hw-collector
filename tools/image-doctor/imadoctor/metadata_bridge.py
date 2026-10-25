#!/usr/bin/env python3
"""Construye la metadata exacta de cada vehiculo y la adjunta a las referencias.

El requisito pide buscar con "marca, modelo, anio, version y color". El nombre
suelto del modelo ('16 Lamborghini Centenario Roadster (2nd Color)') es una query
debil; desarmarlo en campos exactos encuentra la foto correcta.
"""
from __future__ import annotations
import json, os
from typing import Callable

from .config import Config, DEFAULT
from .scanner import ImageRef
from . import metadata as md


def cargar_catalogo(cfg: Config) -> list[dict]:
    """Lee el catalogo crudo (catalog_web.json)."""
    p = os.path.join(cfg.data, 'catalog_web.json')
    try:
        with open(p, encoding='utf-8') as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]
    except Exception:
        return []


def indice_metadata(cfg: Config) -> dict[str, md.MetadataVehiculo]:
    """Metadata indexada por id de modelo."""
    return md.metadata_todos(cargar_catalogo(cfg))


def _idx_de(field_name: str) -> int:
    """Saca el indice de 'im[12]' / 'galeria[3]'."""
    import re
    m = re.search(r'\[(\d+)\]', field_name or '')
    return int(m.group(1)) if m else -1


def adjuntar_metadata(refs: list[ImageRef], cfg: Config = DEFAULT) -> list[ImageRef]:
    """Rellena marca/modelo/anio/version/color en cada referencia rota.

    La referencia trae 'im[12]' -> el registro 12 del catalogo -> su metadata.
    Si el catalogo no esta disponible, se degrada al nombre que ya traia.
    """
    catalogo = cargar_catalogo(cfg)
    if not catalogo:
        for r in refs:
            if not r.marca:
                m = md.metadata_de({'m': r.model_name or r.raw_value})
                r.marca, r.anio, r.version = m.marca, m.anio, m.version
                r.modelo, r.color = m.modelo, m.color
        return refs

    for r in refs:
        i = _idx_de(r.field_name)
        if 0 <= i < len(catalogo):
            m = md.metadata_de(catalogo[i])
        else:
            m = md.metadata_de({'m': r.model_name or r.raw_value})
        # solo rellenar lo que falte: el nombre ya venia del catalogo
        r.marca = r.marca or m.marca
        r.modelo = r.modelo or m.modelo
        r.anio = r.anio or m.anio
        r.version = r.version or m.version
        r.color = r.color or m.color
        r.serie = r.serie or m.serie
        r.toy_number = m.toy_number
        r.casting_code = m.casting_code
    return refs
