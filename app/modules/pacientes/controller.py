from fastapi import APIRouter, Depends
from app.modules.pacientes.schema import (
    PacienteCrearRequest,
    PacienteResponse,
    PacienteActualizarRequest,
    AlergiasActualizarRequest,
)
from app.modules.pacientes.service import PacienteService
from app.modules.pacientes.repository import PacienteRepository
from app.core.dependencies import solo_administrativo, administrativo_o_medico

router = APIRouter()


def get_service():
    repositorio = PacienteRepository()
    return PacienteService(repositorio)


@router.post("", response_model=PacienteResponse)
def registrar_paciente(
    datos: PacienteCrearRequest,
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(solo_administrativo)
):
    return service.registrar_paciente(datos)


@router.get("", response_model=list[PacienteResponse])
def listar_pacientes(
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    return service.listar_pacientes()


@router.get("/buscar", response_model=list[PacienteResponse])
def buscar_pacientes(
    q: str,
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(administrativo_o_medico)
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
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    return service.obtener_por_id(id_paciente)


@router.get("/{id_paciente}/alergias")
def listar_alergias(
    id_paciente: int,
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(solo_administrativo)
):
    return service.listar_alergias(id_paciente)


@router.post("/{id_paciente}/alergias")
def agregar_alergia(
    id_paciente: int,
    datos: dict,
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(solo_administrativo)
):
    return service.agregar_alergia(id_paciente, datos["alergia"])


@router.patch("/{id_paciente}/alergias", response_model=PacienteResponse)
def reemplazar_alergias(
    id_paciente: int,
    datos: AlergiasActualizarRequest,
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(administrativo_o_medico)  # ← fix
):
    return service.reemplazar_alergias(id_paciente, datos.alergias)


@router.delete("/{id_paciente}/alergias/{id_alergia}")
def eliminar_alergia(
    id_paciente: int,
    id_alergia: int,
    service: PacienteService = Depends(get_service),
    usuario_actual: dict = Depends(solo_administrativo)
):
    return {"data": service.eliminar_alergia(id_paciente, id_alergia)}