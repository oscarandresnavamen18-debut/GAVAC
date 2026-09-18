
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from decimal import Decimal

class ProduccionBase(BaseModel):
    litros: Decimal
    fecha: Optional[date] = None
    jornada: str

class ProduccionCreate(ProduccionBase):
    animal_tag: str

class ProduccionOut(ProduccionBase):
    id: int
    animal_id: int
    created_at: datetime

    class Config:
        from_attributes = True
