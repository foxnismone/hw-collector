#!/usr/bin/env python3
"""Orquestador: une los cuatro flujos en una corrida completa.

  1. scan_all()            -> auditoria
  2. planificar()          -> contexto + queries
  3. buscar + validar      -> candidatos filtrados
  4. reparar + registrar   -> correccion con log

Disenado para no caerse: cada fuente, cada candidato y cada escritura van dentro
de su propio manejo de excepciones.
"""
from __future__ import annotations
import os, time
from concurrent.futures import ThreadPoolExecutor, as_completed

from .config import Config, DEFAULT
from .scanner import scan_all, resumen, OK, BROKEN, MISSING, CORRUPT, EMPTY
from .context import planificar, planificar_todos
from .sources import buscar_multiples
from .validate import validar, elegir_mejor, Verdict
from .visual import disponible as clip_disponible, score_visual
from .repair import reparar_catalogo, descargar, _nombre_local
from .metadata_bridge import adjuntar_metadata
from .logger import AuditorLog
from .metadata_bridge import adjuntar_metadata


def _score_fn(consulta: str, datos: bytes, cfg: Config):
    if not clip_disponible():
        return None
    return lambda q, d: score_visual(q, d, cfg)


def run(cfg: Config = DEFAULT, max_reparar: int | None = None,
        limite: int | None = None) -> dict:
    """Corre el pipeline completo. Devuelve el resumen."""
    t0 = time.time()
    log = AuditorLog(cfg)
    cfg.ensure_dirs()

    log.info('inicio', f'image-doctor iniciado (dry_run={cfg.dry_run})')

    # ---------------------------------------------------------- 1. auditoria
    log.info('auditoria', 'escaneando fuentes...')
    try:
        refs = scan_all(cfg, limite=limite)
    except Exception as e:
        log.error('auditoria', f'fallo el escaneo: {str(e)[:120]}')
        return {'error': str(e)[:200]}

    # metadata exacta de cada vehiculo (marca/modelo/anio/version/color)
    try:
        refs = adjuntar_metadata(refs, cfg)
    except Exception as e:
        log.aviso('contexto', f'no se pudo adjuntar metadata: {str(e)[:80]}')

    r = resumen(refs)
    log.info('auditoria',
             f"{r['total']} referencias: {r['ok']} ok, {r['broken']} rotas, "
             f"{r['missing_file']} sin archivo, {r['empty']} vacias, {r['corrupt']} corruptas")

    rotas = [x for x in refs if x.status in (BROKEN, MISSING, CORRUPT, EMPTY)]
    if not rotas:
        log.info('fin', 'no hay imagenes que reparar')
        log.guardar(refs, [], t0)
        return {'resumen': resumen(refs), 'reparadas': 0}

    if max_reparar:
        rotas = rotas[:max_reparar]
        log.info('auditoria', f'limitado a {len(rotas)} imagenes (--max)')

    # ---------------------------------------------------------- 1b. metadata
    # Rellena marca/modelo/anio/version/color en cada referencia rota: es lo que
    # hace que la busqueda encuentre LA foto del vehiculo y no una generica.
    try:
        antes_md = sum(1 for r in rotas if r.marca or r.anio or r.version)
        adjuntar_metadata(rotas, cfg)
        despues_md = sum(1 for r in rotas if r.marca or r.anio or r.version)
        log.info('metadata', f'{despues_md}/{len(rotas)} referencias con metadata exacta '
                             f'(+{despues_md - antes_md} resueltas del catalogo)')
    except Exception as e:
        log.aviso('metadata', f'no se pudo adjuntar metadata: {str(e)[:80]}')

    # ---------------------------------------------------------- 2. contexto
    planes = planificar_todos(rotas)
    sin_plan = [p for p in planes if not p.queries]
    if sin_plan:
        log.aviso('contexto', f'{len(sin_plan)} imagenes sin pistas de busqueda (sin nombre de modelo)')
    log.info('contexto', f'{len(planes) - len(sin_plan)}/{len(planes)} con plan de busqueda')

    # ---------------------------------------------------------- 3. busqueda
    usos_visual = clip_disponible()
    log.info('validacion', f'validacion visual por CLIP: {"activa" if usos_visual else "no disponible"}')

    veredictos: dict[str, Verdict] = {}
    sin_candidato = 0

    def procesar(plan):
        """Busca y valida una sola imagen rota. Nunca lanza."""
        try:
            candidatos = buscar_multiples(plan.queries, cfg)
            if not candidatos:
                return plan, None, 'sin candidatos'
            consulta = plan.queries[0] if plan.queries else plan.ref.model_name
            mejor = elegir_mejor(candidatos, cfg, consulta_visual=consulta,
                                 score_fn=score_visual if usos_visual else None)
            return plan, mejor, None
        except Exception as e:
            return plan, None, f'excepcion: {str(e)[:80]}'

    with ThreadPoolExecutor(max_workers=cfg.concurrency) as ex:
        futures = [ex.submit(procesar, p) for p in planes if p.queries]
        for fut in as_completed(futures):
            try:
                plan, mejor, err = fut.result()
            except Exception as e:
                log.error('busqueda', f'hilo fallo: {str(e)[:80]}')
                continue
            ref = plan.ref
            if err:
                sin_candidato += 1
                continue
            if mejor is None:
                sin_candidato += 1
                log.descartado(plan.queries[0] if plan.queries else '', 'ninguno paso la validacion')
                continue
            veredictos[ref.raw_value] = mejor

    log.info('busqueda', f'{len(veredictos)} imagenes con candidato valido; '
                         f'{sin_candidato} sin ninguno')

    # ---------------------------------------------------------- 4. correccion
    # descargar localmente (o dejar la URL) antes de aplicar
    if not cfg.dry_run:
        for raw, v in veredictos.items():
            if v.local_path and os.path.exists(v.local_path):
                continue
            nombre = _nombre_local(v.url.split('/')[-1].split('?')[0] or 'imagen',
                                   os.path.splitext(v.url.split('?')[0])[1] or '.jpg')
            destino = os.path.join(cfg.img_dir, nombre)
            if os.path.exists(destino):
                v.local_path = destino
                continue
            ok, err = descargar(v.url, destino, cfg)
            if ok:
                v.local_path = destino
                v.url = destino.replace(cfg.base, '').replace('\\', '/').lstrip('/')
            else:
                v.valid = False
                v.reason = err

    reparaciones = reparar_catalogo(rotas, veredictos, cfg)
    for rep in reparaciones:
        if rep.accion != 'omitida':
            log.reparado(rep)
    omitidas = sum(1 for x in reparaciones if x.accion == 'omitida')
    if omitidas:
        log.aviso('reparacion', f'{omitidas} imagenes no pudieron repararse')

    # ---------------------------------------------------------- 5. registro
    json_path, md_path = log.guardar(refs, reparaciones, t0)
    log.info('fin', f"duracion {round(time.time() - t0, 1)}s")
    log.info('registro', f'JSON: {json_path}')
    log.info('registro', f'Informe: {md_path}')

    return {
        'resumen': log.resumen(refs, reparaciones, t0),
        'reparadas': sum(1 for x in reparaciones if x.accion != 'omitida'),
        'omitidas': omitidas,
        'log_json': json_path,
        'log_md': md_path,
    }
