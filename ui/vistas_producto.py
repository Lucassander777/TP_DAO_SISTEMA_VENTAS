import tkinter as tk
from tkinter import ttk, messagebox
from domain.models.catalogo import Producto

class VistaAltaProducto(tk.Toplevel):
    def __init__(self, parent, producto_service, categorias_service, proveedores_service):
        super().__init__(parent)
        self.title("Gestión de Productos")
        self.geometry("450x420")
        
        self.producto_service = producto_service
        self.categorias_service = categorias_service
        self.proveedores_service = proveedores_service
        
        # Cargar datos para los desplegables
        self.lista_categorias = self.categorias_service.obtener_todas()
        self.lista_proveedores = self.proveedores_service.obtener_todos()
        
        self.crear_interfaz()

    def crear_interfaz(self):
        marco = ttk.LabelFrame(self, text="Nuevo Producto / Catálogo")
        marco.pack(padx=15, pady=15, fill="both", expand=True)

        ttk.Label(marco, text="SKU / Código:").grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.entry_sku = ttk.Entry(marco)
        self.entry_sku.grid(row=0, column=1, padx=10, pady=6, sticky="ew")

        ttk.Label(marco, text="Nombre:").grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.entry_nombre = ttk.Entry(marco)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=6, sticky="ew")

        ttk.Label(marco, text="Costo:").grid(row=2, column=0, padx=10, pady=6, sticky="e")
        self.entry_costo = ttk.Entry(marco)
        self.entry_costo.grid(row=2, column=1, padx=10, pady=6, sticky="ew")

        ttk.Label(marco, text="Precio de Venta:").grid(row=3, column=0, padx=10, pady=6, sticky="e")
        self.entry_precio = ttk.Entry(marco)
        self.entry_precio.grid(row=3, column=1, padx=10, pady=6, sticky="ew")

        # --- Nuevos Combobox para Categoría y Proveedor ---
        ttk.Label(marco, text="Categoría:").grid(row=4, column=0, padx=10, pady=6, sticky="e")
        nombres_categorias = [c["nombre"] for c in self.lista_categorias]
        self.combo_categoria = ttk.Combobox(marco, values=nombres_categorias, state="readonly")
        self.combo_categoria.grid(row=4, column=1, padx=10, pady=6, sticky="ew")

        ttk.Label(marco, text="Proveedor:").grid(row=5, column=0, padx=10, pady=6, sticky="e")
        nombres_proveedores = [p["razon_social"] for p in self.lista_proveedores]
        self.combo_proveedor = ttk.Combobox(marco, values=nombres_proveedores, state="readonly")
        self.combo_proveedor.grid(row=5, column=1, padx=10, pady=6, sticky="ew")

        btn_guardar = ttk.Button(marco, text="Guardar Producto", command=self.ejecutar_guardado)
        btn_guardar.grid(row=6, column=0, columnspan=2, pady=15)

    def ejecutar_guardado(self):
        sku = self.entry_sku.get().strip()
        nombre = self.entry_nombre.get().strip()
        costo_str = self.entry_costo.get().strip()
        precio_str = self.entry_precio.get().strip()
        
        idx_categoria = self.combo_categoria.current()
        idx_proveedor = self.combo_proveedor.current()

        if not sku or not nombre or not costo_str or not precio_str or idx_categoria == -1 or idx_proveedor == -1:
            messagebox.showerror("Error", "Todos los campos y selecciones son obligatorios.")
            return

        try:
            costo = float(costo_str)
            precio = float(precio_str)
            
            # Extraemos los IDs reales de la base de datos según la selección
            id_categoria = self.lista_categorias[idx_categoria]["id"]
            id_proveedor = self.lista_proveedores[idx_proveedor]["id"]
            
            nuevo_prod = Producto(
                id_producto=None, 
                sku=sku, 
                nombre=nombre, 
                costo=costo, 
                precio_venta=precio, 
                categoria=id_categoria, 
                proveedor=id_proveedor
            )
            
            self.producto_service.guardar(nuevo_prod)
            messagebox.showinfo("Éxito", f"El producto '{nombre}' fue guardado correctamente.")
            
            self.entry_sku.delete(0, tk.END)
            self.entry_nombre.delete(0, tk.END)
            self.entry_costo.delete(0, tk.END)
            self.entry_precio.delete(0, tk.END)
            self.combo_categoria.set('')
            self.combo_proveedor.set('')
            
        except ValueError:
            messagebox.showerror("Error de formato", "El costo y el precio deben ser números válidos.")
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un problema: {str(e)}")