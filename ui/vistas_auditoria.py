import tkinter as tk
from tkinter import ttk

def mostrar_menu_auditoria(ventana_padre, auditoria_service):
    ventana_aud = tk.Toplevel(ventana_padre)
    ventana_aud.title("Módulo de Auditoría - Inventario Físico")
    ventana_aud.geometry("450x300")

    frame_aud = ttk.LabelFrame(ventana_aud, text="Conciliación de Stock Físico vs Sistema")
    frame_aud.pack(pady=10, padx=10, fill="both", expand=True)

    ttk.Label(frame_aud, text="ID del Producto:").grid(row=0, column=0, padx=10, pady=10)
    entry_id_prod = ttk.Entry(frame_aud)
    entry_id_prod.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(frame_aud, text="ID de Ubicación (Local):").grid(row=1, column=0, padx=10, pady=10)
    entry_id_ubi = ttk.Entry(frame_aud)
    entry_id_ubi.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(frame_aud, text="Cantidad Contada a Mano:").grid(row=2, column=0, padx=10, pady=10)
    entry_cantidad = ttk.Entry(frame_aud)
    entry_cantidad.grid(row=2, column=1, padx=10, pady=10)

    lbl_resultado = ttk.Label(frame_aud, text="", font=("Arial", 9, "bold"))
    lbl_resultado.grid(row=4, column=0, columnspan=2, pady=10)

    def ejecutar_conciliacion():
        try:
            prod_id = int(entry_id_prod.get())
            ubi_id = int(entry_id_ubi.get())
            cant_fisica = int(entry_cantidad.get())

            mensaje = auditoria_service.conciliar_inventario_fisico(prod_id, ubi_id, cant_fisica)

            lbl_resultado.config(text=f"{mensaje}", foreground="blue")
            entry_id_prod.delete(0, tk.END)
            entry_id_ubi.delete(0, tk.END)
            entry_cantidad.delete(0, tk.END)
        except ValueError:
            lbl_resultado.config(text="Error: Ingrese números enteros válidos.", foreground="red")
        except Exception as e:
            lbl_resultado.config(text=f"Error: {e}", foreground="red")

    btn_conciliar = ttk.Button(frame_aud, text="Registrar y Ajustar Stock", command=ejecutar_conciliacion)
    btn_conciliar.grid(row=3, column=0, columnspan=2, pady=15)
        