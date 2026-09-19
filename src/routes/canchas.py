from flask import Blueprint, jsonify
from services.canchas import listar_canchas

canchas_bp = Blueprint('canchas', __name__)

@canchas_bp.route('/canchas', methods=['GET'])
def obtener_canchas():
    lista_canchas = listar_canchas()
    return jsonify({"canchas": lista_canchas}), 200