import tkinter as tk
from tkinter import ttk

def mostrar_menu_logistica(ventana_padre, logistica_service):
    ventana_log = tk.Toplevel(ventana_padre)
    ventana_log.title("Módulo de Logística - Armar y Seguimiento")
    ventana_log.geometry("450x550")

    # ==========================================
    # 1. ALTA DE BULTO NUEVO
    # ==========================================
    lbl_instruccion = ttk.Label(ventana_log, text="Ingrese los datos del nuevo bulto:")
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
    btn_guardar.pack(pady=10)

    # ==========================================
    # 2. ACTUALIZAR ESTADO DE BULTO
    # ==========================================
    frame_estado = ttk.LabelFrame(ventana_log, text="Actualizar Estado del Bulto")
    frame_estado.pack(pady=15, padx=10, fill="both", expand=True)

    ttk.Label(frame_estado, text="Código del Bulto:").grid(row=0, column=0, padx=5, pady=5)
    entry_codigo_est = ttk.Entry(frame_estado)
    entry_codigo_est.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_estado, text="Nuevo Estado:").grid(row=1, column=0, padx=5, pady=5)
    combo_estado = ttk.Combobox(frame_estado, values=["En Tránsito", "Recibido", "Rechazado"], state="readonly")
    combo_estado.grid(row=1, column=1, padx=5, pady=5)
    combo_estado.current(0) # Selecciona "En Tránsito" por defecto

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