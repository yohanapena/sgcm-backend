from typing import Optional

from pydantic import BaseModel
from app.modules.usuarios.schema import UsuarioResponse


class LoginRequest(BaseModel):
    usuario: str
    contrasena: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: str
    rol: str
    id_medico_fk: Optional[int] = None


class MeResponse(BaseModel):
    id_usuario: int
    usuario: str
    rol: str
    id_medico_fk: Optional[int] = None


class MeDataResponse(BaseModel):
    data: MeResponse


class UsuarioDataResponse(BaseModel):
    data: UsuarioResponse
