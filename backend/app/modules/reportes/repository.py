from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.cattle.models import Animal

class ReportRepository:
    def get_ganado_resumen(self, db: Session):
        return db.query(
            Animal.sex,
            Animal.status,
            func.count(Animal.id).label("total")
        ).group_by(Animal.sex, Animal.status).all()

    def get_animales_recientes(self, db: Session, limit = 5):
        return db.query(Animal).order_by(Animal.created_at.desc()).limit(limit).all()
