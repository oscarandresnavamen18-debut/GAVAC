
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import repository as repo
from .schemas import ProduccionCreate
from .models import ProduccionLeche
from app.modules.cattle.models import Animal

def list_produccion(db: Session, finca_id: int, animal_id: int = None):
    if animal_id:
        animal = db.query(Animal).filter(Animal.id == animal_id, Animal.finca_id == finca_id).first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal no encontrado en esta finca")

    query = db.query(ProduccionLeche).join(Animal).filter(Animal.finca_id == finca_id)
    if animal_id:
        query = query.filter(ProduccionLeche.animal_id == animal_id)

    return query.all()

def create_produccion(db: Session, data: ProduccionCreate, finca_id: int):
    # Buscar animal por TAG y Finca
    animal = db.query(Animal).filter(Animal.tag == data.animal_tag, Animal.finca_id == finca_id).first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el animal '{data.animal_tag}' en la finca actual."
        )

    prod_data = data.model_dump(exclude={"animal_tag"})
    db_item = ProduccionLeche(**prod_data, animal_id=animal.id)
    return repo.create(db, db_item)
