import tkinter as tk
from tkinter import ttk, messagebox

def mostrar_menu_logistica(ventana_padre, logistica_service, ubicacion_service, producto_service):
    ventana_log = tk.Toplevel(ventana_padre)
    ventana_log.title("Módulo de Logística - Armar y Seguimiento")
    ventana_log.geometry("580x750") # Un poco más alta para los campos nuevos

    try:
        ubicaciones = ubicacion_service.obtener_todos()
        productos = producto_service.obtener_todos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar sucursales y productos: {e}", parent=ventana_log)
        ventana_log.destroy()
        return

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
    direcciones = [ubicacion["direccion"] or ubicacion["nombre"] for ubicacion in ubicaciones]
    ttk.Label(frame_alta, text="Sucursal Origen:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    combo_origen = ttk.Combobox(frame_alta, values=direcciones, state="readonly", width=15)
    combo_origen.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(frame_alta, text="Sucursal Destino:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    combo_destino = ttk.Combobox(frame_alta, values=direcciones, state="readonly", width=15)
    combo_destino.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    opciones_origen = list(ubicaciones)
    opciones_destino = list(ubicaciones)

    def ubicacion_seleccionada(combo, opciones):
        indice = combo.current()
        return opciones[indice] if 0 <= indice < len(opciones) else None

    def actualizar_opciones_sucursales(origen_id, destino_id):
        opciones_origen[:] = [ubicacion for ubicacion in ubicaciones if ubicacion["id"] != destino_id]
        opciones_destino[:] = [ubicacion for ubicacion in ubicaciones if ubicacion["id"] != origen_id]

        combo_origen.configure(
            values=[ubicacion["direccion"] or ubicacion["nombre"] for ubicacion in opciones_origen],
            state="readonly" if opciones_origen else "disabled"
        )
        combo_destino.configure(
            values=[ubicacion["direccion"] or ubicacion["nombre"] for ubicacion in opciones_destino],
            state="readonly" if opciones_destino else "disabled"
        )

        indice_origen = next(
            (i for i, ubicacion in enumerate(opciones_origen) if ubicacion["id"] == origen_id),
            -1
        )
        indice_destino = next(
            (i for i, ubicacion in enumerate(opciones_destino) if ubicacion["id"] == destino_id),
            -1
        )
        if indice_origen == -1:
            combo_origen.set("")
        else:
            combo_origen.current(indice_origen)
        if indice_destino == -1:
            combo_destino.set("")
        else:
            combo_destino.current(indice_destino)

    origen_inicial = next((u for u in ubicaciones if u["id"] == 1), None)
    if origen_inicial is None and ubicaciones:
        origen_inicial = ubicaciones[0]
    destino_inicial = next(
        (u for u in ubicaciones if u["id"] == 2 and (origen_inicial is None or u["id"] != origen_inicial["id"])),
        None
    )
    if destino_inicial is None:
        destino_inicial = next(
            (u for u in ubicaciones if origen_inicial is None or u["id"] != origen_inicial["id"]),
            None
        )

    actualizar_opciones_sucursales(
        origen_inicial["id"] if origen_inicial else None,
        destino_inicial["id"] if destino_inicial else None
    )

    def cambiar_origen(_event=None):
        origen = ubicacion_seleccionada(combo_origen, opciones_origen)
        destino = ubicacion_seleccionada(combo_destino, opciones_destino)
        if origen and destino and origen["id"] == destino["id"]:
            destino = next((u for u in ubicaciones if u["id"] != origen["id"]), None)
        actualizar_opciones_sucursales(
            origen["id"] if origen else None,
            destino["id"] if destino else None
        )

    def cambiar_destino(_event=None):
        origen = ubicacion_seleccionada(combo_origen, opciones_origen)
        destino = ubicacion_seleccionada(combo_destino, opciones_destino)
        if origen and destino and origen["id"] == destino["id"]:
            origen = next((u for u in ubicaciones if u["id"] != destino["id"]), None)
        actualizar_opciones_sucursales(
            origen["id"] if origen else None,
            destino["id"] if destino else None
        )

    combo_origen.bind("<<ComboboxSelected>>", cambiar_origen)
    combo_destino.bind("<<ComboboxSelected>>", cambiar_destino)

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

    ttk.Label(frame_items, text="Producto:").grid(row=0, column=0, padx=2)
    combo_producto = ttk.Combobox(
        frame_items,
        values=[producto["nombre"] for producto in productos],
        state="readonly",
        width=18
    )
    combo_producto.grid(row=0, column=1, padx=2)

    ttk.Label(frame_items, text="Cant:").grid(row=0, column=2, padx=2)
    entry_cant = ttk.Entry(frame_items, width=8)
    entry_cant.grid(row=0, column=3, padx=2)

    lista_items = tk.Listbox(frame_items, height=4)
    lista_items.grid(row=1, column=0, columnspan=5, pady=5, padx=5, sticky="ew")

    def agregar_item_lista():
        indice_producto = combo_producto.current()
        cant = entry_cant.get()
        if indice_producto == -1 or not cant.isdigit():
            lbl_resultado.config(text="Seleccione un producto e ingrese una cantidad válida", foreground="red")
            return

        producto_seleccionado = productos[indice_producto]

        class ProductoMock:
            def __init__(self, id_prod, nombre):
                self.id = id_prod
                self.nombre = nombre
            
        prod = ProductoMock(producto_seleccionado["id"], producto_seleccionado["nombre"])
        items_temporales[prod] = int(cant)
        lista_items.insert(tk.END, f"{producto_seleccionado['nombre']} | Cantidad: {cant}")
        combo_producto.set("")
        entry_cant.delete(0, tk.END)
        lbl_resultado.config(text="")

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

            indice_origen = combo_origen.current()
            indice_destino = combo_destino.current()
            if indice_origen == -1 or indice_destino == -1:
                lbl_resultado.config(text="Seleccione las sucursales de origen y destino", foreground="red")
                return

            origen_id = opciones_origen[indice_origen]["id"]
            destino_id = opciones_destino[indice_destino]["id"]
            if origen_id == destino_id:
                lbl_resultado.config(text="El origen y el destino deben ser sucursales diferentes", foreground="red")
                return

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