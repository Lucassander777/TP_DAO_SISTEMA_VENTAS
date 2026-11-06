from domain.exceptions import NegocioException

class AuditoriaService:
    def __init__(self, auditoria_dao):
        self.dao = auditoria_dao

    def conciliar_inventario_fisico(self, id_producto, id_ubicacion, cantidad_fisica):
        if cantidad_fisica < 0:
            raise NegocioException("La cantidad física no puede ser negativa.")

        datos_sistema = self.dao.obtener_stock_actual(id_producto, id_ubicacion)
        if not datos_sistema:
            raise NegocioException(f"No hay registro de stock para el producto {id_producto} en la ubicación {id_ubicacion}.")

        stock_sistema = datos_sistema[0]
        nombre_producto = datos_sistema[1]

        diferencia = cantidad_fisica - stock_sistema

        self.dao.ajustar_stock(id_producto, id_ubicacion, cantidad_fisica, diferencia)

        if diferencia < 0:
            return f"Merma detectada: faltan {abs(diferencia)} unidades de {nombre_producto}."
        elif diferencia > 0:
            return f"Sobrante detectado: sobran {diferencia} unidades de {nombre_producto}."
        else:
            return f"Conciliación perfecta. El stock de {nombre_producto} coincide."
        