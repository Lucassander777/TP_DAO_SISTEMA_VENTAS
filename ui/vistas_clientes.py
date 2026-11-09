import tkinter as tk
from tkinter import ttk

def mostrar_menu_clientes(ventana_padre, cliente_service):
    ventana_cli = tk.Toplevel(ventana_padre)
    ventana_cli.title("Módulo de Clientes y Cuentas Corrientes")
    ventana_cli.geometry("450x500")

    # --- SECCIÓN: REGISTRAR CLIENTE ---
    frame_alta = ttk.LabelFrame(ventana_cli, text="Registrar Nuevo Cliente")
    frame_alta.pack(pady=10, padx=10, fill="x")

    ttk.Label(frame_alta, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = ttk.Entry(frame_alta)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_alta, text="DNI:").grid(row=1, column=0, padx=5, pady=5)
    entry_dni = ttk.Entry(frame_alta)
    entry_dni.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_alta, text="Límite Crédito ($):").grid(row=2, column=0, padx=5, pady=5)
    entry_limite = ttk.Entry(frame_alta)
    entry_limite.grid(row=2, column=1, padx=5, pady=5)

    lbl_estado_alta = ttk.Label(frame_alta, text="", font=("Arial", 9))
    lbl_estado_alta.grid(row=4, column=0, columnspan=2, pady=5)

    def registrar():
        try:
            nombre = entry_nombre.get()
            dni = entry_dni.get()
            limite = float(entry_limite.get())

            cliente_service.registrar_cliente(nombre, dni, limite)
            lbl_estado_alta.config(text="Cliente registrado exitosamente", foreground="green")
            entry_nombre.delete(0, tk.END)
            entry_dni.delete(0, tk.END)
            entry_limite.delete(0, tk.END)

        except Exception as e:
            lbl_estado_alta.config(text=f"Error: {e}", foreground="red")

    btn_registrar = ttk.Button(frame_alta, text="Registrar Cliente", command=registrar)
    btn_registrar.grid(row=3, column=0, columnspan=2, pady=10)

    # --- SECCIÓN: GESTIÓN CUENTA CORRIENTE ---
    frame_gestion = ttk.LabelFrame(ventana_cli, text="Gestión de Cuenta Corriente")
    frame_gestion.pack(pady=10, padx=10, fill="x")

    ttk.Label(frame_gestion, text="DNI del Cliente:").grid(row=0, column=0, padx=5, pady=5)
    entry_dni_busqueda = ttk.Entry(frame_gestion)
    entry_dni_busqueda.grid(row=0, column=1, padx=5, pady=5)

    lbl_info_cuenta = ttk.Label(frame_gestion, text="Saldo actual: $0.00", font=("Arial", 10, "bold"))
    lbl_info_cuenta.grid(row=1, column=0, columnspan=3, pady=10)

    def consultar():
        try:
            dni = entry_dni_busqueda.get()
            cuenta = cliente_service.consultar_cuenta(dni)
            lbl_info_cuenta.config(
                text=f"Cliente: {cuenta['nombre']} | Saldo a favor: ${cuenta['saldo']:.2f}",
                foreground="blue"
            )
        except Exception as e:
            lbl_info_cuenta.config(text=f"Error: {e}", foreground="red")

    btn_consultar = ttk.Button(frame_gestion, text="Consultar Saldo", command=consultar)
    btn_consultar.grid(row=0, column=2, padx=5)

    ttk.Label(frame_gestion, text="Monto a Cargar ($):").grid(row=2, column=0, padx=5, pady=5)
    entry_monto = ttk.Entry(frame_gestion)
    entry_monto.grid(row=2, column=1, padx=5, pady=5)

    def cargar_saldo():
        try:
            dni = entry_dni_busqueda.get()
            monto = float(entry_monto.get())
            nuevo_saldo = cliente_service.cargar_saldo(dni, monto)
            lbl_info_cuenta.config(text=f"Carga exitosa. Nuevo Saldo: ${nuevo_saldo:.2f}", foreground="green")
            entry_monto.delete(0, tk.END)
        except Exception as e:
            lbl_info_cuenta.config(text=f"Error: {e}", foreground="red")

    btn_cargar = ttk.Button(frame_gestion, text="Acreditar Saldo", command=cargar_saldo)
    btn_cargar.grid(row=3, column=0, columnspan=3, pady=10)
    
