from typing import Literal, Optional

from pydantic import BaseModel
from app.modules.usuarios.schema import UsuarioResponse


class LoginRequest(BaseModel):
    usuario: str
    contrasena: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    id_usuario: int
    usuario: str
    rol: Literal['Administrativo', 'Medico', 'Administrador']
    estado: str
    id_medico_fk: Optional[int] = None
    nombre_completo: Optional[str] = None


class LoginUser(BaseModel):
    id_usuario: int
    usuario: str
    rol: Literal['Administrativo', 'Medico', 'Administrador']
    estado: str
    id_medico_fk: Optional[int] = None
    nombre_completo: Optional[str] = None


class LoginData(BaseModel):
    token: str
    user: LoginUser


class LoginDataResponse(BaseModel):
    data: LoginData


class MeResponse(BaseModel):
    id_usuario: int
    usuario: str
    rol: Literal['Administrativo', 'Medico', 'Administrador']
    id_medico_fk: Optional[int] = None


class MeDataResponse(BaseModel):
    data: MeResponse


class UsuarioDataResponse(BaseModel):
    data: UsuarioResponse


class UsuarioEstadoResponse(BaseModel):
    id_usuario: int
    status: str


class UsuarioEstadoDataResponse(BaseModel):
    data: UsuarioEstadoResponse
