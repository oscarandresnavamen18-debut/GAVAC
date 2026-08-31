import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from app.database import Base, engine
from app.middleware.security import SecurityHeadersMiddleware
from app.modules.cattle.router import router as cattle_router
from app.modules.auth.router import router as auth_router
from app.modules.reportes.router import router as reportes_router

# Configuración de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GAVAC")

app = FastAPI(title="GAVAC API", version="1.0.0")

# Inicialización Silenciosa de DB
try:
    # Las tablas ya fueron recreadas en el paso anterior. 
    # Mantenemos solo el create_all para uso normal.
    Base.metadata.create_all(bind=engine)
    logger.info("✅ DB SYNC OK")
except Exception as e:
    logger.error(f"❌ DB SYNC FAIL: {e}")

# Middlewares
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Rutas de Archivos Estáticos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_PATH = os.path.join(os.path.dirname(BASE_DIR), "frontend")

if os.path.exists(FRONTEND_PATH):
    app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")
    logger.info(f"✅ FRONTEND MOUNTED: {FRONTEND_PATH}")
else:
    logger.error(f"❌ FRONTEND NOT FOUND AT: {FRONTEND_PATH}")

# Servir el Login como página por defecto
@app.get("/")
def root():
    return RedirectResponse(url="/login")

@app.get("/login")
def login_page():
    index_file = os.path.join(FRONTEND_PATH, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Index.html no encontrado en la ruta configurada"}

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

# Routers de la API (RESTAURADOS)
app.include_router(cattle_router)
app.include_router(auth_router)
app.include_router(reportes_router)

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
