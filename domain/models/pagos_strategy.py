from abc import ABC, abstractmethod
from decimal import Decimal

class MedioPago(ABC):
    @abstractmethod
    def procesar_pago(self, monto: Decimal):
        pass

class PagoEfectivo(MedioPago):
    def procesar_pago(self, monto: Decimal):
        pass

class PagoTrajeta(MedioPago):
    def __init__(self, numero_tarjeta: str, cuotas: int):
        self.numero_tarjeta = numero_tarjeta
        self.cuotas = cuotas

    def procesar_pago(self, monto: Decimal):
        pass

class PagoTransferencia(MedioPago):
    def __init__(self, cbu_origen: str, comprobante_bancario: str):
        self.cbu_origen = cbu_origen
        self.comprobante_bancario = comprobante_bancario

    def procesar_pago(self, monto: Decimal):
        pass
