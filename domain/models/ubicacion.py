from abc import ABC

class Ubicacion(ABC):
    def __init__(self, id_ubicacion: int, nombre: str, direccion: str):
        self.id = id_ubicacion
        self.nombre = nombre
        self.direccion = direccion

class CentroDistribucion(Ubicacion):
    def __init__(self, id_ubicacion: int, nombre: str, direccion: str):
        super().__init__(id_ubicacion, nombre, direccion)

class Local(Ubicacion):
    def __init__(self, id_ubicacion: int, nombre: str, direccion: str):
        super().__init__(id_ubicacion, nombre, direccion)