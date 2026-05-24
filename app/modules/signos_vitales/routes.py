from fastapi import APIRouter

from app.modules.signos_vitales.schema import (
    SignosVitalesCreate
)

from app.modules.signos_vitales.service import (
    SignosVitalesService
)

router = APIRouter()

service = SignosVitalesService()


@router.post("/")
def registrar_signos_vitales(
    signos: SignosVitalesCreate
):

    return service.registrar_signos_vitales(
        signos
    )


@router.get("/historia/{id_historia}")
def obtener_signos_historia(
    id_historia: int
):

    return service.obtener_signos_historia(
        id_historia
    )


@router.get("/consulta/{id_consulta}")
def obtener_signos_consulta(
    id_consulta: int
):

    return service.obtener_signos_consulta(
        id_consulta
    )