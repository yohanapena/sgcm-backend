from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time
from typing import Optional

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
    
class HorarioCrearRequest(BaseModel):
    dia_semana: str
    fecha_vigencia_inicio: date
    fecha_vigencia_fin: Optional[date] = None
    hora_inicial: time
    hora_final: time


class HorarioResponse(BaseModel):
    id_horario_medico: int
    dia_semana: str
    fecha_vigencia_inicio: date
    fecha_vigencia_fin: Optional[date]
    hora_inicial: time
    hora_final: time
    id_medico_fk: int

from pydantic import BaseModel

class MedicoUpdate(BaseModel):
    nombre: str
    primer_apellido: str
    segundo_apellido: str
    tarjeta_profesional: str
    estado: str