"""
Schemas de Pydantic: validan lo que entra (requests) y dan forma a lo que sale (responses).
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from .models import RolEnum

class OrganizacionBase(BaseModel):
    nombre: str
    nit: Optional[str] = None
    plan_contratado: str = "basic"
    estado: str = "activa"

class OrganizacionOut(OrganizacionBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class FincaBreve(BaseModel):
    id: int
    nombre: str
    rol: RolEnum

class UsuarioBase(BaseModel):
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str
    organizacion_id: Optional[int] = None
    nombre_organizacion: Optional[str] = None # Para crear una nueva org al registrarse

class UsuarioLogin(BaseModel):
    email: str # Simplificado de EmailStr para depuración
    password: str

class UsuarioOut(UsuarioBase):
    id: int
    organizacion_id: int
    fincas_autorizadas: Optional[List[FincaBreve]] = []
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut

class AuditoriaLogOut(BaseModel):
    id: int
    organizacion_id: Optional[int] = None
    usuario_id: Optional[int] = None
    email: Optional[str] = None
    accion: str
    detalles: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- PROVISIÓN DESDE LANDING ---

class ProvisionRequest(BaseModel):
    email: EmailStr
    password: str
    nombre_organizacion: str
    nit: Optional[str] = None

class ProvisionResponse(BaseModel):
    status: str
    usuario_id: int
    organizacion_id: int
    finca_id: int
    mensaje: str
