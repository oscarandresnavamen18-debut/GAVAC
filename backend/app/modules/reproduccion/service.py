
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.reproduccion import repository as repo
from app.modules.reproduccion.schemas import ReproduccionCreate
from app.modules.cattle.models import Animal
from app.modules.reproduccion.models import Reproduccion

def list_reproduccion(db: Session, finca_id: int, animal_id: int = None):
    # Validar acceso al animal si se proporciona
    if animal_id:
        animal = db.query(Animal).filter(Animal.id == animal_id, Animal.finca_id == finca_id).first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal no encontrado en esta finca")

    query = db.query(Reproduccion).join(Animal).filter(Animal.finca_id == finca_id)
    if animal_id:
        query = query.filter(Reproduccion.animal_id == animal_id)

    return query.all()

def create_reproduccion(db: Session, data: ReproduccionCreate, finca_id: int):
    # Buscar animal por TAG y Finca
    animal = db.query(Animal).filter(Animal.tag == data.animal_tag, Animal.finca_id == finca_id).first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el animal '{data.animal_tag}' en la finca actual."
        )

    # Crear el registro vinculado al ID del animal
    repro_data = data.model_dump(exclude={"animal_tag"})
    repro_data["animal_id"] = animal.id

    db_item = Reproduccion(**repro_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
