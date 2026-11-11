from repositories.base_dao import BaseDAO

class ReportesDAO(BaseDAO):
    def __init__(self):
        super().__init__()

    def reporte_ventas_ingresos(self):
        """Reporte de Ventas e ingresos por local y medio de pago."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COALESCE(u.nombre, 'Local no registrado') as local, 
                   COALESCE(p.tipo_medio_pago, 'No especificado') as tipo_medio_pago, 
                   COUNT(v.id) as cant_ventas, 
                   SUM(COALESCE(p.monto, v.total)) as total
            FROM Ventas v
            LEFT JOIN Pagos p ON v.id = p.id_venta
            LEFT JOIN Ubicaciones u ON v.id_local = u.id
            WHERE v.estado = 'Completada'
            GROUP BY local, tipo_medio_pago
        """)
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    def reporte_productos_mas_vendidos(self):
        """Reporte de productos más vendidos y margen de ganancia estimado."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COALESCE(pr.nombre, 'Producto sin registro') as nombre, 
                   SUM(iv.cantidad) as unidades,
                   SUM(iv.cantidad * iv.precio_unitario) as recaudacion,
                   SUM(iv.cantidad * (iv.precio_unitario - COALESCE(pr.costo, 0))) as ganancia_estimada
            FROM ItemVenta iv
            LEFT JOIN Productos pr ON iv.id_producto = pr.id
            LEFT JOIN Ventas v ON iv.id_venta = v.id
            GROUP BY pr.nombre
            ORDER BY unidades DESC
        """)
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    def reporte_stock_critico(self):
        """Reporte de existencias actuales vs productos en stock mínimo."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COALESCE(pr.nombre, 'Producto sin registro') as nombre, 
                   COALESCE(u.nombre, 'Ubicación sin registro') as ubicacion, 
                   s.cantidad_fisica, 
                   COALESCE(pr.stock_minimo, 0) as stock_minimo
            FROM Stock s
            LEFT JOIN Productos pr ON s.id_producto = pr.id
            LEFT JOIN Ubicaciones u ON s.id_ubicacion = u.id
            WHERE s.cantidad_fisica <= COALESCE(pr.stock_minimo, 0)
        """)
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    def reporte_bultos_rechazados(self):
        """Lista los bultos que fueron rechazados, indicando, el usuario y el motivo (ej: rotura de precinto)."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT b.codigo, c.fecha_hora, c.usuario, c.observacion
            FROM Bultos b
            JOIN CambioEstadoBulto c ON b.id = c.id_bulto
            WHERE c.estado = 'Rechazado'
            ORDER BY c.fecha_hora DESC
        """)
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    def reporte_tiempo_transito(self):
        """Calcula el tiempo promedio en horas que tarda un bulto desde 'En Tránsito' hasta 'Recibido'."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                b.codigo,
                c1.fecha_hora as fecha_envio,
                c2.fecha_hora as fecha_recepcion,
                ROUND((julianday(c2.fecha_hora) - julianday(c1.fecha_hora)) * 24, 2) as horas_transito
            FROM Bultos b
            JOIN CambioEstadoBulto c1 ON b.id = c1.id_bulto AND c1.estado IN ('EnTransito', 'EnTránsito')
            JOIN CambioEstadoBulto c2 ON b.id = c2.id_bulto AND c2.estado = 'Verificado'
        """)
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    def reporte_valorizacion_inventario(self):
        """Calcula el capital inmovilizado (cantidad * costo) agrupado por ubicación."""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COALESCE(u.nombre, 'Ubicación sin registro') as ubicacion, 
                   SUM(s.cantidad_fisica) as total_unidades,
                   SUM(s.cantidad_fisica * COALESCE(p.costo, 0)) as valorizacion_total
            FROM Stock s
            LEFT JOIN Productos p ON s.id_producto = p.id
            LEFT JOIN Ubicaciones u ON s.id_ubicacion = u.id
            GROUP BY ubicacion
        """)
        resultados = cursor.fetchall()
        conexion.close()
        return resultados