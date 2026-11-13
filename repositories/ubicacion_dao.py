from repositories.base_dao import BaseDAO

class UbicacionDAO(BaseDAO):
    def __init__(self):
        super().__init__()

    def obtener_todos(self):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, direccion FROM Ubicaciones ORDER BY direccion, nombre")
        filas = cursor.fetchall()
        conexion.close()
        return [
            {"id": fila["id"], "nombre": fila["nombre"], "direccion": fila["direccion"]}
            for fila in filas
        ]

    def guardar(self, nombre, direccion):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        
        # Le pasamos un tipo por defecto ('Sucursal') para evitar el error NOT NULL
        cursor.execute("""
            INSERT INTO Ubicaciones (nombre, direccion, tipo) 
            VALUES (?, ?, ?)
        """, (nombre, direccion, 'Sucursal'))
        
        conexion.commit()
        conexion.close()