from flask import Blueprint, jsonify, request
from utils import (
    error_body_invalido,
    obtener_parametros_paginacion,
    construir_respuesta_paginada)
from src.services import socios as socios_services

socios_bp = Blueprint('socios', __name__)

@socios_bp.route('/socios', methods=['GET'])
def get_socios():
    limit, offset, error = obtener_parametros_paginacion(request)
    if error:
        return jsonify(error), 400
    nombre = request.args.get('nombre', type=str)
    activo = request.args.get('activo')
    
    socios, total = socios_services.listar_socios_paginados(limit, offset, nombre, activo)
    respuesta = construir_respuesta_paginada(
        clave="socios",
        items=socios,
        total=total,
        limit=limit,
        offset=offset,
        ruta_base="/socios"
    )
    return jsonify(respuesta), 200

@socios_bp.route('/socios', methods=['POST'])
def post_socio():
    body = request.get_json(silent=True)
    if body is None:
        return error_body_invalido()
    try:
        socio = socios_services.crear_socio(body)
    except ValueError as e:
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(e.args[0]),status
    
    return jsonify(socio), 201
