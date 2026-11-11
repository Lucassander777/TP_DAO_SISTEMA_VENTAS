import sqlite3

conexion = sqlite3.connect('sistema_ventas.db')
cursor = conexion.cursor()

print("Iniciando parcheo de la base de datos...")

# 1. Insertar el Usuario 
try:
    cursor.execute("""
        INSERT OR IGNORE INTO Usuarios (id, username, rol) 
        VALUES (1, 'Lucas', 'Administrador')
    """)
    print("✅ Usuario 'Lucas' asegurado.")
except Exception as e:
    print(f"❌ Error con Usuario: {e}")

# 2. Insertar el Proveedor 
try:
    cursor.execute("""
        INSERT OR IGNORE INTO Proveedores (id, razon_social, cuit) 
        VALUES (1, 'Proveedor de Prueba SA', '30-12345678-9')
    """)
    print("✅ Proveedor de prueba asegurado.")
except Exception as e:
    print(f"❌ Error con Proveedor: {e}")

# 3. Insertar Categoría (Agregado para que no falle al crear productos)
try:
    cursor.execute("INSERT OR IGNORE INTO Categorias (id, nombre) VALUES (1, 'General')")
    print("✅ Categoría base asegurada.")
except Exception as e:
    print(f"❌ Error con Categoría: {e}")

# 4. Insertar Ubicaciones (Agregado para que no fallen ni Ventas ni Bultos)
try:
    cursor.execute("INSERT OR IGNORE INTO Ubicaciones (id, nombre, direccion, tipo) VALUES (1, 'Centro Distribucion Central', 'Ruta 9 Km 15', 'CentroDistribucion')")
    cursor.execute("INSERT OR IGNORE INTO Ubicaciones (id, nombre, direccion, tipo) VALUES (2, 'Local Centro 01', 'San Martin 456', 'Local')")
    print("✅ Ubicaciones (CD y Local) aseguradas.")
except Exception as e:
    print(f"❌ Error con Ubicaciones: {e}")

conexion.commit()
conexion.close()

print("¡Todo listo! Base de datos lista para usar.")