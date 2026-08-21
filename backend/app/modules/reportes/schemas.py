from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ResumenItem(BaseModel):
    sexo: Optional[str]
    estado: str
    cantidad: int

class ReporteGeneralOut(BaseModel):
    fecha_generacion: datetime
    resumen: List[ResumenItem]
