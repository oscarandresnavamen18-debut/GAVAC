
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.sanidad import repository as repo
from app.modules.sanidad.schemas import SanidadCreate
from app.modules.cattle import repository as cattle_repo
from app.modules.sanidad.models import Sanidad
from app.modules.cattle.models import Animal

def list_sanidad(db: Session, finca_id: int, animal_id: int = None):
    # Si viene animal_id, validar que sea de la finca
    if animal_id:
        animal = db.query(Animal).filter(Animal.id == animal_id, Animal.finca_id == finca_id).first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal no encontrado en esta finca")

    # Filtrar sanidad uniendo con animales para asegurar el contexto de finca
    query = db.query(Sanidad).join(Animal).filter(Animal.finca_id == finca_id)
    if animal_id:
        query = query.filter(Sanidad.animal_id == animal_id)

    return query.all()

def create_sanidad(db: Session, data: SanidadCreate, finca_id: int):
    # Buscar animal por TAG y Finca
    animal = db.query(Animal).filter(Animal.tag == data.animal_tag, Animal.finca_id == finca_id).first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el animal '{data.animal_tag}' en la finca actual."
        )

    # Crear el registro vinculado al ID del animal
    sanidad_data = data.model_dump(exclude={"animal_tag"})
    sanidad_data["animal_id"] = animal.id

    db_item = Sanidad(**sanidad_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
