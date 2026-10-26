from datetime import datetime

class OrdenReposicion:
    def __init__(self, id_orden: int, fecha: datetime, estado: str):
        self.id = id_orden
        self.fecha = fecha
        self.estado = estado
        self.items = [] # Lista de itemReposicion

class ItemReposicion:
    def __init__(self, producto, cantidad_solicitada: int):
        self.producto = producto
        self.cantidad_solicitada = cantidad_solicitada

class Precinto:
    def __init__(self, codigo: str):
        self.codigo = codigo
        self.violado = False

class Remito:
    def __init__(self, id_remito: int, numero: str, fecha_despacho: datetime):
        self.id = id_remito
        self.numero = numero
        self.fecha_despacho = fecha_despacho

class ItemBulto:
    def __init__(self, producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad

class CambioEstadoBulto:
    def __init__(self, id_cambio: int, estado: str, fecha_hora: datetime, usuario: str, observacion: str):
        self.id = id_cambio
        self.estado = estado
        self.fecha_hora = fecha_hora
        self.usuario = usuario
        self.observacion = observacion

class Bulto:
    def __init__(self, id_bulto: int, codigo: str, fecha_creacion: datetime, origen, destino):
        self.id = id_bulto
        self.codigo = codigo
        self.fecha_creacion = fecha_creacion
        self.estado_actual = None #Se inicializará con el Patrón State

        self.origen = origen
        self.destino = destino
        self.precinto = None
        self.remito = None
        self.items = [] # Lista de ItemBulto
        self.historial = [] # Lista de CambioEstadoBulto  