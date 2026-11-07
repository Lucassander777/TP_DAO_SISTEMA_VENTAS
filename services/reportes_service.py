class ReportesService:
    def __init__(self, reportes_dao):
        self.dao = reportes_dao

    def obtener_ventas_ingresos(self):
        return self.dao.reporte_ventas_ingresos()

    def obtener_productos_mas_vendidos(self):
        return self.dao.reporte_productos_mas_vendidos()

    def obtener_stock_critico(self):
        return self.dao.reporte_stock_critico()

    def obtener_bultos_rechazados(self):
        return self.dao.reporte_bultos_rechazados()

    def obtener_tiempo_transito(self):
        return self.dao.reporte_tiempo_transito()

    def obtener_valorizacion_inventario(self):
        return self.dao.reporte_valorizacion_inventario()
    