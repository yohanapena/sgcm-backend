from fastapi import APIRouter, Depends
from typing import Optional
from app.modules.signos_vitales.schema import SignosVitalesCreate, SignosVitalesResponse
from app.modules.signos_vitales.service import SignosVitalesService
from app.core.dependencies import administrativo_o_medico

router = APIRouter()

service = SignosVitalesService()


@router.post("/", response_model=SignosVitalesResponse)
def registrar_signos_vitales(
    signos: SignosVitalesCreate,
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    return service.registrar_signos_vitales(signos)


@router.get("/")
def listar_signos(
    id_consulta_fk: Optional[int] = None,
    id_historia_clinica_fk: Optional[int] = None,
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    if id_consulta_fk:
        return {"data": service.obtener_signos_consulta(id_consulta_fk)}
    elif id_historia_clinica_fk:
        return {"data": service.obtener_signos_historia(id_historia_clinica_fk)}
    return {"data": []}