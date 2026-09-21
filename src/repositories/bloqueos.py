from flask import Blueprint, request, jsonify
from db import obtener_conexion


def obtener_bloqueos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True) #El cursor es el objeto que utilizás para ejecutar SQL.

    cursor.execute("""
        SELECT id, cancha_id, fecha_bloqueo, inicio, fin, motivo
        FROM bloqueos
    """)

    bloqueos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return bloqueos


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