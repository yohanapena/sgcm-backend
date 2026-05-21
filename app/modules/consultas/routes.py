from fastapi import APIRouter

from app.modules.consultas.schema import (
    ConsultaCrearRequest
)

from app.modules.consultas.service import (
    ConsultaService
)

router = APIRouter()

consulta_service = ConsultaService()


@router.post("/")
def registrar_consulta(
    consulta: ConsultaCrearRequest
):

    return consulta_service.registrar_consulta(
        consulta
    )


@router.get("/")
def obtener_consultas(
    id_historia_clinica_fk: int
):

    return consulta_service.obtener_consultas(
        id_historia_clinica_fk
    )