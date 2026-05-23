from abc import ABC, abstractmethod


class IConsultaRepository(ABC):

    @abstractmethod
    def crear_consulta(self):
        pass

    @abstractmethod
    def obtener_por_historia(self):
        pass

    @abstractmethod
    def agregar_servicio(self):
        pass

    @abstractmethod
    def obtener_servicios_consulta(self):
        pass

class IConsultaService(ABC):

    @abstractmethod
    def registrar_consulta(self):
        pass

    @abstractmethod
    def obtener_consultas(self):
        pass