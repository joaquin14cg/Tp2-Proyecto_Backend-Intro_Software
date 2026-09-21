from flask import Blueprint, request, jsonify
from repositories import bloqueos as bloqueos_repo
from utils import construir_error_api

def obtener_bloqueos():

    bloqueos_db = bloqueos_repo.obtener_bloqueos()

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


def borrar_bloqueo(id):
    bloqueo = bloqueos_repo.obtener_bloqueo_por_id(id)

    if bloqueo is None:
        return construir_error_api("BLOQUEO_NO_ENCONTRADO", "No existe un bloqueo con ese id", ""), 404

    bloqueos_repo.eliminar_bloqueo_db(id)

    return None, 204