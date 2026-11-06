from datetime import datetime
from decimal import Decimal
from domain.models.ventas import Venta, ItemVenta, Pago, Comprobante
from domain.models.pagos_strategy import MedioPago
from domain.models.inventario import TipoMovimiento
from domain.exceptions import NegocioException
from repositories.venta_dao import VentaDAO
from services.inventario_service import InventarioService

class VentaService:
    def __init__(self, venta_dao: VentaDAO, inventario_service: InventarioService):
        self.dao = venta_dao
        self.inventario_service = inventario_service

    def procesar_venta_completa(self, cajero, local, carrito_items: list, medio_pago: MedioPago, promocion=None) -> Venta:
        """Orquesta todo el flujo de una venta: creación, descuento de stock, cobro y facturación. carrito_items es una lista de diccionarios con {'producto': prod, 'cantidad': cant, 'precio': precio}"""
        if not carrito_items:
            raise NegocioException("No se puede procesaro una venta sin productos en el carrito")

        # 1- Calculamos el total bruto inical
        total_bruto = sum(item['cantidad'] * item['precio'] for item in carrito_items)
        total_venta = Decimal(str(total_bruto))

        if promocion is not None and promocion.aplica(carrito_items):
            descuento = promocion.calcular_descuento(carrito_items)
            total_venta -= descuento

        nueva_venta = Venta(
            id_venta=None,
            fecha=datetime.now(),
            estado="Completada",
            total=total_venta,
            cajero=cajero,
            local=local
        )
        # Guardamos la cabecera en SQLite
        nueva_venta = self.dao.guardar(nueva_venta)

        # 2- Guardamos el detalle y descontamos el stock físico
        for item_data in carrito_items:
            producto = item_data['producto']
            cantidad = item_data['cantidad']

            item_venta = ItemVenta(
                cantidad=cantidad,
                precio_unitario=item_data['precio'],
                producto=producto
            )
            # Persistimos el item de la venta en la BD
            self.dao.agregar_item(nueva_venta.id, item_venta)

            self.inventario_service.registrar_salida(
                id_producto=producto.id,
                id_ubicacion=local.id,
                cantidad=cantidad,
                tipo=TipoMovimiento.VENTA,
                referencia_tipo="Venta",
                referencia_id=nueva_venta.id
            )
        # 3- Aplicamos el Patrón Strategy para procesar el pago
        medio_pago.procesar_pago(nueva_venta.total)

        pago = Pago(
            id_pago=None,
            monto=nueva_venta.total,
            referencia="Pago de Venta",
            medio_pago=medio_pago
        )
        self.dao.registrar_pago(nueva_venta.id, pago)

        # 4- Generamos el comprobante fiscal (Ticket/Factura)
        comprobante = Comprobante(
            id_comprobante=None,
            tipo="Ticket Fiscal",
            numero=f"T-{nueva_venta.id:06d}",
            fecha=datetime.now()
        )
        self.dao.guardar_comprobante(nueva_venta.id, comprobante)

        return nueva_venta