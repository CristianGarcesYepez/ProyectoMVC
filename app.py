import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from controllers.user_controller import UsuarioController
from models.user_model import UsuarioModel
from controllers.login_controller import AuthController

app = Flask(__name__, static_folder='static')

app.secret_key = "mi_clave_secreta_unica_y_segura"

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
    return render_template("menu.html")

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

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get('query')
    # Aquí puedes agregar la lógica para manejar la búsqueda
    return render_template("search_results.html", query=query)

@app.route("/hogar.html")
def hogar_page():
    return render_template("hogar.html")

if __name__ == "__main__":
    app.run(debug=True)