from datetime import datetime, date
from domain.models.compras import RecepcionCompra, ItemRecepcion, OrdenCompra
from domain.models.lote import Lote
from domain.models.inventario import TipoMovimiento
from repositories.compras_dao import ComprasDAO
from services.inventario_service import InventarioService

class ComprasService:
    def __init__(self, compras_dao: ComprasDAO = None, inventario_service: InventarioService = None):
        self.compras_dao = compras_dao
        self.inventario_service = inventario_service

    def generar_ordenes_sugeridas(self):
        """Devuelve la lista de productos que necesitan reponerse."""
        if self.compras_dao:
            return self.compras_dao.obtener_faltantes_stock()
        return []

    def crear_orden_compra(self, proveedor, items: list, total: float) -> OrdenCompra:
        """Crea y guarda una nueva orden de compra en estado Pendiente."""
        # Se asume que 'items' es una lista de objetos ItemOrdenCompra
        nueva_orden = OrdenCompra(
            id_orden=None,
            fecha=datetime.now(),
            proveedor=proveedor,
            items=items,
            estado="Pendiente",
            total=total
        )
        return self.compras_dao.guardar_orden(nueva_orden)

    def recepcionar_orden(self, orden_compra: OrdenCompra, nro_remito_proveedor: str, items_recibidos: list) -> RecepcionCompra:
        """Procesa la llegada del camión y suma stock físico."""
        recepcion = RecepcionCompra(
            id_recepcion=None,
            fecha=datetime.now(),
            nro_remito_proveedor=nro_remito_proveedor,
            orden_compra=orden_compra
        )

        for data in items_recibidos:
            # data debe ser un dict: {'item_orden': ItemOrdenCompra, 'cantidad': int, 'costo': float, 'vencimiento': date}
            producto = data['item_orden'].producto

            nuevo_lote = Lote(
                id_lote=None,
                codigo=f"LOTE-{producto.sku}-{datetime.now().strftime('%Y%m%d')}",
                fecha_ingreso=date.today(),
                fecha_vencimiento=data.get('vencimiento', date.today()), # Valor por defecto seguro
                activo=True,
                producto=producto,
                proveedor=orden_compra.proveedor
            )

            item_recepcion = ItemRecepcion(
                item_orden=data['item_orden'],
                cantidad=data['cantidad'],
                costo_unitario=data['costo'],
                lote=nuevo_lote
            )
            recepcion.items.append(item_recepcion)

            # Sumar al inventario
            if self.inventario_service:
                # Se asume que destino es Ubicacion 1 (Centro Distribucion). Ajustá si es dinámico.
                id_destino = orden_compra.destino.id if hasattr(orden_compra, 'destino') and orden_compra.destino else 1
                
                self.inventario_service.registrar_entrada(
                    id_producto=producto.id,
                    id_ubicacion=id_destino,
                    cantidad=data['cantidad'],
                    tipo=TipoMovimiento.RECEPCION,
                    referencia_tipo="RecepcionCompra",
                    referencia_id=orden_compra.id if hasattr(orden_compra, 'id') else 0
                )

        # Actualizar estado de la orden a Recibida
        if hasattr(orden_compra, 'id') and orden_compra.id:
            self.compras_dao.actualizar_estado_orden(orden_compra.id, "Recibida")

        return recepcion