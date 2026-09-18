
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, func
from app.database import Base

class Reproduccion(Base):
    __tablename__ = "reproduccion"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animales.id", ondelete="CASCADE"))
    tipo = Column(String(50), nullable=False) # Monta, Inseminación, Parto
    fecha_evento = Column(Date, nullable=False)
    estado = Column(String(50), default="En proceso") # Confirmada, En proceso, Completada, Fallida
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
