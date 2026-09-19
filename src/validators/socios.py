from .. import db
import re
def construir_socio_dto(socio:dict)->dict:
    return {
        'id':       socio['id'],
        'nombre':   socio['nombre'],
        'email':    socio['email'],
        'activo':   socio['activo']
    }


def validar_mail(email)->str:
    email = validar_string_no_vacio(email, 'email')
    if not re.match(patron_email, email):

def validar_socio(datos:dict):
    if not datos.get():
        
    