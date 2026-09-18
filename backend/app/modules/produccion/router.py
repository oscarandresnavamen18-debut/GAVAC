from typing import List, Optional, Tuple
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from .schemas import ProduccionCreate, ProduccionOut
from . import service
from app.modules.auth.service import requerir_rol

router = APIRouter(prefix="/api/produccion", tags=["Produccion"])

@router.get("/", response_model=List[ProduccionOut])
def listar_produccion(
    animal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    finca_context: Tuple[int, str] = Depends(requerir_rol("admin", "ganadero", "mayordomo", "operario"))
):
    finca_id, rol = finca_context
    return service.list_produccion(db, finca_id=finca_id, animal_id=animal_id)

@router.post("/", response_model=ProduccionOut, status_code=status.HTTP_201_CREATED)
def registrar_produccion(
    data: ProduccionCreate,
    db: Session = Depends(get_db),
    finca_context: Tuple[int, str] = Depends(requerir_rol("admin", "ganadero", "mayordomo", "operario"))
):
    finca_id, rol = finca_context
    return service.create_produccion(db, data, finca_id=finca_id)
