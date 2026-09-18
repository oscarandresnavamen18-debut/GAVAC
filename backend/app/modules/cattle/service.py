"""
Service: lógica de negocio del módulo de ganado.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .models import Animal, TrasladoAnimal
from .schemas import AnimalCreate, AnimalUpdate, TrasladoCreate
from . import repository as repo
from app.modules.auth.audit_service import registrar_accion

def move_animal(db: Session, data: TrasladoCreate, usuario, ip_address: str):
    animal = repo.find_by_tag(db, data.animal_tag)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")

    # Registrar el traslado
    traslado = TrasladoAnimal(
        animal_id=animal.id,
        origen_finca_id=animal.finca_id,
        destino_finca_id=data.destino_finca_id or animal.finca_id,
        origen_lote=animal.lote,
        destino_lote=data.destino_lote or animal.lote,
        motivo=data.motivo,
        usuario_responsable_id=usuario.id
    )

    # Actualizar animal
    if data.destino_finca_id:
        animal.finca_id = data.destino_finca_id
    if data.destino_lote:
        animal.lote = data.destino_lote

    db.add(traslado)
    db.commit()
    db.refresh(animal)

    registrar_accion(db, "TRASLADO_ANIMAL", usuario.id, usuario.email, f"Movió animal {animal.tag} a finca {animal.finca_id}", ip_address)
    return animal


def list_animals(db: Session, breed=None, sex=None, status_=None, tag=None, usuario=None, ip_address: str = None):
    if usuario:
        registrar_accion(
            db,
            accion="LISTADO_GANADO",
            usuario_id=usuario.id,
            email=usuario.email,
            detalles="Consultó lista completa de animales",
            ip=ip_address
        )
    return repo.find_all(db, raza=breed, sexo=sex, status=status_, tag=tag)


def get_animal(db: Session, animal_id: int, usuario=None, ip_address: str = None):
    animal = repo.find_by_id(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"No existe un animal con id {animal_id}.")
    
    if usuario:
        registrar_accion(
            db,
            accion="CONSULTA_ANIMAL",
            usuario_id=usuario.id,
            email=usuario.email,
            detalles=f"Consultó detalle del animal ID: {animal_id}",
            ip=ip_address
        )
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
