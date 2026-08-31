# ==============================================================================
# GAVAC - Script de Inicio Automático (Robusto)
# ==============================================================================

$ErrorActionPreference = "Stop"
$PROJECT_ROOT = Get-Location

Write-Host "🚀 Iniciando GAVAC..." -ForegroundColor Cyan

# 1. Verificar Entorno Virtual
if (-not (Test-Path "backend/venv")) {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv backend/venv
}

# 2. Activar e Instalar Dependencias
Write-Host "🛠️ Verificando dependencias..." -ForegroundColor Yellow
& "$PROJECT_ROOT/backend/venv/Scripts/python.exe" -m pip install --upgrade pip
& "$PROJECT_ROOT/backend/venv/Scripts/pip.exe" install -r backend/requirements.txt

# 3. Configurar Variables de Entorno
$env:PYTHONPATH = "$PROJECT_ROOT/backend"
Write-Host "✅ Entorno configurado." -ForegroundColor Green

# 4. Iniciar Servidor
Write-Host "🔥 Lanzando servidor en http://localhost:8000" -ForegroundColor Cyan
cd backend
& "$PROJECT_ROOT/backend/venv/Scripts/python.exe" -m uvicorn app.main:app --reload
