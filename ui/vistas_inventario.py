import tkinter as tk
from tkinter import ttk, messagebox

class VistaInventarioGeneral(tk.Toplevel):
    def __init__(self, parent, inventario_service):
        super().__init__(parent)
        self.title("Consulta de Inventario General")
        self.geometry("600x400")
        
        self.inventario_service = inventario_service
        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        marco = ttk.LabelFrame(self, text="Stock Disponible en Sucursales")
        marco.pack(padx=15, pady=15, fill="both", expand=True)

        # Definir columnas de la grilla
        columnas = ("producto", "ubicacion", "fisico", "disponible")
        self.tree = ttk.Treeview(marco, columns=columnas, show="headings", height=15)
        
        self.tree.heading("producto", text="Producto")
        self.tree.heading("ubicacion", text="Ubicación")
        self.tree.heading("fisico", text="Stock Físico (Real)")
        self.tree.heading("disponible", text="Stock Disponible (Ventas)")
        
        self.tree.column("producto", width=200)
        self.tree.column("ubicacion", width=150)
        self.tree.column("fisico", width=100, anchor="center")
        self.tree.column("disponible", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        btn_actualizar = ttk.Button(self, text="Actualizar Grilla", command=self.cargar_datos)
        btn_actualizar.pack(pady=10)

    def cargar_datos(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            registros = self.inventario_service.obtener_inventario_completo()
            for r in registros:
                self.tree.insert("", tk.END, values=(r["producto"], r["ubicacion"], r["cantidad_fisica"], r["cantidad_disponible"]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el inventario: {str(e)}")