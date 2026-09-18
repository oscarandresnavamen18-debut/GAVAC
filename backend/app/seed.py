
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
# Importar todos los modelos para que Base.metadata los reconozca
from app.modules.auth.models import Organizacion, Usuario, Finca, UsuarioFincaRol, RolEnum
from app.modules.cattle.models import Animal, Lote
from app.modules.sanidad.models import Sanidad
from app.modules.reproduccion.models import Reproduccion
from app.modules.produccion.models import ProduccionLeche
from app.modules.inventario.models import InventarioInsumo
from app.modules.auth.service import hash_password

def seed_data():
    db: Session = SessionLocal()
    try:
        print("🛠️  Sincronizando Base de Datos SaaS (Limpieza Total)...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        print("🏢 Creando Organización Demo...")
        org = Organizacion(
            nombre="Ganadería GAVAC Demo",
            nit="900.123.456-1",
            plan_contratado="premium"
        )
        db.add(org)
        db.commit()
        db.refresh(org)

        print("👤 Creando Usuarios de Prueba...")

        # 1. Admin Principal
        admin = Usuario(
            email="admin@gavac.test",
            password_hash=hash_password("admin123"),
            organizacion_id=org.id,
            rol_organizacion=RolEnum.admin
        )

        # 2. Veterinario
        vete = Usuario(
            email="vete@gavac.test",
            password_hash=hash_password("vete123"),
            organizacion_id=org.id,
            rol_organizacion=RolEnum.veterinario
        )

        # 3. Operario de Campo
        campo = Usuario(
            email="campo@gavac.test",
            password_hash=hash_password("campo123"),
            organizacion_id=org.id,
            rol_organizacion=RolEnum.operario
        )

        db.add_all([admin, vete, campo])
        db.commit()
        db.refresh(admin)
        db.refresh(vete)
        db.refresh(campo)

        print("📍 Creando Fincas...")
        finca1 = Finca(nombre="Hacienda El Paraíso", ubicacion="Cundinamarca", organizacion_id=org.id)
        finca2 = Finca(nombre="Finca La Esperanza", ubicacion="Antioquia", organizacion_id=org.id)
        db.add_all([finca1, finca2])
        db.commit()
        db.refresh(finca1)
        db.refresh(finca2)

        print("🎭 Asignando Roles en Fincas...")
        # Admin tiene acceso a ambas fincas
        db.add(UsuarioFincaRol(usuario_id=admin.id, finca_id=finca1.id, rol=RolEnum.admin))
        db.add(UsuarioFincaRol(usuario_id=admin.id, finca_id=finca2.id, rol=RolEnum.admin))

        # Veterinario solo en El Paraíso
        db.add(UsuarioFincaRol(usuario_id=vete.id, finca_id=finca1.id, rol=RolEnum.veterinario))

        # Operario solo en La Esperanza
        db.add(UsuarioFincaRol(usuario_id=campo.id, finca_id=finca2.id, rol=RolEnum.operario))

        db.commit()

        print("\n✅ ¡SISTEMA LISTO PARA PRUEBAS!")
        print("--------------------------------------")
        print("USUARIO 1: admin@gavac.test / admin123")
        print("USUARIO 2: vete@gavac.test / vete123")
        print("USUARIO 3: campo@gavac.test / campo123")
        print("--------------------------------------")

    except Exception as e:
        print(f"❌ Error durante el seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
