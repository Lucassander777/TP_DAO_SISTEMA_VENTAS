import sqlite3

class BaseDAO:
    def __init__(self, db_name="sistema_ventas.db"):
        self.db_name = db_name

    def get_conexion(self):
        """Abre y retorna una conexión a la base de datos SQLite"""
        conexion = sqlite3.connect(self.db_name)
        conexion.row_factory = sqlite3.Row  
        
        conexion.execute("PRAGMA foreign_keys = ON;") 
        
        return conexion