#!/usr/bin/env python3
"""image-doctor — Auditor, buscador y reparador autonomo de imagenes.

Stack: Python 3.11+ (PIL para validacion, urllib para red, CLIP local opcional
para validacion visual). Integra con el pipeline existente del sitio
(data/catalog_web.json -> data/cat.js -> img/).

Cuatro flujos:
  1. Auditoria    -> scan.py    : encuentra y valida cada referencia
  2. Contexto     -> context.py : alt/titulo/nombre/parrafo -> query semantica
  3. Validacion   -> validate.py: HTTP + formato + tamano + (opcional) IA visual
  4. Correccion   -> repair.py  : reemplaza y descarga, con log de auditoria
"""
__version__ = '1.0.0'
