from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.modules.auth.service import get_usuario_actual
from .service import ReportService
from .schemas import ReporteGeneralOut

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
