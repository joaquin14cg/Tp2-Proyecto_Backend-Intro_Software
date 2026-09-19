from flask import Blueprint, request, jsonify
from src.models.bloqueos import Bloqueo

def obtener_bloqueos():
    bloqueos = Bloqueo.query.all()
    return bloqueos