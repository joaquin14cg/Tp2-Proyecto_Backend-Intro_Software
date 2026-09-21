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

def ejecutar_mutacion(sql:str, parametros:tuple = None)->int:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(sql, parametros or ())
        conexion.commit()
        ultimo_id = cursor.lastwrid
        return ultimo_id
    finally:
        cursor.close()
        conexion.close()