from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Medico:
    id_medico: Optional[int]
    nombre: str
    primer_apellido: str
    segundo_apellido: Optional[str]
    tarjeta_profesional: str
    estado: str
    especialidades: list = field(default_factory=list)
    contactos: list = field(default_factory=list)