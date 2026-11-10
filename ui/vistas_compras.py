import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from domain.models.inventario import TipoMovimiento

def mostrar_menu_compras(ventana_padre, compras_service):
    ventana_compras = tk.Toplevel(ventana_padre)
    ventana_compras.title("Módulo de Compras - Sugeridas y Manuales")
    ventana_compras.geometry("700x550")

    # --- SECCIÓN 1: FALTANTES ---
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

    lbl_estado = ttk.Label(frame_sugeridas, text="", font=("Arial", 10))
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
                        item['producto_nombre'], item['stock_actual'], 
                        item['stock_minimo'], item['cantidad_sugerida']
                    ))
                lbl_estado.config(text=f"Se detectaron {len(faltantes)} productos con faltantes.", foreground="orange")
        except Exception as e:
            lbl_estado.config(text=f"Error al consultar faltantes: {e}", foreground="red")

    btn_generar = ttk.Button(frame_sugeridas, text="Calcular Faltantes", command=calcular_sugeridas)
    btn_generar.pack(pady=10)

    # --- SECCIÓN 2: COMPRA MANUAL COMPLETA ---
    frame_manual = ttk.LabelFrame(ventana_compras, text="Registrar Compra (Guarda Orden y Suma Stock)")
    frame_manual.pack(pady=10, padx=10, fill="x")

    # Fila 0
    ttk.Label(frame_manual, text="ID Producto:").grid(row=0, column=0, padx=5, pady=5)
    entry_id_prod = ttk.Entry(frame_manual, width=10)
    entry_id_prod.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_manual, text="Cantidad:").grid(row=0, column=2, padx=5, pady=5)
    entry_cant = ttk.Entry(frame_manual, width=10)
    entry_cant.grid(row=0, column=3, padx=5, pady=5)

    # Fila 1
    ttk.Label(frame_manual, text="ID Proveedor:").grid(row=1, column=0, padx=5, pady=5)
    entry_id_prov = ttk.Entry(frame_manual, width=10)
    entry_id_prov.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_manual, text="Costo Unit:").grid(row=1, column=2, padx=5, pady=5)
    entry_costo = ttk.Entry(frame_manual, width=10)
    entry_costo.grid(row=1, column=3, padx=5, pady=5)

    def registrar_compra_manual():
        try:
            id_prod = int(entry_id_prod.get())
            cant = int(entry_cant.get())
            id_prov = int(entry_id_prov.get())
            costo = float(entry_costo.get())
            
            if cant <= 0 or costo <= 0:
                messagebox.showwarning("Atención", "Cantidad y costo deben ser mayores a 0", parent=ventana_compras)
                return

            # Creamos objetos genéricos en memoria para no romper nada con imports cruzados
            class DummyObj: pass
            
            prov = DummyObj()
            prov.id = id_prov
            
            prod = DummyObj()
            prod.id = id_prod
            
            item = DummyObj()
            item.producto = prod
            item.cantidad = cant
            item.precio = costo
            
            orden = DummyObj()
            orden.fecha = datetime.now()
            orden.estado = "Recibida"
            orden.proveedor = prov
            orden.total = cant * costo
            orden.items = [item]
            
            # 1. Guardar la Orden completa en la BD
            if compras_service.compras_dao:
                compras_service.compras_dao.guardar_orden(orden)
                
            # 2. Sumar el stock al Inventario
            if compras_service.inventario_service:
                compras_service.inventario_service.registrar_entrada(
                    id_producto=id_prod,
                    id_ubicacion=1,
                    cantidad=cant,
                    tipo=TipoMovimiento.RECEPCION,
                    referencia_tipo="CompraManual",
                    referencia_id=orden.id if hasattr(orden, 'id') else 0
                )
                
            messagebox.showinfo("Éxito", f"Compra registrada.\nSe guardó la orden y se sumaron {cant} unidades.", parent=ventana_compras)
            
            # Limpiamos los campos
            entry_id_prod.delete(0, tk.END)
            entry_cant.delete(0, tk.END)
            entry_id_prov.delete(0, tk.END)
            entry_costo.delete(0, tk.END)
            
            calcular_sugeridas()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.", parent=ventana_compras)
        except Exception as e:
            messagebox.showerror("Error de base de datos", f"Falló el guardado: {e}", parent=ventana_compras)

    btn_comprar = ttk.Button(frame_manual, text="Registrar Compra Completa", command=registrar_compra_manual)
    btn_comprar.grid(row=0, column=4, rowspan=2, padx=15, pady=10)
    
    