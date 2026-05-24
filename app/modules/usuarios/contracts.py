from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schema import UsuarioCrearRequest, UsuarioActualizarRequest


class IUsuarioRepository(ABC):
    @abstractmethod
    def crear_usuario(self, usuario: Usuario) -> Usuario:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def listar_usuarios(self) -> List[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def cambiar_estado(self, id_usuario: int, estado: str) -> Usuario:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_nombre(self, usuario: str) -> Optional[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def actualizar_usuario(self, id_usuario: int, datos: UsuarioActualizarRequest) -> Usuario:
        raise NotImplementedError


class IUsuarioService(ABC):
    @abstractmethod
    def crear_usuario(self, datos: UsuarioCrearRequest) -> Usuario:
        raise NotImplementedError

    @abstractmethod
    def listar_usuarios(self) -> List[Usuario]:
        raise NotImplementedError

    @abstractmethod
    def obtener_usuario(self, id_usuario: int) -> Usuario:
        raise NotImplementedError

    @abstractmethod
    def cambiar_estado(self, id_usuario: int, estado: str) -> Usuario:
        raise NotImplementedError

    @abstractmethod
    def actualizar_usuario(self, id_usuario: int, datos: UsuarioActualizarRequest) -> Usuario:
        raise NotImplementedError
