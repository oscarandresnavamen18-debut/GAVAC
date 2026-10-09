from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.auth_models import RolEnum


class EmpleadoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    rol: RolEnum
    finca_id: int | None = None
    created_at: datetime
