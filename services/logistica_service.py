from datetime import datetime
from domain.models.logistica import Bulto, ItemBulto, CambioEstadoBulto
from domain.models.logistica_states import Preparado
from domain.exceptions import TransicionEstadoInvalidaException
from domain.models.inventario import TipoMovimiento 
from repositories.bulto_dao import BultoDAO
from services.inventario_service import InventarioService 

class LogisticaService:
    def __init__(self, bulto_dao: BultoDAO, inventario_service: InventarioService = None):
        self.dao = bulto_dao
        self.inventario_service = inventario_service

    def armar_bulto(self, codigo: str, origen, destino, items_dict: dict, usuario: str) -> Bulto:
        """Crea un nuevo bulto desde cero. items_dict es un diccionario de {producto: cantidad}."""
        if origen and destino and origen.id == destino.id:
            raise ValueError("El origen y el destino del bulto deben ser sucursales diferentes.")

        nuevo_bulto = Bulto(
            id_bulto=None,
            codigo=codigo,
            fecha_creacion=datetime.now(),
            origen=origen,
            destino=destino
        )
        nuevo_bulto.estado_actual = Preparado()
        nuevo_bulto = self.dao.guardar(nuevo_bulto)

        for producto, cantidad in items_dict.items():
            item = ItemBulto(
                producto=producto,
                cantidad=cantidad
            )
            self.dao.agregar_item(nuevo_bulto.id, item)

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
        bulto = self.dao.obtener_por_id(id_bulto)
        if not bulto:
            raise ValueError("El bulto no existe.")
        
        bulto.estado_actual.precintar(bulto)
        self.dao.guardar(bulto)

        cambio = CambioEstadoBulto(
            id_cambio=None,
            estado="Precintado",
            fecha_hora=datetime.now(),
            usuario=usuario,
            observacion=f'Precinto colocado: {codigo_precinto}'
        )
        self.dao.registrar_cambio_estado(bulto.id, cambio)

    def despachar_bulto(self, id_bulto: int, usuario: str, nro_remito: str = None):
        bulto = self.dao.obtener_por_id(id_bulto)
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

        # 1. Registramos el cambio de estado en la cabecera e historial
        cambio = CambioEstadoBulto(
            id_cambio=None,
            estado=estado_str,
            fecha_hora=datetime.now(),
            usuario=usuario,
            observacion=observacion
        )
        self.dao.registrar_cambio_estado(bulto.id, cambio)
        self.dao.actualizar_estado_cabecera(bulto.id, estado_str)

        # 2. REGLA DE NEGOCIO LOGÍSTICA: 
        # Si se verifica la entrega, restamos stock del origen y sumamos en destino
        if estado_str == "Verificado" and self.inventario_service:
            items_bulto = self.dao.obtener_items_por_bulto(bulto.id)
            
            for item in items_bulto:
                id_prod = item.producto.id
                cant = item.cantidad
                
                # A) RESTAR DEL ORIGEN (Centro de Distribución)
                if bulto.origen:
                    stock_origen = self.inventario_service.dao.obtener_stock(id_prod, bulto.origen.id)
                    if stock_origen:
                        nueva_fisica_orig = stock_origen.cantidad_fisica - cant
                        nueva_disp_orig = stock_origen.cantidad_disponible - cant
                        
                        # Control de seguridad por si despachan más de lo que hay
                        if nueva_fisica_orig < 0: nueva_fisica_orig = 0
                        if nueva_disp_orig < 0: nueva_disp_orig = 0
                        
                        self.inventario_service.dao.actualizar_stock(
                            id_prod, bulto.origen.id, nueva_fisica_orig, nueva_disp_orig
                        )

                # B) SUMAR AL DESTINO (Local)
                if bulto.destino:
                    stock_destino = self.inventario_service.dao.obtener_stock(id_prod, bulto.destino.id)
                    if stock_destino:
                        nueva_fisica_dest = stock_destino.cantidad_fisica + cant
                        nueva_disp_dest = stock_destino.cantidad_disponible + cant
                        self.inventario_service.dao.actualizar_stock(
                            id_prod, bulto.destino.id, nueva_fisica_dest, nueva_disp_dest
                        )
                    else:
                        # Si el local nunca tuvo este producto, se crea la fila de stock de cero
                        self.inventario_service.dao.actualizar_stock(
                            id_prod, bulto.destino.id, cant, cant
                        )

        return bulto
