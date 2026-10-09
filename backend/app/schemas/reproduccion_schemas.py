
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ReproduccionBase(BaseModel):
    tipo: str
    fecha_evento: date
    estado: Optional[str] = "En proceso"
    observaciones: Optional[str] = None

class ReproduccionCreate(ReproduccionBase):
    animal_tag: str

class ReproduccionOut(ReproduccionBase):
    id: int
    animal_id: int
    created_at: datetime

    class Config:
        from_attributes = True
