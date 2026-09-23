from repositories import bloqueos as bloqueos_repo
from validators.bloqueos import validar_bloqueo
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

def crear_bloqueo(bloqueo_data):
    es_valido, mensaje = validar_bloqueo(bloqueo_data)

    if not es_valido:
        return construir_error_api("DATOS_INVALIDOS", mensaje, ""), 400

    bloqueos_repo.crear_bloqueo(bloqueo_data)


def borrar_bloqueo(id):
    bloqueo = bloqueos_repo.obtener_bloqueo_por_id(id)

    if bloqueo is None:
        return construir_error_api("BLOQUEO_NO_ENCONTRADO", "No existe un bloqueo con ese id", ""), 404

    bloqueos_repo.eliminar_bloqueo_db(id)

    return None, 204