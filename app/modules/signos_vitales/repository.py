from app.core.database import get_connection
from app.modules.signos_vitales.contracts import ISignosVitalesRepository


class SignosVitalesRepository(
    ISignosVitalesRepository
):

    def crear_signos_vitales(
        self,
        signos
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO signos_vitales (
            peso,
            estatura,
            temperatura,
            presion_arterial,
            frecuencia_cardiaca,
            saturacion_oxigeno,
            id_historia_clinica_fk,
            id_consulta_fk
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        valores = (
            signos["peso"],
            signos["estatura"],
            signos["temperatura"],
            signos["presion_arterial"],
            signos["frecuencia_cardiaca"],
            signos["saturacion_oxigeno"],
            signos["id_historia_clinica_fk"],
            signos["id_consulta_fk"]
        )

        cursor.execute(query, valores)

        connection.commit()

        cursor.close()
        connection.close()

    def obtener_por_historia(
        self,
        id_historia
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True     
        )

        query = """
        SELECT *
        FROM signos_vitales
        WHERE id_historia_clinica_fk = %s
        ORDER BY id_signo DESC
        """

        cursor.execute(
            query,
            (id_historia,)
        )

        resultados = cursor.fetchall()

        cursor.close()
        connection.close()

        return resultados

    def obtener_por_consulta(
        self,
        id_consulta
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
        SELECT *
        FROM signos_vitales
        WHERE id_consulta_fk = %s
        """

        cursor.execute(
            query,
            (id_consulta,)
        )

        resultado = cursor.fetchall()

        cursor.close()
        connection.close()

        return resultado