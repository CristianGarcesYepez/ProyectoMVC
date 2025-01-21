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
        self.connection = None  # Initialize the connection attribute as None
        # This will store the database connection object once established

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexión exitosa")
        except mysql.connector.Error as err:
            print(f"Error al conectar: {err}")

    def cerrar(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")

