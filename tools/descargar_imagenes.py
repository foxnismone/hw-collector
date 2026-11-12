#!/usr/bin/env python3
"""Descarga masiva de imágenes de Fandom para el catálogo Hot Wheels.
Usa hilos paralelos para acelerar la descarga.
"""
import json
import os
import re
import sys
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import unquote, quote

import requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
IMG = os.path.join(BASE, "web", "img")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.8",
    "Referer": "https://hotwheels.fandom.com/",
}

def nombre_unico(modelo):
    """Genera un nombre único basado en el ID del modelo."""
    id_str = str(modelo.get('i', ''))
    return hashlib.md5(id_str.encode()).hexdigest()[:12] + '.webp'

def descargar_imagen(url, destino, session):
    """Descarga una imagen y la guarda en destino."""
    try:
        r = session.get(url, timeout=20)
        if r.status_code == 200:
            ct = r.headers.get('Content-Type', '')
            if 'image' in ct or len(r.content) > 1000:
                with open(destino, 'wb') as f:
                    f.write(r.content)
                return True, len(r.content)
        return False, 0
    except Exception as e:
        return False, 0

def procesar_modelo(modelo, session, stats):
    """Procesa un modelo: descarga la imagen si es necesaria."""
    im = modelo.get('im', '')
    if not im:
        stats['sin_url'] += 1
        return None
    
    # Si ya es local, no hacer nada
    if im.endswith('.webp'):
        stats['ya_local'] += 1
        return None
    
    # Si es URL externa, descargar
    if im.startswith('http'):
        # Extraer la URL de Fandom
        if 'images.weserv.nl' in im:
            # Extraer la URL de Fandom del proxy
            m = re.search(r'url=([^&]+)', im)
            if m:
                url_fandom = 'https://' + unquote(m.group(1))
            else:
                stats['error_url'] += 1
                return None
        elif 'static.wikia.nocookie.net' in im:
            url_fandom = im
        else:
            stats['otra_url'] += 1
            return None
        
        # Generar nombre local
        nombre = nombre_unico(modelo)
        destino = os.path.join(IMG, nombre)
        
        # Si ya existe, no descargar
        if os.path.exists(destino):
            stats['ya_existe'] += 1
            return {'id': modelo.get('i'), 'nuevo_im': nombre}
        
        # Intentar descargar de Fandom directo primero
        ok, size = descargar_imagen(url_fandom, destino, session)
        
        # Si falla, intentar con weserv.nl
        if not ok and 'images.weserv.nl' not in url_fandom:
            url_weserv = 'https://images.weserv.nl/?url=' + url_fandom.replace('https://', '')
            ok, size = descargar_imagen(url_weserv, destino, session)
        
        if ok:
            stats['descargadas'] += 1
            return {'id': modelo.get('i'), 'nuevo_im': nombre}
        else:
            stats['fallidas'] += 1
            return None
    
    return None

def main():
    limite = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    
    # Leer el catálogo
    with open(os.path.join(DATA, 'catalog_web.json'), encoding='utf-8') as f:
        catalogo = json.load(f)
    
    print(f"Modelos en catálogo: {len(catalogo)}")
    print(f"Límite de descarga: {limite}")
    
    # Filtrar modelos con URL externa
    con_url = [m for m in catalogo if m.get('im', '').startswith('http')]
    print(f"Modelos con URL externa: {len(con_url)}")
    
    # Limitar
    a_procesar = con_url[:limite]
    print(f"A procesar: {len(a_procesar)}")
    
    # Estadísticas
    stats = {
        'descargadas': 0,
        'fallidas': 0,
        'ya_local': 0,
        'ya_existe': 0,
        'sin_url': 0,
        'error_url': 0,
        'otra_url': 0,
    }
    
    # Descargar en paralelo
    session = requests.Session()
    session.headers.update(HEADERS)
    
    resultados = []
    inicio = time.time()
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(procesar_modelo, m, session, stats): m for m in a_procesar}
        
        for i, future in enumerate(as_completed(futures)):
            try:
                resultado = future.result()
                if resultado:
                    resultados.append(resultado)
            except Exception as e:
                stats['fallidas'] += 1
            
            # Mostrar progreso cada 100
            if (i + 1) % 100 == 0:
                elapsed = time.time() - inicio
                rate = (i + 1) / elapsed if elapsed > 0 else 0
                print(f"  [{i+1}/{len(a_procesar)}] descargadas={stats['descargadas']} fallidas={stats['fallidas']} ya_existe={stats['ya_existe']} ({rate:.1f}/s)")
    
    elapsed = time.time() - inicio
    print(f"\n=== RESULTADO ===")
    print(f"  Descargadas: {stats['descargadas']}")
    print(f"  Fallidas: {stats['fallidas']}")
    print(f"  Ya existían: {stats['ya_existe']}")
    print(f"  Tiempo: {elapsed:.1f}s")
    
    # Actualizar el catálogo
    if resultados:
        print(f"\nActualizando catálogo con {len(resultados)} imágenes nuevas...")
        
        # Crear un diccionario de actualizaciones
        actualizaciones = {r['id']: r['nuevo_im'] for r in resultados}
        
        # Actualizar el catálogo
        for modelo in catalogo:
            if modelo.get('i') in actualizaciones:
                modelo['im'] = actualizaciones[modelo['i']]
        
        # Guardar el catálogo
        with open(os.path.join(DATA, 'catalog_web.json'), 'w', encoding='utf-8') as f:
            json.dump(catalogo, f, ensure_ascii=False)
        
        # También guardar en web/
        import shutil
        shutil.copy2(os.path.join(DATA, 'catalog_web.json'), os.path.join(BASE, 'web', 'data', 'catalog_web.json'))
        
        print(f"✓ Catálogo actualizado")
    
    # Guardar el log
    log_path = os.path.join(BASE, 'logs', f'descarga_{time.strftime("%Y%m%d_%H%M%S")}.json')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump({
            'stats': stats,
            'resultados': resultados[:100],  # Solo los primeros 100
            'total_resultados': len(resultados),
            'tiempo_seg': elapsed,
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Log guardado en {log_path}")

if __name__ == '__main__':
    main()
