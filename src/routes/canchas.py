from flask import Blueprint, jsonify
from services.canchas import listar_canchas
from services.canchas import borrar_cancha

canchas_bp = Blueprint('canchas', __name__)

@canchas_bp.route('/canchas', methods=['GET'])
def obtener_canchas():
    lista_canchas = listar_canchas()
    return jsonify({"canchas": lista_canchas}), 200

@canchas_bp.route('/canchas/<int:id_cancha>', methods=['DELETE'])
def eliminar_cancha_route(id_cancha):
    try:
        borrar_cancha(id_cancha)
        return '', 204
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]