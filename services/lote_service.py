from datetime import date
from domain.models.lote import Lote
from domain.models.inventario import TipoMovimiento # Asegurate de tener esto importado

class LoteService:
    # 1. Agregamos el inventario_service al constructor
    def __init__(self, lote_dao, inventario_service):
        self.dao = lote_dao
        self.inventario_service = inventario_service

    # 2. Sumamos los dos parámetros nuevos que mandamos desde la interfaz
    def registrar_lote_manual(self, codigo: str, fecha_vencimiento_str: str, producto, cantidad: int, ubicacion_id: int):
        """Registrar un lote nuevo ingresado por el usuario e impactar el stock físico"""

        nuevo_lote = Lote(
            id_lote=None,
            codigo=codigo,
            fecha_ingreso=date.today(),
            fecha_vencimiento=fecha_vencimiento_str,
            activo=True,
            producto=producto,
            proveedor=None
        )

        # Guardamos el registro del lote en la BD
        lote_guardado = self.dao.guardar(nuevo_lote)

        # 3. Sumamos el stock en la base de datos a través del servicio de inventario
        prod_id = producto.id_producto if hasattr(producto, 'id_producto') else producto.id
        
        # Intentamos obtener el ID generado del lote para el registro del movimiento
        lote_id = lote_guardado.id if hasattr(lote_guardado, 'id') else 0 

        self.inventario_service.registrar_entrada(
            id_producto=prod_id,
            id_ubicacion=ubicacion_id,
            cantidad=cantidad,
            tipo=TipoMovimiento.RECEPCION,
            referencia_tipo="Lote",
            referencia_id=lote_id
        )

        return lote_guardado

    def auditar_vencimiento(self):
        """Devuelve una lista de lotes que ya están vencidos al día de hoy."""
        hoy_str = date.today().strftime('%Y-%m-%d')
        return self.dao.obtener_lotes_vencidos(hoy_str)