import os
from sqlalchemy import text, create_engine
from dotenv import load_dotenv

# Cargar variables de entorno desde el backend
load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))

db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("❌ Error: DATABASE_URL no encontrada en .env")
    exit(1)

engine = create_engine(db_url)

commands = [
    # 1. Crear tabla fincas
    """
    CREATE TABLE IF NOT EXISTS fincas (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        ubicacion VARCHAR(255) NULL,
        area_hectareas DECIMAL(10,2) NULL,
        estado VARCHAR(20) DEFAULT 'Activa',
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """,
    # 2. Crear tabla intermedia usuarios_fincas
    """
    CREATE TABLE IF NOT EXISTS usuarios_fincas (
        usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
        finca_id INT REFERENCES fincas(id) ON DELETE CASCADE,
        PRIMARY KEY (usuario_id, finca_id)
    );
    """,
    # 3. Actualizar tabla animales con nuevos campos
    "ALTER TABLE animales ADD COLUMN IF NOT EXISTS especie VARCHAR(50) DEFAULT 'Bovino';",
    "ALTER TABLE animales ADD COLUMN IF NOT EXISTS peso_actual DECIMAL(10,2) NULL;",
    "ALTER TABLE animales ADD COLUMN IF NOT EXISTS edad_meses INT NULL;",
    "ALTER TABLE animales ADD COLUMN IF NOT EXISTS finca_id INT REFERENCES fincas(id) ON DELETE SET NULL;",
    # 4. Crear tabla traslados
    """
    CREATE TABLE IF NOT EXISTS traslados_animales (
        id SERIAL PRIMARY KEY,
        animal_id INT REFERENCES animales(id) ON DELETE CASCADE,
        origen_finca_id INT REFERENCES fincas(id),
        destino_finca_id INT REFERENCES fincas(id),
        origen_lote VARCHAR(50),
        destino_lote VARCHAR(50),
        motivo TEXT,
        usuario_responsable_id INT REFERENCES usuarios(id),
        fecha_traslado TIMESTAMPTZ DEFAULT NOW()
    );
    """
]

with engine.connect() as conn:
    for cmd in commands:
        try:
            conn.execute(text(cmd))
            conn.commit()
            print(f"✅ Ejecutado correctamente.")
        except Exception as e:
            print(f"⚠️ Error: {e}")

print("🏁 Migración V2 completada.")
