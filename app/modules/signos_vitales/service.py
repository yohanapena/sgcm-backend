from app.modules.signos_vitales.contracts import ISignosVitalesService
from app.modules.signos_vitales.repository import SignosVitalesRepository


class SignosVitalesService(
    ISignosVitalesService
):

    def __init__(self):

        self.repository = (
            SignosVitalesRepository()
        )

    def registrar_signos_vitales(
        self,
        signos
    ):

        self.repository.crear_signos_vitales(
            signos
        )

        return {
            "mensaje": "Signos vitales registrados"
        }

    def obtener_signos_historia(
        self,
        id_historia
    ):

        return self.repository.obtener_por_historia(
            id_historia
        )

    def obtener_signos_consulta(
        self,
        id_consulta
    ):

        return self.repository.obtener_por_consulta(
            id_consulta
        )