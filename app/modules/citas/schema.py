from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class CitaCrearRequest(BaseModel):
    fecha: date
    hora: time
    observacion: Optional[str] = None
    id_horario_medico_fk: int
    id_paciente_fk: int


class CitaResponse(BaseModel):
    id_cita: int
    fecha: date
    hora: time
    estado: str
    observacion: Optional[str] = None
    id_horario_medico_fk: int
    id_paciente_fk: int
    paciente_nombre: Optional[str] = None
    paciente_apellido: Optional[str] = None
    medico_nombre: Optional[str] = None
    medico_apellido: Optional[str] = None
    especialidad: Optional[str] = None

class CitaCancelarRequest(BaseModel):
    motivo: str

class CitaActualizarRequest(BaseModel):
    fecha: Optional[str] = None
    hora: Optional[str] = None
    observacion: Optional[str] = None