class UbicacionService:
    def __init__(self, ubicacion_dao):
        self.ubicacion_dao = ubicacion_dao

    def obtener_todos(self):
        return self.ubicacion_dao.obtener_todos()

    def registrar_ubicacion(self, nombre, direccion=""):
        if not nombre:
            raise ValueError("El nombre de la sucursal o depósito es obligatorio.")
        
        self.ubicacion_dao.guardar(nombre, direccion)