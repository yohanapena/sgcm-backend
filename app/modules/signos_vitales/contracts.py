from abc import ABC, abstractmethod


class ISignosVitalesRepository(ABC):

    @abstractmethod
    def crear(self):
        pass

    @abstractmethod
    def obtener_por_consulta(self):
        pass

    @abstractmethod
    def obtener_por_historia(self):
        pass


class ISignosVitalesService(ABC):

    @abstractmethod
    def registrar(self):
        pass

    @abstractmethod
    def obtener_por_consulta(self):
        pass

    @abstractmethod
    def obtener_por_historia(self):
        pass