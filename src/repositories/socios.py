from db import (
    obtener_conexion,
    ejecutar_consulta,
    ejecutar_mutacion
    )


def existe_socio_con_email(email:str, excluir_id : int=0)->bool:
    sql = 'SELECT id FROM socios WHERE email = %s AND id != %s'
    filas = ejecutar_consulta(sql, (email,excluir_id))
    
    return len(filas) > 0

def guardar_socio(datos:dict)->dict:
    query = 'INSERT INTO socios (nombre , emaill, activo) values (%s, %s, %s)'
    valores = (datos['nombre'], datos['email'], datos['activo'])
    datos['id'] = ejecutar_mutacion(query, valores)
    return datos

def obtener_todos_los_socios()->list[dict]:
    sql = 'SELECT id, nombre, email, activo FROM socios ORDER BY id'
    return ejecutar_consulta(sql)

def obtener_socios_paginados(limit:int, offset:int)->list[dict]:
    sql = 'SELECT id, nombre, email, activo FROM socios ORDER BY id LIMIT %s OFFSET %s'
    return ejecutar_consulta(sql, (limit, offset))

def contar_total_socios()->int:
    sql = 'SELECT COUNT(*) AS total FROM socios'
    resultado = ejecutar_consulta(sql)
    return resultado[0]['total'] if resultado else 0

