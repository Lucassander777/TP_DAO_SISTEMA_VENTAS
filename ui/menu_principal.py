import tkinter as tk
from tkinter import ttk
from ui.vistas_logistica import mostrar_menu_logistica
from ui.vistas_ventas import mostrar_menu_ventas
from ui.vistas_lote import mostrar_menu_lotes
from ui.vistas_compras import mostrar_menu_compras
from ui.vistas_clientes import mostrar_menu_clientes
from ui.vistas_auditoria import mostrar_menu_auditoria
from ui.vistas_reportes import mostrar_menu_reportes
from ui.vistas_producto import VistaAltaProducto
from ui.vistas_ubicacion import VistaAltaUbicacion
from ui.vistas_inventario import VistaInventarioGeneral

def iniciar_interfaz(logistica_service, ventas_service, lote_service, compras_service, clientes_service, auditoria_service, reportes_service, producto_service, ubicacion_service, inventario_service):
    ventana = tk.Tk()
    ventana.title("Sistema Central de Gestión")
    ventana.geometry("550x650")

    ttk.Style().theme_use('clam')

    lbl_titulo = ttk.Label(ventana, text="SISTEMA CENTRAL DE VENTAS", font=("Arial", 14, "bold"))
    lbl_titulo.pack(pady=15)

    # --- Funciones de apertura de ventanas ---
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

    def abrir_producto():
        VistaAltaProducto(ventana, producto_service)

    def abrir_ubicacion():
        VistaAltaUbicacion(ventana, ubicacion_service)
        
    def abrir_inventario():
        VistaInventarioGeneral(ventana, inventario_service)

    # --- Botones del menú ---
    btn_producto = ttk.Button(ventana, text="1. Gestión de Productos (Catálogo)", command=abrir_producto)
    btn_producto.pack(pady=5, fill="x", padx=50)

    btn_ubicacion = ttk.Button(ventana, text="2. Gestión de Ubicaciones (Locales)", command=abrir_ubicacion)
    btn_ubicacion.pack(pady=5, fill="x", padx=50)

    btn_compras = ttk.Button(ventana, text="3. Módulo de Compras", command=abrir_compras)
    btn_compras.pack(pady=5, fill="x", padx=50)
    
    btn_logistica = ttk.Button(ventana, text="4. Módulo de Logística (Bultos)", command=abrir_logistica)
    btn_logistica.pack(pady=5, fill="x", padx=50)

    btn_lotes = ttk.Button(ventana, text="5. Módulo de Lotes y Vencimientos", command=abrir_lotes)
    btn_lotes.pack(pady=5, fill="x", padx=50)

    btn_inv = ttk.Button(ventana, text="6. Consulta de Inventario General", command=abrir_inventario)
    btn_inv.pack(pady=5, fill="x", padx=50)

    btn_ventas = ttk.Button(ventana, text="7. Módulo de Ventas", command=abrir_ventas)
    btn_ventas.pack(pady=5, fill="x", padx=50)

    btn_cliente = ttk.Button(ventana, text="8. Módulo de Clientes", command=abrir_cliente)
    btn_cliente.pack(pady=5, fill="x", padx=50)

    btn_auditoria = ttk.Button(ventana, text="9. Módulo de Inventarios Físicos (Auditoría)", command=abrir_auditoria)
    btn_auditoria.pack(pady=5, fill="x", padx=50)

    btn_reporte = ttk.Button(ventana, text="10. Módulo de Reportes Analíticos", command=abrir_reporte)
    btn_reporte.pack(pady=5, fill="x", padx=50)

    # Separador visual
    ttk.Separator(ventana, orient='horizontal').pack(fill='x', pady=10, padx=30)

    btn_salir = ttk.Button(ventana, text="Salir del Sistema", command=ventana.destroy)
    btn_salir.pack(pady=5, fill="x", padx=50)

    ventana.mainloop()