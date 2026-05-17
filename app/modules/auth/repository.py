from typing import List, Optional

from app.modules.auth.contracts import IAuthRepository
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.repository import UsuarioRepository


class AuthRepository(IAuthRepository):
    def __init__(self):
        self._usuario_repository = UsuarioRepository()

    def obtener_usuario_por_nombre(self, usuario: str) -> Optional[Usuario]:
        return self._usuario_repository.obtener_por_nombre(usuario)

    def listar_usuarios(self) -> List[Usuario]:
        return self._usuario_repository.listar_usuarios()

    def cambiar_estado_usuario(self, id_usuario: int, estado: str) -> Usuario:
        return self._usuario_repository.cambiar_estado(id_usuario, estado)

    def crear_usuario(self, usuario: Usuario) -> Usuario:
        return self._usuario_repository.crear_usuario(usuario)

    def obtener_usuario_por_id(self, id_usuario: int) -> Optional[Usuario]:
        return self._usuario_repository.obtener_por_id(id_usuario)
