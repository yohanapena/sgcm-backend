from pydantic import BaseModel
from typing import Optional, Literal, List
from datetime import date


class ContactoResponse(BaseModel):
    id_contacto: Optional[int] = None
    tipo: Optional[str] = None
    dato_contacto: str


class ContactoCrearRequest(BaseModel):
    tipo: Optional[str] = None
    dato_contacto: str


class PacienteCrearRequest(BaseModel):
    numero_identificacion: str
    nombre: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    direccion: Optional[str] = None
    fecha_de_nacimiento: date
    id_eps_fk: int
    id_regimen_fk: int
    sexo: Optional[Literal['M', 'F']] = None
    tipo_sangre: Optional[Literal['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']] = None
    contactos: list[ContactoCrearRequest] = []
    alergias: list[str] = []
    


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
    alergias: Optional[list[str]] = None


class AlergiasActualizarRequest(BaseModel):
    alergias: list[str]


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
    contactos: List[ContactoResponse] = []
    alergias: List[str] = []