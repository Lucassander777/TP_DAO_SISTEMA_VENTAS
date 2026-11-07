import tkinter as tk
from tkinter import ttk
from ui.vistas_logistica import mostrar_menu_logistica
from ui.vistas_ventas import mostrar_menu_ventas
from ui.vistas_lote import mostrar_menu_lotes
from ui.vistas_compras import mostrar_menu_compras
from ui.vistas_clientes import mostrar_menu_clientes
from ui.vistas_auditoria import mostrar_menu_auditoria
from ui.vistas_reportes import mostrar_menu_reportes

def iniciar_interfaz(logistica_service, ventas_service, lote_service, compras_service, clientes_service, auditoria_service, reportes_service):
    ventana = tk.Tk()
    ventana.title("Sistema Central de Gestión")
    ventana.geometry("400x300")

    ttk.Style().theme_use('clam')

    lbl_titulo = ttk.Label(ventana, text="SISTEMA CENTRAL DE VENTAS", font=("Arial", 14, "bold"))
    lbl_titulo.pack(pady=30)

    def abrir_logistica():
        mostrar_menu_logistica(ventana, logistica_service)

    def abrir_ventas():
        mostrar_menu_ventas(ventana, ventas_service)

    def abrir_lotes():
        mostrar_menu_lotes(ventana, lote_service)

    def abrir_compras():
        mostrar_menu_compras(ventana, compras_service)

    def abrir_cliente():
        mostrar_menu_clientes(ventana, clientes_service)

    def abrir_auditoria():
        mostrar_menu_auditoria(ventana, auditoria_service)

    def abrir_reporte():
        mostrar_menu_reportes(ventana, reportes_service)

    btn_logistica = ttk.Button(ventana, text="Módulo de Logística", command=abrir_logistica)
    btn_logistica.pack(pady=10, fill="x", padx=50)

    btn_ventas = ttk.Button(ventana, text="Módulo de Ventas", command=abrir_ventas)
    btn_ventas.pack(pady=10, fill="x", padx=50)

    btn_lotes = ttk.Button(ventana, text="Módulo de Lotes y Vencimientos", command=abrir_lotes)
    btn_lotes.pack(pady=10, fill="x", padx=50)

    btn_compras = ttk.Button(ventana, text="Módulo de Compras", command=abrir_compras)
    btn_compras.pack(pady=10, fill="x", padx=50)

    btn_cliente = ttk.Button(ventana, text="Módulo de Clientes", command=abrir_cliente)
    btn_cliente.pack(pady=10, fill="x", padx=50)

    btn_auditoria = ttk.Button(ventana, text="Módulo de Inventarios Físicos", command=abrir_auditoria)
    btn_auditoria.pack(pady=10, fill="x", padx=50)

    btn_reporte = ttk.Button(ventana, text="Módulo de Reportes Analíticos", command=abrir_reporte)
    btn_reporte.pack(pady=10, fill="x", padx=50)

    btn_salir = ttk.Button(ventana, text="Salir del Sistema", command=ventana.destroy)
    btn_salir.pack(pady=10, fill="x", padx=50)

    ventana.mainloop()