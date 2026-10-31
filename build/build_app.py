#!/usr/bin/env python3
"""
build_app.py - Script de build para Hot Wheels Collector
Aplica fixes al lector de código (escaneo OCR + barcode) en todos los archivos HTML.

Fixes aplicados:
1. ZXing: try/catch robusto con fallback de API (decodeFromVideoDevice / decodeFromVideoElement)
2. Tesseract.js: captura y procesamiento OCR con manejo de errores mejorado
3. extraerCodigos: patrones regex ampliados (asortación, modelo, case, códigos cortos)
4. procesarCodigo: búsqueda flexible con normalización de caracteres
5. buscarEnInternet: instrucciones claras con lista de sitios de búsqueda
"""

import os
import re
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Archivos HTML a procesar
HTML_FILES = [
    "index.html",
    "galeria_catalogo.html",
    "galeria_coleccion.html",
    os.path.join("web", "galeria_catalogo.html"),
    os.path.join("web", "galeria_coleccion.html"),
    os.path.join("web", "index.html"),
]

# ============================================================
# FIX 1: abrirScan - ZXing con try/catch robusto y fallback
# ============================================================
ABRIRSCAN_OLD = r"""    if(typeof ZXing!=='undefined'){
      scanZX=new ZXing.BrowserMultiFormatReader();
      scanZX.decodeFromVideoDevice(undefined,video,(result,err)=>{
        if(result){
          const code=result.getText();
          if(code && code.length>=3){
            detenerScan();
            procesarCodigo(code);
          }
        }
      });
    }"""

ABRIRSCAN_NEW = r"""    if(typeof ZXing!=='undefined'){
      try{
        scanZX=new ZXing.BrowserMultiFormatReader();
        const onDecode=(result,err)=>{
          if(result){
            const code=result.getText();
            if(code && code.length>=3){
              detenerScan();
              procesarCodigo(code);
            }
          }
        };
        if(typeof scanZX.decodeFromVideoDevice==='function'){
          scanZX.decodeFromVideoDevice(undefined,video,onDecode);
        }else if(typeof scanZX.decodeFromVideoElement==='function'){
          scanZX.decodeFromVideoElement(video,onDecode);
        }else{
          throw new Error('API de escaneo no disponible en esta versión de ZXing');
        }
        logMsg('i','Escáner ZXing activo. Apuntá al código de barras o tocá "Capturar (OCR)".');
      }catch(zxErr){
        logMsg('w','ZXing no disponible ('+zxErr.message+'). Usá Capturar (OCR).');
        scanZX=null;
      }
    }else{
      logMsg('w','ZXing no cargado. Usá Capturar (OCR) con Tesseract.js.');
    }"""

# ============================================================
# FIX 2: capturarOCR - Mejor manejo de errores
# ============================================================
CAPTURAR_OCR_OLD = r"""    } else {
      logMsg('a','No se detectaron códigos válidos en la imagen.');
    }
  }catch(e){
    logMsg('a','Error en OCR: '+e.message);
  }"""

CAPTURAR_OCR_NEW = r"""    } else {
      logMsg('a','No se detectaron códigos válidos en la imagen. Intentá con mejor iluminación o acercá el código al centro del recuadro.');
    }
  }catch(e){
    logMsg('a','Error en OCR: '+e.message+'. Verificá que Tesseract.js se cargó correctamente.');
  }"""

# ============================================================
# FIX 3: extraerCodigos - Patrones regex ampliados
# ============================================================
EXTRAER_CODIGOS_OLD = r"""function extraerCodigos(texto){
  const codigos=[];
  // Patrones de códigos Hot Wheels
  const patrones=[
    /\b[LlCcFfGg]\d{4}\b/,           // Asortación: L2593, C4982, 5785
    /\b[A-Z]{3}\d{2}\b/,             // Modelo: FRN78, JKX06
    /\b[A-Z]\d{4}-?\d{3}[A-Z]\b/,    // Case: L2593-976K
    /\bAsst\.?\s*[A-Z]?\d{4}\b/i,    // "Asst. C4982"
  ];
  for(const p of patrones){
    const m=texto.match(p);
    if(m) codigos.push(m[0].toUpperCase());
  }
  return [...new Set(codigos)];
}"""

EXTRAER_CODIGOS_NEW = r"""function extraerCodigos(texto){
  const codigos=[];
  // Patrones de códigos Hot Wheels (mejorados)
  const patrones=[
    /\b[LlCcFfGg]\d{4}\b/,           // Asortación: L2593, C4982, F5785
    /\b[A-Z]{3}\d{2}\b/,             // Modelo: FRN78, JKX06
    /\b[A-Z]\d{4}-?\d{3}[A-Z]\b/,    // Case: L2593-976K
    /\bAsst\.?\s*[A-Z]?\d{4}\b/i,    // "Asst. C4982"
    /\b\d{3}[A-Z]\b/,                // Códigos cortos: 976K
    /\b[A-Z]{2}\d{4}\b/,             // Códigos de 2 letras + 4 números
    /\b\d{4}[A-Z]\b/,                // Códigos de 4 números + letra
  ];
  for(const p of patrones){
    const matches=texto.match(new RegExp(p.source,p.flags.includes('g')?p.flags:p.flags+'g'));
    if(matches){
      matches.forEach(m=>codigos.push(m.toUpperCase().replace(/\s+/g,'')));
    }
  }
  return [...new Set(codigos)];
}"""

# ============================================================
# FIX 4: procesarCodigo - Búsqueda flexible con normalización
# ============================================================
PROCESAR_CODIGO_OLD = r"""  // Buscar en el catálogo local
  const encontrado=buscarPorCodigo(codigo);"""

PROCESAR_CODIGO_NEW = r"""  // Normalizar código para búsqueda (quitar caracteres especiales)
  const codigoNorm=codigo.replace(/[^A-Z0-9]/g,'');
  // Buscar en el catálogo local (intento múltiple)
  const encontrado=buscarPorCodigo(codigo)||buscarPorCodigo(codigoNorm);"""

# ============================================================
# FIX 5: buscarPorCodigo - Búsqueda normalizada
# ============================================================
BUSCAR_POR_CODIGO_OLD = r"""function buscarPorCodigo(codigo){
  // Buscar por ID exacto o por código de asortación
  return CAT.find(c=>c.i===codigo || c.i.includes(codigo) || codigo.includes(c.i));
}"""

BUSCAR_POR_CODIGO_NEW = r"""function buscarPorCodigo(codigo){
  if(!codigo) return null;
  const codigoNorm=codigo.replace(/[^A-Z0-9]/g,'').toUpperCase();
  // Buscar por ID exacto o por código de asortación (normalizado)
  return CAT.find(c=>{
    const ciNorm=c.i.replace(/[^A-Z0-9]/g,'').toUpperCase();
    return c.i===codigo || ciNorm===codigoNorm || ciNorm.includes(codigoNorm) || codigoNorm.includes(ciNorm);
  });
}"""

# ============================================================
# FIX 6: buscarEnInternet - Instrucciones claras
# ============================================================
BUSCAR_EN_INTERNET_OLD = r"""async function buscarEnInternet(codigo){
  const res=document.getElementById('scanresult');
  logMsg('i','🔍 Scraping de rescate para: '+codigo);
  res.innerHTML='<div class="note">🔍 Buscando en internet...<br><br>Ejecutá el scraper de rescate en tu PC:</div>';
  res.innerHTML+='<pre class="note" style="background:var(--elev);padding:8px;border-radius:4px;overflow-x:auto;font-size:12px">python build/scraper_rescate.py "'+codigo+'"</pre>';
  res.innerHTML+='<div class="note" style="margin-top:8px">El scraper buscará en SmartWheelers, HW Wiki, HW Price Guide, Reddit, eBay y Mercado Libre.<br><br>Si el scraper encuentra el modelo, los datos se guardan en caché por 7 días.</div>';
}"""

BUSCAR_EN_INTERNET_NEW = r"""async function buscarEnInternet(codigo){
  const res=document.getElementById('scanresult');
  logMsg('i','🔍 Búsqueda en internet para: '+codigo);
  res.innerHTML=`
    <div class="sec" style="border:1px solid var(--brand);padding:12px">
      <h4 style="margin:0 0 8px">🔍 Buscar en internet</h4>
      <div class="note" style="margin-bottom:8px">Para buscar el código <b>${codigo}</b> en internet, ejecutá el siguiente comando en tu terminal:</div>
      <pre class="note" style="background:var(--elev);padding:12px;border-radius:6px;overflow-x:auto;font-size:13px;margin:0">python build/scraper_rescate.py "${codigo}"</pre>
      <div class="note" style="margin-top:12px">El scraper buscará en:</div>
      <ul class="note" style="margin:8px 0;padding-left:20px">
        <li>SmartWheelers</li>
        <li>HW Wiki</li>
        <li>HW Price Guide</li>
        <li>Reddit</li>
        <li>eBay</li>
        <li>Mercado Libre</li>
      </ul>
      <div class="note">Si el scraper encuentra el modelo, los datos se guardan en caché por 7 días.</div>
    </div>`;
}"""

# Lista de todos los fixes
FIXES = [
    ("abrirScan - ZXing fallback API", ABRIRSCAN_OLD, ABRIRSCAN_NEW),
    ("capturarOCR - mensajes de error", CAPTURAR_OCR_OLD, CAPTURAR_OCR_NEW),
    ("extraerCodigos - patrones ampliados", EXTRAER_CODIGOS_OLD, EXTRAER_CODIGOS_NEW),
    ("procesarCodigo - búsqueda normalizada", PROCESAR_CODIGO_OLD, PROCESAR_CODIGO_NEW),
    ("buscarPorCodigo - búsqueda normalizada", BUSCAR_POR_CODIGO_OLD, BUSCAR_POR_CODIGO_NEW),
    ("buscarEnInternet - instrucciones claras", BUSCAR_EN_INTERNET_OLD, BUSCAR_EN_INTERNET_NEW),
]


def apply_fixes(content: str) -> tuple[str, list[str]]:
    """Aplica todos los fixes al contenido HTML."""
    changes = []
    for name, old, new in FIXES:
        if old in content:
            content = content.replace(old, new)
            changes.append(f"✅ {name}")
        else:
            changes.append(f"⚠️  {name} - no encontrado (ya aplicado o formato diferente)")
    return content, changes


def main():
    """Función principal del build."""
    print("=" * 60)
    print("🔧 Hot Wheels Collector - Build de fixes para lector de código")
    print("=" * 60)
    
    total_files = 0
    total_changes = 0
    
    for html_file in HTML_FILES:
        filepath = BASE_DIR / html_file
        if not filepath.exists():
            print(f"\n⚠️  {html_file}: no existe, saltando...")
            continue
        
        print(f"\n📄 Procesando: {html_file}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content, changes = apply_fixes(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            total_files += 1
            total_changes += sum(1 for c in changes if c.startswith("✅"))
            for change in changes:
                print(f"   {change}")
        else:
            print("   ℹ️  No se encontraron cambios necesarios")
    
    print("\n" + "=" * 60)
    print(f"✅ Build completado: {total_files} archivos modificados, {total_changes} fixes aplicados")
    print("=" * 60)
    
    # Resumen de fixes
    print("\n📋 Resumen de fixes aplicados:")
    for name, _, _ in FIXES:
        print(f"   • {name}")
    
    return 0


if __name__ == "__main__":
    exit(main())
