from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Paciente:
    numero_identificacion: str
    nombre: str
    primer_apellido: str
    fecha_de_nacimiento: date
    id_eps_fk: int
    id_regimen_fk: int
    segundo_apellido: Optional[str] = None
    direccion: Optional[str] = None
    sexo: Optional[str] = None
    tipo_sangre: Optional[str] = None
    id_paciente: Optional[int] = None