from pydantic import BaseModel
from typing import Optional


class ServicioResponse(BaseModel):
    id_servicio: int
    nombre: str
    descripcion: Optional[str] = None


class EpsResponse(BaseModel):
    id_eps: int
    nit_eps: str
    nombre_eps: str


class RegimenResponse(BaseModel):
    id_regimen: int
    tipo_regimen: str


class EspecialidadResponse(BaseModel):
    id_especialidad: int
    nombre_especialidad: str
    descripcion: Optional[str] = None