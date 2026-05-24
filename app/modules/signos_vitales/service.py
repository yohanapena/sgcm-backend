from app.modules.signos_vitales.contracts import ISignosVitalesService
from app.modules.signos_vitales.repository import SignosVitalesRepository


class SignosVitalesService(ISignosVitalesService):

    def __init__(self):
        self.repository = SignosVitalesRepository()

    def registrar(self, signos):
        return self.registrar_signos_vitales(signos)

    def registrar_signos_vitales(self, signos):
        datos = {
            "peso": signos.peso,
            "estatura": signos.estatura,
            "temperatura": signos.temperatura,
            "presion_arterial": signos.presion_arterial,
            "frecuencia_cardiaca": signos.frecuencia_cardiaca,
            "saturacion_oxigeno": signos.saturacion_oxigeno,
            "id_historia_clinica_fk": signos.id_historia_clinica_fk,
            "id_consulta_fk": signos.id_consulta_fk
        }
        return self.repository.crear_signos_vitales(datos)

    def obtener_por_consulta(self, id_consulta):
        return self.repository.obtener_por_consulta(id_consulta)

    def obtener_por_historia(self, id_historia):
        return self.repository.obtener_por_historia(id_historia)

    def obtener_signos_historia(self, id_historia):
        return self.repository.obtener_por_historia(id_historia)

    def obtener_signos_consulta(self, id_consulta):
        return self.repository.obtener_por_consulta(id_consulta)