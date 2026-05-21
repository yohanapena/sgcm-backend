from app.modules.consultas.contracts import IConsultaService
from app.modules.consultas.repository import ConsultaRepository


class ConsultaService(IConsultaService):

    def __init__(self):

        self.repository = ConsultaRepository()

    def registrar_consulta(self):
        pass

    def obtener_servicios(self):
        pass

    def obtener_historia_clinica(self):
        pass