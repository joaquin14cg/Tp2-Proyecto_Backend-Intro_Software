from .. import db
import re
from utils import construir_error_api, validar_string_no_vacio
from constants import (
    CAMPOS_SOCIO,
    PATRON_EMAIL,
    PATRON_NOMBRE
)

def construir_socio_dto(socio:dict)->dict:
    return {
        'id':       socio['id'],
        'nombre':   socio['nombre'],
        'email':    socio['email'],
        'activo':   socio['activo']
    }


def validar_email(email)->str:
    email = validar_string_no_vacio(email, 'email')
    if not re.match(PATRON_EMAIL, email):
        raise ValueError(construir_error_api(
            code = 'invalid.email.format',
            message = "Formato de email invalido",
            description= f"El valor '{email}' no tiene un formato de correo electronico valido "
        ))
    return email

def validar_nombre_o_apellido(valor, nombre_campo: str)->str:
    valor = validar_string_no_vacio(valor, nombre_campo)
    if not re.match(PATRON_NOMBRE, valor):
        raise ValueError(construir_error_api(
            code= f'invalid.{nombre_campo}.format',
            message= f"Formato de '{nombre_campo}' invalido",
            description= f"El formato '{nombre_campo}' solo puede contener letras y espacios simples entre palabras"
        ))
    return valor
        
def validar_body_socio(body:dict)->dict:
    if body is None:
        raise ValueError(construir_error_api(
            code='invalid.body',
            message='Cuerpo de la solicitud invalido',
            description='El cuerpo de la solicitud debe ser un JSON valido con Content-Type aplication/json'
        ))    