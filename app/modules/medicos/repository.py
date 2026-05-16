from app.core.database import get_connection


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