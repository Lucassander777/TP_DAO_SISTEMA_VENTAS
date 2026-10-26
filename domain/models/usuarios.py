class Usuario:
    def __init__(self, id_usuario: int, username: str, nombre: str, apellido: str, rol: str):
        self.id = id_usuario
        self.username = username
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol
        self.activo = True