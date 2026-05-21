from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Consulta:

    id_cita_fk: int
    motivo_consulta: str
    diagnostico: str
    tratamiento: str

    id_consulta: Optional[int] = None
    fecha_creacion: Optional[datetime] = None