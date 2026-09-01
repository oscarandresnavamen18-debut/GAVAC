import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from dotenv import load_dotenv

from alembic import context

# Añadir la ruta del proyecto para que Alembic encuentre el módulo 'app'
sys.path.append(os.getcwd())

# Cargar variables de entorno desde .env


load_dotenv(encoding="utf-8-sig")

# Importar la Base de SQLAlchemy y los modelos para autogeneración
from app.database import Base
from app.modules.auth.models import Usuario, Finca, ProduccionLeche, TareaFinca, AuditoriaLog
from app.modules.cattle.models import Animal

# Metadata del proyecto
target_metadata = Base.metadata

# Configuración de Alembic
config = context.config

# Sobrescribir la URL de la base de datos con la del archivo .env
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
