from flask import Blueprint, jsonify, request
from src.services.canchas import listar_canchas_paginadas, borrar_cancha, obtener_cancha, modificar_cancha, listar_canchas_disponibles
from src.services.canchas import crear_cancha as service_crear_cancha
import utils as ut

canchas_bp = Blueprint('canchas', __name__)

@canchas_bp.route('/canchas', methods=['GET'])
def obtener_canchas():
    limit, offset, error = ut.obtener_parametros_paginacion(request)
    if error:
        return jsonify(error), 400

    id_deporte = request.args.get('id_deporte', type=int)
    nombre = request.args.get('nombre')
    techada, error_techada = ut.obtener_parametro_booleano(request, 'techada')
    if error_techada:
        return jsonify(error_techada), 400
    activa, error_activa = ut.obtener_parametro_booleano(request, 'activa')
    if error_activa:
        return jsonify(error_activa), 400

    canchas, total = listar_canchas_paginadas(limit, offset, id_deporte, nombre, techada, activa)
    respuesta = ut.construir_respuesta_paginada("canchas", canchas, total, limit, offset, "/canchas")
    return jsonify(respuesta), 200

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

@canchas_bp.route('/canchas/disponibles', methods=['GET'])
def obtener_canchas_disponibles():
    permitidos = {
        'fecha', 'hora_inicio', 'hora_fin',
        'id_deporte', 'techada', '_limit', '_offset'
    }
    desconocidos = set(request.args.keys()) - permitidos

    if desconocidos:
        error = ut.construir_error_api(
            code='param.invalid',
            message='Parámetros desconocidos',
            description=f'Parámetros no permitidos: {", ".join(sorted(desconocidos))}'
        )
        return jsonify(error), 400

    fecha = request.args.get('fecha')
    hora_inicio = request.args.get('hora_inicio')
    hora_fin = request.args.get('hora_fin')
    limit, offset, error = ut.obtener_parametros_paginacion(request)

    if error:
        return jsonify(error), 400

    id_deporte = request.args.get('id_deporte')

    if id_deporte is not None:
        try:
            id_deporte = int(id_deporte)
            if id_deporte <= 0:
                raise ValueError
        except ValueError:
            error = ut.construir_error_api(
                code='cancha.invalid',
                message='Parámetro id_deporte inválido',
                description='id_deporte debe ser un entero positivo'
            )
            return jsonify(error), 400

    techada, error_techada = ut.obtener_parametro_booleano(
        request, 'techada'
    )

    if error_techada:
        return jsonify(error_techada), 400
    try:
        resultado = listar_canchas_disponibles(
            fecha,
            hora_inicio,
            hora_fin,
            id_deporte,
            techada,
            limit,
            offset
        )
        return jsonify(resultado), 200

    except ValueError as error:
        payload, status_code = error.args
        return jsonify(payload), status_code