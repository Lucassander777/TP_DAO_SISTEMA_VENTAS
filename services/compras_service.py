from datetime import datetime, date
from domain.models.compras import RecepcionCompra, ItemRecepcion, OrdenCompra
from domain.models.lote import Lote
from domain.models.inventario import TipoMovimiento
from services.inventario_service import InventarioService

class ComprasService:
    def __init__(self, inventario_service: InventarioService):
        self.inventario_service = inventario_service

    def recepcionar_orden(self, orden_compra: OrdenCompra, nro_remito_proveedor: str, items_recibidos: list) -> RecepcionCompra:
        """Procesa la llegada del camión del proveedor. items_recibidos es una lista de diccionarios: [{'item_orden' : ItemOrdenCompra, 'cantidad' : int, 'costo' : Decimal, 'vencimiento' : date}]"""
        # 1- Armamos la cabecera de la recepción
        recepcion = RecepcionCompra(
            id_recepcion=None,
            fecha=datetime.now(),
            nro_remito_proveedor=nro_remito_proveedor,
            orden_compra=orden_compra
        )

        for data in items_recibidos:
            producto = data['item_orden'].producto

            # 2- Generamos el Lote para trazabilidad
            nuevo_lote = Lote(
                id_lote=None,
                codigo=f"LOTE-{producto.sku}-{datetime.now().strftime('%Y%m%d')}",
                fecha_ingreso=date.today(),
                fecha_vencimiento=data['vencimiento'],
                activo=True,
                producto=producto,
                proveedor=orden_compra.proveedor
            )

            # 3- Creamos el detalle de la recepción asociando el lote
            item_recepcion = ItemRecepcion(
                id_orden=data['item_orden'],
                cantidad=data['cantidad'],
                costo_unitario=data['costo'],
                lote=nuevo_lote
            )
            recepcion.items.append(item_recepcion)

            # 4- Llamamos a InventarioService para sumar el stock físico
            self.inventario_service.registrar_entrada(
                id_producto=producto.id,
                id_ubicacion=orden_compra.destino.id,
                cantidad=data['cantidad'],
                tipo=TipoMovimiento.RECEPCION,
                referencia_tipo="RecepcionCompra",
                referencia_id=recepcion.id if recepcion.id else 0
            )

        return recepcion
