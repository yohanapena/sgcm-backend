from app.modules.consultas.contracts import IConsultaRepository
from app.core.database import get_connection


class ConsultaRepository(IConsultaRepository):

    def crear_consulta(self):
        pass

    def asociar_servicio(
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

    def obtener_servicios_consulta(self):
        pass

    def obtener_historia_clinica(self):
        pass

    def obtener_consultas_historia(
        self,
        id_paciente
    ):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            co.*,
            c.fecha,
            c.hora
        FROM consultas co
        INNER JOIN citas c
            ON co.id_cita_fk = c.id_cita
        WHERE c.id_paciente_fk = %s
        ORDER BY c.fecha DESC, c.hora DESC
        """

        cursor.execute(query, (id_paciente,))

        resultado = cursor.fetchall()

        cursor.close()
        connection.close()

        return resultado