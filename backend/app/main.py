from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import os

from app.database import Base, engine
from app.middleware.security import SecurityHeadersMiddleware

# ============================================================
# IMPORTAR MODELOS
# ============================================================
# Estos imports permiten que SQLAlchemy registre los modelos
# antes de ejecutar Base.metadata.create_all().
from app.modules.auth.models import Usuario
from app.modules.cattle.models import Animal

# ============================================================
# IMPORTAR ROUTERS
# ============================================================

from app.modules.cattle.router import router as cattle_router
from app.modules.auth.router import router as auth_router
from app.modules.reportes.router import router as reportes_router


# ============================================================
# CREAR APLICACIÓN FASTAPI
# ============================================================

app = FastAPI(
    title="GAVAC API",
    description="Sistema de Gestión Ganadera Profesional",
    version="1.0.0"
)


# ============================================================
# CREAR TABLAS
# ============================================================
# SQLAlchemy crea las tablas de los modelos registrados
# que todavía no existan en PostgreSQL.

Base.metadata.create_all(bind=engine)


# ============================================================
# MIDDLEWARES DE SEGURIDAD
# ============================================================

# 1. Cabeceras de seguridad (Helmet)
app.add_middleware(SecurityHeadersMiddleware)

# 2. Configuración CORS Profesional
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# CONFIGURACIÓN DEL FRONTEND
# ============================================================

# Ruta robusta para encontrar la carpeta frontend en Windows/Linux
current_file_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.normpath(os.path.join(current_file_dir, "..", "..", "frontend"))


# ============================================================
# ARCHIVOS ESTÁTICOS
# ============================================================

if os.path.exists(frontend_dir):
    app.mount(
        "/static",
        StaticFiles(directory=frontend_dir),
        name="static"
    )


# ============================================================
# PÁGINA PRINCIPAL (Landing / Login)
# ============================================================

@app.get("/")
def index_page():
    # Por ahora servimos el index principal que redirige al login o dashboard
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/login")
def login_page():
    return FileResponse(os.path.join(frontend_dir, "src/modules/auth/index.html"))


# ============================================================
# PÁGINA DE REGISTRO DE GANADO
# ============================================================

@app.get("/ganado")
def ganado_page():
    return FileResponse(os.path.join(frontend_dir, "src/modules/ganado/index.html"))


# ============================================================
# PÁGINA DE REPORTES
# ============================================================

@app.get("/reportes")
def reportes_page():
    return FileResponse(os.path.join(frontend_dir, "src/modules/reportes/index.html"))


# ============================================================
# RUTAS DE LOS MÓDULOS
# ============================================================

app.include_router(cattle_router)
app.include_router(auth_router)
app.include_router(reportes_router)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "database": "PostgreSQL"
    }