from flask import Blueprint, jsonify, request
from db import obtener_conexion
import re

socios_bp = Blueprint('socios', __name__)

@socios_bp.route('/socios', methods=['GET'])
def listar_socios():
    return jsonify({"mensaje": "Lista de socios funcionando"}), 200

@socios_bp.route('/socios', methods=['POST'])
def crear_socio():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400
    if not email:
        return jsonify({"error": "El email es obligatorio"}), 400
    email = email.strip().lower()
    patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(patron_email, email):
        return jsonify({"error": "El formato de email ingresado no es valido"}), 400

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    consulta = "SELECT * FROM socios WHERE email = %s"
    cursor.execute(consulta, (email,))
    socio_existente = cursor.fetchone()
    if socio_existente:
        cursor.close()
        conexion.close()
        return jsonify({"error" : "El email ya se encuentra registrado"}), 409
    else:
        insert_query = "INSERT INTO socios (nombre, email, activo) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (nombre, email, True))
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "El socio fue creado con exito"}), 201