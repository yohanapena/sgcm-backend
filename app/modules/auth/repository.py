from typing import List, Optional

from app.core.database import get_connection
from app.modules.auth.contracts import IAuthRepository
from app.modules.usuarios.model import Usuario, UsuarioEstado, UsuarioRol
from app.modules.usuarios.repository import UsuarioRepository


class AuthRepository(IAuthRepository):
    def __init__(self):
        self._usuario_repository = UsuarioRepository()

    def obtener_usuario_por_nombre(self, usuario: str) -> Optional[Usuario]:
        conexion = get_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            query = (
                "SELECT u.id_usuario, u.usuario, u.contrasena, u.rol, u.estado, "
                "u.fecha_creacion, u.id_medico_fk, "
                "COALESCE(CONCAT(m.nombre, ' ', m.primer_apellido), u.usuario) AS nombre_completo "
                "FROM usuarios u "
                "LEFT JOIN medicos m ON u.id_medico_fk = m.id_medico "
                "WHERE u.usuario = %s"
            )
            cursor.execute(query, (usuario,))
            fila = cursor.fetchone()
            cursor.close()
            if fila is None:
                return None
            return Usuario(
                id_usuario=fila.get("id_usuario"),
                usuario=fila.get("usuario"),
                contrasena=fila.get("contrasena"),
                rol=UsuarioRol(fila.get("rol")),
                estado=UsuarioEstado(fila.get("estado")),
                fecha_creacion=fila.get("fecha_creacion"),
                id_medico_fk=fila.get("id_medico_fk"),
                nombre_completo=fila.get("nombre_completo"),
            )
        finally:
            conexion.close()

    def listar_usuarios(self) -> List[Usuario]:
        return self._usuario_repository.listar_usuarios()

    def cambiar_estado_usuario(self, id_usuario: int, estado: str) -> Usuario:
        return self._usuario_repository.cambiar_estado(id_usuario, estado)

    def crear_usuario(self, usuario: Usuario) -> Usuario:
        return self._usuario_repository.crear_usuario(usuario)

    def obtener_usuario_por_id(self, id_usuario: int) -> Optional[Usuario]:
        return self._usuario_repository.obtener_por_id(id_usuario)
