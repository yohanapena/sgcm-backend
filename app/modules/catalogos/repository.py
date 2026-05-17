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