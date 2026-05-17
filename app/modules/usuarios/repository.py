from typing import List, Optional

from app.core.database import get_connection
from app.modules.usuarios.contracts import IUsuarioRepository
from app.modules.usuarios.model import Usuario, UsuarioRol, UsuarioEstado
from app.modules.usuarios.schema import UsuarioActualizarRequest


class UsuarioRepository(IUsuarioRepository):
    def crear_usuario(self, usuario: Usuario) -> Usuario:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            query = (
                "INSERT INTO usuarios (usuario, contrasena, rol, estado, fecha_creacion, id_medico_fk) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(
                query,
                (
                    usuario.usuario,
                    usuario.contrasena,
                    usuario.rol.value,
                    usuario.estado.value,
                    usuario.fecha_creacion,
                    usuario.id_medico_fk,
                ),
            )
            conexion.commit()
            id_usuario = cursor.lastrowid
            cursor.close()
            return self.obtener_por_id(id_usuario)
        finally:
            conexion.close()

    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            query = (
                "SELECT u.id_usuario, u.usuario, u.contrasena, u.rol, u.estado, "
                "u.fecha_creacion, u.id_medico_fk, m.nombre AS medico_nombre "
                "FROM usuarios u "
                "LEFT JOIN medicos m ON u.id_medico_fk = m.id_medico "
                "WHERE u.id_usuario = %s"
            )
            cursor.execute(query, (id_usuario,))
            fila = cursor.fetchone()
            cursor.close()
            if fila is None:
                return None
            return self._mapear_usuario(fila)
        finally:
            conexion.close()

    def listar_usuarios(self) -> List[Usuario]:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            query = (
                "SELECT u.id_usuario, u.usuario, u.contrasena, u.rol, u.estado, "
                "u.fecha_creacion, u.id_medico_fk, m.nombre AS medico_nombre "
                "FROM usuarios u "
                "LEFT JOIN medicos m ON u.id_medico_fk = m.id_medico "
                "ORDER BY u.fecha_creacion DESC"
            )
            cursor.execute(query)
            filas = cursor.fetchall()
            cursor.close()
            return [self._mapear_usuario(fila) for fila in filas]
        finally:
            conexion.close()

    def cambiar_estado(self, id_usuario: int, estado: str) -> Usuario:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "UPDATE usuarios SET estado = %s WHERE id_usuario = %s"
            cursor.execute(query, (estado, id_usuario))
            conexion.commit()
            cursor.close()
            usuario = self.obtener_por_id(id_usuario)
            if usuario is None:
                raise ValueError("Usuario no encontrado")
            return usuario
        finally:
            conexion.close()

    def obtener_por_nombre(self, usuario: str) -> Optional[Usuario]:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            query = (
                "SELECT u.id_usuario, u.usuario, u.contrasena, u.rol, u.estado, "
                "u.fecha_creacion, u.id_medico_fk, m.nombre AS medico_nombre "
                "FROM usuarios u "
                "LEFT JOIN medicos m ON u.id_medico_fk = m.id_medico "
                "WHERE u.usuario = %s"
            )
            cursor.execute(query, (usuario,))
            fila = cursor.fetchone()
            cursor.close()
            return self._mapear_usuario(fila) if fila else None
        finally:
            conexion.close()

    def actualizar_usuario(self, id_usuario: int, datos: UsuarioActualizarRequest) -> Usuario:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            campos = []
            valores = []
            if datos.usuario is not None:
                campos.append("usuario = %s")
                valores.append(datos.usuario)
            if datos.rol is not None:
                campos.append("rol = %s")
                valores.append(datos.rol.value)
            if datos.estado is not None:
                campos.append("estado = %s")
                valores.append(datos.estado.value)
            if datos.id_medico_fk is not None:
                campos.append("id_medico_fk = %s")
                valores.append(datos.id_medico_fk)

            if not campos:
                cursor.close()
                return self.obtener_por_id(id_usuario)

            query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = %s"
            valores.append(id_usuario)
            cursor.execute(query, tuple(valores))
            conexion.commit()
            cursor.close()
            usuario = self.obtener_por_id(id_usuario)
            if usuario is None:
                raise ValueError("Usuario no encontrado")
            return usuario
        finally:
            conexion.close()

    def _mapear_usuario(self, fila: dict) -> Usuario:
        return Usuario(
            id_usuario=fila.get("id_usuario"),
            usuario=fila.get("usuario"),
            contrasena=fila.get("contrasena"),
            rol=UsuarioRol(fila.get("rol")),
            estado=UsuarioEstado(fila.get("estado")),
            fecha_creacion=fila.get("fecha_creacion"),
            id_medico_fk=fila.get("id_medico_fk"),
            medico_nombre=fila.get("medico_nombre"),
        )
