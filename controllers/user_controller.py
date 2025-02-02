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

    def eliminar_usuario(self, usuario_id):
        try:
            resultado = self.modelo.eliminar_logico(usuario_id)
            return resultado
        except Exception as e:
            print(f"Error en el controlador al eliminar usuario: {e}")
            return False

    def validar_usuario(self, username, password):
        try:
            # Validar que los campos no estén vacíos
            if not username or not password:
                print("Usuario o contraseña vacíos")
                return None

            # Llamar al modelo para validar las credenciales
            usuario = self.modelo.validar_usuario(username, password)
            
            if usuario:
                # Si el usuario existe y está activo
                if usuario.get('estado') == '1':
                    return {
                        'id': usuario['id'],
                        'nombre_usuario': usuario['nombre_usuario'],
                        'rol': usuario['rol']
                    }
                else:
                    print("Usuario inactivo")
                    return None
            else:
                print("Credenciales inválidas")
                return None

        except Exception as e:
            print(f"Error en la validación de usuario: {e}")
            return None

