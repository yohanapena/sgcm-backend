from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.usuarios.model import Usuario


class IAuthRepository(ABC):
    @abstractmethod
    def obtener_usuario_por_nombre(self, usuario: str) -> Optional[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def listar_usuarios(self) -> List[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def cambiar_estado_usuario(self, id_usuario: int, estado: str) -> Usuario:
        raise NotImplementedError

    @abstractmethod
    def crear_usuario(self, usuario: Usuario) -> Usuario:
        raise NotImplementedError
