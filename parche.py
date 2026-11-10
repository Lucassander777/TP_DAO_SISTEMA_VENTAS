import sqlite3

conexion = sqlite3.connect('sistema_ventas.db')
cursor = conexion.cursor()

# Insertamos el usuario respetando las columnas username y rol de tu esquema
cursor.execute("""
    INSERT INTO Usuarios (id, username, rol) 
    VALUES (1, 'Lucas', 'Administrador')
""")

conexion.commit()
conexion.close()

print("¡Usuario creado con éxito!")