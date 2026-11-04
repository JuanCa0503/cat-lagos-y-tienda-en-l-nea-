import os
import psycopg2
from psycopg2 import OperationalError

def conectar_base_datos():
    try:
        # Render y servicios en la nube inyectan las credenciales vía variables de entorno
        conexion = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", "5432")
        )
        print("¡Conexión exitosa a la base de datos en Render!")
        return conexion
    except OperationalError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

if __name__ == "__main__":
    conn = conectar_base_datos()
    if conn:
        conn.close()
