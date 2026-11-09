from datetime import datetime
from repositories.base_dao import BaseDAO

class AuditoriaDAO(BaseDAO):
    def __init__(self):
        super().__init__()

    def obtener_stock_actual(self, id_producto, id_ubicacion):
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT s.cantidad_fisica, COALESCE(p.nombre, 'Producto sin registrar')
            FROM Stock s
            LEFT JOIN Productos p ON s.id_producto = p.id
            WHERE s.id_producto = ? AND s.id_ubicacion = ?
        """, (id_producto, id_ubicacion))

        resultado = cursor.fetchone()
        conexion.close()
        return resultado

    def ajustar_stock(self, id_producto, id_ubicacion, nueva_cantidad, diferencia):
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE Stock
            SET cantidad_fisica = ?, cantidad_disponible = ?
            WHERE id_producto = ? AND id_ubicacion = ?
        """, (nueva_cantidad, nueva_cantidad, id_producto, id_ubicacion))

        cursor.execute("""
            INSERT INTO MovimientoStock (fecha, cantidad, tipo, referencia_tipo, referencia_id, id_producto, id_ubicacion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(),
            diferencia,
            'AJUSTE_AUDITORIA',
            'Conciliacion Fisica',
            0,
            id_producto,
            id_ubicacion
        ))

        conexion.commit()
        conexion.close()