import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os

def obtenerConexion():
    try:
        conexion = psycopg2.connect(
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD")
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos: ", e)
        raise
