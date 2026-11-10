from repositories.proveedores_dao import ProveedoresDAO

class ProveedoresService:
    def __init__(self):
        self.dao = ProveedoresDAO()

    def obtener_todos(self):
        return self.dao.obtener_todos()

    def guardar_proveedor(self, razon_social: str, cuit: str):
        if not razon_social.strip() or not cuit.strip():
            raise ValueError("La razón social y el CUIT son obligatorios.")
        self.dao.guardar(razon_social, cuit)

    def eliminar_proveedor(self, id_proveedor: int):
        self.dao.eliminar(id_proveedor)