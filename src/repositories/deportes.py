from db obtener_conexion

def obtener_todos_los_deportes() -> list:
    conexion = obtener_conexion
    cursor = conexion.cursor(dictionary=True)
    consulta = "SELECT * FROM deportes"
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados