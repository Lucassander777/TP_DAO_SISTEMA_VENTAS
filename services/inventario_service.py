from datetime import datetime
from domain.models.inventario import MovimientoStock, TipoMovimiento
from domain.exceptions import StockInsuficienteException
from repositories.inventario_dao import InventarioDao

class InventarioService:
    def __init__(self, inventario_dao: InventarioDao):
        # Guardamos ambas referencias para que NUNCA más falle por el nombre del atributo
        self.inventario_dao = inventario_dao
        self.dao = inventario_dao  

    def obtener_faltantes(self) -> list:
        return self.inventario_dao.obtener_faltantes_stock()

    def consultar_stock_disponible(self, id_producto: int, id_ubicacion: int) -> int:
        stock = self.inventario_dao.obtener_stock(id_producto, id_ubicacion)
        return stock.cantidad_disponible if stock else 0

    def registrar_entrada(self, id_producto: int, id_ubicacion: int, cantidad: int, tipo: TipoMovimiento, referencia_tipo: str, referencia_id: int):
        if cantidad <= 0:
            raise ValueError("La cantidad de entrada debe ser mayor a cero.")

        stock = self.inventario_dao.obtener_stock(id_producto, id_ubicacion)
        cantidad_fisica = (stock.cantidad_fisica if stock else 0) + cantidad
        cantidad_disponible = (stock.cantidad_disponible if stock else 0) + cantidad

        self.inventario_dao.actualizar_stock(id_producto, id_ubicacion, cantidad_fisica, cantidad_disponible)

        movimiento = MovimientoStock(
            id_movimiento=None,
            fecha=datetime.now(),
            cantidad=cantidad,
            tipo=tipo,
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id,
            producto=None,
            ubicacion=None,
            usuario=None
        )
        self.inventario_dao.registrar_movimiento(movimiento, id_producto, id_ubicacion)
        return movimiento

    def registrar_salida(self, id_producto: int, id_ubicacion: int, cantidad: int, tipo: TipoMovimiento, referencia_tipo: str, referencia_id: int):
        if cantidad <= 0:
            raise ValueError("La cantidad de salida debe ser mayor a cero.")

        stock_actual = self.inventario_dao.consultar_stock_disponible(id_producto, id_ubicacion)
        if stock_actual < cantidad:
            raise StockInsuficienteException(f"No hay stock suficiente. Requerido: {cantidad}, Disponible: {stock_actual}")

        stock = self.inventario_dao.obtener_stock(id_producto, id_ubicacion)
        nueva_fisica = stock.cantidad_fisica - cantidad
        nueva_disponible = stock.cantidad_disponible - cantidad

        self.inventario_dao.actualizar_stock(id_producto, id_ubicacion, nueva_fisica, nueva_disponible)

        movimiento = MovimientoStock(
            id_movimiento=None,
            fecha=datetime.now(),
            cantidad=-cantidad,
            tipo=tipo,
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id,
            producto=None,
            ubicacion=None,
            usuario=None
        )
        self.inventario_dao.registrar_movimiento(movimiento, id_producto, id_ubicacion)
        return movimiento

    def obtener_inventario_completo(self):
        return self.inventario_dao.obtener_inventario_completo()