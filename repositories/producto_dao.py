from repositories.base_dao import BaseDao
from domain.models.catalogo import Producto

class ProductoDao(BaseDao):
    def __init__(self):
        super().__init__()

    def guardar(self, producto: Producto):
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        if producto.id is None:
            sql = "INSERT INTO Productos (sku, nombre, precio_venta, costo, activo) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(sql, (producto.sku, producto.nombre, float(producto.precio_venta), float(producto.costo), producto.activo))
            producto.id = cursor.lastrowid  # Asigna el ID generado automáticamente al producto

        else:
            sql = "UPDATE Productos SET sku=?, nombre=?, precio_venta=?, costo=?, activo=? WHERE id=?"
            cursor.execute(sql, (producto.sku, producto.nombre, float(producto.precio_venta), float(producto.costo), producto.activo, producto.id))

        conexion.commit()
        conexion.close()
        return producto

    def obtener_por_id(self, id_producto: int):
        conexion = self.get.conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM Productos WHERE id=?", (id_producto,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            prod = Producto(
                id_producto=fila["id"],
                sku=fila["sku"],
                nombre=fila["nombre"],
                precio_venta=fila["precio_venta"],
                costo=fila["costo"],
                categoria=None,
                proveedor=None,
            )
            prod.activo = bool(fila['activo'])
            return prod
        
        return None