import re       #Libreria nativa para trabajar con Regular Expresions
from datetime import datetime, timedelta
from utils import construir_error_api

PATRON_FECHA = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}-03:00$')
CAMPOS_RESERVA = ('id_socio', 'id_cancha', 'fecha_hora_inicio', 'fecha_hora_fin')
CAMPOS_RECURRENTE = ('id_socio', 'id_cancha', 'fecha_hora_inicio', 'fecha_hora_fin', 'cantidad_semanas')
ESTADOS_VALIDOS = ('confirmada', 'cancelada', 'finalizada')

def parsear_fecha(valor, nombre):
    if not PATRON_FECHA.match(str(valor)):
        raise ValueError(construir_error_api(
            code=f'reserva.{nombre}.formato_invalido',
            message=f"Formato inválido en '{nombre}'",
            description="Debe tener el formato YYYY-MM-DDTHH:MM:SS.ffffff-03:00"
        ), 400)
    # Eliminamos la zona horaria del final (-03:00) para quedarnos unicamente con la fecha y la hora
    return datetime.strptime(valor[:-6], '%Y-%m-%dT%H:%M:%S.%f')


def validar_intervalo_reserva(inicio, fin):
    if inicio.minute != 0 or inicio.second != 0 or fin.minute != 0 or fin.second != 0:
        raise ValueError(construir_error_api(
            code='reserva.horario_invalido',
            message='El horario debe ser en punto',
            description="Los minutos y segundos deben ser 00"
        ), 400)

    if inicio >= fin:
        raise ValueError(construir_error_api(
            code='reserva.intervalo_invalido',
            message='El inicio debe ser anterior al fin',
            description="fecha_hora_inicio tiene que ser menor a fecha_hora_fin"
        ), 400)

    if inicio.date() != fin.date():
        raise ValueError(construir_error_api(
            code='reserva.atraviesa_medianoche',
            message='La reserva no puede atravesar la medianoche',
            description="fecha_hora_inicio y fecha_hora_fin deben ser del mismo día"
        ), 400)

    duracion_horas = (fin - inicio).total_seconds() / 3600
    if duracion_horas < 1 or duracion_horas > 3:
        raise ValueError(construir_error_api(
            code='reserva.duracion_invalida',
            message='Duración fuera de rango',
            description="La reserva debe durar entre 1 y 3 horas"
        ), 400)

    if inicio.hour < 8 or fin.hour > 23:
        raise ValueError(construir_error_api(
            code='reserva.fuera_de_horario',
            message='Fuera del horario permitido',
            description="El club opera de 08:00 a 23:00"
        ), 400)

    if inicio <= datetime.now():
        raise ValueError(construir_error_api(
            code='reserva.fecha_pasada',
            message='La reserva debe ser a futuro',
            description="fecha_hora_inicio ya pasó"
        ), 400)

def validar_body_reserva(body):
    for campo in CAMPOS_RESERVA:
        if campo not in body:
            raise ValueError(construir_error_api(
                code=f'required.{campo}',
                message=f"Campo requerido: '{campo}'",
                description=f"El campo '{campo}' es obligatorio"
            ), 400)

    inicio = parsear_fecha(body['fecha_hora_inicio'], 'fecha_hora_inicio')
    fin = parsear_fecha(body['fecha_hora_fin'], 'fecha_hora_fin')

    validar_intervalo_reserva(inicio, fin)

    return {'id_socio': body['id_socio'], 'id_cancha': body['id_cancha'], 'inicio': inicio, 'fin': fin}


def validar_body_estado(body):
    estado = body.get('estado')
    if estado not in ESTADOS_VALIDOS:
        raise ValueError(construir_error_api(
            code='reserva.estado_invalido',
            message='Estado inválido',
            description=f"El estado debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"
        ), 400)
    return estado

def validar_body_reservas_recurrentes(body):
    for campo in CAMPOS_RECURRENTE:
        if campo not in body:
            raise ValueError(construir_error_api(
                code=f'required.{campo}',
                message=f"Campo requerido: '{campo}'",
                description=f"El campo '{campo}' es obligatorio"
            ), 400)

    cantidad_semanas = body['cantidad_semanas']
    if not isinstance(cantidad_semanas, int) or cantidad_semanas < 2 or cantidad_semanas > 12:
        raise ValueError(construir_error_api(
            code='reserva.cantidad_semanas_invalida',
            message='Cantidad de semanas inválida',
            description="cantidad_semanas debe ser un entero entre 2 y 12"
        ), 400)

    inicio_base = parsear_fecha(body['fecha_hora_inicio'], 'fecha_hora_inicio')
    fin_base = parsear_fecha(body['fecha_hora_fin'], 'fecha_hora_fin')

    intervalos = []
    for semana in range(cantidad_semanas):
        delta = timedelta(days=7 * semana)
        inicio = inicio_base + delta
        fin = fin_base + delta
        validar_intervalo_reserva(inicio, fin)
        intervalos.append((inicio, fin))

    return body['id_socio'], body['id_cancha'], intervalos