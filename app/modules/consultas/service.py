from app.modules.consultas.contracts import IConsultaService
from app.modules.consultas.repository import ConsultaRepository


class ConsultaService(IConsultaService):

    def __init__(self):

        self.repository = ConsultaRepository()

    def registrar_consulta(
        self,
        consulta
    ):

        id_consulta = self.repository.crear_consulta(
            consulta
        )

        for servicio_id in consulta.servicios_ids:

            self.repository.agregar_servicio(
                id_consulta,
                servicio_id
            )

        return {
            "mensaje": "Consulta registrada"
        }

    def obtener_consultas(
        self,
        id_historia_clinica_fk
    ):

        return self.repository.obtener_por_historia(
            id_historia_clinica_fk
        )