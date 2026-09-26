from flask import Blueprint, jsonify, request
import utils as ut
from src.services import socios as socios_services

socios_bp = Blueprint('socios', __name__)

@socios_bp.route('/socios', methods=['GET'])
def get_socios():
    limit, offset, error = ut.obtener_parametros_paginacion(request)
    if error:
        return jsonify(error), 400
    nombre = request.args.get('nombre', type=str)
    activo = request.args.get('activo')
    
    socios, total = socios_services.listar_socios_paginados(limit, offset, nombre, activo)
    respuesta = ut.construir_respuesta_paginada(
        clave="socios",
        items=socios,
        total=total,
        limit=limit,
        offset=offset,
        ruta_base="/socios"
    )
    if not socios:
        return '', 204
    return jsonify(respuesta), 200

@socios_bp.route('/socios', methods=['POST'])
def post_socio():
    body = request.get_json(silent=True, force=True)
    if body is None:
        return ut.error_body_invalido(), 400
    try:
        socio = socios_services.crear_socio(body)
    except ValueError as e:
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(e.args[0]),status
    
    return jsonify(socio), 201

@socios_bp.route('/socios/<id>', methods=['GET'])
def get_socio_id(id):
    try:
        id_socio = socios_services.validar_id_socio(id) 
    except ValueError as e:
        return jsonify(e.args[0]), 400
    socio = socios_services.buscar_socio_por_id(id_socio)
    if not socio:
        return ut.error_socio_no_encontrado(id_socio)
    return jsonify(socio)

@socios_bp.route('/socios/<id>', methods=['PATCH'])
def actualizar_socio(id):
    # silent=True evita que Flask genere automáticamente un error
    # cuando el body no contiene un JSON válido.
    body = request.get_json(silent=True)
    if body is None:
        return ut.error_body_invalido()
    try:
        socios_services.actualizar_socio(id, body)
    except ValueError as e:
        mensaje_error = e.args[0]
        # Si el service no proporciona un código HTTP, usamos 400 como valor por defecto.
        if len(e.args) > 1:
            codigo_error = e.args[1]
        else:
            codigo_error = 400

        return jsonify(mensaje_error), codigo_error

    # Devuelve 204 No Content 
    return '', 204