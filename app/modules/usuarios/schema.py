from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class UsuarioRol(str, Enum):
    ADMINISTRATIVO = "Administrativo"
    MEDICO = "Medico"
    ADMINISTRADOR = "Administrador"


class UsuarioEstado(str, Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"


class UsuarioCrearRequest(BaseModel):
    usuario: str = Field(..., min_length=3, max_length=50)
    contrasena: str = Field(..., min_length=6)
    rol: UsuarioRol
    estado: UsuarioEstado = UsuarioEstado.ACTIVO
    id_medico_fk: Optional[int] = None

    @model_validator(mode="after")
    def validar_medico(self):
        if self.rol == UsuarioRol.MEDICO and self.id_medico_fk is None:
            raise ValueError("El campo id_medico_fk es obligatorio cuando el rol es Medico")
        return self


class UsuarioActualizarRequest(BaseModel):
    usuario: Optional[str] = Field(None, min_length=3, max_length=50)
    contrasena: Optional[str] = None
    rol: Optional[UsuarioRol] = None
    estado: Optional[UsuarioEstado] = None
    id_medico_fk: Optional[int] = None


    @model_validator(mode="after")
    def validar_medico(self):
        if self.rol == UsuarioRol.MEDICO and self.id_medico_fk is None:
            raise ValueError("El campo id_medico_fk es obligatorio cuando el rol es Medico")
        return self


class UsuarioEstadoRequest(BaseModel):
    estado: UsuarioEstado


class UsuarioResponse(BaseModel):
    id_usuario: int
    usuario: str
    rol: UsuarioRol
    estado: UsuarioEstado
    fecha_creacion: datetime
    id_medico_fk: Optional[int] = None
    medico_nombre: Optional[str] = None

    class Config:
        from_attributes = True
