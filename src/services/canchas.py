from repositories.canchas import obtener_todas_las_canchas
from repositories.canchas import (
    obtener_cancha_por_id,
    tiene_reservas,
    eliminar_cancha
)
from utils import construir_error_api

def construir_cancha_dto(cancha: dict) -> dict:
    return { 
        'id':           cancha['id'],
        'nombre':       cancha['nombre'],
        'id_deporte':   cancha['id_deporte'],
        'precio_hora':  cancha['precio_hora'],
        'techada': bool(cancha['techada']),
        'activa':  bool(cancha['activa'])
    }
def listar_canchas() -> list[dict]:
    return[construir_cancha_dto(c) for c in obtener_todas_las_canchas()]

def obtener_cancha(id_cancha: int) -> dict | None:
    cancha_db = obtener_cancha_por_id(id_cancha)
    if cancha_db = None:
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