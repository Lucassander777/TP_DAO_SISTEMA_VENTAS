from ui.vistas_logistica import mostrar_menu_logistica

def iniciar_interfaz(logistica_service, ventas_service):
    while True:
        print("\n" + "="*30)
        print(" SISTEMA CENTRAL DE GESTIÓN ")
        print("="*30)
        print("1. Módulo de logística (Armado y Despacho)")
        print("2. Módulo de Ventas (Punto de Venta)")
        print("3. Salir del Sistema")

        opcion = input("\nSeleccione una opción:")

        if opcion == '1':
            mostrar_menu_logistica(logistica_service)
        elif opcion == '2':
            print("Módulo de ventas en construcción...")
        elif opcion == '3':
            print("Cerrando el sistema...")
            break
        else:
            print("Opción incorrecta, intente de nuevo.")