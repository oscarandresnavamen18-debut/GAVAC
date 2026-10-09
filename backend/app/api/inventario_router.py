from typing import List, Optional, Tuple
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.inventario_schemas import InventarioCreate, InventarioOut
import app.services.inventario_service as service
from app.services.auth_service import requerir_rol

router = APIRouter(prefix="/api/inventario", tags=["Inventario"])

@router.get("/", response_model=List[InventarioOut])
def listar_inventario(
    categoria: Optional[str] = None,
    db: Session = Depends(get_db),
    finca_context: Tuple[int, str] = Depends(requerir_rol("admin", "ganadero", "mayordomo", "operario"))
):
    finca_id, rol = finca_context
    return service.list_inventario(db, finca_id=finca_id, categoria=categoria)

@router.post("/", response_model=InventarioOut, status_code=status.HTTP_201_CREATED)
def registrar_inventario(
    data: InventarioCreate,
    db: Session = Depends(get_db),
    finca_context: Tuple[int, str] = Depends(requerir_rol("admin", "ganadero", "mayordomo"))
):
    finca_id, rol = finca_context
    return service.create_inventario(db, data, finca_id=finca_id)
