import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from controllers.user_controller import UsuarioController
from models.user_model import UsuarioModel
from controllers.login_controller import AuthController
from flask dance.contrib.google import make_google_blueprint, google
from flask dance.contrib.facebook import make_facebook_blueprint, facebook
from flask dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__, static_folder='static')

app.secret_key = "mi_clave_secreta_unica_y_segura"

# Configuración de flask-login
login_manager = LoginManager()
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name                
        self.email = email
#Diccionario para almacenar usuarios en sesión (solo para pruebas, usa DB en producción)
users = {}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Configuración OAuth con Google
google_bp = make_google_blueprint(client_id="TU_GOOGLE_CLIENT_ID",
                                  client_secret="TU_GOOGLE_CLIENT_SECRET",
                                  redirect_to="google_login")
app.register_blueprint(google_bp, url_prefix="/login")

# Configuración OAuth con Facebook
facebook_bp = make_facebook_blueprint(client_id="TU_FACEBOOK_CLIENT_ID",
                                       client_secret="TU_FACEBOOK_CLIENT_SECRET",
                                       redirect_to="facebook_login")
app.register_blueprint(facebook_bp, url_prefix="/login")

# Configuración OAuth con Twitter
twitter_bp = make_twitter_blueprint(api_key="TU_TWITTER_API_KEY",
                                    api_secret="TU_TWITTER_API_SECRET",
                                    redirect_to="twitter_login")
app.register_blueprint(twitter_bp, url_prefix="/login")

@app.route('/google_login')
def google_login():
    if not google_bp.session.authorized:
        return redirect(url_for("google.login"))
    
    resp = google_bp.session.get("/oauth2/v2/userinfo")
    user_info = resp.json()
    
    user = User(id=user_info["id"], name=user_info["name"], email=user_info["email"])
    users[user.id] = user
    login_user(user)
    
    flash("Inicio de sesión con Google exitoso", "success")
    return redirect(url_for("dashboard"))

@app.route('/facebook_login')
def facebook_login():
    if not facebook_bp.session.authorized:
        return redirect(url_for("facebook.login"))
    
    resp = facebook_bp.session.get("/me?fields=id,name,email")
    user_info = resp.json()

    user = User(id=user_info["id"], name=user_info["name"], email=user_info.get("email", ""))
    users[user.id] = user
    login_user(user)

    flash("Inicio de sesión con Facebook exitoso", "success")
    return redirect(url_for("dashboard"))

@app.route('/twitter_login')
def twitter_login():
    if not twitter_bp.session.authorized:
        return redirect(url_for("twitter.login"))
    
    resp = twitter_bp.session.get("account/verify_credentials.json")
    user_info = resp.json()
    
    user = User(id=user_info["id_str"], name=user_info["name"], email=user_info.get("email", ""))
    users[user.id] = user
    login_user(user)

    flash("Inicio de sesión con Twitter exitoso", "success")
    return redirect(url_for("dashboard"))

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Bienvenido {current_user.name}! <a href='/logout'>Cerrar sesión</a>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("home"))

@app.route('/')
def home():
    return render_template("index.html")

# Instancia del controlador
user_controller = UsuarioController()
user_model = UsuarioModel()

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/", methods=["GET", "POST"])
def first_page():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    return render_template("login.html")

@app.route("/home", methods=["GET", "POST"])
def home_page():
    return render_template("menu.html")
    
@app.route("/users", methods=["GET"])
def users_page():
    usuarios = user_model.obtener_todos()
    return render_template("user.html", usuarios=usuarios)
    
@app.route("/register", methods=["GET", "POST"])
def register_page():
    return render_template("insert_user.html")

@app.route("/insert_user", methods=["POST"])
def insert_user():
    try:
        nombre = request.form.get("name")
        apellido = request.form.get("lastname")
        correo = request.form.get("email")
        nombre_usuario = request.form.get("username")
        clave_usuario = request.form.get("password")
        
        if not (nombre and apellido and correo and nombre_usuario and clave_usuario):
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("register_page"))
        
        user_model.agregar(nombre, apellido, correo, nombre_usuario, clave_usuario)
        flash("Usuario agregado correctamente", "success")
        return redirect(url_for("users_page"))
    except Exception as e:
        flash(f"Error al agregar usuario: {str(e)}", "error")
        return redirect(url_for("register_page"))

@app.route("/update_user/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    if request.method == "GET":
        usuarios = user_model.get_user_by_id(user_id)
        if usuarios:
            return render_template('update_user.html', usuarios=usuarios)
        else:
            flash("Usuario no encontrado", "error")
            return redirect(url_for("users_page"))

    if request.method == "POST":
        try:
            nombre = request.form.get("name")
            apellido = request.form.get("lastname")
            correo = request.form.get("email")
            nombre_usuario = request.form.get("username")
            clave_usuario = request.form.get("password")
            rol = request.form.get("rol")
            estado = request.form.get("status")

            if not (nombre and apellido and correo and nombre_usuario and clave_usuario and rol and estado):
                flash("Todos los campos son obligatorios", "error")
                return redirect(url_for("update_user", user_id=user_id))

            user_model.actualizar(user_id, nombre, apellido, correo, nombre_usuario, clave_usuario, rol, estado)
            flash("Usuario actualizado correctamente", "success")
            return redirect(url_for("users_page"))
        except Exception as e:
            flash(f"Error al actualizar usuario: {str(e)}", "error")
            return redirect(url_for("update_user", user_id=user_id))


@app.route('/usuarios/eliminar/<int:user_id>', methods=['GET', 'POST'])
def eliminar_usuario(user_id):
    # Lógica para actualizar el estado del usuario a inactivo en la base de datos
    exito = user_model.eliminar_logico(user_id)  # Cambiar estado a 0 (inactivo)
    
    if exito:
        flash(f'Usuario {id} eliminado exitosamente', 'success')
    else:
        flash(f'Error al eliminar el usuario {id}', 'error')
    
    return redirect(url_for('users_page'))  # Redirige a la página donde se listan los usuarios

#-------------------LOGIN-------------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        # Obtén los datos enviados desde el formulario
        username = request.form.get("username")
        password = request.form.get("password")
        
        authcontroller = AuthController()
        # Llama al controlador para manejar la lógica
        return authcontroller.login(username, password)
    
    # Si es un GET, envia al menu principal
    return render_template("menu.html")

if __name__ == "__main__":
    app.run(debug=True)
