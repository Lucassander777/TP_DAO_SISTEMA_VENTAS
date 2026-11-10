import tkinter as tk
from tkinter import ttk, messagebox

class VistaABMCategorias(tk.Toplevel):
    def __init__(self, parent, categorias_service):
        super().__init__(parent)
        self.title("Administrar Categorías")
        self.geometry("400x350")
        self.categorias_service = categorias_service
        self.crear_interfaz()
        self.cargar_grilla()

    def crear_interfaz(self):
        marco_alta = ttk.LabelFrame(self, text="Nueva Categoría")
        marco_alta.pack(padx=15, pady=10, fill="x")

        ttk.Label(marco_alta, text="Nombre:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_nombre = ttk.Entry(marco_alta, width=25)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        btn_guardar = ttk.Button(marco_alta, text="Guardar", command=self.guardar)
        btn_guardar.grid(row=0, column=2, padx=10, pady=10)

        marco_lista = ttk.LabelFrame(self, text="Categorías Existentes")
        marco_lista.pack(padx=15, pady=5, fill="both", expand=True)

        self.tree = ttk.Treeview(marco_lista, columns=("ID", "Nombre"), show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=250)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        
        btn_eliminar = ttk.Button(marco_lista, text="Eliminar Seleccionada", command=self.eliminar)
        btn_eliminar.pack(pady=5)

    def cargar_grilla(self):
        for fila in self.tree.get_children():
            self.tree.delete(fila)
        
        categorias = self.categorias_service.obtener_todas()
        for cat in categorias:
            self.tree.insert("", tk.END, values=(cat["id"], cat["nombre"]))

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        try:
            self.categorias_service.guardar_categoria(nombre)
            self.entry_nombre.delete(0, tk.END)
            self.cargar_grilla()
            messagebox.showinfo("Éxito", "Categoría guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una categoría para eliminar.")
            return
        
        id_cat = self.tree.item(seleccion[0])['values'][0]
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar esta categoría?"):
            try:
                self.categorias_service.eliminar_categoria(id_cat)
                self.cargar_grilla()
            except Exception as e:
                messagebox.showerror("Error", str(e))