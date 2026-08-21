
from typing import Optional, List
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.cattle.schemas import AnimalCreate, AnimalUpdate, AnimalOut
from app.modules.cattle import service
from app.modules.auth.service import get_usuario_actual

router = APIRouter(prefix="/api/ganado", tags=["Ganado"])


@router.get("/", response_model=List[AnimalOut])
def listar_animales(
    breed: Optional[str] = None,
    sex: Optional[str] = None,
    status_: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual) # Protegido por JWT
):
    return service.list_animals(db, breed=breed, sex=sex, status_=status_, tag=tag)


@router.get("/{animal_id}", response_model=AnimalOut)
def obtener_animal(
    animal_id: int, 
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual)
):
    return service.get_animal(db, animal_id)


@router.post("/", response_model=AnimalOut, status_code=status.HTTP_201_CREATED)
def registrar_animal(
    data: AnimalCreate, 
    request: Request,
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual) # Solo usuarios autenticados
):
    return service.register_animal(db, data, usuario_actual, request.client.host)


@router.put("/{animal_id}", response_model=AnimalOut)
def actualizar_animal(
    animal_id: int, 
    data: AnimalUpdate, 
    request: Request,
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual)
):
    return service.update_animal(db, animal_id, data, usuario_actual, request.client.host)


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_animal(
    animal_id: int, 
    request: Request,
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual) # Auditoría de eliminación
):
    service.delete_animal(db, animal_id, usuario_actual, request.client.host)
