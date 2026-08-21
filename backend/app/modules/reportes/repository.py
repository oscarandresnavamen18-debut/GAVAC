from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.cattle.models import Animal

class ReportRepository:
    def get_ganado_resumen(self, db: Session):
<<<<<<< HEAD
=======
        """
        Obtiene un resumen del conteo de animales por sexo y estado.
        """
>>>>>>> 2d2f93dc9d18a1cad29ff38af36862b7544d0f7b
        return db.query(
            Animal.sex,
            Animal.status,
            func.count(Animal.id).label("total")
        ).group_by(Animal.sex, Animal.status).all()

<<<<<<< HEAD
    def get_animales_recientes(self, db: Session, limit = 5):
=======
    def get_animales_recientes(self, db: Session, limit: int = 5):
        """
        Obtiene los últimos animales registrados.
        """
>>>>>>> 2d2f93dc9d18a1cad29ff38af36862b7544d0f7b
        return db.query(Animal).order_by(Animal.created_at.desc()).limit(limit).all()
