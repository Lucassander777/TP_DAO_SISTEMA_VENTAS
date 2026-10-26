from datetime import datetime, date
from decimal import Decimal

class ItemOrdenCompra:
    def __init__(self, producto, stock_al_generar: int, minimo_al_generar: int, cantidad_sugerida: int, cantidad_pedida: int, cantidad_recibida: int, costo_unitario: Decimal):
        self.producto = producto
        self.stock_al_generar = stock_al_generar
        self.minimo_al_generar = minimo_al_generar
        self.cantidad_sugerida = cantidad_sugerida
        self.cantidad_pedida = cantidad_pedida
        self.cantidad_recibida = cantidad_recibida
        self.costo_unitario = costo_unitario

class OrdenCompra:
    def __init__(self, id_orden: int, numero: str, fecha: datetime, estado: str, origen: str, fecha_entrega_estimada: date, total_estimado: Decimal, proveedor, destino):
        self.id = id_orden
        self.numero = numero
        self.fecha = fecha
        self.estado = estado
        self.origen = origen
        self.fecha_entrega_estimada = fecha_entrega_estimada
        self.total_estimado = total_estimado

        self.proveedor = proveedor
        self.destino = destino
        self.items = [] # Lista de ItemOrdenCompra

    def aprobar(self, usuario):
        pass
    def cancelar(self, motivo: str):
        pass

class ItemRecepcion:
    def __init__(self, item_orden, cantidad: int, costo_unitario: Decimal, lote=None):
        self.item_orden = item_orden
        self.cantidad = cantidad
        self.costo_unitario = costo_unitario
        self.lote = lote

class RecepcionCompra:
    def __init__(self, id_recepcion: int, fecha: datetime, nro_remito_proveedor: str, orden_compra):
        self.id = id_recepcion
        self.fecha = fecha
        self.nro_remito_proveedor = nro_remito_proveedor
        self.orden_compra = orden_compra
        self.items = [] 