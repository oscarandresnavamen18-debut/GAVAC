from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.services.auth_service import get_usuario_actual
from app.services.reportes_service import ReportService
from app.schemas.reportes_schemas import ReporteGeneralOut
from app.schemas.cattle_schemas import AnimalOut

router = APIRouter(prefix="/api/reportes", tags=["Reportes y Consultas"])
_service = ReportService()

@router.get("/resumen", response_model=ReporteGeneralOut)
def obtener_resumen_ganado(
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual)
):
    """
    Endpoint protegido que genera un resumen del inventario actual.
    Registra automáticamente una entrada en la auditoría.
    """
    resumen = _service.generar_resumen_inventario(db, usuario_actual)
    return {
        "fecha_generacion": datetime.now(),
        "resumen": resumen
    }


@router.get("/recientes", response_model=List[AnimalOut])
def obtener_animales_recientes(
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual)
):
    """
    Obtiene los 5 animales más recientemente registrados.
    """
    return _service.listar_animales_nuevos(db, usuario_actual)
