
from sqlalchemy.orm import Session
import app.repositories.inventario_repository as repo
from app.schemas.inventario_schemas import InventarioCreate

def list_inventario(db: Session, finca_id: int, categoria: str = None):
    return repo.find_all(db, finca_id=finca_id, categoria=categoria)

def create_inventario(db: Session, data: InventarioCreate, finca_id: int):
    return repo.create(db, data, finca_id=finca_id)
