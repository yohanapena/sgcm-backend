from fastapi import APIRouter, HTTPException

from app.modules.citas.schema import (
    CitaCrearRequest,
    CitaResponse,
    CitaCancelarRequest
)

from app.modules.citas.service import (
    CitaService,
    SGCMConflictError
)

router = APIRouter()

cita_service = CitaService()


@router.post(
    "/",
    response_model=CitaResponse,
    status_code=201
)
def crear_cita(cita: CitaCrearRequest):

    try:

        return cita_service.agendar_cita(cita)

    except SGCMConflictError as e:

        raise HTTPException(
            status_code=409,
            detail=str(e)
        )
    
@router.put("/{id_cita}/cancelar")
def cancelar_cita(
    id_cita: int,
    data: CitaCancelarRequest
):
    return cita_service.cancelar_cita(
        id_cita=id_cita,
        motivo=data.motivo
    )