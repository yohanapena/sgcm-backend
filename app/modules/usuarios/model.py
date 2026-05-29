from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class UsuarioRol(str, Enum):
    ADMINISTRATIVO = "Administrativo"
    MEDICO = "Medico"
    ADMINISTRADOR = "Administrador"



class UsuarioEstado(str, Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"


@dataclass
class Usuario:
    usuario: str
    contrasena: str
    rol: UsuarioRol
    estado: UsuarioEstado
    fecha_creacion: datetime
    id_medico_fk: Optional[int] = None
    id_usuario: Optional[int] = None
    medico_nombre: Optional[str] = None
    nombre_completo: Optional[str] = None
