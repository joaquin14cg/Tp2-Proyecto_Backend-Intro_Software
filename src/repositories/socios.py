from db import obtener_conexion



def existe_socio_con_email(email:str)->bool:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT 1 FROM socios WHERE email = %s' , (email,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado is not None