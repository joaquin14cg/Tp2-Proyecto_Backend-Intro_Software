from db import (
    obtener_conexion,
    ejecutar_mutacion
    )


def existe_socio_con_email(email:str)->bool:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT 1 FROM socios WHERE email = %s' , (email,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado is not None

def guardar_socio(datos:dict)->dict:
    query = "INSERT INTO socios (nombre , emaill, activo) values (%s, %s, %s)"
    valores = (datos['nombre'], datos['email'], datos['activo'])
    datos['id'] = ejecutar_mutacion(query, valores)
    return datos
