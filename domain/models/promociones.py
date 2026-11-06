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
        hoy = date.today()
        return self.activa and (self.vigente_desde <= hoy <= self.vigente_hasta)
    
    def calcular_descuento(self, item) -> Decimal:
        if not self.aplica(item):
            return Decimal("0.00")
        return item.precio * (self.porcentaje / Decimal("100"))

class DescuentoMontoFijo(Promocion):
    def __init__(self, nombre: str, descripcion: str, vigente_desde: date, vigente_hasta: date, activa: bool, monto: Decimal):
        super().__init__(nombre, descripcion, vigente_desde, vigente_hasta, activa)
        self.monto = monto

    def aplica(self, item) -> bool:
        hoy = date.today()
        return self.activa and (self.vigente_desde <= hoy <= self.vigente_hasta)
    
    def calcular_descuento(self, item) -> Decimal:
        if not self.aplica(item):
            return Decimal("0.00")
        return min(self.monto, item.precio)

class PromoNxM(Promocion):
    def __init__(self, nombre: str, descripcion: str, vigente_desde: date, vigente_hasta: date, activa: bool, lleva: int, paga: int):
        super().__init__(nombre, descripcion, vigente_desde, vigente_hasta, activa)
        self.lleva = lleva
        self.paga = paga

    def aplica(self, cantidad_comprada: int) -> bool:
        hoy = date.today()
        return self.activa and (self.vigente_desde <= hoy <= self.vigente_hasta) and (cantidad_comprada >= self.lleva)
    
    def calcular_descuento(self, item_precio: Decimal, cantidad_comprada: int) -> Decimal:
        if not self.aplica(cantidad_comprada):
            return Decimal("0.00")
        grupos = cantidad_comprada // self.lleva
        unidades_gratis = grupos * (self.lleva - self.paga)
        return item_precio * Decimal(unidades_gratis)
        

class DescuentoAplicado:
    def __init__(self, id_descuento: int, monto: Decimal, origen: str, descripcion: str):
        self.id = id_descuento
        self.monto = monto
        self.origen = origen
        self.descripcion = descripcion
