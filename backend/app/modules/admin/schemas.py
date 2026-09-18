
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from app.modules.auth.models import RolEnum

class FincaBase(BaseModel):
    nombre: str
    ubicacion: Optional[str] = None
    area_hectareas: Optional[Decimal] = None
    estado: str = "Activa"

class FincaCreate(FincaBase):
    pass

class FincaOut(FincaBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class UsuarioFincaAssignment(BaseModel):
    usuario_id: int
    finca_id: int
    rol: RolEnum

class UsuarioCreateAdmin(BaseModel):
    email: EmailStr
    password: str
    rol: RolEnum = RolEnum.operario

class UsuarioUpdateAdmin(BaseModel):
    email: Optional[EmailStr] = None
    rol: Optional[RolEnum] = None
