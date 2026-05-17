from fastapi import APIRouter, Depends
from app.modules.catalogos.schema import ServicioResponse, EpsResponse, RegimenResponse, EspecialidadResponse
from app.modules.catalogos.repository import CatalogoRepository
from app.core.dependencies import administrativo_o_medico

router = APIRouter()


def get_repository():
    return CatalogoRepository()


@router.get("/servicios")
def obtener_servicios(
    repo: CatalogoRepository = Depends(get_repository),
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    return {"data": repo.obtener_servicios()}


@router.get("/eps")
def obtener_eps(
    repo: CatalogoRepository = Depends(get_repository),
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    return {"data": repo.listar_eps()}


@router.get("/regimenes")
def obtener_regimenes(
    repo: CatalogoRepository = Depends(get_repository),
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    return {"data": repo.listar_regimenes()}


@router.get("/especialidades")
def obtener_especialidades(
    repo: CatalogoRepository = Depends(get_repository),
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    return {"data": repo.listar_especialidades()}