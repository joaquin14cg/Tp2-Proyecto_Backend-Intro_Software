from flask import Blueprint, request, jsonify
from repositories import bloqueos

def obtener_bloqueos():

    bloqueos_db = bloqueos.obtener_bloqueos()

    resultados = []

    for bloqueo in bloqueos_db:
        resultados.append({
            'id': bloqueo.id,
            'cancha_id': bloqueo.cancha_id,
            'fecha_bloqueo': bloqueo.fecha_bloqueo.isoformat(),
            "inicio": bloqueo.inicio,
            "fin":bloqueo.fin,
            'motivo': bloqueo.motivo
        })

    return resultados