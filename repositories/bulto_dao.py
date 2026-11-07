from repositories.base_dao import BaseDAO
from domain.models.logistica import Bulto, ItemBulto, CambioEstadoBulto
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
        cursor.execute("SELECT id, codigo FROM Bultos WHERE codigo = ?", (codigo,))
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            # Devolvemos un objeto Bulto básico para que el Service extraiga el ID
            return Bulto(id_bulto=fila[0], codigo=fila[1], fecha_creacion=None, origen=None, destino=None)
        return None

    def actualizar_estado_cabecera(self, id_bulto: int, nuevo_estado: str):
        """Sobrescribe el estado del bulto en la tabla principal."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE Bultos SET estado_actual = ? WHERE id = ?", (nuevo_estado, id_bulto))
        conexion.commit()
        conexion.close()