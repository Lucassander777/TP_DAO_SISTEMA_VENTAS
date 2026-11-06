from repositories.base_dao import BaseDAO
from domain.models.lote import Lote

class LoteDAO(BaseDAO):
    def __init__(self):
        super().__init__()

    def guardar(self, lote) -> Lote:
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO Lotes (codigo, fecha_ingreso, fecha_vencimiento, activo, id_producto, id_proveedor)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            lote.codigo,
            lote.fecha_ingreso,
            lote.fecha_vencimiento,
            lote.activo,
            lote.producto.id,
            lote.proveedor.id if lote.proveedor else None
        ))

        lote.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return lote

    def obtener_lotes_vencidos(self, fecha_actual_str: str):
        """Busca en SQLite los lotes cuya fecha de vencimiento ya pasó."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT l.codigo, l.fecha_vencimiento, p.nombre
            FROM Lotes l
            JOIN Productos p ON l.id_producto = p.id
            WHERE l.fecha_vencimiento < ? AND l.activo = 1
        """, (fecha_actual_str,))

        vencidos = cursor.fetchall()
        conexion.close()
        return vencidos

