from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.auth.service import get_usuario_actual
from app.modules.auth.audit_service import get_audit_logs

router = APIRouter(prefix="/api/admin", tags=["Administración"])

@router.get("/audit")
def obtener_logs_auditoria(
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual)
):
    """
    Solo el administrador puede ver los logs de auditoría de todo el sistema.
    """
    if not usuario_actual.is_admin:
        raise HTTPException(status_code=403, detail="Acceso denegado: Se requieren permisos de administrador")
    
    return get_audit_logs(db)

@router.get("/stats")
def obtener_estadisticas_sistema(
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual)
):
    if not usuario_actual.is_admin:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    # Aquí podrías sumar el total de animales, usuarios, etc.
    return {
        "total_usuarios": 5,
        "uptime": "99.9%",
        "version_db": "PostgreSQL 15"
    }
