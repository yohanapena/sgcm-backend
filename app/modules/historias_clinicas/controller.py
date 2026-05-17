from fastapi import APIRouter, Depends
from app.modules.historias_clinicas.schema import HistoriaClinicaCrearRequest, HistoriaClinicaResponse
from app.modules.historias_clinicas.service import HistoriaClinicaService
from app.modules.historias_clinicas.repository import HistoriaClinicaRepository
from app.core.dependencies import administrativo_o_medico

router = APIRouter()


def get_service():
    repositorio = HistoriaClinicaRepository()
    return HistoriaClinicaService(repositorio)


@router.get("/", response_model=HistoriaClinicaResponse | None)
def obtener_historia_por_paciente(
    pacienteId: int,
    service: HistoriaClinicaService = Depends(get_service),
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    return service.obtener_por_paciente(pacienteId)


@router.post("/", response_model=HistoriaClinicaResponse)
def crear_historia_clinica(
    datos: HistoriaClinicaCrearRequest,
    service: HistoriaClinicaService = Depends(get_service),
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    return service.crear_o_retornar_historia(datos)