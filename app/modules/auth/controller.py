from typing import Optional

from fastapi import APIRouter, Depends

from app.core.dependencies import get_usuario_actual
from app.modules.auth.schema import LoginRequest, LoginResponse, MeResponse
from app.modules.auth.service import AuthService


router = APIRouter(prefix="", tags=["auth"])


def get_auth_service() -> AuthService:
    return AuthService()


@router.post("/login", response_model=LoginResponse)
async def login(
    datos: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """
    Endpoint de login para obtener JWT token.
    
    Body:
    {
      "usuario": "juan_admin",
      "contrasena": "contraseña123"
    }
    """
    return service.login(datos.usuario, datos.contrasena)


@router.get("/me", response_model=MeResponse)
async def get_me(usuario_actual: dict = Depends(get_usuario_actual)):
    """
    Obtiene la información del usuario autenticado.
    """
    return MeResponse(
        id_usuario=usuario_actual.get("id_usuario"),
        usuario=usuario_actual.get("usuario"),
        rol=usuario_actual.get("rol"),
        id_medico_fk=usuario_actual.get("id_medico_fk"),
    )
