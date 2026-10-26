from datetime import date

class Lote:
    def __init__(self, id_lote: int, codigo: str, fecha_ingreso: date, fecha_vencimiento: date, activo: bool, producto, proveedor=None):
        self.id = id_lote
        self.codigo = codigo
        self.fecha_ingreso = fecha_ingreso
        self.fecha_vencimiento = fecha_vencimiento
        self.activo = activo

        self.producto = producto
        self.proveedor = proveedor

class StockLote:
    def __init__(self, lote, ubicacion, cantidad_fisica: int, cantidad_disponible: int):
        self.cantidad_fisica = cantidad_fisica
        self.cantidad_disponible = cantidad_disponible

        self.lote = lote
        self.ubicacion = ubicacion

class NumeroSerie:
    def __init__(self, id_serie: int, serie: str, estado: str, fecha_alta: date):
        self.id = id_serie
        self.serie = serie
        self.estado = estado
        self.fecha_alta = fecha_alta

        self.ubicacion_actual = None
        self.vendido_en = None
        self.item_bulto = None
        self.item_recepcion = None
        self.movimiento_stock = None
        self.item_conteo = None