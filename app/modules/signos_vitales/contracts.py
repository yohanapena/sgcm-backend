from abc import ABC, abstractmethod


class ISignosVitalesRepository(ABC):

    @abstractmethod
    def crear_signos_vitales(self):
        pass

    @abstractmethod
    def obtener_por_historia(self):
        pass

    @abstractmethod
    def obtener_por_consulta(self):
        pass


class ISignosVitalesService(ABC):

    @abstractmethod
    def registrar_signos_vitales(self):
        pass

    @abstractmethod
    def obtener_signos_historia(self):
        pass

    @abstractmethod
    def obtener_signos_consulta(self):
        pass