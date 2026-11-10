from repositories.categorias_dao import CategoriasDAO

class CategoriasService:
    def __init__(self):
        self.dao = CategoriasDAO()

    def obtener_todas(self):
        return self.dao.obtener_todas()

    def guardar_categoria(self, nombre: str):
        if not nombre.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        self.dao.guardar(nombre)

    def eliminar_categoria(self, id_categoria: int):
        self.dao.eliminar(id_categoria)