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
            
    def obtener_por_id(self, id_paciente: int) -> Optional[Paciente]:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM pacientes WHERE id_paciente = %s",
                (id_paciente,)
            )
            fila = cursor.fetchone()
            if not fila:
                return None
            paciente = Paciente(**fila)

            # Obtener alergias
            cursor.execute(
                "SELECT alergia FROM paciente_alergias WHERE id_paciente_fk = %s",
                (id_paciente,)
            )
            paciente.alergias = [row["alergia"] for row in cursor.fetchall()]

            # Obtener contactos
            cursor.execute(
                "SELECT id_contacto, tipo, dato_contacto FROM contactos WHERE id_paciente_fk = %s",
                (id_paciente,)
            )
            paciente.contactos = cursor.fetchall()

            return paciente
        finally:
            cursor.close()
            conexion.close()

    def actualizar_paciente(self, id_paciente: int, datos: dict) -> Optional[Paciente]:
        conexion = get_connection()
        try:
            # Construir el UPDATE solo con los campos que llegaron
            campos = ", ".join(f"{campo} = %s" for campo in datos.keys())
            valores = list(datos.values())
            valores.append(id_paciente)
            cursor = conexion.cursor()
            cursor.execute(
                f"UPDATE pacientes SET {campos} WHERE id_paciente = %s",
                valores
            )
            conexion.commit()
            return self.obtener_por_id(id_paciente)
        finally:
            cursor.close()
            conexion.close()
            
    def buscar_pacientes(self, criterio: str) -> list:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            busqueda = f"%{criterio}%"
            cursor.execute(
                """
                SELECT * FROM pacientes 
                WHERE nombre LIKE %s 
                OR primer_apellido LIKE %s 
                OR segundo_apellido LIKE %s
                OR numero_identificacion LIKE %s
                """,
                (busqueda, busqueda, busqueda, busqueda)
            )
            filas = cursor.fetchall()
            return [Paciente(**fila) for fila in filas]
        finally:
            cursor.close()
            conexion.close()
            
    def agregar_alergia(self, id_paciente_fk: int, alergia: str) -> dict:
        conexion = get_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO paciente_alergias (id_paciente_fk, alergia) VALUES (%s, %s)",
                (id_paciente_fk, alergia)
            )
            conexion.commit()
            return {"id": cursor.lastrowid, "id_paciente_fk": id_paciente_fk, "alergia": alergia}
        finally:
            cursor.close()
            conexion.close()

    def listar_alergias(self, id_paciente_fk: int) -> list:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, id_paciente_fk, alergia FROM paciente_alergias WHERE id_paciente_fk = %s",
                (id_paciente_fk,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    def eliminar_alergia(self, id_alergia: int, id_paciente_fk: int) -> bool:
        conexion = get_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "DELETE FROM paciente_alergias WHERE id = %s AND id_paciente_fk = %s",
                (id_alergia, id_paciente_fk)
            )
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conexion.close()