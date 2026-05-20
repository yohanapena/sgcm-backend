from abc import ABC, abstractmethod


class ICitaRepository(ABC):

    @abstractmethod
    def crear_cita(self):
        pass

    @abstractmethod
    def obtener_por_id(self):
        pass

    @abstractmethod
    def verificar_disponibilidad(self):
        pass

    @abstractmethod
    def cancelar_cita(self):
        pass

    @abstractmethod
    def marcar_atendida(self):
        pass

    @abstractmethod
    def registrar_historial(self):
        pass

    @abstractmethod
    def obtener_por_paciente(self):
        pass

    @abstractmethod
    def obtener_por_medico(self):
        pass


class ICitaService(ABC):

    @abstractmethod
    def agendar_cita(self):
        pass

    @abstractmethod
    def cancelar_cita(self):
        pass

    @abstractmethod
    def obtener_citas_paciente(self):
        pass

    @abstractmethod
    def obtener_citas_medico(self):
        pass