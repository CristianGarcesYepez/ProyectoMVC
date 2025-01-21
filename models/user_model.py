import sys
import os
from config.conexion import ConexionDB


# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..config')))
 
class UsuarioModel:
    def __init__(self):
        self.conexion = ConexionDB()
        self.conexion.conectar()

    def get_user_by_id(self, user_id):
        cursor = self.conexion.connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def obtener_todos(self):
        try:
            cursor = self.conexion.connection.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, apellido, correo, nombre_usuario, clave_usuario, rol, estado FROM usuarios WHERE estado = '1'")
            usuarios = cursor.fetchall()
            cursor.close()
            return usuarios
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []

    def agregar(self, nombre, apellido, correo, nombre_usuario, clave_usuario):
        try:
            cursor = self.conexion.connection.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, apellido, correo, nombre_usuario, clave_usuario) VALUES (%s, %s, %s, %s, %s)", (nombre, apellido, correo, nombre_usuario, clave_usuario))
            self.conexion.connection.commit()
            cursor.close()
            print("Usuario agregado exitosamente")
        except Exception as e:
            print(f"Error al agregar usuario: {e}")

    
    def actualizar(self, usuario_id, nombre, apellido, correo, nombre_usuario, clave_usuario, rol, estado):
        try:
            cursor = self.conexion.connection.cursor()
            cursor.execute(
                "UPDATE usuarios SET nombre = %s, apellido = %s, correo = %s, nombre_usuario = %s, clave_usuario = %s, rol = %s, estado = %s WHERE id = %s",
                (nombre, apellido, correo, nombre_usuario, clave_usuario, rol, estado, usuario_id)
            )
            self.conexion.connection.commit()
            cursor.close()
            print("Usuario actualizado exitosamente")
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
    
    def eliminar_logico(self, usuario_id):
        try:
            cursor = self.conexion.connection.cursor()
            cursor.execute("UPDATE usuarios SET estado = '0' WHERE id = %s", (usuario_id,))
            self.conexion.connection.commit()
            cursor.close()
            print("Usuario eliminado exitosamente")
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")


    def eliminar(self, usuario_id):
        try:
            cursor = self.conexion.connection.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            self.conexion.connection.commit()
            cursor.close()
            print("Usuario eliminado exitosamente")
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
