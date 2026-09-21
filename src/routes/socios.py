from flask import Blueprint, jsonify, request
from utils import error_body_invalido
from src.services import socios as socios_services

socios_bp = Blueprint('socios', __name__)

@socios_bp.route('/socios', methods=['GET'])
def listar_socios():
    return jsonify({"mensaje": "Lista de socios funcionando"}), 200

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
