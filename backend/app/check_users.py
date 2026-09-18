
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.modules.auth.models import Usuario
from app.modules.auth.service import verificar_password

def check():
    # Importar todo para evitar errores de mapper
    from app.modules.auth.models import Organizacion, Finca, UsuarioFincaRol
    from app.modules.cattle.models import Animal, Lote
    from app.modules.sanidad.models import Sanidad
    from app.modules.reproduccion.models import Reproduccion
    from app.modules.produccion.models import ProduccionLeche
    from app.modules.inventario.models import InventarioInsumo

    db = SessionLocal()
    try:
        users = db.query(Usuario).all()
        print(f"Total usuarios en DB: {len(users)}")
        for u in users:
            match = verificar_password("admin123", u.password_hash) if u.email == "admin@gavac.test" else False
            print(f"- {u.email} (Rol Org: {u.rol_organizacion}) | Password 'admin123' match: {match}")
    finally:
        db.close()

if __name__ == "__main__":
    check()
