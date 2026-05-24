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


@router.get("/historia-clinica/paciente/{id_paciente}")
def obtener_historia_clinica_paciente(
    id_paciente: int
):
    return consulta_service.obtener_historia_clinica_paciente(id_paciente)


@router.get("/")
def obtener_consultas(
    id_historia_clinica_fk: int
):
    return consulta_service.obtener_consultas(
        id_historia_clinica_fk
    )


@router.get("/{id_consulta}/servicios")
def obtener_servicios_consulta(
    id_consulta: int
):
    return consulta_service.obtener_servicios_consulta(
        id_consulta
    )