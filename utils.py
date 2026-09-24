from flask import jsonify
import logging
import constants as const

LIMIT_DEFAULT = 10
LIMIT_MAX = 100
OFFSET_DEFAULT = 0

logger = logging.getLogger(__name__)

def construir_error_api(code:str, message:str, description:str, level:str = 'error')->dict:
    return {
        'errors' : [{
            code:'code',
            message:'message',
            level:'error',
            description:'description'          
        }]
    }

def validar_string_no_vacio(valor, nombre:str)->str:
    if not valor or str(valor).strip():
        raise ValueError(construir_error_api(
            code=const.ERROR_CODE_FIELD_REQUIRED.format(nombre),
            message=f"Campo requerido: '{nombre}'",
            description=f"El campo '{nombre}' es obligatorio y no puede estar vacio"    
        ))
    return str(valor).strip()


def validar_entero(numero, nombre:str = 'numero')->int:
    if numero is None:
        raise ValueError(construir_error_api(
            code=const.ERROR_CODE_INVALID_FORMAT.format(nombre),
            message=f"Formato de {nombre} invalido",
            description=f"El valor de {nombre} no puede ser nulo"
        ))
    try:
        return int(numero)
    except ValueError:
        logger.warning(f"Valor numerico invalido, {nombre} no puede convertirse a entero")
        raise ValueError(construir_error_api(
            code=const.ERROR_CODE_INVALID_FORMAT.format(nombre),
            message=f"Formato de {nombre} invalido",
            description=f"El valor {numero} no puede convertirse a un numero entero"
        ))



def error_body_invalido():
    return jsonify(construir_error_api(
        code=const.ERROR_CODE_INVALID_BODY,
        message='Cuerpo de la solicitud invalido',
        description='El cuerpo de la solicitud debe ser un JSON valido con Content-Type aplication/json'
    )), 400

def obtener_parametros_paginacion(request):
    limit_str = request.args.get("_limit", str(LIMIT_DEFAULT))
    offset_str = request.args.get("_offset", str(OFFSET_DEFAULT))

    if not limit_str.isdigit() or not offset_str.isdigit():
        error = construir_error_api("PAGINACION_INVALIDA", "Parámetros de paginación inválidos", "_limit y _offset deben ser números enteros")
        return None, None, error

    limit = int(limit_str)
    offset = int(offset_str)

    if limit < 1 or limit > LIMIT_MAX:
        error = construir_error_api("PAGINACION_INVALIDA", "Parámetros de paginación inválidos", f"_limit debe estar entre 1 y {LIMIT_MAX}")
        return None, None, error

    if offset < 0:
        error = construir_error_api("PAGINACION_INVALIDA", "Parámetros de paginación inválidos", "_offset no puede ser negativo")
        return None, None, error

    return limit, offset, None

def armar_links(total, limit, offset, ruta_base):
    ultima_pagina_offset = 0
    if total > 0:
        ultima_pagina_offset = ((total - 1) // limit) * limit

    links = {
        "_first": f"{ruta_base}?_limit={limit}&_offset=0",
        "_last": f"{ruta_base}?_limit={limit}&_offset={ultima_pagina_offset}",
        "_prev": None,
        "_next": None
    }

    if offset - limit >= 0:
        links["_prev"] = f"{ruta_base}?_limit={limit}&_offset={offset - limit}"

    if offset + limit < total:
        links["_next"] = f"{ruta_base}?_limit={limit}&_offset={offset + limit}"

    return links

def construir_respuesta_paginada(clave, items, total, limit, offset, ruta_base):
    return {
        clave: items,
        "_links": armar_links(total, limit, offset, ruta_base)
    }

def obtener_parametro_booleano(request, nombre_parametro):
    valor_str = request.args.get(nombre_parametro)
    if valor_str is None:
        return None, None
    valor_lower = valor_str.lower()
    if valor_lower == 'true':
        return True, None
    elif valor_lower == 'false':
        return False, None
    else:
        error = construir_error_api(
            code=const.ERROR_CODE_INVALID_PARAMETER,
            message="Parámetro inválido",
            description=f"El filtro '{nombre_parametro}' debe ser true o false"
        )
        return None, error