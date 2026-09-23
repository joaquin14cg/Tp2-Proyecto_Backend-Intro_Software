from src.repositories.canchas import crear_cancha as repo_crear_cancha
from src.repositories.canchas import obtener_todas_las_canchas
from src.repositories.canchas import (
    obtener_cancha_por_id,
    tiene_reservas,
    eliminar_cancha,
    actualizar_cancha
)
from src.repositories.deportes import obtener_deporte_por_id
from utils import construir_error_api
from constants import MIN_ID
from src.validators.canchas import validar_post_cancha, validar_patch_cancha

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

def crear_cancha(body: dict) -> dict:
    datos = validar_post_cancha(body)
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