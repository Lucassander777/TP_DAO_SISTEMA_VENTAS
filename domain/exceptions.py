class NegocioException(Exception):
    pass

class StockInsuficienteException(NegocioException):
    def __init__(self, mensaje="Stock insuficiente para la operación requerida."):
        super().__init__(mensaje)

class ProductoInactivoException(NegocioException):
    def __init__(self, mensaje="El producto está inactivo."):
        super().__init__(mensaje)

class TransicionEstadoInvalidaException(NegocioException):
    def __init__(self, mensaje="Transición de estado de bulto no permitida."):
        super().__init__(mensaje)

class SaldoInsuficienteException(NegocioException):
    def __init__(self, mensaje="Saldo insuficiente en la cuenta corriente y límite de crédito excedido."):
        super().__init__(mensaje)

class EstadoDocumentoException(NegocioException):
    def __init__(self, mensaje="El documento no se encuentra en un estado válido para esta acción."):
        super().__init__(mensaje)

class PromocionInvalidaException(NegocioException):
    def __init__(self, mensaje="La promoción no está vigente o inactiva."):
        super().__init__(mensaje)