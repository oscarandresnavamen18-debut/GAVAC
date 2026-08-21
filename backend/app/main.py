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
# Estos imports son OBLIGATORIOS antes de create_all() 
# para que SQLAlchemy registre las tablas en Supabase.
from app.modules.auth.models import Usuario
from app.modules.cattle.models import Animal

# ============================================================
# IMPORTAR ROUTERS
# ============================================================
from app.modules.cattle.router import router as cattle_router
from app.modules.auth.router import router as auth_router
from app.modules.reportes.router import router as reportes_router
<<<<<<< HEAD

=======
>>>>>>> 2d2f93dc9d18a1cad29ff38af36862b7544d0f7b

# ============================================================
# CREAR APLICACIÓN FASTAPI
# ============================================================
app = FastAPI(
    title="GAVAC API",
<<<<<<< HEAD
    description="Sistema de Gestión Ganadera Profesional",
    version="1.0.0"
=======
    version="0.1.0",
    description="API para el sistema de registro de ganado conectado a Supabase"
>>>>>>> 2d2f93dc9d18a1cad29ff38af36862b7544d0f7b
)

# ============================================================
# CONFIGURACIÓN CORS (Permite que el frontend hable con el backend)
# ============================================================
<<<<<<< HEAD
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
=======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (ideal para desarrollo)
>>>>>>> 2d2f93dc9d18a1cad29ff38af36862b7544d0f7b
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# CREAR TABLAS EN LA BASE DE DATOS
# ============================================================
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas verificadas/creadas exitosamente en la base de datos.")
except Exception as e:
    print(f"❌ Error al conectar con la base de datos: {e}")

# ============================================================
# CONFIGURACIÓN DEL FRONTEND
# ============================================================
<<<<<<< HEAD

# Ruta robusta para encontrar la carpeta frontend en Windows/Linux
current_file_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.normpath(os.path.join(current_file_dir, "..", "..", "frontend"))
=======
frontend_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../frontend"
    )
)
>>>>>>> 2d2f93dc9d18a1cad29ff38af36862b7544d0f7b

# ============================================================
# ARCHIVOS ESTÁTICOS
# ============================================================
<<<<<<< HEAD

if os.path.exists(frontend_dir):
    app.mount(
        "/static",
        StaticFiles(directory=frontend_dir),
        name="static"
    )
=======
app.mount(
    "/static",
    StaticFiles(directory=frontend_dir),
    name="static"
)
>>>>>>> 2d2f93dc9d18a1cad29ff38af36862b7544d0f7b

# ============================================================
<<<<<<< HEAD
# PÁGINA PRINCIPAL (Landing / Login)
=======
# PÁGINAS (Rutas que sirven el HTML)
>>>>>>> 2d2f93dc9d18a1cad29ff38af36862b7544d0f7b
# ============================================================
@app.get("/")
def index_page():
<<<<<<< HEAD
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
=======
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/ganado")
def ganado_page():
    return FileResponse(os.path.join(frontend_dir, "ganado.html"))

@app.get("/reportes")
def reportes_page():
    return FileResponse(os.path.join(frontend_dir, "reportes.html"))

# ============================================================
# INCLUIR RUTAS DE LA API (MÓDULOS)
>>>>>>> 2d2f93dc9d18a1cad29ff38af36862b7544d0f7b
# ============================================================
app.include_router(cattle_router)
app.include_router(auth_router)
app.include_router(reportes_router)
<<<<<<< HEAD

=======
>>>>>>> 2d2f93dc9d18a1cad29ff38af36862b7544d0f7b

# ============================================================
# HEALTH CHECK (Para verificar que todo está vivo)
# ============================================================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "database": "PostgreSQL (Supabase)",
        "message": "El backend está corriendo y conectado"
    }