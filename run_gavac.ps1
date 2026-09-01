# ==============================================================================
# GAVAC - MASTER SETUP & RUN SCRIPT (ZERO CONFIG EDITION)
# ==============================================================================

$ErrorActionPreference = "Stop"
$ROOT = $PSScriptRoot

if (-not $ROOT -or -not (Test-Path (Join-Path $ROOT "backend")) -or -not (Test-Path (Join-Path $ROOT "frontend"))) {
    throw "No se encontró la estructura de GAVAC junto a este script."
}

Write-Host "`nINICIANDO GAVAC SYSTEM..." -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python no está instalado o no está en PATH. Instala Python 3.12+ y vuelve a ejecutar este script."
}
if (-not (Get-Command node -ErrorAction SilentlyContinue) -or -not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "Node.js/npm no están instalados o no están en PATH. Instala Node.js LTS y vuelve a ejecutar este script."
}

# --- 1. CONFIGURACIÓN DEL BACKEND ---
Write-Host "`nConfigurando Backend..." -ForegroundColor Yellow
Set-Location -LiteralPath (Join-Path $ROOT "backend")

if (-not (Test-Path "venv")) {
    Write-Host "Creando entorno virtual (esto tardará un poco la primera vez)..." -ForegroundColor Gray
    python -m venv venv
}

Write-Host "Verificando dependencias de Python..." -ForegroundColor Gray
.\venv\Scripts\python.exe -m pip install --upgrade pip | Out-Null
.\venv\Scripts\pip.exe install -r requirements.txt | Out-Null
.\venv\Scripts\pip.exe install uvicorn | Out-Null

if (-not (Test-Path ".env")) {
    Write-Host "ADVERTENCIA: No se encontró el archivo .env" -ForegroundColor Red
    Write-Host "Copiando .env.example como base..." -ForegroundColor Gray
    Copy-Item ".env.example" ".env"
    throw "Se creó backend\.env. Configura DATABASE_URL y AUTH_SECRET_KEY, y vuelve a ejecutar el script."
}

if ((Get-Content ".env" -Raw) -match "\[CONTRASEÑA\]|\[PROJECT_ID\]|cambia-esta-clave") {
    throw "El archivo backend\.env aún contiene valores de ejemplo. Configura DATABASE_URL y AUTH_SECRET_KEY."
}

# --- 2. CONFIGURACIÓN DEL FRONTEND ---
Write-Host "`n Configurando Frontend..." -ForegroundColor Yellow
Set-Location -LiteralPath (Join-Path $ROOT "frontend")

if (-not (Test-Path "node_modules")) {
    Write-Host "Instalando paquetes de Node (npm install)..." -ForegroundColor Gray
    npm install
}

Write-Host "Compilando Frontend (Build)..." -ForegroundColor Gray
npm run build

# --- 3. LANZAMIENTO UNIFICADO ---
$PORT = 8000
if (Get-NetTCPConnection -LocalPort $PORT -State Listen -ErrorAction SilentlyContinue) {
    $PORT = 8010
    Write-Host "El puerto 8000 está ocupado. GAVAC usará el puerto 8010." -ForegroundColor Yellow
}

Write-Host "`nTODO LISTO. LANZANDO SERVIDOR..." -ForegroundColor Green
Write-Host "Landing pública: http://127.0.0.1:$PORT/" -ForegroundColor White
Write-Host "Aplicación:      http://127.0.0.1:$PORT/login" -ForegroundColor White
Write-Host "(Presiona CTRL+C para detener)`n" -ForegroundColor Gray

Set-Location -LiteralPath (Join-Path $ROOT "backend")
$env:PYTHONPATH = "."
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port $PORT --reload
