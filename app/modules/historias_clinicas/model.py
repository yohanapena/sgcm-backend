from dataclasses import dataclass, field
from typing import Optional
from datetime import date


@dataclass
class HistoriaClinica:
    id_paciente_fk: int
    id_historia_clinica: Optional[int] = None
    resumen: Optional[str] = None
    fecha_apertura: Optional[date] = None
    antecedentes_personales: Optional[str] = None
    antecedentes_familiares: Optional[str] = None