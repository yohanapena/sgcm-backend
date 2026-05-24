import os
from typing import Any, Dict
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from app.core.security import decodificar_token

security = HTTPBearer(auto_error=False)


def _obtener_token_credenciales(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token de autorización no válido")
    return credentials.credentials


def get_usuario_actual(token: str = Depends(_obtener_token_credenciales)) -> Dict[str, Any]:
    try:
        payload = decodificar_token(token)
    except Exception:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    if "id_usuario" not in payload or "rol" not in payload:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token incompleto")

    return payload


def solo_administrativo(usuario_actual: dict = Depends(get_usuario_actual)) -> dict:
    if usuario_actual.get("rol") not in ["Administrativo", "Administrador"]:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="No autorizado")
    return usuario_actual


def solo_medico(usuario_actual: dict = Depends(get_usuario_actual)) -> dict:
    if usuario_actual.get("rol") != "Medico":
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Requiere rol médico")
    return usuario_actual


def administrativo_o_medico(usuario_actual: dict = Depends(get_usuario_actual)) -> dict:
    if usuario_actual.get("rol") not in {"Administrativo", "Medico"}:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Requiere rol administrativo o médico")
    return usuario_actual
