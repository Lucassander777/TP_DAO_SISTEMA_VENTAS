from datetime import datetime, date
from domain.models.compras import RecepcionCompra, ItemRecepcion, OrdenCompra
from domain.models.lote import Lote
from domain.models.inventario import TipoMovimiento

class ComprasService:
    def __init__(self, compras_dao=None, inventario_service=None):
        # Manejo flexible por si se pasa compras_dao o inventario_service
        self.compras_dao = compras_dao
        self.inventario_service = inventario_service

    def generar_ordenes_sugeridas(self):
        """Llama al DAO de compras que consulta los faltantes en la BD"""
        if self.compras_dao and hasattr(self.compras_dao, 'obtener_faltantes_stock'):
            return self.compras_dao.obtener_faltantes_stock()
        elif self.compras_dao and hasattr(self.compras_dao, 'obtener_faltantes'):
            return self.compras_dao.obtener_faltantes()
        return []

    def recepcionar_orden(self, orden_compra: OrdenCompra, nro_remito_proveedor: str, items_recibidos: list) -> RecepcionCompra:
        """Procesa la llegada del camión del proveedor e incrementa el stock físico."""
        recepcion = RecepcionCompra(
            id_recepcion=None,
            fecha=datetime.now(),
            nro_remito_proveedor=nro_remito_proveedor,
            orden_compra=orden_compra
        )

        for data in items_recibidos:
            producto = data['item_orden'].producto

            nuevo_lote = Lote(
                id_lote=None,
                codigo=f"LOTE-{producto.sku}-{datetime.now().strftime('%Y%m%d')}",
                fecha_ingreso=date.today(),
                fecha_vencimiento=data['vencimiento'],
                activo=True,
                producto=producto,
                proveedor=orden_compra.proveedor
            )

            item_recepcion = ItemRecepcion(
                id_orden=data['item_orden'],
                cantidad=data['cantidad'],
                costo_unitario=data['costo'],
                lote=nuevo_lote
            )
            recepcion.items.append(item_recepcion)

            if self.inventario_service:
                self.inventario_service.registrar_entrada(
                    id_producto=producto.id,
                    id_ubicacion=orden_compra.destino.id,
                    cantidad=data['cantidad'],
                    tipo=TipoMovimiento.RECEPCION,
                    referencia_tipo="RecepcionCompra",
                    referencia_id=recepcion.id if recepcion.id else 0
                )

        return recepcion