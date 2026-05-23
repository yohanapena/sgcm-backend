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

    @abstractmethod
    def obtener_historia_clinica(self, id_paciente: int):
        pass

    @abstractmethod
    def obtener_consultas_historia(self, id_historia_clinica: int):
        pass


class IConsultaService(ABC):

    @abstractmethod
    def registrar_consulta(self):
        pass

    @abstractmethod
    def obtener_consultas(self):
        pass

    @abstractmethod
    def obtener_historia_clinica_paciente(self, id_paciente: int):
        pass