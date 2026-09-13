import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request, jsonify 
import re

load_dotenv()

app = Flask(__name__)


def obtener_conexion():
    conexion = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return conexion

@app.post("/socios")
def crear_socio():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    if not nombre:
        return {"error": "El nombre es obligatorio"}, 400
    if not email:
        return {"error": "El email es obligatorio"}, 400
    email = email.strip().lower()
    patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(patron_email, email):
        return {"error": "El formato de email ingresado no es valido"}, 400

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    consulta = "SELECT * FROM socios WHERE email = %s"
    cursor.execute(consulta, (email,))
    socio_existente = cursor.fetchone()
    if socio_existente:
        cursor.close()
        conexion.close()
        return {"error" : "El email ya se encuentra registrado"}, 409
    else:
        insert_query = "INSERT INTO socios (nombre, email, activo) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (nombre, email, True))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": "El socio fue creado con exito"}, 201
        



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