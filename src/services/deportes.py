from repositories.deportes import obtener_todos_los_deportes

def construir_deportes_dto(deporte: dict) -> dict:
    return {
        'id': deporte['id'],
        'nombre': deporte['nombre']
    }
def listar_deportes() -> list
    resultados = obtener_todos_los_deportes
    return [construir_deportes_dto(d) for d in resultados]