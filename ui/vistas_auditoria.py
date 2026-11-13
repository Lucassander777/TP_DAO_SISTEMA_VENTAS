import tkinter as tk
from tkinter import ttk, messagebox

def mostrar_menu_auditoria(ventana_padre, auditoria_service, producto_service, ubicacion_service):
    ventana_aud = tk.Toplevel(ventana_padre)
    ventana_aud.title("Módulo de Auditoría - Inventario Físico")
    ventana_aud.geometry("550x320")

    try:
        productos = producto_service.obtener_todos_con_sku()
        ubicaciones = ubicacion_service.obtener_todos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar productos y sucursales: {e}", parent=ventana_aud)
        ventana_aud.destroy()
        return

    frame_aud = ttk.LabelFrame(ventana_aud, text="Conciliación de Stock Físico vs Sistema")
    frame_aud.pack(pady=10, padx=10, fill="both", expand=True)

    ttk.Label(frame_aud, text="Producto:").grid(row=0, column=0, padx=10, pady=10)
    combo_producto = ttk.Combobox(
        frame_aud,
        values=[f'{producto["sku"]} - {producto["nombre"]}' for producto in productos],
        state="readonly",
        width=35
    )
    combo_producto.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(frame_aud, text="Sucursal:").grid(row=1, column=0, padx=10, pady=10)
    combo_ubicacion = ttk.Combobox(
        frame_aud,
        values=[ubicacion["direccion"] or ubicacion["nombre"] for ubicacion in ubicaciones],
        state="readonly",
        width=35
    )
    combo_ubicacion.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(frame_aud, text="Cantidad Contada a Mano:").grid(row=2, column=0, padx=10, pady=10)
    entry_cantidad = ttk.Entry(frame_aud)
    entry_cantidad.grid(row=2, column=1, padx=10, pady=10)

    lbl_resultado = ttk.Label(frame_aud, text="", font=("Arial", 9, "bold"))
    lbl_resultado.grid(row=4, column=0, columnspan=2, pady=10)

    def ejecutar_conciliacion():
        try:
            indice_producto = combo_producto.current()
            indice_ubicacion = combo_ubicacion.current()
            if indice_producto == -1 or indice_ubicacion == -1:
                lbl_resultado.config(text="Seleccione un producto y una sucursal.", foreground="red")
                return

            prod_id = productos[indice_producto]["id"]
            ubi_id = ubicaciones[indice_ubicacion]["id"]
            cant_fisica = int(entry_cantidad.get())

            mensaje = auditoria_service.conciliar_inventario_fisico(prod_id, ubi_id, cant_fisica)

            lbl_resultado.config(text=f"{mensaje}", foreground="blue")
            combo_producto.set("")
            combo_ubicacion.set("")
            entry_cantidad.delete(0, tk.END)
        except ValueError:
            lbl_resultado.config(text="Error: Ingrese números enteros válidos.", foreground="red")
        except Exception as e:
            lbl_resultado.config(text=f"Error: {e}", foreground="red")

    btn_conciliar = ttk.Button(frame_aud, text="Registrar y Ajustar Stock", command=ejecutar_conciliacion)
    btn_conciliar.grid(row=3, column=0, columnspan=2, pady=15)
        