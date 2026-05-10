import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import bcrypt
import jwt

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))


def hashear_contrasena(contrasena: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(contrasena.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verificar_contrasena(contrasena_plana: str, contrasena_hashed: str) -> bool:
    return bcrypt.checkpw(contrasena_plana.encode("utf-8"), contrasena_hashed.encode("utf-8"))


def crear_token(payload: dict, expires_minutes: int = JWT_EXPIRES_MINUTES) -> str:
    data = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decodificar_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
