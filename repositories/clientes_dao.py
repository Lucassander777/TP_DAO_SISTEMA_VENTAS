from repositories.base_dao import BaseDAO

class ClienteDAO(BaseDAO):
    def __init__(self):
        super().__init__()

    def guardar(self, nombre, dni, limite_credito):
        conexion = self.get_conexion()
        cursor = conexion.curso()

        cursor.execute("""
            INSERT INTO Clientes (nombre, dni, limite_credito)
            VALUES (?, ?, ?)
        """, (nombre, dni, limite_credito))
        cliente_id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return cliente_id

    def obtener_por_id(self, dni):
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id, nombre, dni, saldo, limite_credito FROM Clientes WHERE dni = ?", (dni,))
        row = cursor.fetchone()
        conexion.close()
        return row

    def actualizar_saldo(self, cliente_id, nuevo_saldo):
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE Clientes SET saldo = ? WHERE id = ?", (nuevo_saldo, cliente_id))
        conexion.commit()
        conexion.close()
