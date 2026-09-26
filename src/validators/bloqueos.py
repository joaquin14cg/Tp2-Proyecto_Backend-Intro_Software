
from datetime import datetime, timedelta, timezone


# Horario de atención del club.
HORA_APERTURA = 8
HORA_CIERRE = 23

# El contrato establece que toda fecha/hora se interpreta
# en GMT-3 y no se realiza conversión de zona horaria.
ZONA_HORARIA_GMT3 = timezone(timedelta(hours=-3))

FORMATO_FECHA = "%Y-%m-%d"
FORMATO_FECHA_HORA = "%Y-%m-%dT%H:%M:%S.%f%z"


def validar_bloqueo(bloqueo_data):

    # El cuerpo debe ser un objeto JSON.
    if not isinstance(bloqueo_data, dict):
        return False, "El cuerpo de la solicitud debe ser un objeto JSON."

    campos_requeridos = {
        "cancha_id",
        "fecha_bloqueo",
        "inicio",
        "fin",
        "motivo"
    }

    campos_permitidos = campos_requeridos


    for campo in bloqueo_data:
        if campo not in campos_permitidos:
            return False, f"El campo '{campo}' no está permitido."

    # Esto también rechaza explícitamente un "id".
    # El servidor genera el identificador automáticamente.

    for campo in campos_requeridos:
        if campo not in bloqueo_data:
            return False, f"El campo '{campo}' es requerido."

    for campo in campos_requeridos:
        valor = bloqueo_data[campo]

        if valor is None:
            return False, f"El campo '{campo}' no puede ser null."

        if isinstance(valor, str) and not valor.strip():
            return False, f"El campo '{campo}' no puede estar vacío."


    cancha_id = bloqueo_data["cancha_id"]

    if isinstance(cancha_id, bool) or not isinstance(cancha_id, int):
        return False, "El campo 'cancha_id' debe ser un entero."

    if cancha_id <= 0:
        return False, "El campo 'cancha_id' debe ser un entero positivo."


    if not isinstance(bloqueo_data["fecha_bloqueo"], str):
        return False, "El campo 'fecha_bloqueo' debe ser una fecha."

    try:
        fecha_bloqueo = datetime.strptime(
            bloqueo_data["fecha_bloqueo"],
            FORMATO_FECHA
        ).date()

    except ValueError:
        return False, (
            "El campo 'fecha_bloqueo' debe tener el formato YYYY-MM-DD."
        )

    if not isinstance(bloqueo_data["inicio"], str):
        return False, "El campo 'inicio' debe ser una fecha y hora."

    try:
        inicio = datetime.strptime(
            bloqueo_data["inicio"],
            FORMATO_FECHA_HORA
        )

    except ValueError:
        return False, (
            "El campo 'inicio' debe tener el formato "
            "YYYY-MM-DDTHH:MM:SS.ffffff-03:00."
        )


    if not isinstance(bloqueo_data["fin"], str):
        return False, "El campo 'fin' debe ser una fecha y hora."

    try:
        fin = datetime.strptime(
            bloqueo_data["fin"],
            FORMATO_FECHA_HORA
        )

    except ValueError:
        return False, (
            "El campo 'fin' debe tener el formato "
            "YYYY-MM-DDTHH:MM:SS.ffffff-03:00."
        )

    if inicio.utcoffset() != timedelta(hours=-3):
        return False, (
            "El campo 'inicio' debe utilizar el desplazamiento GMT-3."
        )

    if fin.utcoffset() != timedelta(hours=-3):
        return False, (
            "El campo 'fin' debe utilizar el desplazamiento GMT-3."
        )

    if inicio >= fin:
        return False, "El inicio debe ser anterior al fin."

    if inicio.date() != fecha_bloqueo:
        return False, (
            "La fecha de 'inicio' debe coincidir con 'fecha_bloqueo'."
        )

    if fin.date() != fecha_bloqueo:
        return False, (
            "La fecha de 'fin' debe coincidir con 'fecha_bloqueo'."
        )

    if inicio.date() != fin.date():
        return False, "El bloqueo no puede atravesar la medianoche."


    ahora = datetime.now(ZONA_HORARIA_GMT3)

    if inicio <= ahora:
        return False, "El bloqueo debe comenzar en el futuro."

    if (
        inicio.minute != 0
        or inicio.second != 0
        or inicio.microsecond != 0
    ):
        return False, "El inicio debe comenzar en una hora en punto."

    if (
        fin.minute != 0
        or fin.second != 0
        or fin.microsecond != 0
    ):
        return False, "El fin debe terminar en una hora en punto."


    hora_inicio = inicio.hour + inicio.minute / 60
    hora_fin = fin.hour + fin.minute / 60

    if hora_inicio < HORA_APERTURA:
        return False, (
            "El inicio está fuera del horario del club. "
            "El horario permitido comienza a las 08:00."
        )

    if hora_fin > HORA_CIERRE:
        return False, (
            "El fin está fuera del horario del club. "
            "El horario permitido termina a las 23:00."
        )
    
    if not isinstance(bloqueo_data["motivo"], str):
        return False, "El campo 'motivo' debe ser un texto."

    motivo = bloqueo_data["motivo"].strip()

    if not motivo:
        return False, "El campo 'motivo' no puede estar vacío."

    if len(motivo) > 255:
        return False, (
            "El campo 'motivo' no puede superar los 255 caracteres."
        )

    return True, ""

