#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trend Scheduler — ejecuta trend_watcher.py periódicamente para mantener
las tendencias activas sin intervención manual.

Uso:
  python build/trend_scheduler.py              # una sola vez
  python build/trend_scheduler.py --loop       # cada 6 horas (para cron/systemd)
  python build/trend_scheduler.py --interval 3600  # intervalo personalizado (segundos)

Integración con cron (Linux/Mac):
  0 */6 * * * cd /ruta/hotwheels_collector && python build/trend_scheduler.py >> logs/trends.log 2>&1

Integración con Task Scheduler (Windows):
  Programar tarea: python build/trend_scheduler.py --loop
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCHER = os.path.join(ROOT, "build", "trend_watcher.py")


def run_once():
    """Ejecuta trend_watcher.py una vez."""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ejecutando trend_watcher...")
    try:
        resultado = subprocess.run(
            [sys.executable, WATCHER, "--sync"],
            cwd=ROOT,
            timeout=600,
            capture_output=True,
            text=True
        )
        if resultado.returncode == 0:
            print("  ✓ Tendencias actualizadas")
        else:
            print(f"  ✗ Error: {resultado.stderr[-200:] if resultado.stderr else 'desconocido'}")
        return resultado.returncode == 0
    except subprocess.TimeoutExpired:
        print("  ✗ Timeout (10 min)")
        return False
    except Exception as e:
        print(f"  ✗ Excepción: {e}")
        return False


def main():
    args = sys.argv[1:]
    loop = "--loop" in args
    interval = 21600  # 6 horas por defecto
    for i, a in enumerate(args):
        if a == "--interval" and i + 1 < len(args):
            try:
                interval = int(args[i + 1])
            except ValueError:
                pass

    print("\n" + "=" * 55)
    print("  TREND SCHEDULER — análisis de tendencias activas")
    print("=" * 55)
    print(f"  Modo: {'loop cada ' + str(interval) + 's' if loop else 'una sola vez'}")
    print(f"  Watcher: {WATCHER}")
    print("=" * 55)

    if loop:
        while True:
            run_once()
            print(f"\n  Próxima ejecución en {interval}s...")
            time.sleep(interval)
    else:
        ok = run_once()
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
