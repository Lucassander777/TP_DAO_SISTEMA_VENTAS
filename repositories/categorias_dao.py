from repositories.base_dao import BaseDAO

class CategoriasDAO(BaseDAO):
    def obtener_todas(self):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM Categorias")
        filas = cursor.fetchall()
        conexion.close()
        return [{"id": f[0], "nombre": f[1]} for f in filas]

    def guardar(self, nombre: str):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Categorias (nombre) VALUES (?)", (nombre,))
        conexion.commit()
        conexion.close()

    def eliminar(self, id_categoria: int):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        # Idealmente acá se valida si hay productos usando esta categoría antes de borrarla
        cursor.execute("DELETE FROM Categorias WHERE id = ?", (id_categoria,))
        conexion.commit()
        conexion.close()