from datetime import datetime
from domain.exceptions import EstadoDocumentoException

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
        if self.estado != "Planificado":
            raise EstadoDocumentoException("Solo se pueden iniciar inventarios planificados.")
        self.estado = "En Proceso"

    def aprobar(self, usuario):
        if self.estado != "Cerrado":
            raise EstadoDocumentoException("Solo se pueden aprobar inventarios cerrados.")
        self.aprobado_por = usuario

    def cerrar(self):
        if self.estado != "En Proceso":
            raise EstadoDocumentoException("El inventario debe estar en proceso para cerrarlo.")
        self.estado = "Cerrado"
        self.fecha_cierre = datetime.now()

    def aplicar(self):
        if not self.aprobado_por:
            raise EstadoDocumentoException("El inventario debe estar aprobado antes de aplicar las diferencias.")
        self.estado = "Aplicado"

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