from fastapi import APIRouter, Depends
from app.modules.pacientes.schema import PacienteCrearRequest, PacienteResponse
from app.modules.pacientes.service import PacienteService
from app.modules.pacientes.repository import PacienteRepository
from app.core.dependencies import solo_administrativo

router = APIRouter()


def get_service():
    repositorio = PacienteRepository()
    return PacienteService(repositorio)


@router.post("/", response_model=PacienteResponse)
def registrar_paciente(
    datos: PacienteCrearRequest,
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(solo_administrativo)
):
    return service.registrar_paciente(datos)

