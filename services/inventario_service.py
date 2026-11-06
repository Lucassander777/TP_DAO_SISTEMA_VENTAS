from datetime import datetime
from domain.models.inventario import MovimientoStock, TipoMovimiento
from domain.exceptions import StockInsuficienteException
from repositories.inventario_dao import InventarioDao

class InventarioService:
    def __init__(self, inventario_dao: InventarioDao):
        self.dao = inventario_dao

    def consultar_stock_disponible(self, id_producto: int, id_ubicacion: int) -> int:
        """Devuelve la cantidad disponible para la venta o despacho"""
        stock = self.dao.obtener_stock(id_producto, id_ubicacion)
        return stock.cantidad_disponible if stock else 0

    def registrar_entrada(self, id_producto: int, id_ubicacion: int, cantidad: int, tipo: TipoMovimiento, referencia_tipo: str, referencia_id: int):
        """Suma stock y deja el registro inmutable en el historial"""
        if cantidad <= 0:
            raise ValueError("La cantidad de entrada debe ser mayor a cero.")

        # 1- Buscamos el stock actual
        stock = self.dao.obtener_stock(id_producto, id_ubicacion)
        cantidad_fisica = (stock.cantidad_fisica if stock else 0) + cantidad
        cantidad_disponible = (stock.cantidad_disponible if stock else 0) + cantidad

        # 2- Actualizamos la tabla stock
        self.dao.actualizar_stock(id_producto, id_ubicacion, cantidad_fisica, cantidad_disponible)

        # 3- Registramos el movimiento para trazabilidad
        movimiento = MovimientoStock(
            id_movimiento=None,
            fecha=datetime.now(),
            cantidad=cantidad,
            tipo=tipo,
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id
        )
        self.dao.registrar_movimiento(movimiento, id_producto, id_ubicacion)
        return movimiento

    def registrar_salida(self, id_producto: int, id_ubicacion: int, cantidad: int, tipo: TipoMovimiento, referencia_tipo: str, referencia_id: int):
        """Resta stock validando que haya disponibilidad suficiente"""
        if cantidad <= 0:
            raise ValueError("La cantidad de salida debe ser mayor a cero.")

        # 1- Validamos regla de negocio fundamental: ¿Hay Stock?
        stock_actual = self.dao.consultar_stock_disponible(id_producto, id_ubicacion)
        if stock_actual < cantidad:
            raise StockInsuficienteException(f"No hay stock suficiente. Requerido: {cantidad}, Disponible: {stock_actual}")

        # 2- Buscamos el stock fisico completo para restarlo
        stock = self.dao.obtener_stock(id_producto, id_ubicacion)
        nueva_fisica = stock.cantidad_fisica - cantidad
        nueva_disponible = stock.cantidad_disponible - cantidad

        # 3- Actualizamos tabla stock
        self.dao.actualizar_stock(id_producto, id_ubicacion, nueva_fisica, nueva_disponible)

        # 4- Registramos el movimiento (Con cantidad negativa para reflejar salida)
        movimiento = MovimientoStock(
            id_movimiento=None,
            fecha=datetime.now(),
            cantidad=-cantidad,
            tipo=tipo,
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id
        )
        self.dao.registrar_movimiento(movimiento, id_producto, id_ubicacion)
        return movimiento
