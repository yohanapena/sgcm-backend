from dataclasses import dataclass
from typing import Optional


@dataclass
class SignosVitales:

    peso: float
    estatura: float
    temperatura: float
    presion_arterial: str
    frecuencia_cardiaca: int
    saturacion_oxigeno: int
    id_historia_clinica_fk: int
    id_consulta_fk: Optional[int] = None