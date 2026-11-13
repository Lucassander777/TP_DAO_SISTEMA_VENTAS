import sqlite3

class Database:
    def __init__(self, db_name="sistema_ventas.db"):
        self.db_name = db_name

    def get_conexion(self):
        conexion = sqlite3.connect(self.db_name)
        conexion.row_factory = sqlite3.Row # Mejor usar sqlite3.Row para acceder por nombre de columna

        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    def incializar_tablas(self):
        """Crea todo el esquema relacional de la base de datos"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()

        # ----------
        # TABLAS MAESTRAS (sin dependencias)
        # ----------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                razon_social TEXT NOT NULL,
                cuit TEXT UNIQUE NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Categorias(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL 
                )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ubicaciones(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT,
                tipo TEXT NOT NULL -- Ej: 'Local', 'CentroDistribucion'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                rol TEXT NOT NULL
            )
        """)

        # ----------
        # CATÁLOGO Y LOTES (dependen de las maestras)
        # ----------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                precio_venta REAL NOT NULL,
                costo REAL NOT NULL,
                stock_actual INTEGER DEFAULT 0, 
                stock_minimo INTEGER DEFAULT 5,
                activo BOOLEAN NOT NULL DEFAULT 1,
                id_categoria INTEGER,
                id_proveedor INTEGER,
                FOREIGN KEY (id_categoria) REFERENCES Categorias(id),
                FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Lotes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                fecha_ingreso DATE NOT NULL,
                fecha_vencimiento DATE NOT NULL,
                activo BOOLEAN NOT NULL DEFAULT 1,
                id_producto INTEGER NOT NULL,
                id_proveedor INTEGER,
                FOREIGN KEY (id_producto) REFERENCES Productos(id),
                FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id)
            )
        """)
        # ----------
        # INVENTARIO (depende de productos y ubicaciones)
        # ----------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Stock(
                id_producto INTEGER NOT NULL,
                id_ubicacion INTEGER NOT NULL,
                cantidad_fisica INTEGER NOT NULL DEFAULT 0,
                cantidad_disponible INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (id_producto, id_ubicacion),
                FOREIGN KEY (id_producto) REFERENCES Productos(id),
                FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MovimientoStock(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATETIME NOT NULL,
                cantidad INTEGER NOT NULL,
                tipo TEXT NOT NULL, -- Ej: 'VENTA', 'RECEPCION'
                referencia_tipo TEXT,
                referencia_id INTEGER,
                id_producto INTEGER NOT NULL,
                id_ubicacion INTEGER NOT NULL,
                FOREIGN KEY (id_producto) REFERENCES Productos(id),
                FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id)
            )
        """)

        # ----------
        # LOGÍSTICA (Bultos y trazabilidad)
        # ----------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bultos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                fecha_creacion DATETIME NOT NULL,
                estado_actual TEXT NOT NULL,
                id_origen INTEGER,
                id_destino INTEGER,
                FOREIGN KEY (id_origen) REFERENCES Ubicaciones(id),
                FOREIGN KEY (id_destino) REFERENCES Ubicaciones(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ItemBulto(
                id_bulto INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                PRIMARY KEY (id_bulto, id_producto),
                FOREIGN KEY (id_bulto) REFERENCES Bultos(id),
                FOREIGN KEY (id_producto) REFERENCES Productos(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CambioEstadoBulto(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_bulto INTEGER NOT NULL,
                estado TEXT NOT NULL,
                fecha_hora DATETIME NOT NULL,
                usuario TEXT NOT NULL,
                observacion TEXT,
                FOREIGN KEY (id_bulto) REFERENCES Bultos(id)
            )
        """)

        # ----------
        # VENTAS (Cabecera, detalle, pagos y devoluciones)
        # ----------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ventas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATETIME NOT NULL,
                estado TEXT NOT NULL,
                total REAL NOT NULL,
                id_cajero INTEGER,
                id_local INTEGER,
                FOREIGN KEY (id_cajero) REFERENCES Usuarios(id),
                FOREIGN KEY (id_local) REFERENCES Ubicaciones(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ItemVenta(
                id_venta INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                PRIMARY KEY (id_venta, id_producto),
                FOREIGN KEY (id_venta) REFERENCES Ventas(id),
                FOREIGN KEY (id_producto) REFERENCES Productos(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pagos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER NOT NULL,
                monto REAL NOT NULL,
                referencia TEXT,
                tipo_medio_pago TEXT NOT NULL,
                FOREIGN KEY (id_venta) REFERENCES Ventas(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Comprobantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER UNIQUE NOT NULL,
                tipo TEXT NOT NULL,
                numero TEXT NOT NULL,
                fecha DATETIME NOT NULL,
                FOREIGN KEY (id_venta) REFERENCES Ventas(id)
            )
        """)

        # NUEVA TABLA: Devoluciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Devoluciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                cantidad_devuelta INTEGER NOT NULL,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_venta) REFERENCES Ventas(id),
                FOREIGN KEY (id_producto) REFERENCES Productos(id)
            )
        """)

        # ----------
        # COMPRAS
        # ----------
        
        # CORRECCIÓN: Renombrado de OrdenesCompra a OrdenCompra para evitar el error de Foreign Key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OrdenCompra(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL,
                total REAL,
                id_proveedor INTEGER,
                FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS DetalleOrdenCompra(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_orden INTEGER,
                id_producto INTEGER,
                cantidad INTEGER,
                precio_unitario REAL,
                FOREIGN KEY (id_orden) REFERENCES OrdenCompra(id),
                FOREIGN KEY (id_producto) REFERENCES Productos(id)
            )
        """)

        # ----------
        # CLIENTES PARA CUENTA CORRIENTE
        # ----------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                dni TEXT UNIQUE NOT NULL,
                saldo REAL DEFAULT 0.0,
                limite_credito REAL DEFAULT 100000.0,
                activo BOOLEAN DEFAULT 1
            )
        """)

        conexion.commit()
        conexion.close()
        print("Base de datos y esquema DDL creados con éxito.")

if __name__ == "__main__":
    db = Database()
    db.incializar_tablas()