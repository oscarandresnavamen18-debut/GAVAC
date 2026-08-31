import logging
from typing import Optional
from sqlalchemy.orm import Session
from .models import AuditoriaLog

# El logger estándar de Python siempre está disponible
logger = logging.getLogger(__name__)

def registrar_accion(
    db: Session, 
    accion: str, 
    usuario_id: Optional[int] = None, 
    email: Optional[str] = None, 
    detalles: Optional[str] = None, 
    ip: Optional[str] = None
):
    try:
        log = AuditoriaLog(
            usuario_id=usuario_id,
            email=email,
            accion=accion,
            detalles=detalles,
            ip_address=ip
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except Exception as e:
        db.rollback()
        # Usamos print como respaldo si el logger falla
        print(f"FALLO CRÍTICO AUDITORÍA: {str(e)}")
        return None

def get_audit_logs(db: Session, limit: int = 100):
    return db.query(AuditoriaLog).order_by(AuditoriaLog.created_at.desc()).limit(limit).all()

