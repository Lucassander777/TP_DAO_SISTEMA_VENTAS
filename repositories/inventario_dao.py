from repositories.base_dao import BaseDAO
from domain.models.inventario import Stock, MovimientoStock, TipoMovimiento
from datetime import datetime

class InventarioDao(BaseDAO):
    def __init__(self):
        super().__init__()

    def obtener_stock(self, id_producto: int, id_ubicacion: int):
        """Devuelve el sotck actual de un producto en una ubicación específica"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        sql = "SELECT cantidad_fisica, cantidad_disponible FROM Stock WHERE id_producto=? AND id_ubicacion=?"
        cursor.execute(sql, (id_producto, id_ubicacion))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            return Stock(
                producto=None,
                ubicacion=None,
                cantidad_fisica=fila['cantidad_fisica'],
                cantidad_disponible=fila['cantidad_disponible']
            )
        return None

    def actualizar_stock(self, id_producto: int, id_ubicacion: int, cantidad_fisica: int, cantidad_disponible: int):
        """Inserta el registro de stock si no existe, o lo actualiza si ya existe"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT 1 FROM Stock WHERE id_producto=? AND id_ubicacion=?", (id_producto, id_ubicacion))
        existe = cursor.fetchone()

        if existe:
            sql = """UPDATE Stock SET cantidad_fisica=?, cantidad_disponible=? WHERE id_producto=? AND id_ubicacion=?"""
            cursor.execute(sql, (cantidad_fisica, cantidad_disponible, id_producto, id_ubicacion))

        else:
            sql = """INSERT INTO Stock (id_producto, id_ubicacion, cantidad_fisica, cantidad_disponible) VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, (id_producto, id_ubicacion, cantidad_fisica, cantidad_disponible))
        conexion.commit()
        conexion.close()

    def registrar_movimiento(self, movimiento: MovimientoStock, id_producto: int, id_ubicacion: int):
        """Guarda un registro inmutable en el historial de movimientos"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        sql = """INSERT INTO MovimientoStock (fecha, cantidad, tipo, referencia_tipo, referencia_id, id_producto, id_ubicacion) VALUES (?, ?, ?, ?, ?, ?, ?)"""

        cursor.execute(sql, (
            movimiento.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            movimiento.cantidad,
            movimiento.tipo.value,
            movimiento.referencia_tipo,
            movimiento.referencia_id,
            id_producto,
            id_ubicacion
        ))

        movimiento.id = cursor.lastrowid  # Asigna el ID generado automáticamente al movimiento
        conexion.commit()
        conexion.close()
        return movimiento