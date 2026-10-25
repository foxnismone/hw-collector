#!/usr/bin/env python3
"""image-doctor — CLI

Audita, busca y repara imagenes faltantes o rotas del sitio Hot Wheels Collector.

Uso:
  python -m imadoctor --scan                 solo auditar (no toca nada)
  python -m imadoctor --dry-run              simula la reparacion
  python -m imadoctor                        audita y repara
  python -m imadoctor --max 50               limita la cantidad de reparaciones
  python -m imadoctor --solo-local           solo audita el directorio img/
  python -m imadoctor --sin-visual           desactiva la validacion por CLIP
  python -m imadoctor --listar-rotas         muestra las rotas y termina
"""
from __future__ import annotations
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from imadoctor.config import DEFAULT, Config
from imadoctor.scanner import (scan_all, resumen, scan_directory, scan_catalog_json,
                               scan_html, BROKEN, MISSING, CORRUPT, EMPTY, OK)
from imadoctor.context import planificar, es_placeholder
from imadoctor.visual import disponible as clip_disponible
from imadoctor import dom as dom_mod


def _pinta_audit(refs, titulo):
    print(f'\n=== {titulo} ===')
    r = resumen(refs)
    print(f"  {r['total']} referencias | {r['ok']} ok | {r['broken']} rotas | "
          f"{r['missing_file']} sin archivo | {r['empty']} vacias | {r['corrupt']} corruptas")
    return r


def cmd_scan(cfg: Config, args) -> int:
    refs = []
    if args.solo_local:
        refs = list(scan_directory(cfg.img_dir, cfg))
    else:
        refs = scan_all(cfg, limite=args.limite, solo_http=args.solo_http)
    r = _pinta_audit(refs, 'AUDITORIA')

    rotas = [x for x in refs if x.status != OK]
    if args.listar_rotas:
        print(f'\n=== {len(rotas)} REFERENCIAS CON PROBLEMAS ===')
        for x in rotas[: args.listar_rotas]:
            tag = 'PLACEHOLDER' if es_placeholder(x) else x.status.upper()
            print(f"  [{tag}] {x.model_name or '(sin modelo)'}")
            print(f"        campo: {x.field_name}")
            print(f"        valor: {(x.raw_value or '(vacio)')[:100]}")
            if x.error:
                print(f"        error: {x.error[:100]}")
            plan = planificar(x)
            if plan.queries:
                print(f"        query: {plan.queries[0][:80]}")
            print()
        if len(rotas) > args.listar_rotas:
            print(f'  ... y {len(rotas) - args.listar_rotas} mas')
        return 0

    # mostrar algunas pistas de contexto
    print('\n=== CONTEXTO Y QUERIES (muestra) ===')
    for x in rotas[:8]:
        plan = planificar(x)
        print(f"  modelo={x.model_name[:34]!r:38} serie={x.series[:18]!r:20} "
              f"alt={x.alt[:14]!r}")
        print(f"      archivo -> {plan.filename_hint[:50]!r}")
        print(f"      queries -> {plan.queries[:2]}")
    if len(rotas) > 8:
        print(f'  ... y {len(rotas) - 8} mas')
    return 0


def cmd_dom(cfg: Config, args) -> int:
    """Audita el DOM renderizado: contenedores vacios, imgs rotas, layout."""
    url = args.dom or 'https://foxnismone.github.io/hw-collector/'
    print(f'\n=== AUDITORIA DOM: {url} ===')
    hallazgos = dom_mod.auditar_dom(url, cfg)
    res = dom_mod.resumen_hallazgos(hallazgos)
    print(f"  {res['total']} hallazgos | {res['por_tipo']}")
    for h in hallazgos:
        icono = {'alta': '\u2717', 'media': '\u26a0', 'baja': '\u2139'}.get(h.severidad, '-')
        print(f"\n  {icono} [{h.tipo}] ({h.severidad})")
        print(f"      selector : {h.selector}")
        print(f"      detalle  : {h.detalle[:110]}")
        if h.modelo:
            print(f"      modelo   : {h.modelo[:110]}")
        print(f"      accion   : {h.accion_sugerida}")
    print(f"\n  Severidad alta: {res['alta']}")
    return 0


def cmd_run(cfg: Config, args) -> int:
    from imadoctor.pipeline import run
    t0 = time.time()
    print('=== image-doctor: auditoria + busqueda + reparacion ===')
    print(f"    dry_run={cfg.dry_run} | visual_CLIP={'si' if clip_disponible() else 'no'}")
    print()
    out = run(cfg, max_reparar=args.max)
    print()
    if 'error' in out:
        print(f"FALLO: {out['error']}")
        return 1
    res = out['resumen']
    print('=== RESULTADO ===')
    a = res['auditoria']
    rp = res['reparacion']
    print(f"  Escaneadas : {a['total_referencias']}")
    print(f"  Rotas      : {a['rotas']} | sin archivo: {a['missing_file']} | corruptas: {a['corruptas']}")
    print(f"  Reparadas  : {out['reparadas']} (local: {rp['descargadas_local']}, url: {rp['url_actualizadas']})")
    print(f"  Omitidas   : {out['omitidas']}")
    print(f"  Descartadas: {rp['descartes_validacion']}")
    print(f"  Duracion   : {res['duracion_seg']}s")
    print(f"  Log JSON   : {out['log_json']}")
    print(f"  Informe MD : {out['log_md']}")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog='imadoctor', description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--scan', action='store_true', help='solo auditar, no reparar')
    p.add_argument('--dry-run', action='store_true', help='simular sin escribir')
    p.add_argument('--max', type=int, default=None, help='limitar reparaciones')
    p.add_argument('--solo-local', action='store_true', help='auditar solo el directorio img/')
    p.add_argument('--sin-visual', action='store_true', help='desactivar CLIP')
    p.add_argument('--listar-rotas', type=int, nargs='?', const=25, default=0,
                   help='listar referencias con problemas (N=25)')
    p.add_argument('--limite', type=int, default=None,
                   help='limitar el escaneo a N referencias (pruebas rapidas)')
    p.add_argument('--solo-http', action='store_true', help='omitir el directorio img/')
    p.add_argument('--dom', nargs='?', const='https://foxnismone.github.io/hw-collector/',
                   default=None, help='auditar el DOM renderizado (bloques vacios, imgs rotas)')
    p.add_argument('--quiet', action='store_true', help='menos salida')
    args = p.parse_args(argv)

    cfg = Config()
    if args.dry_run:
        cfg.dry_run = True
    if args.quiet:
        cfg.verbose = False
    cfg.ensure_dirs()

    if args.dom:
        return cmd_dom(cfg, args)
    if args.scan:
        return cmd_scan(cfg, args)
    return cmd_run(cfg, args)


if __name__ == '__main__':
    raise SystemExit(main())
