from datetime import date
from domain.models.lote import Lote

class LoteService:
    def __init__(self, lote_dao):
        self.dao = lote_dao

    def registrar_lote_manual(self, codigo: str, fecha_vencimiento_str: str, producto):
        """Registrar un lote nuevo ingresado por el ususario"""

        nuevo_lote = Lote(
            id_lote=None,
            codig=codigo,
            fecha_ingreso=date.today(),
            fecha_vencimiento=fecha_vencimiento_str,
            activo=True,
            producto=producto,
            proveedor=None
        )

        return self.dao.guardar(nuevo_lote)

    def auditar_vencimiento(self):
        """Devuelve una lista de lotes que ya están vencidos al día de hoy."""
        hoy_str = date.today().strftime('%Y-%m-%d')
        return self.dao.obtener_lotes_vencidos(hoy_str)