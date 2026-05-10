import os
from dotenv import load_dotenv
import mysql.connector.pooling

load_dotenv(override=True)

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "sgcm"),
    "pool_name": os.getenv("DB_POOL_NAME", "sgcm_pool"),
    "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
    "pool_reset_session": True,
}

_pool = mysql.connector.pooling.MySQLConnectionPool(**DATABASE_CONFIG)


def get_connection():
    """Return a pooled MySQL connection."""
    return _pool.get_connection()
