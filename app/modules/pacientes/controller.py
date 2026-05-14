from fastapi import APIRouter, Depends
from app.modules.pacientes.schema import PacienteCrearRequest, PacienteResponse, PacienteActualizarRequest
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

@router.get("/buscar", response_model=list[PacienteResponse])
def buscar_pacientes(
    q: str,
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(solo_administrativo)
):
    return service.buscar_pacientes(q)

@router.put("/{id_paciente}", response_model=PacienteResponse)
def actualizar_paciente(
    id_paciente: int,
    datos: PacienteActualizarRequest,
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(solo_administrativo)
):
    return service.actualizar_paciente(id_paciente, datos)



@router.get("/{id_paciente}", response_model=PacienteResponse)
def obtener_paciente(
    id_paciente: int,
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(solo_administrativo)
):
    return service.obtener_por_id(id_paciente)