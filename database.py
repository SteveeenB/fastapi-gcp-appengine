import os
import psycopg2
def get_db_connection():
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_CONNECTION_NAME = os.getenv("DB_CONNECTION_NAME")

    connection_kwargs = {
        "database": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
    }

    if DB_CONNECTION_NAME:
        connection_kwargs["host"] = f"/cloudsql/{DB_CONNECTION_NAME}"
    else:
        connection_kwargs["host"] = DB_HOST
        connection_kwargs["port"] = DB_PORT

    return psycopg2.connect(**connection_kwargs)