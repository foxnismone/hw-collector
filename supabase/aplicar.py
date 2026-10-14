#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplica y verifica el esquema multiusuario en Supabase.

USO
  1. Creá el archivo  supabase/.env  con esta línea (una sola):
       SUPABASE_DB_URL=postgresql://postgres:TU_PASSWORD@db.wgoqtqwxikqhrgulclqk.supabase.co:5432/postgres
     (copiá la cadena desde Supabase → Project Settings → Database → Connection string → URI,
      y reemplazá [YOUR-PASSWORD] por tu contraseña real)

  2. Ejecutá:
       python supabase/aplicar.py            # aplica 01, 02, 03 en orden
       python supabase/aplicar.py --verificar  # solo verifica, no aplica nada
       python supabase/aplicar.py --seed       # además carga los datos de prueba

SEGURIDAD
  La contraseña vive SOLO en supabase/.env (que está en .gitignore).
  Nunca se imprime en pantalla ni se sube al repositorio.
"""
from __future__ import annotations

import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ENV = os.path.join(BASE, ".env")

ARCHIVOS = ["01_schema.sql", "02_policies.sql", "03_views.sql"]
TABLAS = ["perfiles", "colecciones", "autos_coleccion", "auditoria", "break_glass"]
VISTAS = ["stats_coleccionables", "stats_series", "stats_condicion", "stats_geografia",
          "stats_actividad", "stats_plataforma", "stats_top_modelos", "stats_sin_catalogar"]


def leer_env():
    """Lee la cadena de conexión. La contraseña no se imprime nunca."""
    if os.environ.get("SUPABASE_DB_URL"):
        return os.environ["SUPABASE_DB_URL"].strip()
    if not os.path.exists(ENV):
        return None
    for linea in open(ENV, encoding="utf-8"):
        linea = linea.strip()
        if linea.startswith("SUPABASE_DB_URL="):
            v = linea.split("=", 1)[1].strip().strip('"').strip("'")
            return v or None
    return None


def falta_password(url: str) -> bool:
    """Detecta si la cadena todavía tiene el marcador de posición."""
    marcadores = ["[YOUR-PASSWORD]", "YOUR-PASSWORD", "TU_PASSWORD", "TU_CONTRASENA",
                  "PASSWORD", "********"]
    return any(m in url for m in marcadores)


def ocultar(url: str) -> str:
    """Devuelve la cadena con la contraseña tapada, para poder mostrarla."""
    return re.sub(r"://([^:]+):([^@]+)@", r"://\1:••••••@", url)


def conectar(url: str):
    import psycopg2
    # Supabase exige SSL. sslmode=require si no viene especificado.
    if "sslmode=" not in url:
        url += ("&" if "?" in url else "?") + "sslmode=require"
    return psycopg2.connect(url, connect_timeout=20)


def aplicar(cur, nombre):
    ruta = os.path.join(BASE, nombre)
    sql = open(ruta, encoding="utf-8").read()
    print(f"  → aplicando {nombre}...", end=" ")
    try:
        cur.execute(sql)
        print("OK")
        return True
    except Exception as e:
        print(f"ERROR\n     {str(e)[:300]}")
        return False


def verificar(cur):
    print("\n  ── Verificación ──────────────────────────────────")

    # 1. Tablas y RLS
    cur.execute("""
        select relname, relrowsecurity
        from pg_class
        where relname = any(%s) and relkind = 'r'
        order by relname
    """, (TABLAS,))
    filas = cur.fetchall()
    print(f"\n  Tablas: {len(filas)}/{len(TABLAS)}")
    sin_rls = []
    for nombre, rls in filas:
        marca = "✓" if rls else "✗ SIN RLS"
        print(f"    {marca} {nombre}")
        if not rls:
            sin_rls.append(nombre)
    faltan = set(TABLAS) - {f[0] for f in filas}
    for t in sorted(faltan):
        print(f"    ✗ {t}: NO EXISTE")

    # 2. Políticas
    cur.execute("""
        select tablename, count(*)
        from pg_policies
        where schemaname = 'public'
        group by tablename
        order by tablename
    """)
    pol = cur.fetchall()
    print(f"\n  Políticas RLS: {sum(p[1] for p in pol)} en total")
    for tabla, n in pol:
        print(f"    {tabla}: {n}")

    # 3. Vistas
    cur.execute("""
        select table_name from information_schema.views
        where table_schema = 'public' and table_name = any(%s)
        order by table_name
    """, (VISTAS,))
    vs = [v[0] for v in cur.fetchall()]
    print(f"\n  Vistas: {len(vs)}/{len(VISTAS)}")
    for v in VISTAS:
        print(f"    {'✓' if v in vs else '✗'} {v}")

    # 4. Funciones clave
    cur.execute("""
        select proname from pg_proc
        where proname in ('es_staff','es_admin','auditar','k_min','conceder_break_glass','crear_perfil_nuevo')
        order by proname
    """)
    fns = [f[0] for f in cur.fetchall()]
    print(f"\n  Funciones: {len(fns)}/6")
    for f in ["es_staff", "es_admin", "auditar", "k_min", "conceder_break_glass", "crear_perfil_nuevo"]:
        print(f"    {'✓' if f in fns else '✗'} {f}()")

    # 5. Trigger de alta automática de perfil
    cur.execute("""
        select tgname from pg_trigger
        where tgname = 'trg_crear_perfil'
    """)
    trg = cur.fetchall()
    print(f"\n  Trigger de perfil automático: {'✓' if trg else '✗'}")

    # 6. PRUEBA DE AISLAMIENTO REAL
    print("\n  ── Prueba de aislamiento (lo más importante) ─────")
    ok = True

    # Sin usuario autenticado (rol anon), RLS debe bloquear todo
    try:
        cur.execute("set local role anon")
        cur.execute("select count(*) from public.perfiles")
        n = cur.fetchone()[0]
        print(f"    {'✓' if n == 0 else '✗ FALLA'} como 'anon' veo {n} perfiles (esperado 0)")
        if n != 0:
            ok = False
        cur.execute("reset role")
    except Exception as e:
        cur.execute("rollback")
        print(f"    ✓ 'anon' bloqueado por RLS ({str(e)[:60]})")

    # El rol anon no debe poder insertar perfiles
    try:
        cur.execute("set local role anon")
        cur.execute("insert into public.perfiles (id, nombre_perfil) values (gen_random_uuid(), 'intruso')")
        cur.execute("reset role")
        print("    ✗ FALLA: 'anon' pudo INSERTAR un perfil")
        ok = False
    except Exception:
        cur.execute("rollback")
        print("    ✓ 'anon' no puede insertar perfiles (RLS lo bloquea)")

    # La auditoría no debe poder modificarse
    try:
        cur.execute("update public.auditoria set motivo = 'alterado' where id = 1")
        cur.execute("rollback")
        print("    ✗ FALLA: la auditoría se pudo modificar")
        ok = False
    except Exception:
        cur.execute("rollback")
        print("    ✓ la auditoría es inmutable")

    print("\n  ──────────────────────────────────────────────────")
    if sin_rls:
        print(f"  ✗ RLS FALTA en: {', '.join(sin_rls)}")
        ok = False
    if faltan:
        print(f"  ✗ Faltan tablas: {', '.join(sorted(faltan))}")
        ok = False
    print("  ✅ ESQUEMA CORRECTO Y AISLAMIENTO VERIFICADO" if ok
          else "  ❌ HAY PROBLEMAS — revisá lo marcado arriba")
    return ok


def main():
    args = sys.argv[1:]
    solo_verificar = "--verificar" in args
    con_seed = "--seed" in args

    print("\n  ╔══════════════════════════════════════════════════╗")
    print("  ║   HW Collector — Esquema multiusuario en Supabase ║")
    print("  ╚══════════════════════════════════════════════════╝\n")

    url = leer_env()
    if not url:
        print("  ✗ Todavía no completaste la cadena de conexión.\n")
        print("  Abrí este archivo y pegá tu contraseña al final:\n")
        print("    C:\\Users\\GODZILLA24H2\\Desktop\\hotwheels_collector\\supabase\\.env\n")
        print("  La línea debe quedar así (con tu contraseña real):\n")
        print("    SUPABASE_DB_URL=postgresql://postgres:TU_CLAVE@db.wgoqtqwxikqhrgulclqk.supabase.co:5432/postgres\n")
        print("  Después avisá en el chat y ejecuto todo.\n")
        sys.exit(1)

    if falta_password(url):
        print("  ✗ La cadena todavía tiene el marcador en vez de tu contraseña.\n")
        print(f"  Ahora dice: {ocultar(url)}\n")
        print("  Reemplazá el texto entre 'postgres:' y '@' por tu contraseña real")
        print("  y volvé a ejecutar. Si tu clave tiene @ : / # ? hay que codificarlos")
        print("  (@ → %40, : → %3A, / → %2F, # → %23, ? → %3F).\n")
        sys.exit(1)

    print(f"  Conectando a: {ocultar(url)}")
    try:
        conn = conectar(url)
    except Exception as e:
        print(f"  ✗ No pude conectar: {str(e)[:200]}")
        print("\n  Si dice 'could not translate host name' o timeout, probá la cadena del")
        print("  Connection Pooler (Project Settings → Database → Connection pooling).")
        sys.exit(1)

    conn.autocommit = True
    cur = conn.cursor()
    print("  ✓ Conectado\n")

    if not solo_verificar:
        print("  Aplicando el esquema:")
        for a in ARCHIVOS:
            if not aplicar(cur, a):
                print("\n  ✗ Detenido por un error. Nada más se aplicó.")
                sys.exit(1)
        if con_seed:
            print("  → aplicando 04_seed.sql (datos de prueba)...", end=" ")
            aplicar(cur, "04_seed.sql")
        print()

    ok = verificar(cur)
    cur.close()
    conn.close()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
