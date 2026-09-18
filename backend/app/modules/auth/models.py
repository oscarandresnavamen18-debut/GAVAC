import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Table, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class RolEnum(str, enum.Enum):
    admin = "admin"
    ganadero = "ganadero"
    veterinario = "veterinario"
    mayordomo = "mayordomo"
    operario = "operario"

class Organizacion(Base):
    __tablename__ = "organizaciones"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    nit = Column(String, unique=True, nullable=True)
    plan_contratado = Column(String, default="basic")
    estado = Column(String, default="activa")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    usuarios = relationship("Usuario", back_populates="organizacion")
    fincas = relationship("Finca", back_populates="organizacion")
    logs = relationship("AuditoriaLog", back_populates="organizacion")

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rol_organizacion = Column(Enum(RolEnum, native_enum=False), default=RolEnum.operario)
    organizacion_id = Column(Integer, ForeignKey("organizaciones.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organizacion = relationship("Organizacion", back_populates="usuarios")
    finca_roles = relationship("UsuarioFincaRol", back_populates="usuario")
    logs = relationship("AuditoriaLog", back_populates="usuario")

    @property
    def fincas_autorizadas(self):
        return [
            {"id": fr.finca_id, "nombre": fr.finca.nombre, "rol": fr.rol}
            for fr in self.finca_roles
        ]

class Finca(Base):
    __tablename__ = "fincas"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ubicacion = Column(String, nullable=True)
    area_hectareas = Column(Numeric(10, 2), nullable=True)
    estado = Column(String, default="Activa")
    organizacion_id = Column(Integer, ForeignKey("organizaciones.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organizacion = relationship("Organizacion", back_populates="fincas")
    usuarios_roles = relationship("UsuarioFincaRol", back_populates="finca")

    # Relaciones con otros módulos
    animales = relationship("Animal", back_populates="finca")
    lotes = relationship("Lote", back_populates="finca")
    insumos = relationship("InventarioInsumo", back_populates="finca")

class UsuarioFincaRol(Base):
    __tablename__ = "usuario_finca_roles"
    __table_args__ = {'extend_existing': True}

    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    finca_id = Column(Integer, ForeignKey("fincas.id", ondelete="CASCADE"), primary_key=True)
    rol = Column(Enum(RolEnum, native_enum=False), nullable=False)

    usuario = relationship("Usuario", back_populates="finca_roles")
    finca = relationship("Finca", back_populates="usuarios_roles")

class AuditoriaLog(Base):
    __tablename__ = "logs_auditoria"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    organizacion_id = Column(Integer, ForeignKey("organizaciones.id", ondelete="SET NULL"), nullable=True)
    email = Column(String, nullable=True)
    accion = Column(String, nullable=False)
    detalles = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="logs")
    organizacion = relationship("Organizacion", back_populates="logs")
