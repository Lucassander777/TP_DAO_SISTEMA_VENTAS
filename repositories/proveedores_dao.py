from repositories.base_dao import BaseDAO

class ProveedoresDAO(BaseDAO):
    def obtener_todos(self):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, razon_social, cuit FROM Proveedores")
        filas = cursor.fetchall()
        conexion.close()
        return [{"id": f[0], "razon_social": f[1], "cuit": f[2]} for f in filas]

    def guardar(self, razon_social: str, cuit: str):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Proveedores (razon_social, cuit) VALUES (?, ?)", (razon_social, cuit))
        conexion.commit()
        conexion.close()

    def eliminar(self, id_proveedor: int):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Proveedores WHERE id = ?", (id_proveedor,))
        conexion.commit()
        conexion.close()