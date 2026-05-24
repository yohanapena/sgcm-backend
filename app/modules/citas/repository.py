from app.core.database import get_connection
from datetime import timedelta

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

    def cancelar_cita(self, id_cita: int, motivo: str):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            UPDATE citas
            SET estado = 'Cancelada',
                observacion = %s
            WHERE id_cita = %s
        """

        cursor.execute(query, (motivo, id_cita))

        connection.commit()

        cursor.execute(
            "SELECT * FROM citas WHERE id_cita = %s",
            (id_cita,)
        )

        cita_actualizada = cursor.fetchone()

        cursor.close()
        connection.close()

        return cita_actualizada

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

    def listar_citas(
        self,
        medico_id: int = None,
        paciente_id: int = None,
        estado: str = None
    ):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            c.id_cita,
            c.fecha,
            c.hora,
            c.estado,
            c.observacion,
            c.id_horario_medico_fk,
            c.id_paciente_fk,
            p.nombre as paciente_nombre,
            p.primer_apellido as paciente_apellido,
            m.nombre as medico_nombre,
            m.primer_apellido as medico_apellido,
            e.nombre_especialidad as especialidad
        FROM citas c
        LEFT JOIN pacientes p ON p.id_paciente = c.id_paciente_fk
        LEFT JOIN horarios_medicos hm ON hm.id_horario_medico = c.id_horario_medico_fk
        LEFT JOIN medicos m ON m.id_medico = hm.id_medico_fk
        LEFT JOIN especialidades_medicos em ON em.id_medico_fk = m.id_medico
            AND em.id_especialidad_fk = (
                SELECT MIN(id_especialidad_fk)
                FROM especialidades_medicos
                WHERE id_medico_fk = m.id_medico
            )
        LEFT JOIN especialidades e ON e.id_especialidad = em.id_especialidad_fk
        """

        condiciones = []
        valores = []

        if medico_id is not None:
            condiciones.append("hm.id_medico_fk = %s")
            valores.append(medico_id)
        if paciente_id is not None:
            condiciones.append("c.id_paciente_fk = %s")
            valores.append(paciente_id)
        if estado is not None:
            condiciones.append("c.estado = %s")
            valores.append(estado)

        if condiciones:
            query += "\nWHERE " + " AND ".join(condiciones)

        query += "\nORDER BY c.fecha, c.hora"

        cursor.execute(query, tuple(valores))
        resultados = cursor.fetchall()

        # Convertir campos hora (tiempo) que MySQL puede devolver como timedelta
        for row in resultados:
            if "hora" in row and isinstance(row["hora"], timedelta):
                total_seconds = int(row["hora"].total_seconds())
                horas = total_seconds // 3600
                minutos = (total_seconds % 3600) // 60
                segundos = total_seconds % 60
                row["hora"] = f"{horas:02}:{minutos:02}:{segundos:02}"

        cursor.close()
        connection.close()
        return resultados
    
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