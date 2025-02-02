import os
import sys
import mysql.connector

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..models')))


class ConexionDB:
    def __init__(self, host="localhost", user="root", password="", database="dbusers"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def conectar(self):
        try:
            # Cerrar conexión existente si hay una
            if self.connection and self.connection.is_connected():
                self.connection.close()
                
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
        except mysql.connector.Error as err:
            print(f"Error al conectar: {err}")

    def obtener_conexion(self):
        if not self.connection or not self.connection.is_connected():
            self.conectar()
        return self.connection

    def cerrar(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

