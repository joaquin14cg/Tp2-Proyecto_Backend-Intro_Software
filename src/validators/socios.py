import re
import utils as utils_socios
import constants as constants_socios

def validar_email(email)->str:
    email = utils_socios.validar_string_no_vacio(email, 'email')
    if not re.match(constants_socios.PATRON_EMAIL, email):
        raise ValueError(utils_socios.construir_error_api(
            code = 'invalid.email.format',
            message = "Formato de email invalido",
            description= f"El valor '{email}' no tiene un formato de correo electronico valido "
        ))
    return email

def validar_nombre_o_apellido(valor, nombre_campo: str)->str:
    valor = utils_socios.validar_string_no_vacio(valor, nombre_campo)
    if not re.match(constants_socios.PATRON_NOMBRE, valor):
        raise ValueError(utils_socios.construir_error_api(
            code= f'invalid.{nombre_campo}.format',
            message= f"Formato de '{nombre_campo}' invalido",
            description= f"El formato '{nombre_campo}' solo puede contener letras y espacios simples entre palabras"
        ))
    return valor

VALIDADORES_CAMPO = {
    'nombre': lambda valor: validar_nombre_o_apellido(valor, 'nombre'),
    'email': validar_email,
}   

def validar_body_socio(body:dict)->dict:
    if body is None:
        raise ValueError(construir_error_api(
            code='ERROR_CODE_INVALID_BODY',
            message='Cuerpo de la solicitud invalido',
            description='El cuerpo de la solicitud debe ser un JSON valido con Content-Type aplication/json'
        ))    
    errores = []
    datos = {}

    for campo in constants_socios.CAMPOS_SOCIO:
        try:
            datos[campo] = VALIDADORES_CAMPO[campo](body.get(campo))
        except ValueError as e:
            errores.extend(e.args[0]['errors'])
    if errores:
        raise ValueError({'errors': errores})
    datos['activo'] = True
    return datos

def validar_id_socio(id_str)->int:
    return utils_socios.validar_minimo(utils_socios.validar_entero(id_str, 'id'), constants_socios.MIN_ID, 'id')


def validar_patch_socio(body: dict) -> dict:
    if body is None:
        raise ValueError(construir_error_api(
            code=constants_socios.ERROR_CODE_INVALID_BODY,
            message='Cuerpo de la solicitud invalido',
            description='El cuerpo de la solicitud debe ser un JSON valido'
        ))

    if not body:
        raise ValueError(utils_socios.construir_error_api(
            code=constants_socios.ERROR_CODE_INVALID_BODY,
            message='Cuerpo de la solicitud invalido',
            description='Debe enviarse al menos un campo para actualizar'
        ))

    errores = []
    datos = {}

    for campo, valor in body.items():
        try:
            if campo in VALIDADORES_CAMPO:
                datos[campo] = VALIDADORES_CAMPO[campo](valor)

            elif campo == 'activo':
                datos[campo] = valor

            else:
                errores.append({
                    'code': constants_socios.ERROR_CODE_INVALID_PARAMETER,
                    'message': f"El campo '{campo}' no puede ser actualizado"
                })

        except ValueError as e:
            errores.extend(e.args[0]['errors'])

    if errores:
        raise ValueError({'errors': errores})

    return datos