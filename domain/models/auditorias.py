from datetime import datetime

class ItemConteo:
    def __init__(self, producto, cantidad_sistema: int, cantidad_contada: int, diferencia: int, lote=None):
        self.producto = producto
        self.cantidad_sistema = cantidad_sistema
        self.cantidad_contada = cantidad_contada
        self.diferencia = diferencia
        self.lote = lote

class InventarioFisico:
    def __init__(self, id_inventario: int, fecha_inicio: datetime, fecha_cierre: datetime, estado: str, responsable, ubicacion):
        self.id = id_inventario
        self.fecha_inicio = fecha_inicio
        self.fecha_cierre = fecha_cierre
        self.estado = estado
        self.reponsable = responsable
        self.ubicacion = ubicacion
        self.items = [] # Lista de ItemConteo

    def iniciar(self):
        pass
    def aprobar(self, usuario):
        pass
    def cerrar(self):
        pass
    def aplicar(self):
        pass

class AjusteStock:
    def __init__(self, id_ajuste: int, tipo : int, fecha: datetime, estado: str, cantidad_ajuste:int, motivo: str, producto, ubicacion, usuario):
        self.id = id_ajuste
        self.tipo = tipo
        self.fecha = fecha
        self.estado = estado
        self.cantidad_ajuste = cantidad_ajuste
        self.motivo = motivo

        self.producto = producto
        self.ubicacion = ubicacion
        self.usuario = usuario