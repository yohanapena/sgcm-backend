from typing import List

from fastapi import APIRouter, Depends, status

from app.core.dependencies import solo_administrativo
from app.modules.usuarios.schema import (
    UsuarioActualizarRequest,
    UsuarioCrearRequest,
    UsuarioEstadoRequest,
    UsuarioResponse,
)
from app.modules.usuarios.service import UsuarioService
from app.modules.usuarios.repository import UsuarioRepository

router = APIRouter(prefix="", tags=["usuarios"], dependencies=[Depends(solo_administrativo)])


def get_service() -> UsuarioService:
    repository = UsuarioRepository()
    return UsuarioService(repository=repository)


@router.get("", response_model=List[UsuarioResponse])
async def listar_usuarios(service: UsuarioService = Depends(get_service)):
    return service.listar_usuarios()


@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    datos: UsuarioCrearRequest,
    service: UsuarioService = Depends(get_service),
):
    return service.crear_usuario(datos)


@router.put("/{id_usuario}", response_model=UsuarioResponse)
async def actualizar_usuario(
    id_usuario: int,
    datos: UsuarioActualizarRequest,
    service: UsuarioService = Depends(get_service),
):
    return service.actualizar_usuario(id_usuario, datos)


@router.patch("/{id_usuario}/estado", response_model=UsuarioResponse)
async def cambiar_estado(
    id_usuario: int,
    datos: UsuarioEstadoRequest,
    service: UsuarioService = Depends(get_service),
):
    return service.cambiar_estado(id_usuario, datos.estado.value)
