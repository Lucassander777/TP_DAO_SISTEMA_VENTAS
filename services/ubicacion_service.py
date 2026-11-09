class UbicacionService:
    def __init__(self, ubicacion_dao):
        self.ubicacion_dao = ubicacion_dao

    def registrar_ubicacion(self, nombre, direccion=""):
        if not nombre:
            raise ValueError("El nombre de la sucursal o depósito es obligatorio.")
        
        self.ubicacion_dao.guardar(nombre, direccion)