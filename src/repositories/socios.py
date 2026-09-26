from db import (
    ejecutar_consulta,
    ejecutar_mutacion
    )


def existe_socio_con_email(email:str, excluir_id : int=0)->bool:
    sql = 'SELECT id FROM socios WHERE email = %s AND id != %s'
    filas = ejecutar_consulta(sql, (email,excluir_id))
    
    return len(filas) > 0

def guardar_socio(datos:dict)->dict:
    query = 'INSERT INTO socios (nombre , email, activo) values (%s, %s, %s)'
    valores = (datos['nombre'], datos['email'], datos['activo'])
    datos['id'] = ejecutar_mutacion(query, valores)
    return datos

def obtener_todos_los_socios()->list[dict]:
    sql = 'SELECT id, nombre, email, activo FROM socios ORDER BY id'
    return ejecutar_consulta(sql)

def obtener_socios_paginados(limit:int, offset:int, nombre: str = None, activo : bool = None)->list:
    sql = 'SELECT id, nombre, email, activo FROM socios WHERE 1=1'
    params = []
    if nombre is not None:
        sql += ' AND LOWER(nombre) LIKE LOWER(%s)'
        params.append(f"%{nombre}%")
    if activo is not None:
        sql += 'AND activo = %s'
        params.append(activo)    
    sql += ' ORDER BY id ASC LIMIT %s OFFSET %s'
    params.extend([limit, offset])
    return ejecutar_consulta(sql, params)


def contar_total_socios(nombre: str = None, activo: bool = None) -> int:
    sql = 'SELECT COUNT(*) AS total FROM socios WHERE 1=1'
    params = []

    if nombre is not None:
        sql += ' AND LOWER(nombre) LIKE LOWER(%s)'
        params.append(f"%{nombre}%")

    if activo is not None:
        sql += ' AND activo = %s'
        params.append(activo)

    resultado = ejecutar_consulta(sql, params)

    return resultado[0]['total'] if resultado else 0


def obtener_socio_por_id(id_socio: int) -> dict:
    sql = "SELECT id, nombre, email, activo FROM socios WHERE id = %s"
    filas = ejecutar_consulta(sql, (id_socio,))
    return filas[0] if filas else None

def actualizar_socio(id_socio: int, datos: dict) -> dict:
    campos = []
    valores = []

    for campo, valor in datos.items():
        campos.append(f"{campo} = %s")
        valores.append(valor)

    valores.append(id_socio)

    sql = f"""
        UPDATE socios
        SET {', '.join(campos)}
        WHERE id = %s
    """

    ejecutar_mutacion(sql, valores)

    return obtener_socio_por_id(id_socio)