from utils import construir_error_api

CAMPOS_EDITABLES = ('nombre', 'precio_hora', 'techada', 'activa')

def validar_patch_cancha(body: dict) -> dict:
    if not isinstance(body, dict):
        raise ValueError(
            construir_error_api(
                code='cancha.invalid',
                message='Body inválido',
                description='El body debe ser un objeto JSON'
            ),
            400
        )

    if not body:
        raise ValueError(
            construir_error_api(
                code='cancha.invalid',
                message='Body vacío',
                description='Debe enviar al menos un campo para modificar la cancha'
            ),
            400
        )
    for campo in body:
        if campo not in CAMPOS_EDITABLES:
            raise ValueError(
                construir_error_api(
                    code='cancha.invalid',
                    message='Campo no permitido',
                    description=f'El campo {campo} no se puede modificar'
                ),
                400
            )
    datos = {}

    if 'nombre' in body:
        nombre = body['nombre']

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError(
                construir_error_api(
                    code='cancha.invalid',
                    message='Nombre inválido',
                    description='El nombre no puede estar vacío'
                ),
                400
            )
        datos['nombre'] = nombre.strip()

    if 'precio_hora' in body:
        precio = body['precio_hora']

        if isinstance(precio, bool) or not isinstance(precio, int) or precio <= 0:
            raise ValueError(
                construir_error_api(
                    code='cancha.invalid',
                    message='Precio inválido',
                    description='El precio_hora debe ser un entero positivo'
                ),
                400
            )
        datos['precio_hora'] = precio

    if 'techada' in body:
        if not isinstance(body['techada'], bool):
            raise ValueError(
                construir_error_api(
                    code='cancha.invalid',
                    message='Valor inválido',
                    description='El campo techada debe ser booleano'
                ),
                400
            )
        datos['techada'] = body['techada']

    if 'activa' in body:
        if not isinstance(body['activa'], bool):
            raise ValueError(
                construir_error_api(
                    code='cancha.invalid',
                    message='Valor inválido',
                    description='El campo activa debe ser booleano'
                ),
                400
            )
        datos['activa'] = body['activa']
    return datos