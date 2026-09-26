from src.repositories import bloqueos as bloqueos_repo
from src.repositories import canchas as canchas_repo
from src.validators.bloqueos import validar_bloqueo
from src.repositories import reservas as reservas_repo
from utils import construir_error_api


def obtener_bloqueos():
    bloqueos_db = bloqueos_repo.obtener_bloqueos()
    resultados = []

    for bloqueo in bloqueos_db:
        resultados.append({
            'id': bloqueo['id'],
            'cancha_id': bloqueo['cancha_id'],
            'fecha_bloqueo': bloqueo['fecha_bloqueo'].isoformat(),
            'inicio': bloqueo['inicio'].isoformat(),
            'fin': bloqueo['fin'].isoformat(),
            'motivo': bloqueo['motivo']
        })

    return resultados

def crear_bloqueo(bloqueo_data):

    es_valido, mensaje = validar_bloqueo(bloqueo_data)

    if not es_valido:
        return construir_error_api(
            "DATOS_INVALIDOS",
            mensaje,
            ""
        ), 400

    existe_cancha = canchas_repo.existe_cancha(
        bloqueo_data["cancha_id"]
    )

    if not existe_cancha:
        return construir_error_api(
            "CANCHA_NO_ENCONTRADA",
            "No existe una cancha con el id indicado.",
            ""
        ), 404

    existe_reserva = reservas_repo.existe_reserva_confirmada_superpuesta(
        bloqueo_data["cancha_id"],
        bloqueo_data["inicio"],
        bloqueo_data["fin"]
    )

    if existe_reserva:
        return construir_error_api(
            "BLOQUEO_NO_DISPONIBLE",
            "No se puede crear el bloqueo porque se superpone con una reserva confirmada.",
            ""
        ), 409

    existe_bloqueo = bloqueos_repo.existe_bloqueo_superpuesto(
        bloqueo_data["cancha_id"],
        bloqueo_data["inicio"],
        bloqueo_data["fin"]
    )

    if existe_bloqueo:
        return construir_error_api(
            "BLOQUEO_SUPERPUESTO",
            "No se puede crear el bloqueo porque se superpone con otro bloqueo de la misma cancha.",
            ""
        ), 409

    id_bloqueo = bloqueos_repo.crear_bloqueo(bloqueo_data)

    resultado = {
        "id": id_bloqueo,
        "cancha_id": bloqueo_data["cancha_id"],
        "fecha_bloqueo": bloqueo_data["fecha_bloqueo"],
        "inicio": bloqueo_data["inicio"],
        "fin": bloqueo_data["fin"],
        "motivo": bloqueo_data["motivo"].strip()
    }

    return resultado, 201

def borrar_bloqueo(id):
    bloqueo = bloqueos_repo.obtener_bloqueo_por_id(id)

    if bloqueo is None:
        return construir_error_api("BLOQUEO_NO_ENCONTRADO", "No existe un bloqueo con ese id", ""), 404

    bloqueos_repo.eliminar_bloqueo_db(id)

    return None, 204