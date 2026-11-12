# Hot Wheels Collector — Bridge de datos

## ¿Qué es el bridge?

El bridge es un servidor local que sirve los datos actualizados (seguimiento, tendencias, cajas, mercados, precios) al puerto **8081**. La app los usa para mantener los módulos al día.

## Cómo iniciarlo

### Opción 1: Script de inicio (recomendado)
Doble clic en **`iniciar.bat`** en la carpeta del proyecto.

### Opción 2: Línea de comandos
```bash
cd C:\Users\GODZILLA24H2\Desktop\hotwheels_collector
python3 agent_bridge.py
```

### Opción 3: Sin ventana (segundo plano)
```bash
pythonw agent_bridge.py
```

## Verificar que funciona

Abrí en el navegador: **http://localhost:8081/agent/status**

Debería mostrar:
```json
{
  "vivo": true,
  "version": "2.0",
  "archivos": [...]
}
```

## Uso con la app

1. Iniciá el bridge (dejá la ventana abierta)
2. Abrí la app: https://foxnismone.github.io/hw-collector/
3. La app detecta el bridge y sincroniza los datos automáticamente
4. Los módulos (Seguimiento, Tendencias, Cajas, Mercados) se actualizan

## Endpoints del bridge

| Endpoint | Descripción |
|----------|-------------|
| `/` | La app (index.html) |
| `/agent/status` | Estado + lista de archivos con hash |
| `/sync/file?name=<archivo>` | Datos de un archivo |
| `/trends` | Tendencias activas |
| `/img/<archivo>` | Imágenes |

## Archivos de datos

| Archivo | Variable en la app |
|---------|-------------------|
| `catalog_web.json` | `CAT` |
| `cajas.json` | `CAJ` |
| `tendencias.json` | `TEND` |
| `mercados.json` | `MKT` |
| `precios_referencia.json` | `PRE` |
| `indice.json` | `IDXINFO` |
| `seguimiento.json` | `SEG` |
| `historias.json` | `HIST` |
| `owned_collection.json` | `OWNED_DEMO` |

## Solución de problemas

**La app no sincroniza:**
- Verificá que el bridge esté corriendo (http://localhost:8081/agent/status)
- Recargá la app (F5)
- Verificá la consola del navegador (F12) por errores

**Puerto 8081 ocupado:**
```bash
netstat -ano | findstr :8081
taskkill /F /PID <PID>
```

**Los módulos siguen vacíos:**
- Los datos embebidos en el HTML son la base (funcionan sin bridge)
- El bridge solo actualiza con datos más recientes
- Verificá que los archivos JSON en `data/` existan
