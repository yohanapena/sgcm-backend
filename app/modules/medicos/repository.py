from app.core.database import get_connection
from datetime import timedelta

class MedicoRepository:

    def crear_medico(self, medico):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        INSERT INTO medicos (
            nombre,
            primer_apellido,
            segundo_apellido,
            tarjeta_profesional
        )
        VALUES (%s, %s, %s, %s)
        """

        valores = (
            medico.nombre,
            medico.primer_apellido,
            medico.segundo_apellido,
            medico.tarjeta_profesional
        )

        cursor.execute(query, valores)

        connection.commit()

        id_medico = cursor.lastrowid

        cursor.close()
        connection.close()

        return id_medico

    def agregar_especialidad(
        self,
        id_medico,
        id_especialidad
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT IGNORE INTO especialidades_medicos (
            id_medico_fk,
            id_especialidad_fk
        )
        VALUES (%s, %s)
        """

        cursor.execute(
            query,
            (id_medico, id_especialidad)
        )

        connection.commit()

        cursor.close()
        connection.close()

    def buscar_tarjeta_profesional(
        self,
        tarjeta_profesional
    ):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM medicos
        WHERE tarjeta_profesional = %s
        """

        cursor.execute(
            query,
            (tarjeta_profesional,)
        )

        resultado = cursor.fetchone()

        cursor.close()
        connection.close()

        return resultado
    
    def verificar_superposicion(
        self,
        id_medico,
        dia_semana,
        hora_inicial,
        hora_final
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
        SELECT *
        FROM horarios_medicos
        WHERE id_medico_fk = %s
        AND dia_semana = %s
        AND (
            (%s BETWEEN hora_inicial AND hora_final)
            OR
            (%s BETWEEN hora_inicial AND hora_final)
            OR
            (hora_inicial BETWEEN %s AND %s)
        )
        """

        cursor.execute(
            query,
            (
                id_medico,
                dia_semana,
                hora_inicial,
                hora_final,
                hora_inicial,
                hora_final
            )
        )

        resultado = cursor.fetchone()

        cursor.close()
        connection.close()

        return resultado
    
    def crear_horario(
        self,
        id_medico,
        horario
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
        INSERT INTO horarios_medicos (
            dia_semana,
            fecha_vigencia_inicio,
            fecha_vigencia_fin,
            hora_inicial,
            hora_final,
            id_medico_fk
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            horario.dia_semana,
            horario.fecha_vigencia_inicio,
            horario.fecha_vigencia_fin,
            horario.hora_inicial,
            horario.hora_final,
            id_medico
        )

        cursor.execute(query, valores)

        connection.commit()

        id_horario = cursor.lastrowid

        cursor.close()
        connection.close()

        return {
            "id_horario_medico": id_horario,
            "dia_semana": horario.dia_semana,
            "fecha_vigencia_inicio": horario.fecha_vigencia_inicio,
            "fecha_vigencia_fin": horario.fecha_vigencia_fin,
            "hora_inicial": horario.hora_inicial,
            "hora_final": horario.hora_final,
            "id_medico_fk": id_medico
        }
    
    def obtener_horarios(
        self,
        id_medico
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
       )

        query = """
        SELECT *
        FROM horarios_medicos
        WHERE id_medico_fk = %s
        """

        cursor.execute(
            query,
            (id_medico,)
        )

        resultados = cursor.fetchall()

        for horario in resultados:

            if isinstance(horario["hora_inicial"], timedelta):

                total_seconds = int(
                    horario["hora_inicial"].total_seconds()
                )

                horas = total_seconds // 3600
                minutos = (total_seconds % 3600) // 60
                segundos = total_seconds % 60

                horario["hora_inicial"] = (
                    f"{horas:02}:{minutos:02}:{segundos:02}"
                )

            if isinstance(horario["hora_final"], timedelta):

                total_seconds = int(
                    horario["hora_final"].total_seconds()
                )

                horas = total_seconds // 3600
                minutos = (total_seconds % 3600) // 60
                segundos = total_seconds % 60

                horario["hora_final"] = (
                    f"{horas:02}:{minutos:02}:{segundos:02}"
                )

        cursor.close()
        connection.close()

        return resultados
    
    def obtener_medico_por_id(self, id_medico):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM medicos WHERE id_medico = %s",
            (id_medico,)
        )

        medico = cursor.fetchone()

        cursor.close()
        connection.close()

        return medico
    
    def actualizar_medico(self, id_medico, medico):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            UPDATE medicos
            SET nombre = %s,
                primer_apellido = %s,
                segundo_apellido = %s,
                tarjeta_profesional = %s,
                estado = %s
            WHERE id_medico = %s
        """

        valores = (
            medico.nombre,
            medico.primer_apellido,
            medico.segundo_apellido,
            medico.tarjeta_profesional,
            medico.estado,
            id_medico
        )

        cursor.execute(query, valores)

        connection.commit()

        cursor.execute(
            "SELECT * FROM medicos WHERE id_medico = %s",
            (id_medico,)
        )

        medico_actualizado = cursor.fetchone()

        cursor.close()
        connection.close()

        return medico_actualizado