# ==============================================================================
# GAVAC - MASTER SETUP & RUN SCRIPT (ZERO CONFIG EDITION)
# ==============================================================================

$ErrorActionPreference = "Stop"
$ROOT = Get-Location

Write-Host "`n🚀 INICIANDO GAVAC SYSTEM..." -ForegroundColor Cyan

# --- 1. CONFIGURACIÓN DEL BACKEND ---
Write-Host "`n🐍 Configurando Backend..." -ForegroundColor Yellow
cd "$ROOT/backend"

if (-not (Test-Path "venv")) {
    Write-Host "📦 Creando entorno virtual (esto tardará un poco la primera vez)..." -ForegroundColor Gray
    python -m venv venv
}

Write-Host "🧪 Verificando dependencias de Python..." -ForegroundColor Gray
.\venv\Scripts\python.exe -m pip install --upgrade pip | Out-Null
.\venv\Scripts\pip.exe install -r requirements.txt | Out-Null
.\venv\Scripts\pip.exe install uvicorn | Out-Null

if (-not (Test-Path ".env")) {
    Write-Host "⚠️ ADVERTENCIA: No se encontró el archivo .env" -ForegroundColor Red
    Write-Host "Copiando .env.example como base..." -ForegroundColor Gray
    Copy-Item ".env.example" ".env"
}

# --- 2. CONFIGURACIÓN DEL FRONTEND ---
Write-Host "`n🎨 Configurando Frontend..." -ForegroundColor Yellow
cd "$ROOT/frontend"

if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Instalando paquetes de Node (npm install)..." -ForegroundColor Gray
    npm install
}

Write-Host "🛠️ Compilando Frontend (Build)..." -ForegroundColor Gray
npm run build

# --- 3. LANZAMIENTO UNIFICADO ---
Write-Host "`n🔥 TODO LISTO. LANZANDO SERVIDOR..." -ForegroundColor Green
Write-Host "Accede en: http://localhost:8000" -ForegroundColor White
Write-Host "(Presiona CTRL+C para detener)`n" -ForegroundColor Gray

cd "$ROOT/backend"
$env:PYTHONPATH = "."
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
