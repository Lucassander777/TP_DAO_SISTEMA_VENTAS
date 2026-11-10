import tkinter as tk
from tkinter import ttk, messagebox

class VistaABMProveedores(tk.Toplevel):
    def __init__(self, parent, proveedores_service):
        super().__init__(parent)
        self.title("Administrar Proveedores")
        self.geometry("500x400")
        self.proveedores_service = proveedores_service
        self.crear_interfaz()
        self.cargar_grilla()

    def crear_interfaz(self):
        marco_alta = ttk.LabelFrame(self, text="Nuevo Proveedor")
        marco_alta.pack(padx=15, pady=10, fill="x")

        ttk.Label(marco_alta, text="Razón Social:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_razon = ttk.Entry(marco_alta, width=30)
        self.entry_razon.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(marco_alta, text="CUIT:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_cuit = ttk.Entry(marco_alta, width=30)
        self.entry_cuit.grid(row=1, column=1, padx=10, pady=5)

        btn_guardar = ttk.Button(marco_alta, text="Guardar Proveedor", command=self.guardar)
        btn_guardar.grid(row=2, column=0, columnspan=2, pady=10)

        marco_lista = ttk.LabelFrame(self, text="Proveedores Existentes")
        marco_lista.pack(padx=15, pady=5, fill="both", expand=True)

        self.tree = ttk.Treeview(marco_lista, columns=("ID", "Razón Social", "CUIT"), show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Razón Social", text="Razón Social")
        self.tree.heading("CUIT", text="CUIT")
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Razón Social", width=200)
        self.tree.column("CUIT", width=120, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        
        btn_eliminar = ttk.Button(marco_lista, text="Eliminar Seleccionado", command=self.eliminar)
        btn_eliminar.pack(pady=5)

    def cargar_grilla(self):
        for fila in self.tree.get_children():
            self.tree.delete(fila)
        
        proveedores = self.proveedores_service.obtener_todos()
        for prov in proveedores:
            self.tree.insert("", tk.END, values=(prov["id"], prov["razon_social"], prov["cuit"]))

    def guardar(self):
        razon = self.entry_razon.get().strip()
        cuit = self.entry_cuit.get().strip()
        try:
            self.proveedores_service.guardar_proveedor(razon, cuit)
            self.entry_razon.delete(0, tk.END)
            self.entry_cuit.delete(0, tk.END)
            self.cargar_grilla()
            messagebox.showinfo("Éxito", "Proveedor guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un proveedor para eliminar.")
            return
        
        id_prov = self.tree.item(seleccion[0])['values'][0]
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este proveedor?"):
            try:
                self.proveedores_service.eliminar_proveedor(id_prov)
                self.cargar_grilla()
            except Exception as e:
                messagebox.showerror("Error", str(e))