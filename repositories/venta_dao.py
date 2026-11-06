from repositories.base_dao import BaseDAO
from domain.models.ventas import Venta, ItemVenta, Pago, Comprobante
from datetime import datetime

class VentaDAO(BaseDAO):
    def __init__(self):
        super().__init__()

    def guardar(self, venta: Venta):
        """Inserta la cabecera de la venta en la base de datos"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        if venta.id is None:
            sql = """INSERT INTO Ventas (fecha, estado, total, id_cajeero, id_local) VALUES (?, ?, ?, ?, ?) """
            cursor.execute(sql, (
                venta.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                venta.estado,
                float(venta.total),
                venta.cajero.id if venta.cajero else None,
                venta.local.id if venta.local else None
            ))
            venta.id = cursor.lastrowid

        else:
            sql = """UPDATE Ventas SET estado = ?, total = ? WHERE id = ?"""
            cursor.execute(sql,(venta.estado, float(venta.total), venta.id))

        conexion.commit()
        conexion.close()
        return venta

    def agregar_item(self, id_venta: int, item: ItemVenta):
        """Guarda un registro en la tabla detalle relacionando la venta con el producto"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        sql = """INSERT INTO ItemVenta (id_venta, id_producto, cantidad, precio_unitario) VALUES (?, ?, ?, ?)"""
        cursor.execute(sql, (
            id_venta,
            item.producto.id,
            item.cantidad,
            float(item.precio_unitario)
        ))
        conexion.commit()
        conexion.close()

    def registrar_pago(self, id_venta: int, pago: Pago):
        """Persiste el pago asociado a la venta, guardando el tipo de estrategia utilizada"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        tipo_medio_pago = pago.medio_pago.__class__.__name__ if pago.medio_pago else "Desconocido"

        sql = """INSERT INTO Pagos (id_venta, monto, referencia, tipo_medio_pago) VALUES (?, ?, ?, ?)"""
        cursor.execute(sql, (
            id_venta,
            float(pago.monto),
            pago.referencia,
            tipo_medio_pago
        ))

        pago.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return pago

    def guardar_comprobante(self, id_venta: int, comprobante: Comprobante):
        """Guarda la factura o ticket fiscal generado para la venta"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        sql = """INSERT INTO Comprobantes (id_venta, tipo, numero, fecha) VALUES (?, ?, ?, ?)"""
        cursor.execute(sql, (
            id_venta,
            comprobante.tipo,
            comprobante.numero,
            comprobante.fecha.strftime("%Y-%m-%d %H:%M:%S") if comprobante.fecha else None
        ))

        comprobante.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return comprobante