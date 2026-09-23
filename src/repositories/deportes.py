from db import obtener_conexion

def obtener_todos_los_deportes() -> list:
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM deportes")
    deportes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return deportes

def obtener_deporte_por_id(id_deporte: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM deportes WHERE id = %s",(id_deporte,))
    deporte = cursor.fetone()
    cursor.close()
    conexion.close()
    return deporte
