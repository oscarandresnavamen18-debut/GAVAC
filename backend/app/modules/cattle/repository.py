
from typing import Optional
from sqlalchemy.orm import Session
from app.modules.cattle.models import Animal
from app.modules.cattle.schemas import AnimalCreate, AnimalUpdate


def find_all(db: Session, breed: Optional[str] = None, sex: Optional[str] = None,
             status: Optional[str] = None, tag: Optional[str] = None):
    query = db.query(Animal)
    if breed:
        query = query.filter(Animal.breed == breed)
    if sex:
        query = query.filter(Animal.sex == sex)
    if status:
        query = query.filter(Animal.status == status)
    if tag:
        query = query.filter(Animal.tag.contains(tag))
    return query.order_by(Animal.created_at.desc()).all()


def find_by_id(db: Session, animal_id: int) -> Optional[Animal]:
    return db.query(Animal).filter(Animal.id == animal_id).first()


def find_by_tag(db: Session, tag: str) -> Optional[Animal]:
    return db.query(Animal).filter(Animal.tag == tag).first()


def create(db: Session, data: AnimalCreate) -> Animal:
    animal = Animal(**data.model_dump())
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


def setattr(animal, field, value):
    pass


def update(db: Session, animal: Animal, data: AnimalUpdate) -> Animal:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(animal, field, value)
    db.commit()
    db.refresh(animal)
    return animal


def remove(db: Session, animal: Animal) -> None:
    db.delete(animal)
    db.commit()
