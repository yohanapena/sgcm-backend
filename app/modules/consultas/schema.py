from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ConsultaCrearRequest(BaseModel):

    id_cita_fk: int
    motivo_consulta: str
    diagnostico: str
    tratamiento: str
    servicios: List[int] = []


class ConsultaResponse(BaseModel):

    id_consulta: int
    id_cita_fk: int
    motivo_consulta: str
    diagnostico: str
    tratamiento: str
    fecha_creacion: Optional[datetime]