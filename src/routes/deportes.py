from flask import Blueprint, jsonify
from services.deportes import listar_deportes

deportes_bp = Blueprint('deportes' __name__)
@deportes_bp.route('/deportes', methods=['GET'])
def obtener_deportes()
    lista_deportes = listar_deportes()
    return jsonify(lista_deportes), 200