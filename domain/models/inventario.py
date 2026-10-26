from enum import Enum
from datetime import datetime

class TipoMovimiento(Enum):
    VENTA = "Venta"
    DEVOLUCION = "Devolución"
    DESPACHO = "Despacho"
    RECEPCION = "Recepción"
    VERIFICACION = "Verificación"
    RECHAZO = "Rechazo"

class Stock:
    def __init__(self, ubicacion, producto, cantidad_fisica: int = 0, cantidad_disponible: int = 0):
        self.ubicacion = ubicacion
        self.producto = producto
        self.cantidad_fisica = cantidad_fisica
        self.cantidad_disponible = cantidad_disponible

class MovimientoStock:
    def __init__(self, id_movimiento: int, fecha: datetime, cantidad: int, tipo: TipoMovimiento, referencia_tipo: str, referencia_id: int, producto, ubicacion, usuario):
        self.id = id_movimiento
        self.fecha = fecha
        self.cantidad = cantidad
        self.tipo = tipo
        self.referencia_tipo = referencia_tipo
        self.referencia_id = referencia_id

        self.producto = producto
        self.ubicacion = ubicacion
        self.usuario = usuario

class NivelMinimo:
    def __init__(self, producto, ubicacion, cantidad_minima: int):
        self.producto = producto
        self.ubicacion = ubicacion
        self.cantidad_minima = cantidad_minima