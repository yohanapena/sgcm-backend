from app.modules.consultas.contracts import IConsultaService
from app.modules.consultas.repository import ConsultaRepository
from app.modules.citas.repository import CitaRepository
from app.modules.signos_vitales.repository import SignosVitalesRepository

class ConsultaService(IConsultaService):

    def __init__(self):

        self.repository = ConsultaRepository()
        self.cita_repository = CitaRepository()
        self.signos_repository = SignosVitalesRepository()

    def registrar_consulta(
            self,
            consulta
        ):

        id_consulta = self.repository.crear_consulta(
            consulta
        )

        if consulta.signos_vitales:

            try:

                self.signos_repository.crear_signos_vitales({
                    "peso": consulta.signos_vitales.peso,
                    "estatura": consulta.signos_vitales.estatura,
                    "temperatura": consulta.signos_vitales.temperatura,
                    "presion_arterial": consulta.signos_vitales.presion_arterial,
                    "frecuencia_cardiaca": consulta.signos_vitales.frecuencia_cardiaca,
                    "saturacion_oxigeno": consulta.signos_vitales.saturacion_oxigeno,
                    "id_historia_clinica_fk": consulta.id_historia_clinica_fk,
                    "id_consulta_fk": id_consulta
                })

            except Exception as e:

                print("Error registrando signos vitales:", e)

        for servicio_id in consulta.servicios_ids:

            self.repository.agregar_servicio(
                id_consulta,
                servicio_id
            )

            self.cita_repository.marcar_atendida(
                consulta.id_cita_fk
            )

            self.cita_repository.registrar_historial(
                id_cita=consulta.id_cita_fk,
                estado_anterior="Agendada",
                estado_nuevo="Atendida",
                motivo="Consulta registrada"
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
    
    def obtener_servicios_consulta(
        self,
        id_consulta
    ):

        return self.repository.obtener_servicios_consulta(
            id_consulta
        )