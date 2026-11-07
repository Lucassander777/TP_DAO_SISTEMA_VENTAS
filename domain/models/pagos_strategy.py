from abc import ABC, abstractmethod
from decimal import Decimal

class MedioPago(ABC):
    @abstractmethod
    def validar(self, monto: Decimal):
        pass
        
    @abstractmethod
    def procesar_pago(self, monto: Decimal):
        pass

class PagoEfectivo(MedioPago):
    def validar(self, monto: Decimal):
        # El efectivo no requiere validación extra de comprobantes
        return True
        
    def procesar_pago(self, monto: Decimal):
        pass

class PagoTarjeta(MedioPago):
    def __init__(self, numero_tarjeta: str, cuotas: int):
        self.numero_tarjeta = numero_tarjeta
        self.cuotas = cuotas

    def validar(self, monto: Decimal):
        if not self.numero_tarjeta:
            raise ValueError("Falta el número de tarjeta")
        return True

    def procesar_pago(self, monto: Decimal):
        pass

class PagoTransferencia(MedioPago):
    def __init__(self, cbu_origen: str, comprobante_bancario: str):
        self.cbu_origen = cbu_origen
        self.comprobante_bancario = comprobante_bancario

    def validar(self, monto: Decimal):
        if not self.comprobante_bancario:
            raise ValueError("Falta el comprobante de transferencia")
        return True

    def procesar_pago(self, monto: Decimal):
        pass