#!/usr/bin/env python3
"""Metadatos exactos de cada vehiculo para la busqueda de imagenes.

Del nombre del modelo ('m') y las categorias de Fandom ('categorias_fandom')
se extraen por separado: marca, modelo, anio, version/color y serie. Usar el
nombre completo como query de busqueda es debil; usar 'Lamborghini Centenario
Roadster 2016 2nd color' encuentra la foto correcta.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field

# Anios con dos digitos: '68 -> 1968, '16 -> 2016, '05 -> 2005
ANIO_RE = re.compile(r"^'(\d{2})\s+(.*)$")
ANIO_LARGO_RE = re.compile(r"^((?:19|20)\d{2})\s+(.*)$")
VERSION_RE = re.compile(r"\(([^)]*(?:color|color|edition|variant|version|"
                        r"paint|spectraflame|zamac|matte|pearl)[^)]*)\)", re.I)
NUMERO_RE = re.compile(r"\((?:(\d)(?:st|nd|rd|th)\s+Color)\)", re.I)
MFR_RE = re.compile(r'^Mfr:(.+)$')
PREFIJO_ANIO_RE = re.compile(r"^(?:'(\\d{2})|(?:19|20)\\d{2})\\s+")

MARCAS_CONOCIDAS = {
    'Acura', 'Alfa Romeo', 'AM General', 'AMC', 'Aston Martin', 'Audi',
    'Austin', 'Bentley', 'BMW', 'Bricklin', 'Buick', 'Cadillac', 'Chevrolet',
    'Chrysler', 'Citroen', 'Citroën', 'Daewoo', 'Datsun', 'De Tomaso', 'Dodge',
    'Eagle', 'Edsel', 'Ferrari', 'Fiat', 'Ford', 'Freightliner', 'Geo',
    'GMC', 'Hino', 'Holden', 'Honda', 'Hummer', 'Hyundai', 'Infiniti',
    'International', 'Isuzu', 'Jaguar', 'Jeep', 'Jensen', 'Kia', 'Lamborghini',
    'Lancia', 'Land Rover', 'Lexus', 'Lincoln', 'Lotus', 'Maserati', 'Mazda',
    'McLaren', 'Mercedes-Benz', 'Mercury', 'MG', 'Mini', 'Mitsubishi',
    'Morgan', 'Morris', 'Nissan', 'Oldsmobile', 'Opel', 'Packard', 'Peugeot',
    'Plymouth', 'Pontiac', 'Porsche', 'Ram', 'Renault', 'Rolls-Royce', 'Saab',
    'Saturn', 'Scion', 'Shelby', 'Smart', 'Subaru', 'Suzuki', 'Toyota',
    'Triumph', 'Vauxhall', 'Volkswagen', 'Volvo', 'Willys', 'Batmobile',
    'K.I.T.T.', 'KITT', 'Back to the Future', 'Batman', 'Joker', 'Penguin',
    'Gordon Murray Automotive', 'Radford', 'Tesla', 'Rivian', 'Lucid',
    'Bugatti', 'Koenigsegg', 'Pagani', 'Saleen', 'Vector', 'Vector Aeromotive',
}


@dataclass
class MetadataVehiculo:
    id: str = ''
    nombre_original: str = ''
    marca: str = ''
    modelo: str = ''
    anio: int = 0
    version: str = ''
    color: str = ''
    serie: str = ''
    categoria: str = ''
    numero: str = ''
    toy_number: str = ''
    casting_code: str = ''
    pais: str = ''
    disenador: str = ''
    fuentes: dict = field(default_factory=dict)

    def query_principal(self) -> str:
        """Query mas fiel: marca + modelo + anio (+ version si existe)."""
        partes = [p for p in (self.marca, self.modelo) if p]
        if self.anio:
            partes.append(str(self.anio))
        if self.version and self.version.lower() not in ' '.join(partes).lower():
            partes.append(self.version)
        q = ' '.join(partes)
        return q or self.nombre_original

    def query_alternativas(self) -> list[str]:
        out = []
        base = f"{self.marca} {self.modelo}".strip()
        if base:
            out.append(f'{base} Hot Wheels')
            if self.anio:
                out.append(f'{base} {self.anio} Hot Wheels diecast')
            if self.version:
                out.append(f'{base} {self.anio} {self.version} Hot Wheels')
        if self.serie:
            out.append(f'{base} {self.serie} Hot Wheels'.strip())
        if self.toy_number:
            out.append(f'Hot Wheels {self.toy_number} {self.marca} {self.modelo}'.strip())
        return [q for q in out if len(q) > 6][:5]

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def _anio_de(texto: str, y_campo) -> tuple[int, str]:
    """Saca el anio del nombre y devuelve (anio, resto)."""
    if y_campo:
        try:
            return int(y_campo), texto
        except Exception:
            pass
    m = ANIO_RE.match(texto or '')
    if m:
        dd = int(m.group(1))
        return (1900 + dd if dd >= 30 else 2000 + dd), m.group(2)
    m = ANIO_LARGO_RE.match(texto or '')
    if m:
        return int(m.group(1)), m.group(2)
    return 0, texto


def _quitar_marca(nombre: str, marca: str) -> str:
    """Saca la marca del principio del nombre (viene de Mfr: y sigue ahi)."""
    if not marca:
        return nombre
    if nombre.lower().startswith(marca.lower()):
        return nombre[len(marca):].strip(" ,\'-")
    return nombre


def _marca_de(resto: str, categorias: list) -> tuple[str, str]:
    """Detecta la marca (Mfr: de Fandom o el nombre) y la quita del modelo."""
    marca = ''
    for c in categorias or []:
        m = MFR_RE.match(str(c))
        if m:
            marca = m.group(1).strip()
            break
    if marca:
        return marca, _quitar_marca(resto, marca)
    for m in sorted(MARCAS_CONOCIDAS, key=len, reverse=True):
        if resto.lower().startswith(m.lower() + ' '):
            return m, resto[len(m):].strip()
    for alias, real in (('Chevy', 'Chevrolet'), ('VW', 'Volkswagen'),
                        ('Mercedes', 'Mercedes-Benz'), ('Lambo', 'Lamborghini')):
        if resto.lower().startswith(alias.lower() + ' '):
            return real, resto[len(alias):].strip()
    return '', resto


def _version_de(nombre: str) -> tuple[str, str]:
    """Extrae '(2nd Color)' / '(ZAMAC)' y lo saca del nombre base."""
    version = ''
    m = VERSION_RE.search(nombre or '')
    if m:
        version = m.group(1).strip()
    m2 = NUMERO_RE.search(nombre or '')
    if m2 and not version:
        version = f"{m2.group(1)} color"
    if not version:
        return '', nombre
    limpio = nombre.replace(m.group(0) if m else m2.group(0) if m2 else '', '')
    limpio = re.sub(r'\s{2,}', ' ', limpio).strip(' ,')
    return version, limpio


def metadata_de(registro: dict) -> MetadataVehiculo:
    """Construye los metadatos exactos de un registro del catalogo.

    Orden importa: primero se saca la version (entre parentesis), despues el
    anio del nombre, y recien entonces la marca — si se detecta la marca por
    'Mfr:' el nombre sigue trayendo el prefijo de anio, que hay que limpiar.
    """
    nombre = str(registro.get('m') or '')
    cats = registro.get('categorias_fandom') or []
    if isinstance(cats, str):
        cats = [cats]

    # 1) version/color entre parentesis
    version, limpio = _version_de(nombre)

    # 2) anio: el del nombre manda (es el anio del casting, no el de la edicion)
    anio, limpio = _anio_de(limpio, None)
    if not anio:
        anio, limpio = _anio_de(limpio, registro.get('y'))
    # si el anio vino del campo 'y', el nombre puede seguir trayendo el prefijo
    limpio = PREFIJO_ANIO_RE.sub('', limpio).strip()

    # 3) marca: primero Mfr: de Fandom, si no el nombre
    marca, modelo = _marca_de(limpio, cats)
    modelo = modelo.strip(' ,\'-')

    # 4) color explicito
    color = ''
    mc = re.search(r'\b(Red|Blue|Green|Yellow|Orange|Purple|Black|White|Silver|'
                   r'Gold|Bronze|Copper|Pink|Teal|Grey|Gray|Tan|Lime|Magenta|'
                   r'Burgundy|Maroon|Navy|Cream|Pearl|Spectraflame|ZAMAC)\b',
                   nombre or '', re.I)
    if mc and not re.search(r'\(.*color.*\)', nombre, re.I):
        color = mc.group(1)

    disenador = (registro.get('disenador') or registro.get('diseñador') or '')

    return MetadataVehiculo(
        id=str(registro.get('i') or ''),
        nombre_original=nombre,
        marca=marca,
        modelo=modelo,
        anio=anio,
        version=version,
        color=color,
        serie=str(registro.get('s') or ''),
        categoria=str(registro.get('k') or ''),
        numero=str(registro.get('n') or ''),
        toy_number=str(registro.get('t') or ''),
        casting_code=str(registro.get('c') or ''),
        pais=str(registro.get('pais') or ''),
        disenador=str(disenador),
    )


def metadata_todos(catalogo: list[dict]) -> dict[str, MetadataVehiculo]:
    """Metadata indexada por id de modelo."""
    out = {}
    for r in catalogo:
        md = metadata_de(r)
        if md.id:
            out[md.id] = md
    return out


def resolver_metadata(registros: list[dict], ref) -> MetadataVehiculo:
    """Busca la metadata que corresponde a una referencia del scanner."""
    try:
        idx = int(str(ref.field_name).split('[')[1].rstrip(']'))
    except Exception:
        return MetadataVehiculo(nombre_original=ref.model_name or ref.raw_value)
    if 0 <= idx < len(registros):
        return metadata_de(registros[idx])
    return MetadataVehiculo(nombre_original=ref.model_name or ref.raw_value)
