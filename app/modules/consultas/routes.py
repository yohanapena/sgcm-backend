from fastapi import APIRouter
from app.modules.consultas.service import ConsultaService
from app.modules.consultas.schema import (
    ConsultaCrearRequest
)

router = APIRouter()

consulta_service = ConsultaService()


@router.post("/")
def registrar_consulta(
    consulta: ConsultaCrearRequest
):

    return {
        "mensaje": "Consulta registrada"
    }