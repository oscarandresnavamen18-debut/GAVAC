from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import relationship
from app.database import Base

class Lote(Base):
    __tablename__ = "lotes"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    finca_id = Column(Integer, ForeignKey("fincas.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    area_hectareas = Column(Numeric(10, 2), nullable=True)
    descripcion = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    finca = relationship("Finca", back_populates="lotes")
    animales = relationship("Animal", back_populates="lote")

class Animal(Base):
    __tablename__ = "animales"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=True)
    especie = Column(String(50), default="Bovino")
    raza = Column(String(50), nullable=True)
    sexo = Column(String(10), nullable=True)
    peso_actual = Column(Numeric(10, 2), nullable=True)
    edad_meses = Column(Integer, nullable=True)
    finca_id = Column(Integer, ForeignKey("fincas.id", ondelete="SET NULL"), nullable=True)
    lote_id = Column(Integer, ForeignKey("lotes.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    finca = relationship("Finca", back_populates="animales")
    lote = relationship("Lote", back_populates="animales")

class TrasladoAnimal(Base):
    __tablename__ = "traslados_animales"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animales.id", ondelete="CASCADE"), nullable=False)
    origen_finca_id = Column(Integer, ForeignKey("fincas.id"), nullable=True)
    destino_finca_id = Column(Integer, ForeignKey("fincas.id"), nullable=True)
    origen_lote_id = Column(Integer, ForeignKey("lotes.id"), nullable=True)
    destino_lote_id = Column(Integer, ForeignKey("lotes.id"), nullable=True)
    motivo = Column(String, nullable=True)
    usuario_responsable_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_traslado = Column(DateTime, server_default=func.now())
