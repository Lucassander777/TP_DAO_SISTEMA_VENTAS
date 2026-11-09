from repositories.base_dao import BaseDAO
from domain.models.inventario import Stock, MovimientoStock, TipoMovimiento
from datetime import datetime

class InventarioDao(BaseDAO):
    def __init__(self):
        super().__init__()

    def obtener_stock(self, id_producto: int, id_ubicacion: int):
        """Devuelve el stock actual de un producto en una ubicación específica"""
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

        movimiento.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return movimiento

    def consultar_stock_disponible(self, id_producto: int, id_ubicacion: int) -> int:
        """Devuelve la cantidad física actual de un producto en un local/ubicación específica."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        
        sql = "SELECT cantidad_disponible FROM Stock WHERE id_producto = ? AND id_ubicacion = ?"
        cursor.execute(sql, (id_producto, id_ubicacion))
        fila = cursor.fetchone()
        conexion.close()
        
        if fila:
            return fila[0]
        return 0

    def obtener_faltantes_stock(self):
        """Busca productos con stock disponible inferior al stock mínimo"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("PRAGMA table_info(Productos)")
        columnas = [col[1] for col in cursor.fetchall()]
        col_minimo = "p.stock_minimo" if "stock_minimo" in columnas else "10"

        sql = f"""
            SELECT 
                p.nombre AS producto_nombre,
                COALESCE(SUM(s.cantidad_disponible), 0) AS stock_actual,
                {col_minimo} AS stock_minimo
            FROM Productos p
            LEFT JOIN Stock s ON p.id = s.id_producto
            GROUP BY p.id, p.nombre
            HAVING stock_actual < stock_minimo
        """
        cursor.execute(sql)
        filas = cursor.fetchall()
        conexion.close()

        faltantes = []
        for fila in filas:
            nombre = fila['producto_nombre'] if hasattr(fila, '__getitem__') and isinstance(fila, dict) or hasattr(fila, 'keys') else fila[0]
            actual = fila['stock_actual'] if hasattr(fila, '__getitem__') and isinstance(fila, dict) or hasattr(fila, 'keys') else fila[1]
            minimo = fila['stock_minimo'] if hasattr(fila, '__getitem__') and isinstance(fila, dict) or hasattr(fila, 'keys') else fila[2]

            sugerido = max(0, minimo - actual)
            faltantes.append({
                'producto_nombre': nombre,
                'stock_actual': actual,
                'stock_minimo': minimo,
                'cantidad_sugerida': sugerido
            })
        return faltantes