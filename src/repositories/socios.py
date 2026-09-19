from db import obtener_conexion



def validar_email_disponible(email:str)->bool:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT 1 FROM socios WHERE email = %s' , (email,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado is not None