from abc import ABC, abstractmethod
from typing import Optional

from app.modules.usuarios.model import Usuario


class IAuthRepository(ABC):
    @abstractmethod
    def obtener_usuario_por_nombre(self, usuario: str) -> Optional[Usuario]:
        raise NotImplementedError
