import tkinter as tk
from tkinter import ttk

def mostrar_menu_logistica(ventana_padre, logistica_service):
    ventana_log = tk.TopLevel(ventana_padre)
    ventana_log.tittle("Módulo de Logística - Armar Bulto")
    ventana_log.geometry("350x250")

    lbl_instruccion = ttk.Label(ventana_log, text="Ingrese los daotos del nuevo bulto:")
    lbl_instruccion.pack(pady=10)

    lbl_codigo = ttk.Label(ventana_log, text="Código del Bulto:")
    lbl_codigo.pack()
    entry_codigo = ttk.Entry(ventana_log, width=30)
    entry_codigo.pack(pady=5)

    lbl_usuario = ttk.Label(ventana_log, text="Usuario:")
    lbl_usuario.pack()
    entry_usuario = ttk.Entry(ventana_log, width=30)
    entry_usuario.pack(pady=5)

    lbl_resultado = ttk.Label(ventana_log, text="", foreground="blue")
    lbl_resultado.pack(pady=5)

    def armar_bulto_click():
        codigo_ingresado = entry_codigo.get()
        usuario_ingresado = entry_usuario.get()

        try:
            bulto = logistica_service.armar_bulto(
                codigo=codigo_ingresado,
                origen=None,
                destino=None,
                items_dict={},
                usuario=usuario_ingresado
            )
            lbl_resultado.config(text=f"Bulto {bulto.codigo} armado exitosamente", foreground="green")
            entry_codigo.delete(0, tk.END)
            entry_usuario.delete(0, tk.END)

        except Exception as e:
            lbl_resultado.config(text=f"Error: {e}", foreground="red")

    btn_guardar = ttk.Button(ventana_log, text="Guardar Bulto", command=armar_bulto_click)
    btn_guardar.pack(pady=15)