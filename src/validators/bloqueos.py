from datetime import datetime


def validar_bloqueo(bloqueo_data):

    campos_requeridos = [
        'cancha_id',
        'fecha_bloqueo',
        'inicio',
        'fin',
        'motivo'
    ]

    for campo in campos_requeridos:
        if campo not in bloqueo_data:
            return False, f"El campo '{campo}' es requerido."

    for campo in campos_requeridos:
        if not bloqueo_data[campo]:
            return False, f"El campo '{campo}' no puede estar vacío."

    try:
        datetime.strptime(
            bloqueo_data['fecha_bloqueo'],
            '%Y-%m-%d'
        )
    except ValueError:
        return False, "La fecha de bloqueo debe tener el formato YYYY-MM-DD."

    try:
        inicio = datetime.strptime(
            bloqueo_data['inicio'],
            '%Y-%m-%d %H:%M:%S.%f'
        )

        fin = datetime.strptime(
            bloqueo_data['fin'],
            '%Y-%m-%d %H:%M:%S.%f'
        )

    except ValueError:
        return False, "El inicio y fin deben tener el formato YYYY-MM-DD HH:MM:SS.ffffff."

    if inicio >= fin:
        return False, "El inicio debe ser anterior al fin."

    return True, ""