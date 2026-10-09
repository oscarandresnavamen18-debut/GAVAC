from typing import List, Optional, Tuple
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.sanidad_schemas import SanidadCreate, SanidadOut
import app.services.sanidad_service as service
from app.services.auth_service import requerir_rol

router = APIRouter(prefix="/api/sanidad", tags=["Sanidad"])

@router.get("/", response_model=List[SanidadOut])
def listar_sanidad(
    animal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    finca_context: Tuple[int, str] = Depends(requerir_rol("admin", "ganadero", "veterinario", "operario"))
):
    finca_id, rol = finca_context
    return service.list_sanidad(db, finca_id=finca_id, animal_id=animal_id)

@router.post("/", response_model=SanidadOut, status_code=status.HTTP_201_CREATED)
def registrar_sanidad(
    data: SanidadCreate,
    db: Session = Depends(get_db),
    finca_context: Tuple[int, str] = Depends(requerir_rol("admin", "ganadero", "veterinario"))
):
    finca_id, rol = finca_context
    return service.create_sanidad(db, data, finca_id=finca_id)
