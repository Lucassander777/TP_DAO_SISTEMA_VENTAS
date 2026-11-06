import sqlite3

class BaseDao:
    def __init__(self, db_name="sistema_ventas.db"):
        self.db_name = db_name

    def get_conexion(self):
        """Abre y retorna una conexión a la base de datos SQLite"""
        conexion = sqlite3.connect(self.db_name)
        conexion.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
        return conexion