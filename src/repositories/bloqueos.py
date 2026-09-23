from db import obtener_conexion


def obtener_bloqueos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True) #El cursor es el objeto que utilizás para ejecutar SQL.

    cursor.execute(""" 
        SELECT id, cancha_id, fecha_bloqueo, inicio, fin, motivo
        FROM bloqueos
    """) #Ejecuta la consulta SQL para obtener todos los bloqueos de la base de datos.

    bloqueos = cursor.fetchall() #Trae todos los resultados de la consulta y los guarda en la variable bloqueos.

    cursor.close()
    conexion.close()

    return bloqueos

def crear_bloqueo(bloqueo_data):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO bloqueos (cancha_id, fecha_bloqueo, inicio, fin, motivo)
        VALUES (%s, %s, %s, %s, %s)
    """, (bloqueo_data['cancha_id'], bloqueo_data['fecha_bloqueo'], bloqueo_data['inicio'], bloqueo_data['fin'], bloqueo_data['motivo']))

    conexion.commit()

    cursor.close()
    conexion.close(

        
    )
def obtener_bloqueo_por_id(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT id, cancha_id, fecha_bloqueo, inicio, fin, motivo FROM bloqueos WHERE id = %s", (id,))

    bloqueo = cursor.fetchone()

    cursor.close()
    conexion.close()

    return bloqueo


def eliminar_bloqueo_db(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM bloqueos WHERE id = %s", (id,))
    conexion.commit()

    cursor.close()
    conexion.close()