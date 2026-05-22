from pydantic import BaseModel
from typing import List
from typing import List, Optional


class SignosVitalesConsulta(BaseModel):
    peso: float
    estatura: float
    temperatura: float
    presion_arterial: str
    frecuencia_cardiaca: int
    saturacion_oxigeno: int

class ConsultaCrearRequest(BaseModel):
    id_cita_fk: int
    id_historia_clinica_fk: int
    diagnostico: str
    observacion: str
    servicios_ids: List[int]
    signos_vitales: Optional[SignosVitalesConsulta] = None

class ConsultaResponse(BaseModel):
    id_consulta: int
    fecha: str
    diagnostico: str
    observacion: str
    servicios: List[str]
