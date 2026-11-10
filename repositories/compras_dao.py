from repositories.base_dao import BaseDAO
from domain.models.compras import OrdenCompra

class ComprasDAO(BaseDAO):
    def __init__(self):
        super().__init__()

    def obtener_faltantes_stock(self):
        """Cruza la tabla de inventario con los productos para detectar cuáles están por debajo del stock mínimo."""

        conexion = self.get_conexion()
        cursor = conexion.cursor()

        # Usamos LEFT JOIN para sumar el stock físico real desde la tabla Stock
        cursor.execute("""
            SELECT 
                p.id, 
                p.nombre, 
                COALESCE(SUM(s.cantidad_disponible), 0) as stock_real, 
                p.stock_minimo
            FROM Productos p
            LEFT JOIN Stock s ON p.id = s.id_producto
            WHERE p.activo = 1
            GROUP BY p.id, p.nombre, p.stock_minimo
            HAVING stock_real < p.stock_minimo
        """)

        faltantes = cursor.fetchall()
        conexion.close()

        lista_faltantes = []
        for f in faltantes:
            lista_faltantes.append({
                'producto_id': f[0],
                'producto_nombre': f[1],
                'stock_actual': f[2],
                'stock_minimo': f[3],
                'cantidad_sugerida': f[3] - f[2]
            })
        return lista_faltantes

    def guardar_orden(self, orden: OrdenCompra) -> OrdenCompra:
        """Guarda la cabecera de la Orden de Compra sugerida en la base de datos."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO OrdenesCompra (fecha, estado, id_proveedor, total)
            VALUES (?, ?, ?, ?)
        """, (
            orden.fecha,
            orden.estado,
            orden.proveedor.id if orden.proveedor else None,
            orden.total
        ))
        orden.id = cursor.lastrowid

        conexion.commit()
        conexion.close()
        return orden