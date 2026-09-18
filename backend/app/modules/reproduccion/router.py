from typing import List, Optional, Tuple
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.reproduccion.schemas import ReproduccionCreate, ReproduccionOut
from app.modules.reproduccion import service
from app.modules.auth.service import requerir_rol

router = APIRouter(prefix="/api/reproduccion", tags=["Reproduccion"])

@router.get("/", response_model=List[ReproduccionOut])
def listar_reproduccion(
    animal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    finca_context: Tuple[int, str] = Depends(requerir_rol("admin", "ganadero", "veterinario", "operario"))
):
    finca_id, rol = finca_context
    return service.list_reproduccion(db, finca_id=finca_id, animal_id=animal_id)

@router.post("/", response_model=ReproduccionOut, status_code=status.HTTP_201_CREATED)
def registrar_reproduccion(
    data: ReproduccionCreate,
    db: Session = Depends(get_db),
    finca_context: Tuple[int, str] = Depends(requerir_rol("admin", "ganadero", "veterinario"))
):
    finca_id, rol = finca_context
    return service.create_reproduccion(db, data, finca_id=finca_id)
