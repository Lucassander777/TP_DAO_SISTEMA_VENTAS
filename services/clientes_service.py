from domain.exceptions import NegocioException

class ClienteService:
    def __init__(self, cliente_dao):
        self.dao = cliente_dao

    def registrar_cliente(self, nombre, dni, limite_credito):
        if self.dao.obtener_por_dni(dni):
            raise NegocioException("Ya existe un cliente registrado con ese DNI.")
        return self.dao.guardar(nombre, dni, limite_credito)

    def consultar_cuenta(self, dni):
        cliente = self.dao.obtener_por_dni(dni)
        if not cliente:
            raise NegocioException("Cliente no encontrado.")

        return{
            'id': cliente[0],
            'nombre': cliente[1],
            'dni': cliente[2],
            'saldo': cliente[3],
            'limite_credito': cliente[4]
        }

    def cargar_saldo(self, dni, monto):
        if monto <= 0:
            raise NegocioException("El monto a cargar debe ser mayor a cero.")
        cuenta = self.consultar_cuenta(dni)
        nuevo_saldo = cuenta['saldo'] + monto

        self.dao.actualizar_saldo(cuenta['id'], nuevo_saldo)
        return nuevo_saldo