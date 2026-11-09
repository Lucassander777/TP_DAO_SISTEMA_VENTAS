import tkinter as tk
from tkinter import ttk, messagebox

class VistaAltaUbicacion(tk.Toplevel):
    def __init__(self, parent, ubicacion_service):
        super().__init__(parent)
        self.title("Gestión de Ubicaciones")
        self.geometry("350x200")
        
        self.ubicacion_service = ubicacion_service
        self.crear_interfaz()

    def crear_interfaz(self):
        marco = ttk.LabelFrame(self, text="Nueva Sucursal / Depósito")
        marco.pack(padx=15, pady=15, fill="both", expand=True)

        ttk.Label(marco, text="Nombre:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_nombre = ttk.Entry(marco)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(marco, text="Dirección (Opcional):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_direccion = ttk.Entry(marco)
        self.entry_direccion.grid(row=1, column=1, padx=10, pady=10)

        btn_guardar = ttk.Button(marco, text="Guardar Ubicación", command=self.ejecutar_guardado)
        btn_guardar.grid(row=2, column=0, columnspan=2, pady=15)

    def ejecutar_guardado(self):
        nombre = self.entry_nombre.get().strip()
        direccion = self.entry_direccion.get().strip()

        try:
            self.ubicacion_service.registrar_ubicacion(nombre, direccion)
            messagebox.showinfo("Éxito", f"La ubicación '{nombre}' fue registrada.")
            
            self.entry_nombre.delete(0, tk.END)
            self.entry_direccion.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un problema: {str(e)}")