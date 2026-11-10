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

# 3. Arreglar el nombre de la tabla de plural a singular
try:
    cursor.execute("ALTER TABLE OrdenesCompra RENAME TO OrdenCompra;")
    print("✅ Tabla 'OrdenesCompra' renombrada a 'OrdenCompra' con éxito.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Nota sobre la tabla: {e} (Probablemente ya se corrigió antes).")

conexion.commit()
conexion.close()

print("¡Todo listo! Base de datos parcheada y lista para usar.")