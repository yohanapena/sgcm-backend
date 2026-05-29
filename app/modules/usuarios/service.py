from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from app.core.security import hashear_contrasena
from app.modules.usuarios.contracts import IUsuarioRepository, IUsuarioService
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schema import (
    UsuarioActualizarRequest,
    UsuarioCrearRequest,
    UsuarioResponse,
    UsuarioRol,
    UsuarioEstado,
)
from app.modules.usuarios.repository import UsuarioRepository


class UsuarioService(IUsuarioService):
    def __init__(self, repository: IUsuarioRepository = None):
        self.repository = repository or UsuarioRepository()

    def crear_usuario(self, datos: UsuarioCrearRequest) -> UsuarioResponse:
        if datos.rol == UsuarioRol.MEDICO and datos.id_medico_fk is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El campo id_medico_fk es obligatorio cuando el rol es Medico",
            )

        usuario_existente = self.repository.obtener_por_nombre(datos.usuario)
        if usuario_existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario con nombre '{datos.usuario}'",
            )

        usuario = Usuario(
            usuario=datos.usuario,
            contrasena=hashear_contrasena(datos.contrasena),
            rol=datos.rol,
            estado=datos.estado,
            fecha_creacion=datetime.utcnow(),
            id_medico_fk=datos.id_medico_fk,
        )

        usuario_guardado = self.repository.crear_usuario(usuario)
        return self._mapear_response(usuario_guardado)

    def listar_usuarios(self) -> List[UsuarioResponse]:
        usuarios = self.repository.listar_usuarios()
        return [self._mapear_response(usuario) for usuario in usuarios]

    def obtener_usuario(self, id_usuario: int) -> UsuarioResponse:
        usuario = self.repository.obtener_por_id(id_usuario)
        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        return self._mapear_response(usuario)

    def cambiar_estado(self, id_usuario: int, estado: str) -> UsuarioResponse:
        if estado not in {UsuarioEstado.ACTIVO.value, UsuarioEstado.INACTIVO.value}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estado inválido",
            )
        usuario_actualizado = self.repository.cambiar_estado(id_usuario, estado)
        return self._mapear_response(usuario_actualizado)

    def actualizar_usuario(self, id_usuario: int, datos: UsuarioActualizarRequest) -> UsuarioResponse:
        usuario_existente = self.repository.obtener_por_id(id_usuario)
        if usuario_existente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        if datos.rol == UsuarioRol.MEDICO and datos.id_medico_fk is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El campo id_medico_fk es obligatorio cuando el rol es Medico",
            )

        if datos.contrasena is not None:
            # Compatibilidad con frontend: si llega '' no se actualiza
            if datos.contrasena != "":
                datos.contrasena = hashear_contrasena(datos.contrasena)
            else:
                datos.contrasena = None

        if datos.rol is None and usuario_existente.rol == UsuarioRol.MEDICO and datos.id_medico_fk is None:
            datos.id_medico_fk = usuario_existente.id_medico_fk

        usuario_actualizado = self.repository.actualizar_usuario(id_usuario, datos)
        return self._mapear_response(usuario_actualizado)


    def obtener_resumen_dashboard(self):
        return self.repository.obtener_resumen_dashboard()

    def _mapear_response(self, usuario: Usuario) -> UsuarioResponse:
        return UsuarioResponse(
            id_usuario=usuario.id_usuario,
            usuario=usuario.usuario,
            rol=usuario.rol,
            estado=usuario.estado,
            fecha_creacion=usuario.fecha_creacion,
            id_medico_fk=usuario.id_medico_fk,
            medico_nombre=usuario.medico_nombre,
        )
