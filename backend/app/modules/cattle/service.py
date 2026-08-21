"""
Service: lógica de negocio del módulo de ganado.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.cattle import repository as repo
from app.modules.cattle.schemas import AnimalCreate, AnimalUpdate
from app.modules.auth.audit_service import registrar_accion


def list_animals(db: Session, breed=None, sex=None, status_=None, tag=None):
    return repo.find_all(db, breed=breed, sex=sex, status=status_, tag=tag)


def get_animal(db: Session, animal_id: int):
    animal = repo.find_by_id(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"No existe un animal con id {animal_id}.")
    return animal


def register_animal(db: Session, data: AnimalCreate, usuario, ip_address: str):
    if repo.find_by_tag(db, data.tag):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                             detail=f"Ya existe un animal registrado con el tag '{data.tag}'.")
    
    animal = repo.create(db, data)
    
    # Auditoría Profesional
    registrar_accion(
        db,
        accion="REGISTRO_ANIMAL",
        usuario_id=usuario.id,
        email=usuario.email,
        detalles=f"Registró animal con TAG: {data.tag}",
        ip=ip_address
    )
    
    return animal


def update_animal(db: Session, animal_id: int, data: AnimalUpdate, usuario, ip_address: str):
    animal = get_animal(db, animal_id)
    if data.tag:
        existente = repo.find_by_tag(db, data.tag)
        if existente and existente.id != animal_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                 detail=f"Ya existe otro animal con el tag '{data.tag}'.")
    
    resultado = repo.update(db, animal, data)
    
    registrar_accion(
        db,
        accion="ACTUALIZACION_ANIMAL",
        usuario_id=usuario.id,
        email=usuario.email,
        detalles=f"Actualizó datos del animal ID: {animal_id}",
        ip=ip_address
    )
    
    return resultado


def delete_animal(db: Session, animal_id: int, usuario, ip_address: str):
    animal = get_animal(db, animal_id)
    tag_eliminado = animal.tag
    repo.remove(db, animal)
    
    registrar_accion(
        db,
        accion="ELIMINACION_ANIMAL",
        usuario_id=usuario.id,
        email=usuario.email,
        detalles=f"Eliminó animal con TAG: {tag_eliminado}",
        ip=ip_address
    )
