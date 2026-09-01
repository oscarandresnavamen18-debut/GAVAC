"""
Schemas de Pydantic: validan automáticamente los datos que entran y
definen qué datos salen en las respuestas. Esta es la gran ventaja de
FastAPI: si el cliente manda datos mal formados, FastAPI responde con
un error 422 claro sin que tengas que validar manualmente.
"""
from datetime import date, datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

Sexo = Literal["macho", "hembra"]
Estado = Literal["active", "inactive", "sold", "deceased"]


class AnimalBase(BaseModel):
    breed: Optional[str] = Field(default=None, max_length=50, description="Raza del animal")
    sex: Optional[Sexo] = Field(default=None, description="Sexo: macho o hembra")
    birth_date: Optional[date] = Field(default=None, description="Fecha de nacimiento")


class AnimalCreate(AnimalBase):
    """Datos requeridos para registrar un animal nuevo."""
    tag: str = Field(
        ...,
        pattern=r"^[A-Za-z]{2,10}-[0-9]{1,6}$",
        description="Identificador único con formato letras-números, por ejemplo GAV-001",
    )
    status: Estado = "active"


class AnimalUpdate(AnimalBase):
    """Todos los campos son opcionales al actualizar."""
    tag: Optional[str] = Field(
        default=None,
        pattern=r"^[A-Za-z]{2,10}-[0-9]{1,6}$",
        description="Identificador con formato letras-números, por ejemplo GAV-001",
    )
    status: Optional[Estado] = None


class AnimalOut(AnimalBase):
    """Lo que devolvemos al cliente."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    tag: str
    status: Estado
    created_at: datetime
    updated_at: datetime
