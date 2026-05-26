from pydantic import BaseModel, Field
from typing import List, Optional


class SignosVitalesConsulta(BaseModel):
    peso: float
    estatura: float
    temperatura: float
    presion_arterial: str = Field(alias="presion")
    frecuencia_cardiaca: int = Field(alias="frecuenciaCardiaca")
    saturacion_oxigeno: int = Field(alias="saturacion")

    model_config = {"populate_by_name": True}

class ConsultaCrearRequest(BaseModel):
    id_cita_fk: int
    id_historia_clinica_fk: int
    diagnostico: str
    observacion: str
    servicios_ids: Optional[List[int]] = []
    signos_vitales: Optional[SignosVitalesConsulta] = None

class ConsultaResponse(BaseModel):
    id_consulta: int
    fecha: str
    diagnostico: str
    observacion: str
    servicios: List[str]
