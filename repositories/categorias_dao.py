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
        nombre = nombre.strip()
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("BEGIN IMMEDIATE")
            cursor.execute("SELECT nombre FROM Categorias")
            nombres_existentes = cursor.fetchall()
            if any(fila["nombre"].strip().casefold() == nombre.casefold() for fila in nombres_existentes):
                raise ValueError("Ya existe una categoría con ese nombre.")

            cursor.execute("INSERT INTO Categorias (nombre) VALUES (?)", (nombre,))
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def eliminar(self, id_categoria: int):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        # Idealmente acá se valida si hay productos usando esta categoría antes de borrarla
        cursor.execute("DELETE FROM Categorias WHERE id = ?", (id_categoria,))
        conexion.commit()
        conexion.close()