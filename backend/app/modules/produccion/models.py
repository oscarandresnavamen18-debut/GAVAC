
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric, func
from app.database import Base

class ProduccionLeche(Base):
    __tablename__ = "produccion_leche"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animales.id", ondelete="CASCADE"), nullable=False)
    litros = Column(Numeric(10, 2), nullable=False)
    fecha = Column(Date, server_default=func.current_date())
    jornada = Column(String(20), nullable=False) # Mañana, Tarde
    created_at = Column(DateTime, server_default=func.now())
