
from sqlalchemy.orm import Session
from app.modules.inventario.models import InventarioInsumo
from app.modules.inventario.schemas import InventarioCreate

def find_all(db: Session, finca_id: int, categoria: str = None):
    query = db.query(InventarioInsumo).filter(InventarioInsumo.finca_id == finca_id)
    if categoria:
        query = query.filter(InventarioInsumo.categoria == categoria)
    return query.all()

def create(db: Session, data: InventarioCreate, finca_id: int):
    db_item = InventarioInsumo(**data.model_dump(), finca_id=finca_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
