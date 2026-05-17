from typing import Optional

from app.modules.auth.contracts import IAuthRepository
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.repository import UsuarioRepository


class AuthRepository(IAuthRepository):
    def __init__(self):
        self._usuario_repository = UsuarioRepository()

    def obtener_usuario_por_nombre(self, usuario: str) -> Optional[Usuario]:
        return self._usuario_repository.obtener_por_nombre(usuario)
