from db import obtener_conexion
from src.repositories import socios as socios_repo
from src.validators.socios import (
    validar_nombre_o_apellido,
    validar_email,
    validar_body_socio
    )
from utils import (construir_error_api, validar_string_no_vacio)
from constants import (
    ERROR_CODE_SOCIO_EXISTS,
    ERROR_CODE_SOCIO_NOT_FOUND
    )


def construir_socio_dto(socio:dict)->dict:
    return {
        'id':       socio['id'],
        'nombre':   socio['nombre'],
        'email':    socio['email'],
        'activo':   socio['activo'],
    }

def listar_socios_paginados(limit: int, offset: int, nombre: str = None, activo: bool = None)-> tuple[list, int]:
    socios_raw = socios_repo.obtener_socios_paginados(limit, offset, nombre, activo)
    total = socios_repo.contar_total_socios(nombre, activo)
    socios = [construir_socio_dto(s) for s in socios_raw]
    return socios, total
    


def buscar_socio_por_id(id_socio: int)->dict:
    socio = obtener_socio_por_id(id_socio)
    if not socio:
        return {}

    return construir_socio_dto(socio)




def validar_email_disponible(email: str)->None:
    if socios_repo.existe_socio_con_email(email):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_SOCIO_EXISTS,
            message='El socio ya existe',
            description=f"Ya existe un socio registrado con el email '{email}'"
        ), 409)
    


def crear_socio(body:dict)->dict:
    datos = validar_body_socio(body)
    validar_email_disponible(datos['email'])
    
    return construir_socio_dto(body)
    

    
    