from dotenv import load_dotenv
from flask import Flask
from src.routes.socios import socios_bp
from src.routes.canchas import canchas_bp
from src.routes.reservas import reservas_bp
from src.routes.bloqueos import bloqueos_bp

from db import obtener_conexion
load_dotenv()

app = Flask(__name__)


app.json.ensure_ascii = False #esto sirve para que tome tildes como caracteres

app.register_blueprint(socios_bp)
app.register_blueprint(canchas_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(bloqueos_bp)

@app.get("/")
def inicio():
    conexion = obtener_conexion()

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM deportes")

    deportes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return {"deportes": deportes}


if __name__ == "__main__":
    app.run(debug=True)