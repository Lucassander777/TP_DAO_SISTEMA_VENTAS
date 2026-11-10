import tkinter as tk
from tkinter import ttk

def mostrar_menu_logistica(ventana_padre, logistica_service):
    ventana_log = tk.Toplevel(ventana_padre)
    ventana_log.title("Módulo de Logística - Armar y Seguimiento")
    # Agrandamos la ventana para que entre la lista de productos
    ventana_log.geometry("550x650") 

    # Diccionario temporal para guardar los productos antes de presionar "Guardar"
    items_temporales = {}

    # ==========================================
    # 1. ALTA DE BULTO NUEVO (Con Productos)
    # ==========================================
    frame_alta = ttk.LabelFrame(ventana_log, text="Armar Nuevo Bulto")
    frame_alta.pack(pady=10, padx=10, fill="both", expand=True)

    lbl_codigo = ttk.Label(frame_alta, text="Código del Bulto:")
    lbl_codigo.grid(row=0, column=0, padx=5, pady=5)
    entry_codigo = ttk.Entry(frame_alta, width=20)
    entry_codigo.grid(row=0, column=1, padx=5, pady=5)

    lbl_usuario = ttk.Label(frame_alta, text="Usuario:")
    lbl_usuario.grid(row=1, column=0, padx=5, pady=5)
    entry_usuario = ttk.Entry(frame_alta, width=20)
    entry_usuario.grid(row=1, column=1, padx=5, pady=5)

    # --- SECCIÓN: AGREGAR PRODUCTOS AL BULTO ---
    frame_items = ttk.LabelFrame(frame_alta, text="Productos a incluir en la caja")
    frame_items.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

    ttk.Label(frame_items, text="ID Prod:").grid(row=0, column=0, padx=2)
    entry_id_prod = ttk.Entry(frame_items, width=8)
    entry_id_prod.grid(row=0, column=1, padx=2)

    ttk.Label(frame_items, text="Cant:").grid(row=0, column=2, padx=2)
    entry_cant = ttk.Entry(frame_items, width=8)
    entry_cant.grid(row=0, column=3, padx=2)

    lista_items = tk.Listbox(frame_items, height=4)
    lista_items.grid(row=1, column=0, columnspan=5, pady=5, padx=5, sticky="ew")

    def agregar_item_lista():
        prod_id = entry_id_prod.get()
        cant = entry_cant.get()
        if prod_id.isdigit() and cant.isdigit():
            # Creamos un objeto falso (Mock) de Producto solo con el ID para que el servicio no falle
            class ProductoMock:
                def __init__(self, id_prod):
                    self.id = id_prod
            
            prod = ProductoMock(int(prod_id))
            items_temporales[prod] = int(cant)
            
            lista_items.insert(tk.END, f"ID Producto: {prod_id} | Cantidad: {cant}")
            entry_id_prod.delete(0, tk.END)
            entry_cant.delete(0, tk.END)

    btn_add_item = ttk.Button(frame_items, text="Agregar Item", command=agregar_item_lista)
    btn_add_item.grid(row=0, column=4, padx=5)

    # --- GUARDAR EL BULTO COMPLETO ---
    lbl_resultado = ttk.Label(frame_alta, text="", foreground="blue")
    lbl_resultado.grid(row=4, column=0, columnspan=2, pady=5)

    def armar_bulto_click():
        codigo_ingresado = entry_codigo.get()
        usuario_ingresado = entry_usuario.get()

        try:
            # Simulamos las ubicaciones (1: Centro Distribución, 2: Local Destino)
            class UbicacionMock:
                def __init__(self, id_ub):
                    self.id = id_ub

            bulto = logistica_service.armar_bulto(
                codigo=codigo_ingresado,
                origen=UbicacionMock(1),
                destino=UbicacionMock(2),
                items_dict=items_temporales,
                usuario=usuario_ingresado
            )
            lbl_resultado.config(text=f"Bulto {bulto.codigo} armado exitosamente", foreground="green")
            entry_codigo.delete(0, tk.END)
            entry_usuario.delete(0, tk.END)
            lista_items.delete(0, tk.END)
            items_temporales.clear() # Limpiamos para el próximo bulto

        except Exception as e:
            lbl_resultado.config(text=f"Error: {e}", foreground="red")

    btn_guardar = ttk.Button(frame_alta, text="Guardar Bulto con Productos", command=armar_bulto_click)
    btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)

    # ==========================================
    # 2. ACTUALIZAR ESTADO DE BULTO
    # ==========================================
    frame_estado = ttk.LabelFrame(ventana_log, text="Actualizar Estado del Bulto")
    frame_estado.pack(pady=15, padx=10, fill="both", expand=True)

    ttk.Label(frame_estado, text="Código del Bulto:").grid(row=0, column=0, padx=5, pady=5)
    entry_codigo_est = ttk.Entry(frame_estado)
    entry_codigo_est.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_estado, text="Nuevo Estado:").grid(row=1, column=0, padx=5, pady=5)
    
    # IMPORTANTE: Agregamos el estado "Verificado" requerido por las consignas del TP
    combo_estado = ttk.Combobox(frame_estado, values=["Preparado", "Precintado", "En Transito", "Recibido", "Verificado", "Rechazado"], state="readonly")
    combo_estado.grid(row=1, column=1, padx=5, pady=5)
    combo_estado.current(2)

    ttk.Label(frame_estado, text="Usuario:").grid(row=2, column=0, padx=5, pady=5)
    entry_usuario_est = ttk.Entry(frame_estado)
    entry_usuario_est.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_estado, text="Obs. (Si es Rechazado):").grid(row=3, column=0, padx=5, pady=5)
    entry_obs = ttk.Entry(frame_estado)
    entry_obs.grid(row=3, column=1, padx=5, pady=5)

    lbl_mensaje_est = ttk.Label(frame_estado, text="", font=("Arial", 9, "bold"))
    lbl_mensaje_est.grid(row=5, column=0, columnspan=2, pady=5)

    def actualizar_estado():
        try:
            codigo = entry_codigo_est.get()
            estado = combo_estado.get()
            usuario = entry_usuario_est.get()
            obs = entry_obs.get()
            
            logistica_service.actualizar_estado_bulto(codigo, estado, usuario, obs)
            lbl_mensaje_est.config(text=f"Bulto '{codigo}' actualizado a {estado}", foreground="blue")
            
            entry_codigo_est.delete(0, tk.END)
            entry_obs.delete(0, tk.END)
        except Exception as e:
            lbl_mensaje_est.config(text=f"Error: {e}", foreground="red")

    btn_actualizar = ttk.Button(frame_estado, text="Registrar Movimiento", command=actualizar_estado)
    btn_actualizar.grid(row=4, column=0, columnspan=2, pady=10)