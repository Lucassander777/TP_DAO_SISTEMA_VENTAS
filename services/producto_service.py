from repositories.producto_dao import ProductoDao
from domain.models.catalogo import Producto

class ProductoService:
    def __init__(self, producto_dao):
        # Respetamos la inyección de dependencias que viene del main.py
        self.producto_dao = producto_dao

    def registrar_producto(self, sku, nombre, precio_venta, costo, categoria="General", proveedor=1):
        # 1. Validación de reglas de negocio
        if not sku or not nombre:
            raise ValueError("El código SKU y el nombre son obligatorios.")
        
        try:
            precio_venta = float(precio_venta)
            costo = float(costo)
        except ValueError:
            raise ValueError("El precio y el costo deben ser números válidos.")

        if precio_venta <= 0 or costo < 0:
            raise ValueError("Los valores no pueden ser negativos.")

        # 2. Creación del objeto de dominio
        nuevo_producto = Producto(
            id_producto=None,
            sku=sku,
            nombre=nombre,
            precio_venta=precio_venta,
            costo=costo,
            categoria=categoria,
            proveedor=proveedor
        )
        nuevo_producto.id = None
        nuevo_producto.activo = True

        # 3. Persistencia en la base de datos
        return self.producto_dao.guardar(nuevo_producto)

    def guardar(self, producto):
        # Método directo utilizado por la interfaz gráfica (VistaAltaProducto)
        return self.producto_dao.guardar(producto)   