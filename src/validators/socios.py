from .. import db

def construir_socio_dto(socio:dict)->dict:
    return {
        'id':       socio['id'],
        'nombre':   socio['nombre'],
        'email':    socio['email'],
        'activo':   socio['activo']
    }

def crear_socio():
    if not validar_mail():
        return jsonify({"error" : "Ingrese un formato de mail valido"}), 400
    if not validar_nombre():
        return jsonify({"error": "El campo 'Nombre' es obligatorio"}), 400
    