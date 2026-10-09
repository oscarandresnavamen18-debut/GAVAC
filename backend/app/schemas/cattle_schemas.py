
from datetime import date, datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

Sexo = Literal["macho", "hembra"]
Estado = Literal["active", "inactive", "sold", "deceased"]

class AnimalBase(BaseModel):
    nombre: Optional[str] = Field(default=None, max_length=100)
    especie: str = Field(default="Bovino", max_length=50)
    raza: Optional[str] = Field(default=None, max_length=50)
    sexo: Optional[Sexo] = Field(default=None)
    peso_actual: Optional[Decimal] = None
    edad_meses: Optional[int] = None
    lote: Optional[str] = Field(default=None, max_length=50)
    finca_id: Optional[int] = None

class AnimalCreate(AnimalBase):
    tag: str = Field(..., min_length=1, max_length=50)
    status: Estado = "active"

class AnimalUpdate(AnimalBase):
    tag: Optional[str] = Field(default=None, min_length=1, max_length=50)
    status: Optional[Estado] = None

class AnimalOut(AnimalBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tag: str
    status: Estado
    created_at: datetime
    updated_at: datetime

class TrasladoCreate(BaseModel):
    animal_tag: str
    destino_finca_id: Optional[int] = None
    destino_lote: Optional[str] = None
    motivo: Optional[str] = None
