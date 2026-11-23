"""
Punto de Entrada Principal (Main) para Software FJ.
Permite ejecutar la batería automatizada de las 10+ simulaciones o acceder a un menú interactivo.
"""
import sys
from gestor_sistema import SistemaGestionSoftwareFJ
from modelos import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from simulaciones import ejecutar_diez_simulaciones
from logger_config import logger


def menu_interactivo():
    sistema = SistemaGestionSoftwareFJ()

    # Pre-cargar algunos servicios base
    sistema.registrar_servicio(ReservaSala("SRV-S1", "Sala de Juntas Ejecutiva", 50000.0, "REUNIONES", 12, True))
    sistema.registrar_servicio(AlquilerEquipo("SRV-E1", "Laptop Core i7 32GB", 60000.0, "Dell Latitude 5540", True))
    sistema.registrar_servicio(AsesoriaEspecializada("SRV-A1", "Consultoría en Ciberseguridad", 150000.0, "Seguridad Ofensiva", "SENIOR"))

    while True:
        print("\n" + "="*50)
        print("  SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
        print("="*50)
        print(" 1. Registrar Nuevo Cliente")
        print(" 2. Listar Clientes")
        print(" 3. Listar Servicios Disponibles")
        print(" 4. Crear Nueva Reserva")
        print(" 5. Confirmar Reserva")
        print(" 6. Cancelar Reserva")
        print(" 7. Listar Todas las Reservas")
        print(" 8. Ejecutar Batería de 10 Simulaciones Automáticas")
        print(" 0. Salir")
        print("="*50)

        opcion = input(" Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                id_cli = input(" ID Cliente: ").strip()
                nombre = input(" Nombre completo: ").strip()
                email = input(" Correo electrónico: ").strip()
                tel = input(" Teléfono: ").strip()
                cli = sistema.registrar_cliente(id_cli, nombre, email, tel)
                if cli:
                    print(f" [OK] Cliente registrado: {cli.obtener_resumen()}")
                else:
                    print(" [X] No fue posible registrar al cliente. Verifique los datos o consulte 'software_fj.log'.")
            except Exception as e:
                logger.error(f"Error en entrada de usuario: {e}")
                print(f" Error: {e}")

        elif opcion == "2":
            clientes = sistema.listar_clientes()
            print(f"\n--- CLIENTES REGISTRADOS ({len(clientes)}) ---")
            for c in clientes:
                print(f" - {c.obtener_resumen()}")

        elif opcion == "3":
            servicios = sistema.listar_servicios()
            print(f"\n--- CATÁLOGO DE SERVICIOS ({len(servicios)}) ---")
            for s in servicios:
                print(f" - [{s.identificador}] {s.describir_servicio()}")

        elif opcion == "4":
            try:
                id_res = input(" ID para la Reserva: ").strip()
                id_cli = input(" ID del Cliente: ").strip()
                id_srv = input(" Código del Servicio: ").strip()
                duracion_str = input(" Duración (horas o días según servicio): ").strip()
                duracion = float(duracion_str)
                desc_str = input(" Descuento decimal (ej. 0.10 para 10%, ENTER para 0): ").strip()
                desc = float(desc_str) if desc_str else 0.0

                res = sistema.crear_reserva(id_res, id_cli, id_srv, duracion, desc)
                if res:
                    print(f" [OK] Reserva creada: {res.obtener_resumen()}")
                else:
                    print(" [X] La reserva fue rechazada por reglas de validación. Consulte 'software_fj.log'.")
            except ValueError:
                print(" [X] Error: la duración o el descuento deben ser valores numéricos válidos.")
            except Exception as e:
                logger.error(f"Error en captura de reserva: {e}")
                print(f" Error: {e}")

        elif opcion == "5":
            id_res = input(" ID de la Reserva a Confirmar: ").strip()
            if sistema.confirmar_reserva(id_res):
                print(f" [OK] Reserva {id_res} confirmada con éxito.")
            else:
                print(f" [X] No se pudo confirmar la reserva {id_res}. Revise el log.")

        elif opcion == "6":
            id_res = input(" ID de la Reserva a Cancelar: ").strip()
            motivo = input(" Motivo de cancelación: ").strip() or "Solicitud de usuario"
            if sistema.cancelar_reserva(id_res, motivo):
                print(f" [OK] Reserva {id_res} cancelada.")
            else:
                print(f" [X] No fue posible cancelar la reserva {id_res}. Revise el log.")

        elif opcion == "7":
            reservas = sistema.listar_reservas()
            print(f"\n--- LISTADO DE RESERVAS ({len(reservas)}) ---")
            for r in reservas:
                print(f" - {r.obtener_resumen()}")

        elif opcion == "8":
            ejecutar_diez_simulaciones()

        elif opcion == "0":
            print("\n Finalizando sistema Software FJ. ¡Hasta pronto!\n")
            break

        else:
            print(" Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    # Si se pasa argumento '--simulacion' corre las simulaciones directamente
    if len(sys.argv) > 1 and sys.argv[1] == "--simulacion":
        ejecutar_diez_simulaciones()
    else:
        # Por defecto ejecuta las simulaciones y luego entra al menú
        ejecutar_diez_simulaciones()
        menu_interactivo()
