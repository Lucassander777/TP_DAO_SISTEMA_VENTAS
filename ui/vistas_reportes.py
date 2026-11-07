import tkinter as tk
from tkinter import ttk

def mostrar_menu_reportes(ventana_padre, reportes_service):
    ventana_rep = tk.Toplevel(ventana_padre)
    ventana_rep.title("Módulo de Reportes y Estadísticas")
    ventana_rep.geometry("800x550")

    notebook = ttk.Notebook(ventana_rep)
    notebook.pack(pady=10, padx=10, fill="both", expand=True)

    # INGRESOS POR MEDIO DE PAGO
    tab_ventas = ttk.Frame(notebook)
    notebook.add(tab_ventas, text="Ingresos por Local/Pago")

    tabla_v = ttk.Treeview(tab_ventas, columns=("local", "medio", "cant", "total"), show="headings")
    tabla_v.heading("local", text="Local")
    tabla_v.heading("medio", text="Medio de Pago")
    tabla_v.heading("cant", text="Cant. Ventas")
    tabla_v.heading("total", text="Total Recaudado")
    tabla_v.pack(pady=10, padx=10, fill="both", expand=True)

    def cargar_v():
        for f in tabla_v.get_children(): tabla_v.delete(f)
        datos = reportes_service.obtener_ventas_ingresos()
        for d in datos: tabla_v.insert("", tk.END, values=(d[0], d[1], d[2], f"${d[3]:.2f}"))

    ttk.Button(tab_ventas, text="Generar Reporte", command=cargar_v).pack(pady=5)

    # PRODUCTOS MÁS VENDIDOS
    tab_prods = ttk.Frame(notebook)
    notebook.add(tab_prods, text="Top Productos y Margen")

    tabla_p = ttk.Treeview(tab_prods, columns=("prod", "unidades", "recaudacion", "ganancia"), show="headings")
    tabla_p.heading("prod", text="Producto")
    tabla_p.heading("unidades", text="Unidades Vendidas")
    tabla_p.heading("recaudacion", text="Recaudación Bruta")
    tabla_p.heading("ganancia", text="Ganancia Neta")
    tabla_p.pack(pady=10, padx=10, fill="both", expand=True)

    def cargar_p():
        for f in tabla_p.get_children(): tabla_p.delete(f)
        datos = reportes_service.obtener_productos_mas_vendidos()
        for d in datos: tabla_p.insert("", tk.END, values=(d[0], d[1], f"${d[2]:.2f}", f"${d[3]:.2f}"))

    ttk.Button(tab_prods, text="Generar Ranking", command=cargar_p).pack(pady=5)

    # ALERTA DE STOCK MÍNIMO
    tab_stock = ttk.Frame(notebook)
    notebook.add(tab_stock, text="Alertas de Stock")

    tabla_s = ttk.Treeview(tab_stock, columns=("prod", "ubi", "actual", "minimo"), show="headings")
    tabla_s.heading("prod", text="Producto")
    tabla_s.heading("ubi", text="Ubicacion")
    tabla_s.heading("actual", text="Stock Físico Actual")
    tabla_s.heading("minimo", text="Stock Mínimo")
    tabla_s.pack(pady=10, padx=10, fill="both", expand=True)

    def cargar_s():
        for f in tabla_s.get_children(): tabla_s.delete(f)
        datos = reportes_service.obtener_stock_critico()
        for d in datos: tabla_s.insert("", tk.END, values=(d[0], d[1], d[2], d[3]))

    ttk.Button(tab_stock, text="Revisar Stock", command=cargar_s).pack(pady=5)

    # LOGÍSTICA - RECHAZOS Y TRÁNSITOS
    tab_logistica = ttk.Frame(notebook)
    notebook.add(tab_logistica, text="Control Logístico")

    ttk.Label(tab_logistica, text="Bultos Rechazados / Rotura de Precinto", font=("Arial", 10, "bold")).pack(pady=5)
    tabla_r = ttk.Treeview(tab_logistica, columns=("codigo", "fecha", "usuario", "motivo"), show="headings", height=5)
    tabla_r.heading("codigo", text="Código Bulto")
    tabla_r.heading("fecha", text="Fecha/Hora")
    tabla_r.heading("usuario", text="Usuario")
    tabla_r.heading("motivo", text="Motivo / Observación")
    tabla_r.pack(pady=5, padx=10, fill="x")

    ttk.Label(tab_logistica, text="Tiempos de Tránsito (CD -> Locales)", font=("Arial", 10, "bold")).pack(pady=5)
    tabla_t = ttk.Treeview(tab_logistica, columns=("codigo", "envio", "recepcion", "horas"), show="headings", height=5)
    tabla_t.heading("codigo", text="Código Bulto")
    tabla_t.heading("envio", text="Fecha Envío")
    tabla_t.heading("recepcion", text="Fecha Recepción")
    tabla_t.heading("horas", text="Horas en Tránsito")
    tabla_t.pack(pady=5, padx=10, fill="x")

    def cargar_logistica():
        for f in tabla_r.get_children(): tabla_r.delete(f)
        for f in tabla_t.get_children(): tabla_t.delete(f)

        rechazos = reportes_service.obtener_bultos_rechazados()
        for r in rechazos: tabla_r.insert("", tk.END, values=(r[0], r[1], r[2], r[3]))

        tiempos = reportes_service.obtener_tiempo_transito()
        for t in tiempos: tabla_t.insert("", tk.END, values=(t[0], t[1], t[2], f"{t[3]} hs"))

    ttk.Button(tab_logistica, text="Actualizar Métricas Logísticas", command=cargar_logistica).pack(pady=10)

    # VALORIZACIÓN DE INVENTARIO
    tab_valor = ttk.Frame(notebook)
    notebook.add(tab_valor, text="Valorización Inventario")

    tabla_val = ttk.Treeview(tab_valor, columns=("ubi", "unidades", "capital"), show="headings")
    tabla_val.heading("ubi", text="Ubicación (Local/CD)")
    tabla_val.heading("unidades", text="Total Unidades Físicas")
    tabla_val.heading("capital", text="Capital Inmovilizado (Costo)")
    tabla_val.pack(pady=10, padx=10, fill="both", expand=True)

    def cargar_valorizacion():
        for f in tabla_val.get_children(): tabla_val.delete(f)
        datos = reportes_service.obtener_valorizacion_inventario()
        for d in datos: tabla_val.insert("", tk.END, values=(d[0], d[1], f"${d[2]:.2f}"))

    ttk.Button(tab_valor, text="Calcular Valorización", command=cargar_valorizacion).pack(pady=5)
     