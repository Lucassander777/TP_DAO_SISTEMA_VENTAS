import tkinter as tk
from tkinter import ttk

def mostrar_menu_compras(ventana_padre, compras_service):
    ventana_compras = tk.Toplevel(ventana_padre)
    ventana_compras.title("Módulo de Compras - Sugeridas por Faltantes")
    ventana_compras.geometry("550x400")

    frame_sugeridas = ttk.LabelFrame(ventana_compras, text="Órdenes de Compra Sugeridas (Por debajo del stock mínimo)")
    frame_sugeridas.pack(pady=10, padx=10, fill="both", expand=True)

    columnas = ("producto", "stock_actual", "stock_minimo", "a_comprar")
    tabla_faltantes = ttk.Treeview(frame_sugeridas, columns=columnas, show="headings", height=8)

    tabla_faltantes.heading("producto", text="Producto")
    tabla_faltantes.heading("stock_actual", text="Stock Actual")
    tabla_faltantes.heading("stock_minimo", text="Stock Mín.")
    tabla_faltantes.heading("a_comprar", text="Cant. a Reponer")

    tabla_faltantes.column("producto", width=180)
    tabla_faltantes.column("stock_actual", width=100, anchor="center")
    tabla_faltantes.column("stock_minimo", width=100, anchor="center")
    tabla_faltantes.column("a_comprar", width=100, anchor="center")
    
    tabla_faltantes.pack(pady=10, padx=10, fill="both")

    lbl_estado = ttk.Label(ventana_compras, text="", font=("Arial", 10))
    lbl_estado.pack(pady=5)

    def calcular_sugeridas():
        for fila in tabla_faltantes.get_children():
            tabla_faltantes.delete(fila)

        try:
            faltantes = compras_service.generar_ordenes_sugeridas()

            if not faltantes:
                lbl_estado.config(text="El stock está óptimo. No hay faltantes.", foreground="green")
            else:
                for item in faltantes:
                    tabla_faltantes.insert("", tk.END, values=(
                        item['producto_nombre'],
                        item['stock_actual'],
                        item['stock_minimo'],
                        item['cantidad_sugerida']
                    ))
                # Corregido: dentro del else para que no sobreescriba el mensaje verde
                lbl_estado.config(text=f"Se detectaron {len(faltantes)} productos con faltantes.", foreground="orange")

        except Exception as e:
            lbl_estado.config(text=f"Error al consultar faltantes: {e}", foreground="red")

    btn_generar = ttk.Button(frame_sugeridas, text="Calcular Faltantes y Sugerir Compra", command=calcular_sugeridas)
    btn_generar.pack(pady=10)
    
    