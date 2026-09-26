from db import obtener_conexion

def obtener_todas_las_canchas() -> list:
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM canchas")
    canchas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return canchas

def crear_cancha(nombre: str, id_deporte: int, precio_hora: int, techada: bool, activa: bool) -> int:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(consulta,(nombre, id_deporte, precio_hora, techada, activa))
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    return nuevo_id
    
def obtener_cancha_por_id(id_cancha: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM canchas WHERE id = %s", (id_cancha,))
    cancha = cursor.fetchone()
    cursor.close()
    conexion.close()

    return cancha

def tiene_reservas(id_cancha: int) -> bool:
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT 1 FROM reservas WHERE cancha_id = %s LIMIT 1",(id_cancha,))
    reserva = cursor.fetchone()
    cursor.close()
    conexion.close()

    return reserva is not None

def eliminar_cancha(id_cancha: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM canchas WHERE id = %s",(id_cancha,))
    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar_cancha(id_cancha: int, datos: dict):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    campos = []
    valores = []

    for campo, valor in datos.items():
        campos.append(f"{campo} = %s")
        valores.append(valor)

    valores.append(id_cancha)

    consulta = f"""
        UPDATE canchas
        SET {', '.join(campos)}
        WHERE id = %s
    """

    cursor.execute(consulta, tuple(valores))
    conexion.commit()
    cursor.close()
    conexion.close()


# Esta funcion debe recibir un limit y un offset, y opcionalmente id_deporte, nombre, techada y activa, se ponen en None automaticamente si no se pasan
# Los if lo que hacen es que si se pasan los parametros opcionales, se agregan a la lista de condiciones y a la lista de parametros, para luego armar la consulta SQL con un WHERE que contenga todas las condiciones concatenadas con AND
def obtener_canchas_paginadas(limit, offset, id_deporte=None, nombre=None, techada=None, activa=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    condiciones = []
    params = []

    if id_deporte is not None:
        condiciones.append("id_deporte = %s")
        params.append(id_deporte)

    if nombre is not None:
        condiciones.append("LOWER(nombre) LIKE LOWER(%s)")
        params.append(f"%{nombre}%")

    if techada is not None:
        condiciones.append("techada = %s")
        params.append(techada)

    if activa is not None:
        condiciones.append("activa = %s")
        params.append(activa)

    where = ""
    if condiciones:
        where = "WHERE " + " AND ".join(condiciones)

    cursor.execute(f"SELECT * FROM canchas {where} ORDER BY id ASC LIMIT %s OFFSET %s", params + [limit, offset])
    canchas = cursor.fetchall()

    cursor.close()
    conexion.close()
    return canchas

def contar_canchas(id_deporte=None, nombre=None, techada=None, activa=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    condiciones = []
    params = []
    if id_deporte is not None:
        condiciones.append("id_deporte = %s")
        params.append(id_deporte)
    if nombre is not None:
        condiciones.append("LOWER(nombre) LIKE LOWER(%s)")
        params.append(f"%{nombre}%")
    if techada is not None:
        condiciones.append("techada = %s")
        params.append(techada)
    if activa is not None:
        condiciones.append("activa = %s")
        params.append(activa)

    where = ""
    if condiciones:
        where = "WHERE " + " AND ".join(condiciones)

    cursor.execute(f"SELECT COUNT(*) AS total FROM canchas {where}", params)
    total = cursor.fetchone()["total"]

    cursor.close()
    conexion.close()
    return total