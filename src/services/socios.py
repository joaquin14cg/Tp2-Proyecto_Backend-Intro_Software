from .. import db
from ..repositories import socios as socios_db


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


    
def editar_socio(id_socio: int, socio:dict)->dict:


def crear_socio(body:dict)->dict:
    datos = validar_body_socio(body)
    validar_email(email)
    
    