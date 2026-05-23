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
    
    def obtener_cita(self, id_cita: int):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT * FROM citas
            WHERE id_cita = %s
        """

        cursor.execute(query, (id_cita,))
        cita = cursor.fetchone()

        cursor.close()
        connection.close()

        return cita

    def registrar_historial(
        self,
        id_cita: int,
        estado_anterior: str,
        estado_nuevo: str,
        motivo: str
    ):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO historial_citas (
                estado_anterior,
                estado_nuevo,
                motivo,
                id_cita_fk
            )
            VALUES (%s, %s, %s, %s)
        """

        valores = (
            estado_anterior,
            estado_nuevo,
            motivo,
            id_cita
        )

        cursor.execute(query, valores)

        connection.commit()

        cursor.close()
        connection.close()

    def cancelar_cita(self, id_cita: int):
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE citas
            SET estado = 'Cancelada'
            WHERE id_cita = %s
        """

        cursor.execute(query, (id_cita,))

        connection.commit()

        cursor.close()
        connection.close()

    def marcar_atendida(
        self,
        id_cita
    ):

        connection = get_connection()

        cursor = connection.cursor()

        query = """
        UPDATE citas
        SET estado = 'Atendida'
        WHERE id_cita = %s
        """

        cursor.execute(
            query,
            (id_cita,)
        )

        connection.commit()

        cursor.close()
        connection.close()
    
    def obtener_por_paciente(
        self,
        id_paciente,
        fecha_inicio=None,
        fecha_fin=None
    ):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            c.id_cita,
            c.fecha,
            c.hora,
            c.estado,
            CONCAT(
                m.nombre,
                ' ',
                m.primer_apellido
            ) AS medico_nombre
        FROM citas c
        INNER JOIN horarios_medicos hm
            ON c.id_horario_medico_fk = hm.id_horario_medico
        INNER JOIN medicos m
            ON hm.id_medico_fk = m.id_medico
        WHERE c.id_paciente_fk = %s
        """

        valores = [id_paciente]

        if fecha_inicio and fecha_fin:

            query += """
            AND c.fecha BETWEEN %s AND %s
            """

            valores.extend([fecha_inicio, fecha_fin])

        query += """
        ORDER BY c.fecha, c.hora
        """

        cursor.execute(query, tuple(valores))

        resultado = cursor.fetchall()

        cursor.close()
        connection.close()

        return resultado
    
    def obtener_por_medico(
        self,
        id_medico,
        fecha=None
    ):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            c.id_cita,
            c.fecha,
            c.hora,
            c.estado,
            CONCAT(
                p.nombre,
                ' ',
                p.primer_apellido
            ) AS paciente_nombre
        FROM citas c
        INNER JOIN horarios_medicos hm
            ON c.id_horario_medico_fk = hm.id_horario_medico
        INNER JOIN pacientes p
            ON c.id_paciente_fk = p.id_paciente
        WHERE hm.id_medico_fk = %s
        """

        valores = [id_medico]

        if fecha:

            query += """
            AND c.fecha = %s
            """

            valores.append(fecha)

        query += """
        ORDER BY c.fecha, c.hora
        """

        cursor.execute(query, tuple(valores))

        resultado = cursor.fetchall()

        cursor.close()
        connection.close()

        return resultado
    
    def obtener_citas_medico_fecha(
        self,
        id_medico,
        fecha
    ):

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT 
            c.id_cita,
            c.hora,
            c.estado,
            c.id_paciente_fk
        FROM citas c
        INNER JOIN horarios_medicos hm
            ON c.id_horario_medico_fk = hm.id_horario_medico
        WHERE hm.id_medico_fk = %s
        AND c.fecha = %s
        """

        cursor.execute(
            query,
            (id_medico, fecha)
        )

        citas = cursor.fetchall()

        cursor.close()
        connection.close()

        return citas
    
    def actualizar_cita(self, id_cita, datos):

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM citas WHERE id_cita = %s",
            (id_cita,)
        )

        cita = cursor.fetchone()

        if not cita:
            cursor.close()
            conexion.close()
            return None

        campos = []
        valores = []

        if "fecha" in datos:
            campos.append("fecha = %s")
            valores.append(datos["fecha"])

        if "hora" in datos:
            campos.append("hora = %s")
            valores.append(datos["hora"])

        if "observacion" in datos:
            campos.append("observacion = %s")
            valores.append(datos["observacion"])

        if campos:

            query = f"""
                UPDATE citas
                SET {", ".join(campos)}
                WHERE id_cita = %s
            """

            valores.append(id_cita)

            cursor.execute(query, tuple(valores))
            conexion.commit()

        cursor.close()
        conexion.close()

        return cita
    
    def obtener_cita_por_id(self, id_cita):

        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM citas WHERE id_cita = %s",
            (id_cita,)
        )

        cita = cursor.fetchone()

        cursor.close()
        conexion.close()

        return cita