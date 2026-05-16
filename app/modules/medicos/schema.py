from pydantic import BaseModel
from typing import List, Optional


class MedicoCrearRequest(BaseModel):
    nombre: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    tarjeta_profesional: str
    especialidades: List[int]


class MedicoResponse(BaseModel):
    id_medico: int
    nombre: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    tarjeta_profesional: str
    estado: str