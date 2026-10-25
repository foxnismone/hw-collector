#!/usr/bin/env python3
"""Registro de auditoria.

Genera dos salidas:
  - logs/imadoctor-<timestamp>.json  : maquina-legible, con cada decision
  - logs/imadoctor-<timestamp>.md    : informe humano para revisar a mano

Incluye: acciones realizadas, imagenes reemplazadas, errores encontrados,
descartes y su motivo, y metricas finales.
"""
from __future__ import annotations
import json, os, time
from dataclasses import dataclass, field, asdict
from typing import Any

from .config import Config, DEFAULT
from .scanner import ImageRef, OK
from .repair import Reparacion


@dataclass
class EntradaLog:
    ts: str
    fase: str
    nivel: str            # 'info' | 'aviso' | 'error' | 'reparado' | 'descartado'
    mensaje: str
    datos: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


class AuditorLog:
    def __init__(self, cfg: Config = DEFAULT):
        self.cfg = cfg
        cfg.ensure_dirs()
        self.stamp = time.strftime('%Y%m%d-%H%M%S')
        self.entradas: list[EntradaLog] = []
        self.descartes: list[dict] = []

    def _ahora(self) -> str:
        return time.strftime('%H:%M:%S')

    def info(self, fase: str, mensaje: str, **datos):
        self.entradas.append(EntradaLog(self._ahora(), fase, 'info', mensaje, datos))
        if self.cfg.verbose:
            print(f'  [{fase}] {mensaje}')

    def aviso(self, fase: str, mensaje: str, **datos):
        self.entradas.append(EntradaLog(self._ahora(), fase, 'aviso', mensaje, datos))
        if self.cfg.verbose:
            print(f'  ⚠ [{fase}] {mensaje}')

    def error(self, fase: str, mensaje: str, **datos):
        self.entradas.append(EntradaLog(self._ahora(), fase, 'error', mensaje, datos))
        if self.cfg.verbose:
            print(f'  ✗ [{fase}] {mensaje}')

    def reparado(self, r: Reparacion):
        self.entradas.append(EntradaLog(
            self._ahora(), 'reparacion', 'reparado',
            f"{r.ref.model_name or r.ref.raw_value[:40]} -> {r.nuevo_valor[:60]}",
            r.to_dict()))

    def descartado(self, url: str, motivo: str, query: str = ''):
        d = {'url': url, 'motivo': motivo, 'query': query}
        self.descartes.append(d)
        self.entradas.append(EntradaLog(self._ahora(), 'validacion', 'descartado',
                                        f'{motivo[:70]}', d))

    # ---------------------------------------------------------------- salidas
    def resumen(self, refs: list[ImageRef], reparaciones: list[Reparacion],
                inicio: float) -> dict:
        from collections import Counter
        c = Counter(r.status for r in refs)
        acc = Counter(r.accion for r in reparaciones)
        return {
            'ejecutado_en': time.strftime('%Y-%m-%d %H:%M:%S'),
            'duracion_seg': round(time.time() - inicio, 1),
            'dry_run': self.cfg.dry_run,
            'auditoria': {
                'total_referencias': len(refs),
                'ok': c.get('ok', 0),
                'rotas': c.get('broken', 0),
                'missing_file': c.get('missing_file', 0),
                'vacias': c.get('empty', 0),
                'corruptas': c.get('corrupt', 0),
            },
            'reparacion': {
                'descargadas_local': acc.get('descargada_local', 0),
                'url_actualizadas': acc.get('url_actualizada', 0),
                'omitidas': acc.get('omitida', 0),
                'descartes_validacion': len(self.descartes),
            },
        }

    def guardar(self, refs: list[ImageRef], reparaciones: list[Reparacion],
                inicio: float) -> tuple[str, str]:
        res = self.resumen(refs, reparaciones, inicio)
        base = os.path.join(self.cfg.log_dir, f'imadoctor-{self.stamp}')

        # --- JSON ---
        json_path = base + '.json'
        payload = {
            'resumen': res,
            'entradas': [e.to_dict() for e in self.entradas],
            'descartes': self.descartes,
            'referencias': [
                {
                    'modelo': r.model_name, 'campo': r.field_name,
                    'valor': r.raw_value, 'estado': r.status,
                    'error': r.error, 'status_http': r.http_status,
                    'dimensiones': f'{r.width}x{r.height}',
                    'reparada': any(x.ref.raw_value == r.raw_value and x.accion != 'omitida'
                                    for x in reparaciones),
                }
                for r in refs if r.status != OK
            ],
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        # --- Markdown ---
        md_path = base + '.md'
        L = []
        L.append('# Auditoria de imagenes — image-doctor\n')
        L.append(f"Ejecutado: {res['ejecutado_en']} · Duracion: {res['duracion_seg']}s"
                 + (' · **DRY RUN**' if self.cfg.dry_run else '') + '\n')
        L.append('## Resumen\n')
        a = res['auditoria']
        L.append(f"- Referencias escaneadas: **{a['total_referencias']}**")
        L.append(f"- OK: **{a['ok']}**")
        L.append(f"- Rotas: **{a['rotas']}**")
        L.append(f"- Archivos faltantes: **{a['missing_file']}**")
        L.append(f"- Referencias vacias: **{a['vacias']}**")
        L.append(f"- Archivos corruptos: **{a['corruptas']}**")
        rp = res['reparacion']
        L.append(f"- Reemplazadas (descargadas): **{rp['descargadas_local']}**")
        L.append(f"- Reemplazadas (URL): **{rp['url_actualizadas']}**")
        L.append(f"- Omitidas sin candidato: **{rp['omitidas']}**")
        L.append(f"- Descartadas en validacion: **{rp['descartes_validacion']}**")
        L.append('')

        if reparaciones:
            L.append('## Reparaciones\n')
            L.append('| Modelo | Campo | Antes | Despues | Motivo |')
            L.append('|---|---|---|---|---|')
            for r in reparaciones:
                if r.accion == 'omitida':
                    continue
                antes = (r.ref.raw_value or '')[:55].replace('|', '/')
                desp = (r.nuevo_valor or '')[:55].replace('|', '/')
                L.append(f"| {r.ref.model_name[:28] or '-'} | {r.ref.field_name} | `{antes}` | `{desp}` | {r.motivo[:45]} |")
            L.append('')

        omitidas = [r for r in reparaciones if r.accion == 'omitida']
        if omitidas:
            L.append('## Omitidas (sin candidato valido)\n')
            for r in omitidas[:60]:
                L.append(f"- **{r.ref.model_name or r.ref.raw_value[:50]}** "
                         f"(`{r.ref.field_name}`): {r.ref.error[:70]}")
            if len(omitidas) > 60:
                L.append(f"- ... y {len(omitidas) - 60} mas")
            L.append('')

        if self.descartes:
            L.append('## Descartadas en validacion\n')
            L.append('| URL | Motivo |')
            L.append('|---|---|')
            for d in self.descartes[:40]:
                L.append(f"| `{d['url'][:80]}` | {d['motivo'][:60]} |")
            L.append('')

        errores = [e for e in self.entradas if e.nivel == 'error']
        if errores:
            L.append('## Errores encontrados\n')
            for e in errores[:40]:
                L.append(f"- [{e.fase}] {e.mensaje}")
            L.append('')

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(L))

        return json_path, md_path
