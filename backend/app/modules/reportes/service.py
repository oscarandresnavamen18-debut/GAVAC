from sqlalchemy.orm import Session
from .repository import ReportRepository
from app.modules.auth.audit_service import registrar_accion

class ReportService:
    def __init__(self):
        self._repo = ReportRepository()

    def generar_resumen_inventario(self, db: Session, usuario):
        # Auditoría: Registrar que el usuario consultó el reporte
        registrar_accion(
            db, 
            accion="CONSULTA_REPORTE", 
            usuario_id=usuario.id, 
            email=usuario.email,
            detalles="Resumen de inventario de ganado"
        )
        
        datos = self._repo.get_ganado_resumen(db)
        # Transformar a formato legible
        return [{"sexo": d.sex, "estado": d.status, "cantidad": d.total} for d in datos]

    def listar_animales_nuevos(self, db: Session, usuario):
        registrar_accion(
            db, 
            accion="CONSULTA_REPORTE", 
            usuario_id=usuario.id, 
            email=usuario.email,
            detalles="Listado de animales recientes"
        )
        return self._repo.get_animales_recientes(db)
