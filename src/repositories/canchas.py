from db import obtener_conexion

def obtener_todas_las_canchas() -> list:
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM canchas")
    canchas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return canchas
    