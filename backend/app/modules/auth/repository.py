from sqlalchemy.orm import Session

from . import models


def get_usuario_by_email(db: Session, email: str) -> models.Usuario | None:
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def get_usuario_by_id(db: Session, usuario_id: int) -> models.Usuario | None:
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()


def get_logs_auditoria(db: Session, limit: int = 100):
    return db.query(models.AuditoriaLog).order_by(models.AuditoriaLog.created_at.desc()).limit(limit).all()


def crear_usuario(
    db: Session, email: str, password_hash: str, organizacion_id: int, rol_organizacion: str = "operario"
) -> models.Usuario:
    db_usuario = models.Usuario(
        email=email,
        password_hash=password_hash,
        organizacion_id=organizacion_id,
        rol_organizacion=rol_organizacion
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario