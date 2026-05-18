from fastapi import APIRouter, Depends

from app.core.dependencies import solo_administrativo
from app.modules.usuarios.service import UsuarioService
from app.modules.usuarios.repository import UsuarioRepository

dashboard_router = APIRouter()


def get_service():
    return UsuarioService(UsuarioRepository())


@dashboard_router.get("/admin/summary")
def resumen_dashboard(
    service: UsuarioService = Depends(get_service),
    usuario_actual: dict = Depends(solo_administrativo),
):
    resumen = service.obtener_resumen_dashboard()
    return {"data": resumen}
