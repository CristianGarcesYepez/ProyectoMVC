import sys
import os
from flask import render_template, request, redirect, url_for, session, flash, Flask
from models.user_model import UsuarioModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..models')))
 
app = Flask(__name__)
app.secret_key = 'secret_key'


class AuthController:
    def __init__(self):
        self.model = UsuarioModel()

    def login(self, username, password):
        try:
            # Validar las credenciales con el modelo
            user = self.model.validar_usuario(username, password)
            
            if user:
                # Si las credenciales son válidas y el usuario está activo
                if user.get('estado') == '1':
                    # Guardar datos en la sesión
                    session['user_logged_in'] = True
                    session['user_id'] = user['id']
                    session['username'] = user['nombre_usuario']
                    session['rol'] = user.get('rol', 'user')
                    return True, 'Inicio de sesión exitoso'
                else:
                    return False, 'Usuario inactivo'
            else:
                return False, 'Credenciales incorrectas'
                
        except Exception as e:
            print(f"Error en login: {str(e)}")
            return False, 'Error en el servidor'

    def logout(self):
        try:
            session.clear()
            return True, 'Sesión cerrada exitosamente'
        except Exception as e:
            print(f"Error en logout: {str(e)}")
            return False, 'Error al cerrar sesión'

    def check_session(self):
        return session.get('user_logged_in', False)

    def get_current_user(self):
        if self.check_session():
            return {
                'id': session.get('user_id'),
                'username': session.get('username'),
                'rol': session.get('rol')
            }
        return None


