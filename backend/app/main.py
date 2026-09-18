import os
import logging
<<<<<<< HEAD
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
=======
from fastapi import Depends, FastAPI, Request
>>>>>>> a583192508a8de8f5f8a80617669f41a01d080f0
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from app.database import Base, engine
from app.middleware.security import SecurityHeadersMiddleware
from app.modules.cattle.router import router as cattle_router
from app.modules.auth.router import router as auth_router
from app.modules.auth.service import requerir_rol
from app.modules.reportes.router import router as reportes_router
from app.modules.empleados.router import router as empleados_router
from app.modules.sanidad.router import router as sanidad_router
from app.modules.reproduccion.router import router as reproduccion_router
from app.modules.inventario.router import router as inventario_router
from app.modules.produccion.router import router as produccion_router
from app.modules.admin.router import router as admin_api_router

# Configuración de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GAVAC")

app = FastAPI(title="GAVAC API", version="1.0.0")

# La creación automática solo se permite explícitamente en desarrollo.
if os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true":
    Base.metadata.create_all(bind=engine)
    logger.info("DB SYNC OK")

# --- CONFIGURACIÓN DE MIDDLEWARES (ORDEN CRÍTICO) ---

# 1. Seguridad Profesional
app.add_middleware(SecurityHeadersMiddleware)

# 2. CORS - DEBE SER EL ÚLTIMO AGREGADO PARA SER EL ENVOLTORIO MÁS EXTERNO
# (Garantiza que los errores 500 también tengan cabeceras CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5434",
        "http://127.0.0.1:5434",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
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
    app.mount("/dist", StaticFiles(directory=os.path.join(FRONTEND_PATH, "dist")), name="dist")
    app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")
    logger.info(f"FRONTEND MOUNTED AT: {FRONTEND_PATH}")
else:
    logger.error(f"❌ FRONTEND NOT FOUND")

# Servir el Login como página de inicio
@app.get("/")
def root():
<<<<<<< HEAD
    path = os.path.join(FRONTEND_PATH, "login.html")
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "No se encontró el archivo login.html"}
=======
    for name in ["landing.html", "index.html"]:
        path = os.path.join(FRONTEND_PATH, name)
        if os.path.exists(path):
            return FileResponse(path)
    return {"error": "No se encontró el archivo de inicio"}
>>>>>>> a583192508a8de8f5f8a80617669f41a01d080f0

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

@app.get("/fincas")
def fincas_page():
    path = os.path.join(FRONTEND_PATH, "fincas.html")
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "Archivo fincas.html no encontrado"}

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
def admin_page(_usuario=Depends(requerir_rol("admin"))):
    admin_file = os.path.join(FRONTEND_PATH, "src", "modules", "admin", "index.html")
    if os.path.exists(admin_file):
        return FileResponse(admin_file)
    return {"error": "index.html de administración no encontrado"}

@app.get("/empleados")
def empleados_page(_usuario=Depends(requerir_rol("admin"))):
    empleados_file = os.path.join(FRONTEND_PATH, "src", "modules", "empleados", "index.html")
    if os.path.exists(empleados_file):
        return FileResponse(empleados_file)
    return {"error": "index.html de empleados no encontrado"}

@app.get("/sanidad")
def sanidad_page():
    sanidad_file = os.path.join(FRONTEND_PATH, "src", "modules", "sanidad", "index.html")
    if os.path.exists(sanidad_file):
        return FileResponse(sanidad_file)
    return {"error": "index.html de sanidad no encontrado"}

@app.get("/reproduccion")
def reproduccion_page():
    reproduccion_file = os.path.join(FRONTEND_PATH, "src", "modules", "reproduccion", "index.html")
    if os.path.exists(reproduccion_file):
        return FileResponse(reproduccion_file)
    return {"error": "index.html de reproducción no encontrado"}

@app.get("/inventario")
def inventario_page():
    inventario_file = os.path.join(FRONTEND_PATH, "src", "modules", "inventario", "index.html")
    if os.path.exists(inventario_file):
        return FileResponse(inventario_file)
    return {"error": "index.html de inventario no encontrado"}

@app.get("/produccion")
def produccion_page():
    produccion_file = os.path.join(FRONTEND_PATH, "src", "modules", "produccion", "index.html")
    if os.path.exists(produccion_file):
        return FileResponse(produccion_file)
    return {"error": "index.html de producción no encontrado"}

# Routers de la API (RESTAURADOS)
app.include_router(cattle_router)
app.include_router(auth_router)
app.include_router(reportes_router)
app.include_router(empleados_router)
app.include_router(admin_api_router)
app.include_router(sanidad_router)
app.include_router(reproduccion_router)
app.include_router(inventario_router)
app.include_router(produccion_router)

@app.get("/health")
def health():
    return {"status": "ok"}

# Manejador de errores de validación (422) para ver el detalle en consola
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    logger.error(f"❌ ERROR DE VALIDACIÓN: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors, "mensaje": "Los datos enviados no son válidos"}
    )

# Manejador de errores global para depuración con blindaje CORS
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"GLOBAL ERROR: {str(exc)}", exc_info=True)
    response = JSONResponse(
        status_code=500,
        content={"detail": f"Error del servidor: {str(exc)}"}
    )
    # Blindaje CORS Manual (Último recurso)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
