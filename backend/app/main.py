import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from app.database import Base, engine
from app.middleware.security import SecurityHeadersMiddleware
from app.modules.cattle.router import router as cattle_router
from app.modules.auth.router import router as auth_router
from app.modules.reportes.router import router as reportes_router
from app.modules.empleados.router import router as empleados_router

# Configuración de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GAVAC")

app = FastAPI(title="GAVAC API", version="1.0.0")

# La creación automática solo se permite explícitamente en desarrollo.
if os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true":
    Base.metadata.create_all(bind=engine)
    logger.info("✅ DB SYNC OK")

# Middlewares
app.add_middleware(SecurityHeadersMiddleware)
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8000,http://127.0.0.1:8000",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Rutas de Archivos Estáticos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
FRONTEND_PATH = os.path.join(PROJECT_ROOT, "frontend")

# Debug para consola
print(f"--- GAVAC PATH DEBUG ---")
print(f"BASE_DIR: {BASE_DIR}")
print(f"FRONTEND_PATH: {FRONTEND_PATH}")
print(f"LOGIN EXISTS: {os.path.exists(os.path.join(FRONTEND_PATH, 'login.html'))}")
print(f"------------------------")

if os.path.exists(FRONTEND_PATH):
    app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")
    logger.info(f"✅ FRONTEND MOUNTED AT: {FRONTEND_PATH}")
else:
    logger.error(f"❌ FRONTEND NOT FOUND")

# Servir la Landing Page
@app.get("/")
def root():
    for name in ["index.html", "landing.html"]:
        path = os.path.join(FRONTEND_PATH, name)
        if os.path.exists(path):
            return FileResponse(path)
    return {"error": "No se encontró el archivo de inicio"}

# Servir el Login
@app.get("/login")
def login_page():
    path = os.path.join(FRONTEND_PATH, "login.html")
    if os.path.exists(path):
        return FileResponse(path)



    # Si no está en la raíz, buscar en el módulo de auth
    auth_path = os.path.join(FRONTEND_PATH, "src", "modules", "auth", "login.html")
    if os.path.exists(auth_path):
        return FileResponse(auth_path)

    return {"error": f"Archivo login.html no encontrado en {FRONTEND_PATH}"}

@app.get("/dashboard")
def dashboard_page():
    dash_file = os.path.join(FRONTEND_PATH, "dashboard.html")
    if os.path.exists(dash_file):
        return FileResponse(dash_file)
    return {"error": "Dashboard no encontrado"}

@app.get("/ganado")
def ganado_page():
    ganado_file = os.path.join(FRONTEND_PATH, "src", "modules", "ganado", "index.html")
    if os.path.exists(ganado_file):
        return FileResponse(ganado_file)
    return {"error": "index.html de ganado no encontrado"}

@app.get("/reportes")
def reportes_page():
    reportes_file = os.path.join(FRONTEND_PATH, "src", "modules", "reportes", "index.html")
    if os.path.exists(reportes_file):
        return FileResponse(reportes_file)
    return {"error": "index.html de reportes no encontrado"}

@app.get("/admin")
def admin_page():
    admin_file = os.path.join(FRONTEND_PATH, "src", "modules", "admin", "index.html")
    if os.path.exists(admin_file):
        return FileResponse(admin_file)
    return {"error": "index.html de administración no encontrado"}

@app.get("/empleados")
def empleados_page():
    empleados_file = os.path.join(FRONTEND_PATH, "src", "modules", "empleados", "index.html")
    if os.path.exists(empleados_file):
        return FileResponse(empleados_file)
    return {"error": "index.html de empleados no encontrado"}

# Routers de la API (RESTAURADOS)
app.include_router(cattle_router)
app.include_router(auth_router)
app.include_router(reportes_router)
app.include_router(empleados_router)
from app.modules.admin.router import router as admin_api_router
app.include_router(admin_api_router)

@app.get("/health")
def health():
    return {"status": "ok"}

# Manejador de errores global para depuración
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"GLOBAL ERROR: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Error del servidor: {str(exc)}"}
    )
