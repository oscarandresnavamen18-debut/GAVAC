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
    # Eliminar tabla vieja si existe (para limpiar conflictos)
    "DROP TABLE IF EXISTS produccion_leche CASCADE;",

    # Crear la tabla oficial vinculada a animales
    """
    CREATE TABLE produccion_leche (
        id SERIAL PRIMARY KEY,
        animal_id INT REFERENCES animales(id) ON DELETE CASCADE,
        litros DECIMAL(10,2) NOT NULL,
        fecha DATE DEFAULT CURRENT_DATE,
        jornada VARCHAR(20) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
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

print("🏁 Migración de Producción completada.")
