from pydantic import BaseModel
from typing import Optional
from datetime import date


class PacienteCrearRequest(BaseModel):
    numero_identificacion: str
    nombre: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    direccion: Optional[str] = None
    fecha_de_nacimiento: date
    id_eps_fk: int
    id_regimen_fk: int
    sexo: Optional[str] = None
    tipo_sangre: Optional[str] = None


class PacienteResponse(BaseModel):
    id_paciente: int
    numero_identificacion: str
    nombre: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    direccion: Optional[str] = None
    fecha_de_nacimiento: date
    id_eps_fk: int
    id_regimen_fk: int
    sexo: Optional[str] = None
    tipo_sangre: Optional[str] = None