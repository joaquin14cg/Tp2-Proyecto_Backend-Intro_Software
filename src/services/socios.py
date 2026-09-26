from db import obtener_conexion
from src.repositories import socios as socios_repo
from src.validators.socios import (
    validar_body_socio,
    validar_patch_socio,
    validar_id_socio
    )
import utils as ut
import constants as const


def construir_socio_dto(socio:dict)->dict:
    return {
        'id':       socio['id'],
        'nombre':   socio['nombre'],
        'email':    socio['email'],
        'activo':   bool(socio['activo']),
    }

def listar_socios_paginados(limit: int, offset: int, nombre: str = None, activo = None)-> tuple[list, int]:
    if isinstance(activo,str):
        activo = activo.lower() in ['true', '1']
    socios_raw = socios_repo.obtener_socios_paginados(limit, offset, nombre, activo)
    total = socios_repo.contar_total_socios(nombre, activo)
    socios = [construir_socio_dto(s) for s in socios_raw]
    return socios, total
    


def buscar_socio_por_id(id_str: int)->dict:
    socio_id = validar_id_socio(id_str)
    socio = socios_repo.obtener_socio_por_id(socio_id)
    if not socio:
        raise ValueError(ut.construir_error_api(
            code=const.ERROR_CODE_SOCIO_NOT_FOUND,
            message='Socio no encontrado',
            description=f"No se encontro un socio registrado con el ID {socio_id}"
        ))
    return construir_socio_dto(socio)




def validar_email_disponible(email: str)->None:
    if socios_repo.existe_socio_con_email(email):
        raise ValueError(ut.construir_error_api(
            code=const.ERROR_CODE_SOCIO_EXISTS,
            message='El socio ya existe',
            description=f"Ya existe un socio registrado con el email '{email}'"
        ), 409)
    


def crear_socio(body:dict)->dict:
    datos = validar_body_socio(body)
    validar_email_disponible(datos['email'])
    datos['activo'] = True
    socio_nuevo = socios_repo.guardar_socio(datos)
    return construir_socio_dto(socio_nuevo)



def actualizar_socio(id_socio: int, body: dict) -> dict:
    socio = socios_repo.obtener_socio_por_id(id_socio)

    if not socio:
        raise ValueError(ut.construir_error_api(
            code=const.ERROR_CODE_SOCIO_NOT_FOUND,
            message='Socio no encontrado',
            description=f"No se encontró un socio con el id '{id_socio}'"
        ), 404)

    datos_actualizados = validar_patch_socio(body)

    if 'email' in datos_actualizados:
        email_nuevo = datos_actualizados['email']

        if email_nuevo != socio['email']:
            validar_email_disponible(email_nuevo)

    socio_actualizado = socios_repo.actualizar_socio(
        id_socio,
        datos_actualizados
    )

    return construir_socio_dto(socio_actualizado)