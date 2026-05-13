from abc import ABC, abstractmethod
from typing import Optional
from app.modules.pacientes.model import Paciente


class IPacienteRepository(ABC):

    @abstractmethod
    def crear_paciente(self, paciente: Paciente) -> Paciente:
        pass

    @abstractmethod
    def obtener_por_identificacion(self, numero_identificacion: str) -> Optional[Paciente]:
        pass