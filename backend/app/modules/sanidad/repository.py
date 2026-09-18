
from sqlalchemy.orm import Session
from app.modules.sanidad.models import Sanidad
from app.modules.sanidad.schemas import SanidadCreate

def find_all(db: Session, animal_id: int = None):
    query = db.query(Sanidad)
    if animal_id:
        query = query.filter(Sanidad.animal_id == animal_id)
    return query.all()

def create(db: Session, data: SanidadCreate):
    db_item = Sanidad(**data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
