from pydantic import BaseModel
from typing import Optional

class ServicioResponse(BaseModel):
    id_servicio: int
    nombre: str
    descripcion: Optional[str] = None