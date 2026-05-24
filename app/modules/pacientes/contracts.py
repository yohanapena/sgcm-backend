from abc import ABC, abstractmethod
from typing import Optional, List
from app.modules.pacientes.model import Paciente


class IPacienteRepository(ABC):

    @abstractmethod
    def crear_paciente(self, paciente: Paciente) -> Paciente:
        pass

    @abstractmethod
    def obtener_por_identificacion(self, numero_identificacion: str) -> Optional[Paciente]:
        pass

    @abstractmethod
    def obtener_por_id(self, id_paciente: int) -> Optional[Paciente]:
        pass

    @abstractmethod
    def actualizar_paciente(self, id_paciente: int, datos: dict) -> Optional[Paciente]:
        pass

    @abstractmethod
    def buscar_pacientes(self, criterio: str) -> List[Paciente]:
        pass

    @abstractmethod
    def agregar_alergia(self, id_paciente_fk: int, alergia: str) -> dict:
        pass

    @abstractmethod
    def listar_alergias(self, id_paciente_fk: int) -> list:
        pass

    @abstractmethod
    def eliminar_alergia(self, id_alergia: int, id_paciente_fk: int) -> bool:
        pass