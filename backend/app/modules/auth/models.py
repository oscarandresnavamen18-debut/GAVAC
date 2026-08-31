"""
Modelo SQLAlchemy: tabla de usuarios.

IMPORTANTE: este archivo importa `Base` desde app.database.
Si en tu database.py la clase base tiene otro nombre, ajusta el import.
"""

import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum, Date
from sqlalchemy.sql import func

from app.database import Base


class RolEnum(str, enum.Enum):
    admin = "admin"
    ganadero = "ganadero"
    veterinario = "veterinario"
    mayordomo = "mayordomo"
    operario = "operario"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rol = Column(Enum(RolEnum, native_enum=False), default=RolEnum.operario, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación con Finca (si es mayordomo o dueño)
    finca_id = Column(Integer, nullable=True)

class Finca(Base):
    __tablename__ = "fincas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ubicacion = Column(String, nullable=True)
    area_hectareas = Column(Integer, nullable=True)
    dueno_id = Column(Integer, nullable=True) # ID del Ganadero
    mayordomo_id = Column(Integer, nullable=True) # ID del Mayordomo
    estado = Column(String, default="PRODUCIENDO") # PRODUCIENDO, ENGORDE, PAUSA
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProduccionLeche(Base):
    __tablename__ = "produccion_leche"
    id = Column(Integer, primary_key=True, index=True)
    finca_id = Column(Integer, nullable=False)
    litros = Column(Integer, nullable=False)
    fecha = Column(Date, server_default=func.current_date())

class TareaFinca(Base):
    __tablename__ = "tareas_finca"
    id = Column(Integer, primary_key=True, index=True)
    finca_id = Column(Integer, nullable=False)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    categoria = Column(String, nullable=True) # ORDEÑO, VACUNACION, PESAJE
    estado = Column(String, default="PENDIENTE")


class AuditoriaLog(Base):
    __tablename__ = "logs_auditoria"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=True)
    email = Column(String, nullable=True)
    accion = Column(String, nullable=False)
    detalles = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
