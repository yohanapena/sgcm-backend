from datetime import datetime

from datetime import datetime

from fastapi import HTTPException, status

from app.core.security import verificar_contrasena, crear_token, hashear_contrasena
from app.modules.auth.contracts import IAuthRepository
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schema import LoginResponse
from app.modules.usuarios.model import Usuario, UsuarioEstado, UsuarioRol
from app.modules.usuarios.schema import UsuarioCrearRequest, UsuarioResponse


class AuthService:
    def __init__(self, repository: IAuthRepository = None):
        self.repository = repository or AuthRepository()

    def login(self, usuario: str, contrasena: str) -> LoginResponse:
        GENERIC_AUTH_ERROR = "Credenciales incorrectas o usuario inactivo"

        usuario_encontrado = self.repository.obtener_usuario_por_nombre(usuario)
        if usuario_encontrado is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=GENERIC_AUTH_ERROR,
            )

        if not verificar_contrasena(contrasena, usuario_encontrado.contrasena):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=GENERIC_AUTH_ERROR,
            )

        if usuario_encontrado.estado != UsuarioEstado.ACTIVO:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=GENERIC_AUTH_ERROR,
            )

        payload = {
            "id_usuario": usuario_encontrado.id_usuario,
            "usuario": usuario_encontrado.usuario,
            "rol": usuario_encontrado.rol.value,
            "id_medico_fk": usuario_encontrado.id_medico_fk,
        }

        token = crear_token(payload)

        return LoginResponse(
            access_token=token,
            id_usuario=usuario_encontrado.id_usuario,
            usuario=usuario_encontrado.usuario,
            rol=usuario_encontrado.rol.value,
            estado=usuario_encontrado.estado.value,
            id_medico_fk=usuario_encontrado.id_medico_fk,
            nombre_completo=usuario_encontrado.nombre_completo,
        )

    def crear_usuario(self, datos: UsuarioCrearRequest) -> UsuarioResponse:
        usuario_existente = self.repository.obtener_usuario_por_nombre(datos.usuario)
        if usuario_existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario con nombre '{datos.usuario}'",
            )

        if datos.rol == UsuarioRol.MEDICO and datos.id_medico_fk is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El campo id_medico_fk es obligatorio cuando el rol es Medico",
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

    def listar_usuarios(self):
        usuarios = self.repository.listar_usuarios()
        return [self._mapear_response(usuario) for usuario in usuarios]

    def cambiar_estado_usuario(self, id_usuario: int, estado: str) -> UsuarioResponse:
        if estado not in {UsuarioEstado.ACTIVO.value, UsuarioEstado.INACTIVO.value}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estado inválido",
            )

        try:
            usuario_actualizado = self.repository.cambiar_estado_usuario(id_usuario, estado)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        if usuario_actualizado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        return self._mapear_response(usuario_actualizado)

    def obtener_usuario_por_id(self, id_usuario: int) -> UsuarioResponse:
        usuario = None
        try:
            usuario = self.repository.obtener_usuario_por_id(id_usuario)
        except Exception:
            usuario = None

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        return self._mapear_response(usuario)

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

    def crear_usuario(self, datos: UsuarioCrearRequest) -> UsuarioResponse:
        usuario_existente = self.repository.obtener_usuario_por_nombre(datos.usuario)
        if usuario_existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario con nombre '{datos.usuario}'",
            )

        if datos.rol == UsuarioRol.MEDICO and datos.id_medico_fk is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El campo id_medico_fk es obligatorio cuando el rol es Medico",
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
