from app.core.database import get_connection


class CitaRepository:

    def verificar_disponibilidad(
        self,
        fecha,
        hora,
        id_horario_medico_fk
    ):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM citas
        WHERE fecha = %s
        AND hora = %s
        AND id_horario_medico_fk = %s
        AND estado != 'Cancelada'
        """

        cursor.execute(
            query,
            (fecha, hora, id_horario_medico_fk)
        )

        resultado = cursor.fetchone()

        cursor.close()
        connection.close()

        return resultado


    def crear_cita(self, cita):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
        INSERT INTO citas(
            fecha,
            hora,
            estado,
            observacion,
            id_horario_medico_fk,
            id_paciente_fk
        )
        VALUES(%s,%s,%s,%s,%s,%s)
        """

        valores = (
            cita.fecha,
            cita.hora,
            'Agendada',
            cita.observacion,
            cita.id_horario_medico_fk,
            cita.id_paciente_fk
        )

        cursor.execute(query, valores)

        connection.commit()

        cita_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return {
            "id_cita": cita_id,
            "fecha": cita.fecha,
            "hora": cita.hora,
            "estado": "Agendada",
            "observacion": cita.observacion,
            "id_horario_medico_fk": cita.id_horario_medico_fk,
            "id_paciente_fk": cita.id_paciente_fk
        }