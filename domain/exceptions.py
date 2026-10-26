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