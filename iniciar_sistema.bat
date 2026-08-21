@echo off
setlocal
echo ==========================================
echo INICIANDO SISTEMA GAVAC (SEGURIDAD ACTIVA)
echo ==========================================

:: Obtener la ruta base
set BASE_DIR=%~dp0
cd /d "%BASE_DIR%"

:: Liberar puerto 8000
echo [1/3] Limpiando procesos previos...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /F /PID %%a 2>nul

:: Verificar dependencias
echo [2/3] Verificando entorno de seguridad...
cd backend
if not exist venv (
    echo Error: No se encontro la carpeta venv. Ejecuta la instalacion primero.
    pause
    exit
)

:: Iniciar Servidor Unificado
echo [3/3] Iniciando Servidor GAVAC Profesional...
start "GAVAC SERVER" cmd /k "venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1"

:: Abrir navegador
timeout /t 5 > nul
start http://127.0.0.1:8000/ganado

echo ==========================================
echo ¡SISTEMA LISTO Y PROTEGIDO!
echo Servidor corriendo en: http://127.0.0.1:8000
echo ==========================================
pause
