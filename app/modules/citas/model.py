from dataclasses import dataclass
from typing import Optional
from datetime import date, time, datetime


@dataclass
class Cita:

    fecha: date
    hora: time
    id_horario_medico_fk: int
    id_paciente_fk: int

    id_cita: Optional[int] = None
    estado: str = "Agendada"
    observacion: Optional[str] = None
    fecha_creacion: Optional[datetime] = None