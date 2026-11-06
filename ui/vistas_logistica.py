def mostrar_menu_logistica(logistica_service):
    while True:
        print("\n--- MÓDULO DE LOGÍSTICA ---")
        print("1. Armar nuevo bulto")
        print("2. Precintar bulto existente")
        print("3. Despachar bulto")
        print("4. Volver al menú principal")

        opcion = input("\nOpción:")

        if opcion == '1':
            print("\n[ARMADO DE BULTO]")
            codigo = input("Ingrese código del bulto (ej. BULT-001):")
            usuario = input("Ingrese su nombre de usuario:")

            try:
                bulto = logistica_service.armar_bulto(
                    codigo=codigo,
                    origen=None,
                    destino=None,
                    items_dict={},
                    usuario=usuario
                )
                print(f"Bulto {bulto.codigo} creado en estado: {bulto.estado_actual.__class__.__name__}")
            except Exception as e:
                print(f"Error al armar el bulto: {e}")

        elif opcion == '2':
            id_bulto = int(input("Ingrese el ID numérico del bulto a precintar:"))
            precinto = input("Ingrese código del precinto:")
            usuario = input("Ingrese su nombre de usuario:")

            try:
                logistica_service.precintar_bulto(id_bulto, usuario, precinto)
                print("Bulto precintado con éxito.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '4':
            break