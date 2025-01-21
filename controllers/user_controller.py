import sys
import os
from flask import render_template, request, redirect, url_for
from models.user_model import UsuarioModel


# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..models')))


class UsuarioController:
    def __init__(self):
        self.modelo = UsuarioModel()

    def obtener_usuarios(self):
        try:
            return self.modelo.obtener_todos()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []

