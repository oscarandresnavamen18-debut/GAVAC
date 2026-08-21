from sqlalchemy.orm import Session
from .models import AuditoriaLog

def registrar_accion(db: Session, accion: str, usuario_id: int = None, email: str = None, detalles: str = None, ip: str = None):
    """
    Registra una acción en la tabla de auditoría para trazabilidad.
    """
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
