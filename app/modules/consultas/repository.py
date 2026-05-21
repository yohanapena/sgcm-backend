from app.modules.consultas.contracts import IConsultaRepository
from app.core.database import get_connection


class ConsultaRepository(IConsultaRepository):

    def crear_consulta(
        self,
        consulta
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO consultas (
            observacion,
            diagnostico,
            id_cita_fk,
            id_historia_clinica_fk
        )
        VALUES (%s, %s, %s, %s)
        """

        valores = (
            consulta.observacion,
            consulta.diagnostico,
            consulta.id_cita_fk,
            consulta.id_historia_clinica_fk
        )

        cursor.execute(query, valores)

        connection.commit()

        id_consulta = cursor.lastrowid

        cursor.close()
        connection.close()

        return id_consulta

    def agregar_servicio(
        self,
        id_consulta,
        id_servicio
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        INSERT IGNORE INTO consultas_servicios (
            id_consulta_fk,
            id_servicio_fk
        )
        VALUES (%s, %s)
        """

        cursor.execute(
            query,
            (id_consulta, id_servicio)
        )

        connection.commit()

        cursor.close()
        connection.close()

    def obtener_por_historia(
        self,
        id_historia_clinica_fk
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
        SELECT
            co.id_consulta,
            c.fecha,
            co.diagnostico,
            co.observacion
        FROM consultas co
        INNER JOIN citas c
            ON co.id_cita_fk = c.id_cita
        WHERE co.id_historia_clinica_fk = %s
        """

        cursor.execute(
            query,
            (id_historia_clinica_fk,)
        )

        resultado = cursor.fetchall()

        cursor.close()
        connection.close()

        return resultado