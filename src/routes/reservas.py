from flask import Blueprint, jsonify, request
from src.services.reservas import (
    crear_reserva, obtener_reserva, cambiar_estado_reserva, listar_reservas, crear_reservas_recurrentes,
    )

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def listar_reservas_route():
    try:
        resultado = listar_reservas(request.args, request.base_url)
        return jsonify(resultado), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]

@reservas_bp.route('/reservas', methods=['POST'])
def crear_reserva_route():
    body = request.get_json(silent=True) or {}
    try:
        reserva = crear_reserva(body)
        return jsonify(reserva), 201
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]

@reservas_bp.route('/reservas/<int:id_reserva>', methods=['GET'])
def obtener_reserva_route(id_reserva):
    try:
        reserva = obtener_reserva(id_reserva)
        return jsonify(reserva), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]

@reservas_bp.route('/reservas/<int:id_reserva>/estado', methods=['PUT'])
def cambiar_estado_route(id_reserva):
    body = request.get_json(silent=True) or {}
    try:
        reserva = cambiar_estado_reserva(id_reserva, body)
        return jsonify(reserva), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]

@reservas_bp.route('/reservas/recurrentes', methods=['POST'])
def crear_reservas_recurrentes_route():
    body = request.get_json(silent=True) or {}
    try:
        reservas = crear_reservas_recurrentes(body)
        return jsonify(reservas), 201
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]