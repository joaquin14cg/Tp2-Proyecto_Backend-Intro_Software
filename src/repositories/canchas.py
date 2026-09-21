from db import obtener_conexion

def obtener_todas_las_canchas() -> list:
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM canchas")
    canchas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return canchas
    
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