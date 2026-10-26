from decimal import Decimal

class Categoria:
    def __init__(self, id_categoria: int, nombre: str, descripcion: str):
        self.id = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion

class Proveedor:
    def __init__(self, id_proveedor: int, cuit: str, razon_social: str, contacto: str):
        self.id = id_proveedor
        self.cuit = cuit
        self.razon_social = razon_social
        self.contacto = contacto

class Producto:
    def __init__(self, id_producto: int, sku: str, nombre: str, precio_venta: Decimal, costo: Decimal, categoria: Categoria, proveedor: Proveedor):
        self.id = id_producto
        self.sku = sku # Restricción: debe ser único
        self.nombre = nombre
        self.precio_venta = precio_venta
        self.costo = costo
        self.activo = True # Por defecto, el producto está activo

        self.categoria = categoria
        self.proveedor = proveedor
