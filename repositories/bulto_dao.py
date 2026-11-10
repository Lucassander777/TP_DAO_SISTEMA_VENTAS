from repositories.base_dao import BaseDAO
from domain.models.logistica import Bulto, ItemBulto, CambioEstadoBulto
from domain.models.ubicacion import Local
from domain.models.catalogo import Producto
from datetime import datetime

class BultoDAO(BaseDAO):
    def __init__(self):
        super().__init__()

    def guardar(self, bulto: Bulto):
        """Inserta un nuevo bulto o actualiza su estado actual en la base de datos"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        nombre_estado = bulto.estado_actual.__class__.__name__ if bulto.estado_actual else "Preparado"

        if bulto.id is None:
            sql = """INSERT INTO Bultos (codigo, fecha_creacion, estado_actual, id_origen, id_destino) VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(sql, (
                bulto.codigo,
                bulto.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
                nombre_estado,
                bulto.origen.id if bulto.origen else None,
                bulto.destino.id if bulto.destino else None
            ))
            bulto.id = cursor.lastrowid
        else:
            sql = "UPDATE Bultos SET estado_actual=? WHERE id=?"
            cursor.execute(sql, (nombre_estado, bulto.id))

        conexion.commit()
        conexion.close()
        return bulto

    def agregar_item(self, id_bulto: int, item: ItemBulto):
        """Guarda un registro en la tabla detalle (ItemBulto) relacionando bulto y producto"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        sql = "INSERT INTO  ItemBulto(id_bulto, id_producto, cantidad) VALUES (?, ?, ?)"
        cursor.execute(sql, (id_bulto, item.producto.id, item.cantidad))

        conexion.commit()
        conexion.close()

    def registrar_cambio_estado(self, id_bulto: int, cambio: CambioEstadoBulto):
        """Guarda el registro inmutable de trazabilidad de los estados del bulto"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        sql = """INSERT INTO CambioEstadoBulto(id_bulto, estado, fecha_hora, usuario, observacion) VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(sql, (
            id_bulto,
            cambio.estado,
            cambio.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
            cambio.usuario,
            cambio.observacion
        ))
        cambio.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return cambio

    def obtener_por_codigo(self, codigo: str):
        """Busca un bulto en la base de datos usando su código alfanumérico."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id, codigo, id_origen, id_destino FROM Bultos WHERE codigo = ?", (codigo,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            id_bulto = fila['id'] if isinstance(fila, dict) or hasattr(fila, 'keys') else fila[0]
            codigo_b = fila['codigo'] if isinstance(fila, dict) or hasattr(fila, 'keys') else fila[1]
            id_origen = fila['id_origen'] if isinstance(fila, dict) or hasattr(fila, 'keys') else fila[2]
            id_destino = fila['id_destino'] if isinstance(fila, dict) or hasattr(fila, 'keys') else fila[3]

            # Instanciamos tu clase concreta real (Local hereda de Ubicacion)
            origen_obj = Local(id_ubicacion=id_origen, nombre="", direccion="") if id_origen else None
            destino_obj = Local(id_ubicacion=id_destino, nombre="", direccion="") if id_destino else None

            return Bulto(
                id_bulto=id_bulto, 
                codigo=codigo_b, 
                fecha_creacion=None, 
                origen=origen_obj, 
                destino=destino_obj
            )
        return None

    def actualizar_estado_cabecera(self, id_bulto: int, nuevo_estado: str):
        """Sobrescribe el estado del bulto en la tabla principal."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE Bultos SET estado_actual = ? WHERE id = ?", (nuevo_estado, id_bulto))
        conexion.commit()
        conexion.close()

    def obtener_items_por_bulto(self, id_bulto: int) -> list:
        """Busca los productos y cantidades guardados dentro de un bulto específico."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        
        sql = "SELECT id_producto, cantidad FROM ItemBulto WHERE id_bulto = ?"
        cursor.execute(sql, (id_bulto,))
        filas = cursor.fetchall()
        conexion.close()
        
        items = []
        for fila in filas:
            id_prod = fila['id_producto'] if isinstance(fila, dict) or hasattr(fila, 'keys') else fila[0]
            cantidad = fila['cantidad'] if isinstance(fila, dict) or hasattr(fila, 'keys') else fila[1]
            
            # Le agregamos categoria=None y proveedor=None para satisfacer a tu clase real
            prod_obj = Producto(
                id_producto=id_prod, 
                sku="N/A", 
                nombre="Prod DB", 
                precio_venta=0.0, 
                costo=0.0,
                categoria=None,
                proveedor=None
            )
            
            item = ItemBulto(producto=prod_obj, cantidad=cantidad)
            items.append(item)
            
        return items