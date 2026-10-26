from datetime import datetime, date
from decimal import Decimal

class NivelCliente:
    def __init__(self, id_nivel: int, nombre: str, monto_minimo_acumulado: Decimal, descuento_porcentaje: Decimal, puntos_por_peso: Decimal):
        self.id = id_nivel
        self.nombre = nombre
        self.monto_minimo_acumulado = monto_minimo_acumulado
        self.descuento_porcentaje = descuento_porcentaje
        self.puntos_por_peso = puntos_por_peso

class MovimientoPuntos:
    def __init__(self, id_movimiento: int, fecha: datetime, tipo: str, puntos: int):
        self.id = id_movimiento
        self.fecha = fecha
        self.tipo = tipo
        self.puntos = puntos

class CuentaCorriente:
    def __init__(self, id_cuenta: int, saldo: Decimal, limite_credito: Decimal, activa: bool):
        self.id = id_cuenta
        self.saldo = saldo
        self.limite_credito = limite_credito
        self.activa = activa

    def puede_cargar(self, monto: Decimal) -> bool:
        pass

class MovimientoCuenta:
    def __init__(self, id_movimiento: int, fecha: datetime, tipo: str, monto: Decimal, saldo_posterior: Decimal, venta=None):
        self.id = id_movimiento
        self.fecha = fecha
        self.tipo = tipo
        self.monto = monto
        self.saldo_posterior = saldo_posterior
        self.venta = venta

class Cliente:
    def __init__(self, id_cliente: int, tipo_documento: str, nro_documento: str, nombre: str, apellido: str, email: str, telefono: str, direccion: str, fecha_alta: date, puntos: int, activo: bool):
        self.id = id_cliente
        self.tipo_documento = tipo_documento
        self.nro_documento = nro_documento
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.fecha_alta = fecha_alta
        self.puntos = puntos
        self.activo = activo

        self.nivel = None
        self.lista_precios = None
        self.cuenta_corriente = None
        self.movimientos_puntos = None
