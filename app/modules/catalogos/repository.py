from app.core.database import get_connection


class CatalogoRepository:

    def obtener_servicios(self) -> list:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id_servicio, nombre, descripcion FROM servicios")
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    def listar_eps(self) -> list:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id_eps, nit_eps, nombre_eps FROM eps")
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    def listar_regimenes(self) -> list:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id_regimen, tipo_regimen FROM regimenes")
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    def listar_especialidades(self) -> list:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id_especialidad, nombre_especialidad, descripcion FROM especialidades")
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()