from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, HTTPException, Query

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

@router.get("/paciente/{id_paciente}")
def obtener_citas_paciente(
    id_paciente: int,
    fecha_inicio: str = None,
    fecha_fin: str = None
):

    return cita_service.obtener_citas_paciente(
        id_paciente,
        fecha_inicio,
        fecha_fin
    )

@router.get("/medico/{id_medico}")
def obtener_citas_medico(
    id_medico: int,
    fecha: str = None
):

    return cita_service.obtener_citas_medico(
        id_medico,
        fecha
    )

@router.get(
    "/dashboard/medico/{id_medico}/citas"
)
def obtener_citas_dashboard(
    id_medico: int,
    fecha: str = Query(default=None)
):

    return cita_service.obtener_citas_dashboard(
        id_medico,
        fecha
    )