from flask import Blueprint, request, jsonify

from services import bloqueos



bloqueos_bp = Blueprint('bloqueos', __name__)
@bloqueos_bp.route('/bloqueos', methods=['GET'])
def get_bloqueos():
    # Llamar al service para obtener los bloqueos
    resultados = bloqueos.obtener_bloqueos()
    return jsonify(resultados), 200

@bloqueos_bp.route('/bloqueos', methods=['post'])
def crear_bloqueo():
    return jsonify(), 200