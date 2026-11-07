import tkinter as tk
from tkinter import ttk
from datetime import date
from decimal import Decimal

from domain.models.usuarios import Usuario
from domain.models.ubicacion import Ubicacion
from domain.models.catalogo import Producto
from domain.models.pagos_strategy import PagoEfectivo, PagoTarjeta, PagoTransferencia
from domain.models.promociones import DescuentoPorcentaje, DescuentoMontoFijo, PromoNxM

def mostrar_menu_ventas(ventana_padre, ventana_service):
    ventana_ventas = tk.Toplevel(ventana_padre)
    ventana_ventas.title("Módulo de Ventas - Punto de Venta")
    ventana_ventas.geometry("550x550")

    # Mocks para el TP
    cajero_actual = Usuario(id_usuario=1, username="cajero_Pablo", rol="Cajero", nombre="Pablo", apellido="Perez")
    local_actual = Ubicacion(id_ubicacion=1, nombre="Local Centro", direccion="San Martín 456")
    carrito = []

    # AGREGAR PRODUCTOS
    frame_prod = ttk.LabelFrame(ventana_ventas, text="Agregar Producto al Carrito")
    frame_prod.pack(pady=10, padx=10, fill="x")

    ttk.Label(frame_prod, text="ID Prod:").grid(row=0, column=0, padx=5, pady=5)
    entry_id = ttk.Entry(frame_prod, width=8)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_prod, text="Cant:").grid(row=0, column=2, padx=5, pady=5)
    entry_cant = ttk.Entry(frame_prod, width=8)
    entry_cant.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(frame_prod, text="Precio: $").grid(row=0, column=4, padx=5, pady=5)
    entry_precio = ttk.Entry(frame_prod, width=10)
    entry_precio.grid(row=0, column=5, padx=5, pady=5)

    def agregar_al_carrito():
        try:
            prod_id = int(entry_id.get())
            cant = int(entry_cant.get())
            precio = Decimal(entry_precio.get())

            prod_simulado = Producto(
                id_producto=prod_id, sku=f"SKU-{prod_id}", nombre="Producto de prueba", precio_venta=precio, costo=Decimal("0.0"), categoria=None, proveedor=None
            )

            carrito.append({'producto': prod_simulado, 'cantidad': cant, 'precio': precio})
            lista_carrito.insert(tk.END, f"{cant}x Producto {prod_id} - ${precio:.2f} c/u")

            entry_id.delete(0, tk.END)
            entry_cant.delete(0, tk.END)
            entry_precio.delete(0, tk.END)
            lbl_estado.config(text="")
        except ValueError:
            lbl_estado.config(text="Ingrese números válidos", foreground="red")

    btn_agregar = ttk.Button(frame_prod, text="Agregar", command=agregar_al_carrito)
    btn_agregar.grid(row=0, column=6, padx=10)

    # CARRITO VISUAL
    lista_carrito = tk.Listbox(ventana_ventas, height=8)
    lista_carrito.pack(pady=5, padx=10, fill="both")

    # PROMOCIONES Y DESCUENTOS
    frame_promo = ttk.LabelFrame(ventana_ventas, text="Aplicar Promoción")
    frame_promo.pack(pady=5, padx=10, fill="x")

    opciones_promo = ["Sin Promoción", "10% de Descuento", "Descuento Fijo $2000", "Promo 3x2 (NxM)"]
    combo_promo = ttk.Combobox(frame_promo, values=opciones_promo, state="readonly")
    combo_promo.current(0)
    combo_promo.pack(pady=10, padx=20, fill="x")

    # ESTRATEGIA DE PAGO
    frame_pago = ttk.LabelFrame(ventana_ventas, text="Medio de Pago")
    frame_pago.pack(pady=10, padx=10, fill="x")

    opcion_pago = tk.StringVar(value="efectivo")
    ttk.Radiobutton(frame_pago, text="Efectivo", variable=opcion_pago, value="efectivo").pack(side="left", padx=20, pady=10)
    ttk.Radiobutton(frame_pago, text="Tarjeta", variable=opcion_pago, value="tarjeta").pack(side="left", padx=20, pady=10)
    ttk.Radiobutton(frame_pago, text="Transferencia", variable=opcion_pago, value="transferencia").pack(side="left", padx=20, pady=10)

    lbl_estado = ttk.Label(ventana_ventas, text="", font=("Arial", 10, "bold"))
    lbl_estado.pack(pady=5)

    def cobrar_venta():
        if not carrito:
            lbl_estado.config(text="El carrito está vacío", foreground="red")
            return
        
        seleccion = opcion_pago.get()
        if seleccion == "efectivo":
            estrategia = PagoEfectivo()
        elif seleccion == "tarjeta":
            estrategia = PagoTarjeta(numero_tarjeta="4567", cuotas=1)
        else:
            estrategia = PagoTransferencia(cbu_origen="00001111", comprobante_bancario="TRX999")

        seleccion_promo = combo_promo.get()
        promocion_aplicar = None
        hoy = date.today()

        if seleccion_promo == "10% de Descuento":
            promocion_aplicar = DescuentoPorcentaje("Desc 10%", "10% OFF", hoy, hoy, True, Decimal("10.0"))
        elif seleccion_promo == "Descuento Fijo $2000":
            promocion_aplicar = DescuentoMontoFijo("Fijo 2000", "$2000 OFF", hoy, hoy, True, Decimal("2000.0"))
        elif seleccion_promo == "Promo 3x2 (NxM)":
            promocion_aplicar = PromoNxM("3x2", "Llevá 3 pagás 2", hoy, hoy, True, 3, 2)
        
        try:
            nueva_venta = ventana_service.procesar_venta_completa(
                cajero=cajero_actual,
                local=local_actual,
                carrito_items=carrito,
                medio_pago=estrategia,
                promocion=promocion_aplicar
            )
            lbl_estado.config(text=f"VENTA {nueva_venta.id} COMPLETADA (${nueva_venta.total:.2f})", foreground="green")
            carrito.clear()
            lista_carrito.delete(0, tk.END)
            combo_promo.current(0)
        except Exception as e:
            lbl_estado.config(text=f"Error en BD: {e}", foreground="red")

    btn_cobrar = ttk.Button(ventana_ventas, text="PROCESAR VENTA", command=cobrar_venta)
    btn_cobrar.pack(pady=10)



