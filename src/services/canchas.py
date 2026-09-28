from src.repositories.canchas import crear_cancha as repo_crear_cancha
from src.repositories.canchas import obtener_todas_las_canchas
from src.repositories.canchas import (
    obtener_cancha_por_id,
    obtener_cancha_por_nombre,
    tiene_reservas,
    eliminar_cancha,
    actualizar_cancha,
    obtener_canchas_paginadas,
    contar_canchas,
    obtener_canchas_activas,
)
from src.repositories.deportes import obtener_deporte_por_id
from utils import construir_error_api
from constants import MIN_ID
from src.validators.canchas import validar_post_cancha, validar_patch_cancha, validar_disponibilidad
from src.repositories.reservas import existe_reserva_confirmada_superpuesta

def construir_cancha_dto(cancha: dict) -> dict:
    return { 
        'id':           cancha['id'],
        'nombre':       cancha['nombre'],
        'id_deporte':   cancha['id_deporte'],
        'precio_hora':  cancha['precio_hora'],
        'techada': bool(cancha['techada']),
        'activa':  bool(cancha['activa'])
    }

def listar_canchas_paginadas(limit, offset, id_deporte=None, nombre=None, techada=None, activa=None):
    canchas = obtener_canchas_paginadas(limit, offset, id_deporte, nombre, techada, activa)
    total = contar_canchas(id_deporte, nombre, techada, activa)
    return [construir_cancha_dto(c) for c in canchas], total

def crear_cancha(body: dict) -> dict:
    datos = validar_post_cancha(body)
    cancha_existente = obtener_cancha_por_nombre(datos['nombre'])
    if cancha_existente is not None:
        raise ValueError(
            construir_error_api(
                code='cancha.conflict',
                message='Nombre duplicado',
                description=f"Ya existe una cancha con el nombre '{datos['nombre']}'"
            ),
            409
        )
    deporte = obtener_deporte_por_id(datos['id_deporte'])
    if deporte is None:
        raise ValueError(
            construir_error_api(
                code='deporte_not_found',
                message='Deporte no encontrado',
                description=f"El deporte con id {datos['id_deporte']} no existe"
            ),
            404
        )
    nuevo_id = repo_crear_cancha(
        nombre=datos['nombre'],
        id_deporte=datos['id_deporte'],
        precio_hora=datos['precio_hora'],
        techada=datos['techada'],
        activa=datos['activa']
    )
    datos['id'] = nuevo_id
    return datos

def obtener_cancha(id_cancha: int) -> dict | None:
    cancha_db = obtener_cancha_por_id(id_cancha)
    if cancha_db == None:
        return None
    return construir_cancha_dto(cancha_db)

def borrar_cancha(id_cancha: int) -> None:

    if id_cancha <= 0:
        raise ValueError(
            construir_error_api(
                code='cancha.invalid_id',
                message='ID de cancha inválido',
                description='El ID de la cancha debe ser un entero positivo'
            ),
            400
        )
    cancha = obtener_cancha_por_id(id_cancha)

    if cancha is None:
        raise ValueError(
            construir_error_api(
                code='cancha.not_found',
                message='Cancha no encontrada',
                description=f'No existe una cancha con el id {id_cancha}'
            ),
            404
        )

    if tiene_reservas(id_cancha):
        raise ValueError(
            construir_error_api(
                code='cancha.has_reservas',
                message='No se puede eliminar la cancha',
                description='La cancha tiene reservas asociadas'
            ),
            409
        )

    eliminar_cancha(id_cancha)

def modificar_cancha(id_cancha: int, body: dict) -> None:

    if id_cancha < MIN_ID:
        raise ValueError(
            construir_error_api(
                code='cancha.invalid_id',
                message='ID de cancha inválido',
                description='El ID de la cancha debe ser un entero positivo'
            ),
            400
        )
        
    cancha = obtener_cancha_por_id(id_cancha)

    if cancha is None:
        raise ValueError(
            construir_error_api(
                code='cancha.not_found',
                message='Cancha no encontrada',
                description=f'No existe una cancha con el id {id_cancha}'
            ),
            404
        )

    datos = validar_patch_cancha(body)
    actualizar_cancha(id_cancha, datos)

def listar_canchas_disponibles(
    fecha: str,
    hora_inicio: str,
    hora_fin: str,
    id_deporte=None,
    techada=None,
    limit: int = 10,
    offset: int = 0
) -> dict:

    inicio, fin = validar_disponibilidad(
        fecha,
        hora_inicio,
        hora_fin
    )

    canchas = obtener_canchas_activas(
        id_deporte,
        techada
    )
    canchas_disponibles = []

    for cancha in canchas:
        if not existe_reserva_confirmada_superpuesta(
            cancha['id'],
            inicio,
            fin
        ):
            canchas_disponibles.append(
                construir_cancha_dto(cancha)
            )

    total = len(canchas_disponibles)
    canchas_paginadas = canchas_disponibles[
        offset:offset + limit
    ]
    ultimo_offset = 0

    if total > 0:
        ultimo_offset = ((total - 1) // limit) * limit
    base_url = '/canchas/disponibles'

    def construir_url(nuevo_offset):
        parametros = [
            f'fecha={fecha}',
            f'hora_inicio={hora_inicio}',
            f'hora_fin={hora_fin}'
        ]

        if id_deporte is not None:
            parametros.append(f'id_deporte={id_deporte}')

        if techada is not None:
            parametros.append(f'techada={str(techada).lower()}')

        parametros.append(f'_limit={limit}')
        parametros.append(f'_offset={nuevo_offset}')

        return base_url + '?' + '&'.join(parametros)

    links = {
    '_first': {
        'href': construir_url(0)
    }
    }

    if offset > 0:
    links['_prev'] = {
        'href': construir_url(max(0, offset - limit))
    }

    if offset + limit < total:
    links['_next'] = {
        'href': construir_url(offset + limit)
    }

i   f total > 0:
    links['_last'] = {
        'href': construir_url(ultimo_offset)
    }

    return {
        'canchas': canchas_paginadas,
        '_limit': limit,
        '_offset': offset,
        '_links': links
    }