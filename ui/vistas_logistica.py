import tkinter as tk
from tkinter import ttk

def mostrar_menu_logistica(ventana_padre, logistica_service):
    ventana_log = tk.Toplevel(ventana_padre)
    ventana_log.title("Módulo de Logística - Armar y Seguimiento")
    ventana_log.geometry("580x750") # Un poco más alta para los campos nuevos

    items_temporales = {}

    # ==========================================
    # 1. ALTA DE BULTO NUEVO (Con Origen, Destino, Remito y Precinto)
    # ==========================================
    frame_alta = ttk.LabelFrame(ventana_log, text="Armar y Despachar Nuevo Bulto")
    frame_alta.pack(pady=10, padx=10, fill="both", expand=True)

    # Fila 0
    ttk.Label(frame_alta, text="Código Bulto:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_codigo = ttk.Entry(frame_alta, width=15)
    entry_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(frame_alta, text="Usuario:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_usuario = ttk.Entry(frame_alta, width=15)
    entry_usuario.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    # Fila 1: Origen y Destino (Req. del TP)
    ttk.Label(frame_alta, text="ID Local Origen:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_origen = ttk.Entry(frame_alta, width=15)
    entry_origen.insert(0, "1") # Por defecto el 1
    entry_origen.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(frame_alta, text="ID Local Destino:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    entry_destino = ttk.Entry(frame_alta, width=15)
    entry_destino.insert(0, "2") # Por defecto el 2
    entry_destino.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    # Fila 2: Precinto y Remito (Req. del TP)
    ttk.Label(frame_alta, text="Nro. Precinto:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_precinto = ttk.Entry(frame_alta, width=15)
    entry_precinto.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(frame_alta, text="Nro. Remito:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    entry_remito = ttk.Entry(frame_alta, width=15)
    entry_remito.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    # --- SECCIÓN: AGREGAR PRODUCTOS ---
    frame_items = ttk.LabelFrame(frame_alta, text="Productos a incluir en la caja")
    frame_items.grid(row=3, column=0, columnspan=4, pady=10, padx=5, sticky="ew")

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
    lbl_resultado.grid(row=5, column=0, columnspan=4, pady=5)

    def armar_bulto_click():
        codigo_ingresado = entry_codigo.get().strip()
        usuario_ingresado = entry_usuario.get().strip()
        precinto = entry_precinto.get().strip()
        remito = entry_remito.get().strip()

        if not codigo_ingresado or not items_temporales:
            lbl_resultado.config(text="Falta código o productos", foreground="red")
            return

        try:
            class UbicacionMock:
                def __init__(self, id_ub):
                    self.id = id_ub

            origen_id = int(entry_origen.get()) if entry_origen.get().isdigit() else 1
            destino_id = int(entry_destino.get()) if entry_destino.get().isdigit() else 2

            # 1. Armamos el bulto
            bulto = logistica_service.armar_bulto(
                codigo=codigo_ingresado,
                origen=UbicacionMock(origen_id),
                destino=UbicacionMock(destino_id),
                items_dict=items_temporales,
                usuario=usuario_ingresado
            )
            
            # 2. Si le pusieron precinto, llamamos a tu función de precintado
            if precinto:
                logistica_service.precintar_bulto(bulto.id, usuario_ingresado, precinto)
            
            # 3. Si le pusieron remito, llamamos a tu función de despacho
            if remito:
                logistica_service.despachar_bulto(bulto.id, usuario_ingresado, remito)

            lbl_resultado.config(text=f"Bulto {bulto.codigo} creado y despachado con éxito", foreground="green")
            
            # Limpiar campos
            entry_codigo.delete(0, tk.END)
            entry_precinto.delete(0, tk.END)
            entry_remito.delete(0, tk.END)
            lista_items.delete(0, tk.END)
            items_temporales.clear()

        except Exception as e:
            lbl_resultado.config(text=f"Error: {e}", foreground="red")

    btn_guardar = ttk.Button(frame_alta, text="Armar y Despachar Bulto", command=armar_bulto_click)
    btn_guardar.grid(row=4, column=0, columnspan=4, pady=10)

    # ==========================================
    # 2. ACTUALIZAR ESTADO DE BULTO (Recepción)
    # ==========================================
    frame_estado = ttk.LabelFrame(ventana_log, text="Recepción y Verificación de Bulto")
    frame_estado.pack(pady=10, padx=10, fill="both", expand=True)

    ttk.Label(frame_estado, text="Código del Bulto:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_codigo_est = ttk.Entry(frame_estado, width=25)
    entry_codigo_est.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(frame_estado, text="Nuevo Estado:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    combo_estado = ttk.Combobox(frame_estado, values=["Recibido", "Verificado", "Rechazado"], state="readonly", width=22)
    combo_estado.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    combo_estado.current(1) # Por defecto Verificado

    ttk.Label(frame_estado, text="Usuario:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_usuario_est = ttk.Entry(frame_estado, width=25)
    entry_usuario_est.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # VALIDACIÓN DEL PRECINTO (Requisito clave)
    ttk.Label(frame_estado, text="Estado del Precinto:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    
    estado_precinto = tk.StringVar(value="intacto")
    frame_radios = ttk.Frame(frame_estado)
    frame_radios.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    ttk.Radiobutton(frame_radios, text="Intacto", variable=estado_precinto, value="intacto").pack(side="left")
    ttk.Radiobutton(frame_radios, text="Violado (Rechazar)", variable=estado_precinto, value="violado").pack(side="left", padx=10)

    ttk.Label(frame_estado, text="Obs. (Opcional):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    entry_obs = ttk.Entry(frame_estado, width=30)
    entry_obs.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    lbl_mensaje_est = ttk.Label(frame_estado, text="", font=("Arial", 9, "bold"))
    lbl_mensaje_est.grid(row=6, column=0, columnspan=2, pady=5)

    def actualizar_estado():
        try:
            codigo = entry_codigo_est.get().strip()
            estado = combo_estado.get()
            usuario = entry_usuario_est.get().strip()
            obs = entry_obs.get().strip()
            
            # REGLA DE NEGOCIO: Si al recibirlo el precinto está violado, se rechaza automáticamente.
            if estado in ["Recibido", "Verificado"] and estado_precinto.get() == "violado":
                estado = "Rechazado"
                obs = f"[ALERTA PRECINTO ROTO] {obs}"
            
            # Llamamos a tu servicio original, que ya hace la resta/suma de stock perfectamente
            logistica_service.actualizar_estado_bulto(codigo, estado, usuario, obs)
            
            msg = f"Bulto '{codigo}' actualizado a {estado}"
            color = "red" if estado == "Rechazado" else "blue"
            lbl_mensaje_est.config(text=msg, foreground=color)
            
            entry_codigo_est.delete(0, tk.END)
            entry_obs.delete(0, tk.END)
        except Exception as e:
            lbl_mensaje_est.config(text=f"Error: {e}", foreground="red")

    btn_actualizar = ttk.Button(frame_estado, text="Registrar Recepción", command=actualizar_estado)
    btn_actualizar.grid(row=5, column=0, columnspan=2, pady=10)