from abc import ABC, abstractmethod


class IMedicoRepository(ABC):

    @abstractmethod
    def crear_medico(self):
        pass

    @abstractmethod
    def obtener_por_id(self):
        pass

    @abstractmethod
    def agregar_especialidad(self):
        pass

    @abstractmethod
    def obtener_especialidades(self):
        pass

    @abstractmethod
    def crear_horario(self):
        pass

    @abstractmethod
    def obtener_horarios(self):
        pass

    @abstractmethod
    def verificar_superposicion(self):
        pass


class IMedicoService(ABC):

    @abstractmethod
    def registrar_medico(self):
        pass

    @abstractmethod
    def agregar_horario(self):
        pass

    @abstractmethod
    def obtener_horarios(self):
        pass