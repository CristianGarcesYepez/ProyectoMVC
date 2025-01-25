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
        # Valida las credenciales con el modelo
        user = self.model.validar_usuario(username, password)
        if user:
            # Si las credenciales son válidas, guarda los datos en la sesión
            session["user_id"] = user["ID"]
            session["username"] = user["NOMBRE_USUARIO"]
            return redirect(url_for("dashboard"))  # Redirige al dashboard
        
        # Si son inválidas, muestra un mensaje de error
        flash("Usuario o contraseña inválidos", "error")
        return render_template("login.html")


