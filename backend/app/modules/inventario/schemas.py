
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class InventarioBase(BaseModel):
    nombre: str
    categoria: str
    cantidad: Decimal
    unidad: str
    finca_id: Optional[int] = None
    estado: Optional[str] = "Disponible"

class InventarioCreate(InventarioBase):
    pass

class InventarioOut(InventarioBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
