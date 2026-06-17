from sqlalchemy import create_engine, text
import urllib.parse

DB_USER = "root"
DB_PASSWORD = "mysql"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "tpi_rendimiento_academico"


def obtener_engine(con_base=True):
    # URL-encode de la contraseña en caso de caracteres especiales
    password_encoded = urllib.parse.quote(DB_PASSWORD, safe='')
    base = f"mysql+pymysql://{DB_USER}:{password_encoded}@{DB_HOST}:{DB_PORT}"
    url = f"{base}/{DB_NAME}" if con_base else base
    return create_engine(url)


def inicializar_base():
    engine = obtener_engine(con_base=False)
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.commit()
    print(f"Base de datos '{DB_NAME}' lista")
    return obtener_engine()


def verificar_conexion():
    try:
        engine = obtener_engine(con_base=False)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Conexion exitosa al servidor MySQL")
        return True
    except Exception as e:
        print(f"Error de conexion: {e}")
        return False
