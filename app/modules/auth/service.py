from fastapi import HTTPException, status

from app.core.security import verificar_contrasena, crear_token
from app.modules.auth.contracts import IAuthRepository
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schema import LoginResponse
from app.modules.usuarios.model import UsuarioEstado


class AuthService:
    def __init__(self, repository: IAuthRepository = None):
        self.repository = repository or AuthRepository()

    def login(self, usuario: str, contrasena: str) -> LoginResponse:
        usuario_encontrado = self.repository.obtener_usuario_por_nombre(usuario)
        if usuario_encontrado is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña inválidos",
            )

        if usuario_encontrado.estado != UsuarioEstado.ACTIVO:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El usuario se encuentra inactivo",
            )

        if not verificar_contrasena(contrasena, usuario_encontrado.contrasena):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña inválidos",
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
            usuario=usuario_encontrado.usuario,
            rol=usuario_encontrado.rol.value,
            id_medico_fk=usuario_encontrado.id_medico_fk,
        )
