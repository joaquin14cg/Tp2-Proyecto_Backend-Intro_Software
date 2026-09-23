from flask import Blueprint, jsonify, request
from src.services.canchas import listar_canchas, borrar_cancha, obtener_cancha, modificar_cancha
from src.services.canchas import crear_cancha as service_crear_cancha

canchas_bp = Blueprint('canchas', __name__)

@canchas_bp.route('/canchas', methods=['GET'])
def obtener_canchas():
    lista_canchas = listar_canchas()
    return jsonify({"canchas": lista_canchas}), 200

@canchas_bp.route('/canchas/<int:id_cancha>', methods=['GET'])
def obtener_cancha_por_id_route(id_cancha: int):
    cancha = obtener_cancha(id_cancha)
    if cancha is None:
        return jsonify({'mensaje': 'Cancha no encontrada'}), 404
    return jsonify(cancha), 200

@canchas_bp.route('/canchas', methods=['POST'])
def post_cancha():
    try:
        body = request.get_json()
        nueva_cancha = service_crear_cancha(body)
        return jsonify(nueva_cancha), 201
    except ValueError as error:
        payload, status_code = error.args
        return jsonify(payload), status_code

@canchas_bp.route('/canchas/<int:id_cancha>', methods=['DELETE'])
def eliminar_cancha_route(id_cancha):
    try:
        borrar_cancha(id_cancha)
        return '', 204
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]

@canchas_bp.route('/canchas/<int:id_cancha>', methods=['PATCH'])
def modificar_cancha_route(id_cancha):
    try:
        body = request.get_json(silent=True)
        modificar_cancha(id_cancha, body)
        return '', 204
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]