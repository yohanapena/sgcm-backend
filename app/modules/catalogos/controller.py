from fastapi import APIRouter, Depends
from app.modules.catalogos.schema import ServicioResponse
from app.modules.catalogos.repository import CatalogoRepository
from app.core.dependencies import administrativo_o_medico

router = APIRouter()

def get_repository():
    return CatalogoRepository()


@router.get("/servicios", response_model=list[ServicioResponse])
def obtener_servicios(
    repo: CatalogoRepository = Depends(get_repository),
    usuario_actual: dict = Depends(administrativo_o_medico)
):
    return repo.obtener_servicios()