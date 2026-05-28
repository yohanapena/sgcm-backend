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
    "charset": "utf8mb4",
    "use_unicode": True,
    "collation": "utf8mb4_unicode_ci",
}

_pool = mysql.connector.pooling.MySQLConnectionPool(**DATABASE_CONFIG)


def get_connection():
    """Return a pooled MySQL connection."""
    conn = _pool.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SET NAMES utf8mb4")
        cur.execute("SET CHARACTER SET utf8mb4")
        cur.close()
    except Exception:
        # If setting session charset fails, return the connection anyway
        pass
    return conn
