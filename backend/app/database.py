"""
Configuración de la base de datos de GAVAC.
Responsable: Elian (Módulo de Base de Datos)

La conexión se obtiene desde la variable DATABASE_URL
definida en el archivo .env (Apunta a Supabase - PostgreSQL).
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ============================================================
# 1. CARGAR VARIABLES DEL ARCHIVO .env
# ============================================================
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "⚠️ Error: No se encontró DATABASE_URL en el archivo .env. "
        "Revisa la configuración de Supabase."
    )

# ============================================================
# 2. CONFIGURAR EL MOTOR (ENGINE) PARA SUPABASE
# ============================================================
# pool_pre_ping=True: Verifica que la conexión con la nube esté viva 
# antes de hacer una consulta (muy útil para bases de datos en la nube).
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False  # Cambia a True si quieres ver el SQL real en la terminal para depurar
)

# ============================================================
# 3. CONFIGURAR SESIONES
# ============================================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================================================
# 4. BASE PARA LOS MODELOS (Tablas)
# ============================================================
Base = declarative_base()

# ============================================================
# 5. DEPENDENCIA PARA FASTAPI (Para tus compañeros)
# ============================================================
def get_db():
    """
    Crea una sesión de base de datos para una petición
    y la cierra automáticamente al finalizar.
    Uso: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()