import tkinter as tk
from tkinter import ttk
from domain.models.catalogo import Producto

def mostrar_menu_lotes(ventana_padre, lote_service):
    ventana_lotes = tk.Toplevel(ventana_padre)
    ventana_lotes.title("Módulo de Lotes y Vencimientos")
    ventana_lotes.geometry("450x550") # Agrandé un poco la ventana para que entre todo

    # 1. REGISTRAR LOTE
    frame_registro = ttk.LabelFrame(ventana_lotes, text="Registrar Nuevo Lote")
    frame_registro.pack(pady=10, padx=10, fill="x")

    ttk.Label(frame_registro, text="Código del Lote:").grid(row=0, column=0, padx=5, pady=5)
    entry_codigo = ttk.Entry(frame_registro)
    entry_codigo.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_registro, text="ID Producto:").grid(row=1, column=0, padx=5, pady=5)
    entry_prod = ttk.Entry(frame_registro)
    entry_prod.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_registro, text="Vencimiento (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
    entry_venc = ttk.Entry(frame_registro)
    entry_venc.grid(row=2, column=1, padx=5, pady=5)

    # NUEVO: Campo para la Cantidad
    ttk.Label(frame_registro, text="Cantidad Físico:").grid(row=3, column=0, padx=5, pady=5)
    entry_cant = ttk.Entry(frame_registro)
    entry_cant.grid(row=3, column=1, padx=5, pady=5)

    # NUEVO: Campo para el ID de la Ubicación (Local)
    ttk.Label(frame_registro, text="ID Ubicación:").grid(row=4, column=0, padx=5, pady=5)
    entry_ubi = ttk.Entry(frame_registro)
    entry_ubi.grid(row=4, column=1, padx=5, pady=5)

    lbl_estado = ttk.Label(frame_registro, text="", font=("Arial", 9))
    lbl_estado.grid(row=6, column=0, columnspan=2, pady=5)

    def guardar_lote():
        try:
            codigo = entry_codigo.get()
            vencimiento = entry_venc.get()
            if len(vencimiento) != 10 or vencimiento[4] != "-" or vencimiento[7] != "-":
                raise ValueError("La fecha debe tener el formato exacto YYYY-MM-DD (ej: 2027-12-31)")
            prod_id = int(entry_prod.get())
            prod_id = int(entry_prod.get())
            cantidad = int(entry_cant.get())
            ubicacion_id = int(entry_ubi.get())

            prod_simulado = Producto(
                id_producto=prod_id, 
                sku=f"SKU-{prod_id}", 
                nombre="Producto Simulado", 
                precio_venta=0, 
                costo=0, 
                categoria=None, 
                proveedor=None
            )

            # AHORA LE PASAMOS LA CANTIDAD Y UBICACIÓN AL SERVICIO
            lote_service.registrar_lote_manual(codigo, vencimiento, prod_simulado, cantidad, ubicacion_id)

            lbl_estado.config(text="Lote y stock registrados con éxito", foreground="green")
            entry_codigo.delete(0, tk.END)
            entry_venc.delete(0, tk.END)
            entry_prod.delete(0, tk.END)
            entry_cant.delete(0, tk.END)
            entry_ubi.delete(0, tk.END)

        except Exception as e:
            lbl_estado.config(text=f"Error: {e}", foreground="red")

    btn_guardar = ttk.Button(frame_registro, text="Registrar Lote", command=guardar_lote)
    btn_guardar.grid(row=5, column=0, columnspan=2, pady=10)

    # 2. AUDITORÍA DE VENCIDOS
    frame_auditoria = ttk.LabelFrame(ventana_lotes, text="Auditoría de Vencimientos")
    frame_auditoria.pack(pady=10, padx=10, fill="both", expand=True)

    lista_vencidos = tk.Listbox(frame_auditoria, height=6)
    lista_vencidos.pack(pady=5, padx=10, fill="both")

    def auditar():
        lista_vencidos.delete(0, tk.END)
        vencidos = lote_service.auditar_vencimiento()

        if not vencidos:
            lista_vencidos.insert(tk.END, "No hay lotes vencidos en el sistema.")
        else:
            for v in vencidos:
                lista_vencidos.insert(tk.END, f"VENCIDO: {v[0]} - {v[2]} (Venció: {v[1]})")

    btn_auditar = ttk.Button(frame_auditoria, text="Consultar Vencimientos", command=auditar)
    btn_auditar.pack(pady=5)