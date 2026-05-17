from pydantic import BaseModel
from typing import Optional
from datetime import date


class HistoriaClinicaCrearRequest(BaseModel):
    id_paciente_fk: int
    resumen: Optional[str] = "Historia clínica creada automáticamente"
    fecha_apertura: Optional[date] = None


class HistoriaClinicaResponse(BaseModel):
    id_historia_clinica: int
    id_paciente_fk: int
    resumen: Optional[str] = None
    fecha_apertura: Optional[date] = None
    alergias: Optional[str] = None
    antecedentes_personales: Optional[str] = None
    antecedentes_familiares: Optional[str] = None