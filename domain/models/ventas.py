from datetime import datetime
from decimal import Decimal

class ItemVenta:
    def __init__(self, producto, cantidad: int, precio_unitario: Decimal):
        self.prodcuto = producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

class Comprobante:
    def __init__(self, id_comprobante: int, tipo: str, numero: str, fecha: datetime):
        self.id = id_comprobante
        self.tipo = tipo
        self.numero = numero
        self.fecha = fecha

class Pago:
    def __init__(self, id_pago: int, monto: Decimal, referencia: str):
        self.id = id_pago
        self.monto = monto
        self.referecnia = referencia
        self.medio_pago = None # Se integrará en el Patrón Strategy

class Venta:
    def __init__(self, id_venta: int, fecha: datetime, estado: str, total: Decimal, cajero, local):
        self.id = id_venta
        self.fecha = fecha
        self.estado = estado
        self.total = total

        self.cajero = cajero
        self.local = local
        self.items = [] # Lista de ItemVenta
        self.comprobante = None 
        self.pago = None 

class ItemDevolucion:
    def __init__(self, producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad

class Devolucion:
    def __init__(self, id_devolucion: int, fecha: datetime, motivo: str, monto_reintegrado: Decimal, venta_original=None):
        self.id_devolucion = id_devolucion
        self.fecha = fecha
        self.motivo = motivo
        self.monto_reintegrado = monto_reintegrado

        self.venta_original = venta_original
        self.items = [] # Lista de ItemDevolucion

class MovimientoCaja:
    def __init__(self, id_movimiento: int, fecha: datetime, tipo: str, monto: Decimal):
        self.id = id_movimiento
        self.fecha = fecha
        self.tipo = tipo
        self.monto = monto
