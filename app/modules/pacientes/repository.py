from typing import Optional
from app.core.database import get_connection
from app.modules.pacientes.model import Paciente
from app.modules.pacientes.contracts import IPacienteRepository


class PacienteRepository(IPacienteRepository):

    def obtener_por_identificacion(self, numero_identificacion: str) -> Optional[Paciente]:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM pacientes WHERE numero_identificacion = %s",
                (numero_identificacion,)
            )
            fila = cursor.fetchone()
            if not fila:
                return None
            return Paciente(**fila)
        finally:
            cursor.close()
            conexion.close()

    def crear_paciente(self, paciente: Paciente) -> Paciente:
        conexion = get_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                """
                INSERT INTO pacientes (
                    numero_identificacion, nombre, primer_apellido,
                    segundo_apellido, direccion, fecha_de_nacimiento,
                    id_eps_fk, id_regimen_fk, sexo, tipo_sangre
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    paciente.numero_identificacion,
                    paciente.nombre,
                    paciente.primer_apellido,
                    paciente.segundo_apellido,
                    paciente.direccion,
                    paciente.fecha_de_nacimiento,
                    paciente.id_eps_fk,
                    paciente.id_regimen_fk,
                    paciente.sexo,
                    paciente.tipo_sangre,
                )
            )
            conexion.commit()
            paciente.id_paciente = cursor.lastrowid
            return paciente
        finally:
            cursor.close()
            conexion.close()