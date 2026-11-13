import tkinter as tk
from tkinter import ttk, messagebox
from domain.models.catalogo import Producto

def mostrar_menu_lotes(ventana_padre, lote_service, producto_service, ubicacion_service):
    ventana_lotes = tk.Toplevel(ventana_padre)
    ventana_lotes.title("Módulo de Lotes y Vencimientos")
    ventana_lotes.geometry("450x550") # Agrandé un poco la ventana para que entre todo

    try:
        productos = producto_service.obtener_todos_con_sku()
        ubicaciones = ubicacion_service.obtener_todos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar productos y sucursales: {e}", parent=ventana_lotes)
        ventana_lotes.destroy()
        return

    # 1. REGISTRAR LOTE
    frame_registro = ttk.LabelFrame(ventana_lotes, text="Registrar Nuevo Lote")
    frame_registro.pack(pady=10, padx=10, fill="x")

    ttk.Label(frame_registro, text="Código del Lote:").grid(row=0, column=0, padx=5, pady=5)
    entry_codigo = ttk.Entry(frame_registro)
    entry_codigo.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_registro, text="Producto (SKU):").grid(row=1, column=0, padx=5, pady=5)
    combo_producto = ttk.Combobox(
        frame_registro,
        values=[f'{producto["sku"]} - {producto["nombre"]}' for producto in productos],
        state="readonly",
        width=28
    )
    combo_producto.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_registro, text="Vencimiento (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
    entry_venc = ttk.Entry(frame_registro)
    entry_venc.grid(row=2, column=1, padx=5, pady=5)

    # NUEVO: Campo para la Cantidad
    ttk.Label(frame_registro, text="Cantidad Físico:").grid(row=3, column=0, padx=5, pady=5)
    entry_cant = ttk.Entry(frame_registro)
    entry_cant.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame_registro, text="Sucursal:").grid(row=4, column=0, padx=5, pady=5)
    combo_ubicacion = ttk.Combobox(
        frame_registro,
        values=[ubicacion["direccion"] or ubicacion["nombre"] for ubicacion in ubicaciones],
        state="readonly",
        width=28
    )
    combo_ubicacion.grid(row=4, column=1, padx=5, pady=5)

    lbl_estado = ttk.Label(frame_registro, text="", font=("Arial", 9))
    lbl_estado.grid(row=6, column=0, columnspan=2, pady=5)

    def guardar_lote():
        try:
            codigo = entry_codigo.get()
            vencimiento = entry_venc.get()
            if len(vencimiento) != 10 or vencimiento[4] != "-" or vencimiento[7] != "-":
                raise ValueError("La fecha debe tener el formato exacto YYYY-MM-DD (ej: 2027-12-31)")
            indice_producto = combo_producto.current()
            indice_ubicacion = combo_ubicacion.current()
            if indice_producto == -1 or indice_ubicacion == -1:
                raise ValueError("Seleccione un producto y una sucursal.")

            producto_seleccionado = productos[indice_producto]
            ubicacion_id = ubicaciones[indice_ubicacion]["id"]
            cantidad = int(entry_cant.get())

            prod_simulado = Producto(
                id_producto=producto_seleccionado["id"],
                sku=producto_seleccionado["sku"],
                nombre=producto_seleccionado["nombre"],
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
            combo_producto.set("")
            entry_cant.delete(0, tk.END)
            combo_ubicacion.set("")

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