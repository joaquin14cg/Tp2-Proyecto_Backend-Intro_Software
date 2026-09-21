from .. import db
from repositories.socios import existe_socio_con_email
from validators.socios import (
    validar_nombre_o_apellido,
    validar_email
    )
from utils import (construir_error_api, validar_string_no_vacio)
from constants import ERROR_CODE_SOCIO_EXISTS, ERROR_CODE_SOCIO_NOT_FOUND


def construir_socio_dto(socio:dict)->dict:
    return {
        'id':       socio['id'],
        'nombre':   socio['nombre'],
        'email':    socio['email'],
        'activo':   socio['activo'],
    }

def listar_socios()->list[dict]:
    return [construir_socio_dto(s) for s in socios_db.obtener_todos_los_socios()]


def buscar_socio_por_id(id_socio: int)->dict:
    socio = socios_db.obtener_socio_por_id(id_socio)
    if not socio:
        return {}

    return construir_socio_dto(socio)




def validar_email_disponible(email: str)->None:
    if existe_socio_con_email(email):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_SOCIO_EXISTS,
            message='El socio ya existe',
            description=f"Ya existe un socio registrado con el email '{email}'"
        ), 409)
    


def crear_socio(body:dict)->dict:
    datos = validador_socios(body)
    
    email = nuevo_socio.get('email')
    if validar_email_disponible(email) == False:
        return validar_email_disponible(nuevo_socio['email'])

    
    