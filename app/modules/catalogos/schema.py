from pydantic import BaseModel
from typing import Optional
from datetime import date, time

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


class HorarioResponse(BaseModel):
    id_horario_medico: int
    dia_semana: str
    fecha_vigencia_inicio: date
    fecha_vigencia_fin: Optional[date] = None
    hora_inicial: time
    hora_final: time
    id_medico_fk: int