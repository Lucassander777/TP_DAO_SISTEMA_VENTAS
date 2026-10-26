from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal

class ItemListaPrecios:
    def __init__(self, id_item: int, precio: Decimal, producto):
        self.id = id_item
        self.precio = precio 
        self.producto = producto

class ListaPrecios:
    def __init__(self, id_lista: int, nombre: str, vigente_desde: date, vigente_hasta: date, es_default: bool, activa: bool):
        self.id = id_lista
        self.nombre = nombre
        self.vigente_desde = vigente_desde
        self.vigente_hasta = vigente_hasta
        self.es_default = es_default
        self.activa = activa
        self.items = []

class Promocion(ABC):
    def __init__(self, nombre: str, descripcion: str, vigente_desde: date, vigente_hasta: date, activa: bool):
        self.nombre = nombre
        self.descripcion = descripcion
        self.vigente_desde = vigente_desde
        self.vigente_hasta = vigente_hasta
        self.activa = activa

    @abstractmethod
    def aplica(self, item) -> bool:
        pass

    @abstractmethod
    def calcular_descuento(self, item) -> Decimal:
        pass

class DescuentoPorcentaje(Promocion):
    def __init__(self, nombre: str, descripcion: str, vigente_desde: date, vigente_hasta: date, activa: bool, porcentaje: Decimal):
        super().__init__(nombre, descripcion, vigente_desde, vigente_hasta, activa)
        self.porcentaje = porcentaje

    def aplica(self, item) -> bool:
        pass
    def calcular_descuento(self, item) -> Decimal:
        pass

class DescuentoMontoFijo(Promocion):
    def __init__(self, nombre: str, descripcion: str, vigente_desde: date, vigente_hasta: date, activa: bool, monto: Decimal):
        super().__init__(nombre, descripcion, vigente_desde, vigente_hasta, activa)
        self.monto = monto

    def aplica(self, item) -> bool:
        pass
    def calcular_descuento(self, item) -> Decimal:
        pass

class PromoNxM(Promocion):
    def __init__(self, nombre: str, descripcion: str, vigente_desde: date, vigente_hasta: date, activa: bool, lleva: int, paga: int):
        super().__init__(nombre, descripcion, vigente_desde, vigente_hasta, activa)
        self.lleva = lleva
        self.paga = paga

    def aplica(self, item) -> bool:
        pass
    def calcular_descuento(self, item) -> Decimal:
        pass

class DescuentoAplicado:
    def __init__(self, id_descuento: int, monto: Decimal, origen: str, descripcion: str):
        self.id = id_descuento
        self.monto = monto
        self.origen = origen
        self.descripcion = descripcion
