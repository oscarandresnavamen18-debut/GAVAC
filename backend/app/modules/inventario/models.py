
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class InventarioInsumo(Base):
    __tablename__ = "inventario_insumos"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    finca_id = Column(Integer, ForeignKey("fincas.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(255), nullable=False)
    categoria = Column(String(100), nullable=False) # Medicamento, Alimento, Suplemento
    cantidad = Column(Numeric(10, 2), nullable=False, default=0)
    unidad = Column(String(20), nullable=False) # Dosis, Kg, Litros
    estado = Column(String(20), default="Disponible") # Disponible, Bajo Stock, Agotado
    created_at = Column(DateTime, server_default=func.now())

    finca = relationship("Finca", back_populates="insumos")
