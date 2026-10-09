
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class SanidadBase(BaseModel):
    tipo: str
    producto: str
    dosis: Optional[str] = None
    fecha_aplicacion: Optional[date] = None
    proxima_fecha: Optional[date] = None
    estado: Optional[str] = "Completada"

class SanidadCreate(SanidadBase):
    animal_tag: str

class SanidadOut(SanidadBase):
    id: int
    animal_id: int
    created_at: datetime

    class Config:
        from_attributes = True
