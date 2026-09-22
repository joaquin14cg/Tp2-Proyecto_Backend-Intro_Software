import mysql.connector
import os

def obtener_conexion():
    conexion = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return conexion


def ejecutar_consulta(sql:str, parametros:tuple = None)->list[dict]:
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(sql, parametros or ())
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()

def ejecutar_mutacion(sql:str, parametros:tuple = None)->int:
    conexion = obtener_conexion() 
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(sql, parametros or ())
        conexion.commit()
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()

