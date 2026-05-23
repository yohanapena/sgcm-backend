from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Consulta:

    observacion: str
    diagnostico: str
    id_cita_fk: int
    id_historia_clinica_fk: int

    id_consulta: Optional[int] = None

    servicios: list = field(default_factory=list)