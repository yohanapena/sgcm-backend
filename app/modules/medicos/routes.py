from fastapi import APIRouter
from app.modules.medicos.schema import MedicoUpdate

from app.modules.medicos.schema import (
    MedicoCrearRequest,
    MedicoResponse,
    HorarioCrearRequest,
    HorarioResponse,
    MedicoEstadoUpdate
)

from app.modules.medicos.service import (
    MedicoService
)

router = APIRouter()

medico_service = MedicoService()

@router.get("", response_model=list[MedicoResponse])
def listar_medicos(query: str = None):
    return medico_service.listar_medicos(query)

@router.post(
    "",
    response_model=MedicoResponse,
    status_code=201
)
def registrar_medico(
    medico: MedicoCrearRequest
):

    return medico_service.registrar_medico(
        medico
    )

@router.post(
    "/{id_medico}/horarios",
    response_model=HorarioResponse,
    status_code=201
)
def agregar_horario(
    id_medico: int,
    horario: HorarioCrearRequest
):

    return medico_service.agregar_horario(
        id_medico,
        horario
    )

@router.get(
    "/{id_medico}/horarios",
    response_model=list[HorarioResponse]
)
def obtener_horarios(
    id_medico: int
):

    return medico_service.obtener_horarios(
        id_medico
    )

@router.put("/{id_medico}")
def actualizar_medico(
    id_medico: int,
    medico: MedicoUpdate
):

    return medico_service.actualizar_medico(
        id_medico,
        medico
    )

@router.patch("/{id_medico}/estado")
def cambiar_estado_medico(
    id_medico: int,
    datos: MedicoEstadoUpdate
):
    
    return medico_service.cambiar_estado(
        id_medico,
        datos
    )