from pydantic import BaseModel
from typing import List


class ConsultaCrearRequest(BaseModel):
    id_cita_fk: int
    id_historia_clinica_fk: int
    diagnostico: str
    observacion: str
    servicios_ids: List[int]

class ConsultaResponse(BaseModel):
    id_consulta: int
    fecha: str
    diagnostico: str
    observacion: str
    servicios: List[str]