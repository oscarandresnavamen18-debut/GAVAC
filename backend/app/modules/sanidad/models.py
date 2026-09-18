
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from app.database import Base

class Sanidad(Base):
    __tablename__ = "sanidad"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animales.id", ondelete="CASCADE"))
    tipo = Column(String(50), nullable=False) # Vacuna, Tratamiento, Control
    producto = Column(String(100), nullable=False)
    dosis = Column(String(50), nullable=True)
    fecha_aplicacion = Column(Date, server_default=func.current_date())
    proxima_fecha = Column(Date, nullable=True)
    estado = Column(String(20), default="Completada") # Completada, Pendiente
    created_at = Column(DateTime, server_default=func.now())
