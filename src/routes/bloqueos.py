from flask import Blueprint, request, jsonify

from src.services import bloqueos



bloqueos_bp = Blueprint('bloqueos', __name__)
@bloqueos_bp.route('/bloqueos', methods=['GET'])
def get_bloqueos(): # Llamar al service para obtener los bloqueos
    resultados = bloqueos.obtener_bloqueos()
    return jsonify(resultados), 200


@bloqueos_bp.route("/bloqueos", methods=["POST"])
def crear_bloqueo():
    
    data = request.get_json()
    resultado, codigo = bloqueos.crear_bloqueo(data)
    return jsonify(resultado), codigo




@bloqueos_bp.route("/bloqueos/<int:id>", methods=["DELETE"])
def eliminar_bloqueo(id):
    resultado, codigo = bloqueos.borrar_bloqueo(id)
    if resultado is None:
        return "", codigo

    return jsonify(resultado), codigo