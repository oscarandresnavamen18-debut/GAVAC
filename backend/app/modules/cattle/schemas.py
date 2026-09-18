
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
<<<<<<< HEAD
    tag: str = Field(..., min_length=1, max_length=50)
=======
    """Datos requeridos para registrar un animal nuevo."""
    tag: str = Field(
        ...,
        pattern=r"^[A-Za-z]{2,10}-[0-9]{1,6}$",
        description="Identificador único con formato letras-números, por ejemplo GAV-001",
    )
>>>>>>> a583192508a8de8f5f8a80617669f41a01d080f0
    status: Estado = "active"

class AnimalUpdate(AnimalBase):
<<<<<<< HEAD
    tag: Optional[str] = Field(default=None, min_length=1, max_length=50)
=======
    """Todos los campos son opcionales al actualizar."""
    tag: Optional[str] = Field(
        default=None,
        pattern=r"^[A-Za-z]{2,10}-[0-9]{1,6}$",
        description="Identificador con formato letras-números, por ejemplo GAV-001",
    )
>>>>>>> a583192508a8de8f5f8a80617669f41a01d080f0
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
