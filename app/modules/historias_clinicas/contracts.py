from abc import ABC, abstractmethod
from typing import Optional
from app.modules.historias_clinicas.model import HistoriaClinica


class IHistoriaClinicaRepository(ABC):

    @abstractmethod
    def crear_historia_clinica(self, historia: HistoriaClinica) -> HistoriaClinica:
        pass

    @abstractmethod
    def obtener_por_paciente(self, id_paciente_fk: int) -> Optional[HistoriaClinica]:
        pass