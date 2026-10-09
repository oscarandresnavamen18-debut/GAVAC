
from sqlalchemy.orm import Session
from app.models.reproduccion_models import Reproduccion
from app.schemas.reproduccion_schemas import ReproduccionCreate

def find_all(db: Session, animal_id: int = None):
    query = db.query(Reproduccion)
    if animal_id:
        query = query.filter(Reproduccion.animal_id == animal_id)
    return query.all()

def create(db: Session, data: ReproduccionCreate):
    db_item = Reproduccion(**data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
