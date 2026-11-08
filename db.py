"""
db.py · Conexión a MySQL (XAMPP en local, Aiven en producción).

Todos los datos de conexión se leen de VARIABLES DE ENTORNO:
  - En tu computadora vienen del archivo .env
  - En Render vienen de la sección "Environment"
Así las contraseñas NUNCA quedan escritas en el código ni en GitHub.
"""
import os

import pymysql
from dotenv import load_dotenv

load_dotenv()  # lee el archivo .env si existe (en Render no existe y no pasa nada)


def obtener_conexion():
    """Abre y regresa una conexión nueva a la base de datos."""
    opciones = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "tareas_db"),
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,
        "connect_timeout": 10,
    }

    # Aiven exige conexión cifrada (SSL). Si DB_SSL_CA tiene una ruta,
    # se usa ese certificado. En XAMPP se deja vacío.
    ruta_ca = os.getenv("DB_SSL_CA", "").strip()
    if ruta_ca:
        opciones["ssl"] = {"ca": ruta_ca}

    return pymysql.connect(**opciones)
