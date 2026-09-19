from repositories.canchas import obtener_todas_las_canchas

def construir_cancha_dto(cancha: dict) -> dict:
    return { 
        'id':           cancha['id'],
        'nombre':       cancha['nombre'],
        'id_deporte':   cancha['id_deporte'],
        'precio_hora':  cancha['precio_hora'],
        'techada': bool(cancha['techada']),
        'activa':  bool(cancha['activa'])
    }
def listar_canchas() -> list[dict]:
    return[construir_cancha_dto(c) for c in obtener_todas_las_canchas()]
    
