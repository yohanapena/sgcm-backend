from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_usuario_actual, solo_administrativo
from app.modules.auth.schema import LoginRequest, LoginResponse, MeResponse, MeDataResponse
from app.modules.auth.service import AuthService
from app.modules.usuarios.schema import UsuarioCrearRequest, UsuarioEstadoRequest, UsuarioResponse


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


@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    datos: UsuarioCrearRequest,
    service: AuthService = Depends(get_auth_service),
    _: dict = Depends(solo_administrativo),
):
    return service.crear_usuario(datos)


@router.get("/usuarios", response_model=List[UsuarioResponse])
async def listar_usuarios(
    service: AuthService = Depends(get_auth_service),
    _: dict = Depends(solo_administrativo),
):
    return service.listar_usuarios()


@router.patch("/usuarios/{id_usuario}/estado", response_model=UsuarioResponse)
async def cambiar_estado_usuario(
    id_usuario: int,
    datos: UsuarioEstadoRequest,
    service: AuthService = Depends(get_auth_service),
    _: dict = Depends(solo_administrativo),
):
    return service.cambiar_estado_usuario(id_usuario, datos.estado.value)


@router.get("/me", response_model=MeDataResponse)
async def get_me(usuario_actual: dict = Depends(get_usuario_actual)):
    """
    Obtiene la información del usuario autenticado.
    Requiere JWT token válido en header Authorization.
    """
    me = MeResponse(
        id_usuario=usuario_actual.get("id_usuario"),
        usuario=usuario_actual.get("usuario"),
        rol=usuario_actual.get("rol"),
        id_medico_fk=usuario_actual.get("id_medico_fk"),
    )
    return MeDataResponse(data=me)
