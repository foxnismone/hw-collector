@echo off
REM ============================================================
REM  Hot Wheels Collector - Inicio rápido
REM  Arranca el bridge de datos (puerto 8081) y abre la app
REM ============================================================

echo.
echo ============================================================
echo   Hot Wheels Collector - Inicio
echo ============================================================
echo.

REM Verificar si el bridge ya está corriendo
netstat -ano | findstr ":8081" | findstr "LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo [OK] El bridge ya está corriendo en el puerto 8081
    goto :abrir
)

echo [1/2] Iniciando bridge de datos en puerto 8081...
start "HW Bridge" /min pythonw agent_bridge.py
timeout /t 3 /nobreak >nul

REM Verificar que arrancó
netstat -ano | findstr ":8081" | findstr "LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Bridge corriendo en http://localhost:8081
) else (
    echo [ERROR] No se pudo iniciar el bridge
    echo         Verificá que python3 esté instalado
    pause
    exit /b 1
)

:abrir
echo [2/2] Abriendo la app en el navegador...
echo.
echo   - App local:   http://localhost:8081/
echo   - App web:     https://foxnismone.github.io/hw-collector/
echo.
echo   Para que los datos se sincronicen, dejá esta ventana abierta.
echo   Cerrá la ventana del bridge (HW Bridge) para detenerlo.
echo.
start "" "https://foxnismone.github.io/hw-collector/"
pause
