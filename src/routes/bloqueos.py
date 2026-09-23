from flask import Blueprint, request, jsonify

from services import bloqueos



bloqueos_bp = Blueprint('bloqueos', __name__)
@bloqueos_bp.route('/bloqueos', methods=['GET'])
def get_bloqueos(): # Llamar al service para obtener los bloqueos
    resultados = bloqueos.obtener_bloqueos()
    return jsonify(resultados), 200


@bloqueos_bp.route('/bloqueos', methods=['POST'])
def crear_bloqueo():
    data = request.get_json() #contiene el JSON enviado en el cuerpo de la solicitud.
    bloqueo = bloqueos.crear_bloqueo(data)
    return jsonify(bloqueo), 201


@bloqueos_bp.route("/bloqueos/<int:id>", methods=["DELETE"])
def eliminar_bloqueo(id):
    resultado, codigo = bloqueos.borrar_bloqueo(id)
    if resultado is None:
        return "", codigo

    return jsonify(resultado), codigo