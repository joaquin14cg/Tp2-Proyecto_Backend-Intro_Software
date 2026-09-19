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