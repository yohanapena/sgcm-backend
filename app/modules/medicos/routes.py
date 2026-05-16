from fastapi import APIRouter

from app.modules.medicos.schema import (
    MedicoCrearRequest,
    MedicoResponse
)

from app.modules.medicos.service import (
    MedicoService
)

router = APIRouter()

medico_service = MedicoService()


@router.post(
    "/",
    response_model=MedicoResponse,
    status_code=201
)
def registrar_medico(
    medico: MedicoCrearRequest
):

    return medico_service.registrar_medico(
        medico
    )