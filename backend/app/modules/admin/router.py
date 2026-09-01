from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.modules.auth.service import get_usuario_actual
from app.modules.auth.audit_service import get_audit_logs
from app.modules.auth.models import Finca, ProduccionLeche, TareaFinca, Usuario
from app.modules.cattle.models import Animal

router = APIRouter(prefix="/api/admin", tags=["Administración"])

@router.get("/dashboard-stats")
def obtener_metricas_dashboard(
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual)
):
    if usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="Permisos insuficientes")

    total_ganado = db.query(Animal).count()
    total_fincas = db.query(Finca).count()
    leche_hoy = db.query(func.sum(ProduccionLeche.litros)).filter(ProduccionLeche.fecha == func.current_date()).scalar() or 0
    
    return {
        "ganado_total": total_ganado,
        "leche_hoy_lts": leche_hoy,
        "fincas_activas": total_fincas,
        "alertas_salud": 2 # Simulado por ahora
    }

@router.get("/board-data")
def obtener_tablero_control(
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual)
):
    if usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="Permisos insuficientes")

    fincas = db.query(Finca).all()
    resultado = []
    for finca in fincas:
        tareas = db.query(TareaFinca).filter(TareaFinca.finca_id == finca.id).all()
        resultado.append({
            "id": finca.id,
            "nombre": finca.nombre,
            "estado": finca.estado,
            "tareas": tareas
        })
    return resultado

@router.get("/audit")
def obtener_logs_auditoria(
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual)
):
    """
    Solo el administrador puede ver los logs de auditoría de todo el sistema.
    """
    if usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado: Se requieren permisos de administrador")
    
    return get_audit_logs(db)

@router.get("/stats")
def obtener_estadisticas_sistema(
    db: Session = Depends(get_db),
    usuario_actual = Depends(get_usuario_actual)
):
    if usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    # Aquí podrías sumar el total de animales, usuarios, etc.
    return {
        "total_usuarios": 5,
        "uptime": "99.9%",
        "version_db": "PostgreSQL 15"
    }
