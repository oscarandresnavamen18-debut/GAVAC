
from sqlalchemy.orm import Session
from .models import ProduccionLeche

def find_all(db: Session, animal_id: int = None):
    query = db.query(ProduccionLeche)
    if animal_id:
        query = query.filter(ProduccionLeche.animal_id == animal_id)
    return query.order_by(ProduccionLeche.created_at.desc()).all()

def create(db: Session, db_item: ProduccionLeche):
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
