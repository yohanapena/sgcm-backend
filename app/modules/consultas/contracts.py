from abc import ABC, abstractmethod


class IConsultaRepository(ABC):

    @abstractmethod
    def crear_consulta(self):
        pass

    @abstractmethod
    def asociar_servicio(self):
        pass

    @abstractmethod
    def obtener_servicios_consulta(self):
        pass

    @abstractmethod
    def obtener_historia_clinica(self):
        pass

    @abstractmethod
    def obtener_consultas_historia(self):
        pass


class IConsultaService(ABC):

    @abstractmethod
    def registrar_consulta(self):
        pass

    @abstractmethod
    def obtener_servicios(self):
        pass

    @abstractmethod
    def obtener_historia_clinica(self):
        pass