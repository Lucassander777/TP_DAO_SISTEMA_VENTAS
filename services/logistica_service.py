from datetime import datetime
from domain.models.logistica import Bulto, ItemBulto, CambioEstadoBulto
from domain.models.logistica_states import Preparado
from domain.exceptions import TransicionEstadoInvalidaException
from repositories.bulto_dao import BultoDAO

class LogisticaService:
    def __init__(self, bulto_dao: BultoDAO):
        self.dao = bulto_dao

    def armar_bulto(self, codigo: str, origen, destino, items_dict: dict, usuario: str) -> Bulto:
        """Crea un nuevo bulto desde cero. items_dict es un diccionario de {producto: cantidad}."""
        # 1- Instanciamos el Bulto (por defecto arranca en estado Preparado)
        nuevo_bulto = Bulto(
            id_bulto=None,
            codigo=codigo,
            fecha_creacion=datetime.now(),
            origen=origen,
            destino=destino
        )
        nuevo_bulto.estado_actual = Preparado()

        # 2- Guardamos la cabecera en la BD
        nuevo_bulto = self.dao.guardar(nuevo_bulto)

        # 3- Agregamos los ítems físicos
        for producto, cantidad in items_dict.items():
            item = ItemBulto(
                producto=producto,
                cantidad=cantidad
            )
            self.dao.agregar_item(nuevo_bulto.id, item)

        # 4- Registramos el movimiento inicial en la auditoría
        cambio_inicial = CambioEstadoBulto(
            id_cambio=None,
            estado="Preparado",
            fecha_hora=datetime.now(),
            usuario=usuario,
            observacion="Armado inicial del bulto"
        )
        self.dao.registrar_cambio_estado(nuevo_bulto.id, cambio_inicial)
        return nuevo_bulto

    def precintar_bulto(self, id_bulto: int, usuario: str, codigo_precinto: str):
        """Avanza el bulto al estado Precintado"""
        bulto = self.dao.obtener_por_id(id_bulto)
        if not bulto:
            raise ValueError("El bulto no existe.")

        # 1- Delegamos la validación de negocio al Patrón State
        bulto.estado_actual.precintar(bulto)

        # 2- Si pasó la validación, actualizamos la base de datos
        self.dao.guardar(bulto)

        # 3- Asentamos la trazabilidad inmutable
        cambio = CambioEstadoBulto(
            id_cambio=None,
            estado="Precintado",
            fecha_hora=datetime.now(),
            usuario=usuario,
            observacion=f'Precinto colocado: {codigo_precinto}'
        )
        self.dao.registrar_cambio_estado(bulto.id, cambio)

    def despachar_bulto(self, id_bulto: int, usuario: str, nro_remito: str = None):
        """Avanza el bulto al estado EnTransito"""
        bulto = self.dao.obtener_por_id(id_bulto)

        # Validamos usando el Patrón State (debe estar en Precintado para poder despacharse)
        bulto.estado_actual.despachar(bulto)

        self.dao.guardar(bulto)

        observacion = f"Despachado con remito {nro_remito}" if nro_remito else "Despachado sin remito"
        cambio = CambioEstadoBulto(
            id_cambio=None,
            estado="EnTransito",
            fecha_hora=datetime.now(),
            usuario=usuario,
            observacion=observacion
        )
        self.dao.registrar_cambio_estado(bulto.id, cambio)

    def actualizar_estado_bulto(self, codigo: str, estado_str: str, usuario: str, observacion: str):
        """Busca un bulto por su código y le cambia el estado, registrando la auditoría."""
        bulto = self.dao.obtener_por_codigo(codigo)
        if not bulto:
            raise ValueError(f"No se encontró ningún bulto con el código '{codigo}'")

        # 1. Registramos el movimiento en la tabla CambioEstadoBulto (Auditoría)
        cambio = CambioEstadoBulto(
            id_cambio=None,
            estado=estado_str,
            fecha_hora=datetime.now(),
            usuario=usuario,
            observacion=observacion
        )
        self.dao.registrar_cambio_estado(bulto.id, cambio)

        # 2. Actualizamos el estado actual en la tabla principal de Bultos
        self.dao.actualizar_estado_cabecera(bulto.id, estado_str)
