from flask import Flask, render_template, request, url_for, redirect, flash, session
from controllers.login_controller import AuthController
from controllers.user_controller import UsuarioController
from models.user_model import UsuarioModel
from functools import wraps

app = Flask(__name__, static_folder='static')
app.secret_key = "tu_clave_secreta_aqui"

# Instancias de controladores
auth_controller = AuthController()
user_controller = UsuarioController()
user_model = UsuarioModel()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not auth_controller.check_session():
            flash('Por favor inicie sesión para acceder', 'error')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET"])
def index():
    return redirect(url_for('login_page'))

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, message = auth_controller.login(username, password)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('home_page'))
        else:
            flash(message, 'error')
            return redirect(url_for('login_page'))
            
    return render_template("login.html")

# Solo una ruta para home_page
@app.route("/home")
@login_required
def home_page():
    return render_template("menu.html")

@app.route("/users")
@login_required
def users_page():
    usuarios = user_model.obtener_todos()
    return render_template("user.html", usuarios=usuarios)

@app.route('/logout')
def logout():
    success, message = auth_controller.logout()
    flash(message, 'success' if success else 'error')
    return redirect(url_for('login_page'))

# Rutas adicionales para las páginas de categorías
@app.route("/hogar")
def hogar_page():
    return render_template("hogar.html")

@app.route("/jardineria")
def jardineria_page():
    return render_template("jardineria.html")

@app.route("/ropa")
def ropa_page():
    return render_template("ropa.html")

@app.route("/tecnologia")
def tecnologia_page():
    return render_template("tecnologia.html")

@app.route("/herramientas")
def herramientas_page():
    return render_template("herramientas.html")

@app.route("/carrito")
@login_required
def carrito_page():
    return render_template("carrito.html")

@app.route("/procesar_compra", methods=['POST'])
@login_required
def procesar_compra():
    # Lógica para procesar la compra
    return "Compra procesada"

@app.route("/register", methods=["GET"])
def register_page():
    # Obtener la página de origen desde el parámetro de consulta
    origin = request.args.get('origin', 'login')  # 'login' es el valor por defecto
    print(f"Página de origen: {origin}")  # Debug log
    return render_template('insert_user.html', origin_page=origin)

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
    try:
        user_controller.eliminar_usuario(user_id)
        flash('Usuario eliminado exitosamente', 'success')
        app.run(debug=True)
        return redirect(url_for('users_page'))
    except Exception as e:
        flash(f'Error al eliminar el usuario: {str(e)}', 'error')
        return redirect(url_for('users_page'))

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get('query')
    # Aquí puedes agregar la lógica para manejar la búsqueda
    return render_template("search_results.html", query=query)

if __name__ == "__main__":
    app.run(debug=True)