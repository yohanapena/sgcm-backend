from pydantic import BaseModel
from typing import Optional, Literal
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
    
# Este esquema se puede usar para actualizar los datos del paciente, permitiendo que todos los campos sean opcionales

class PacienteActualizarRequest(BaseModel):
    nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    direccion: Optional[str] = None
    fecha_de_nacimiento: Optional[date] = None
    id_eps_fk: Optional[int] = None
    id_regimen_fk: Optional[int] = None
    sexo: Optional[Literal['M', 'F']] = None
    tipo_sangre: Optional[Literal['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']] = None