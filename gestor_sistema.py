"""
Módulo de Gestión Central del Sistema Software FJ.
Administra las colecciones en memoria de clientes, servicios y reservas.
Implementa el manejo robusto de excepciones exigido por la rúbrica:
- try / except
- try / except / else
- try / finally
- Encadenamiento de excepciones (raise ... from err)
- Logging continuo en cada evento
"""
from typing import Dict, List, Optional
from modelos import Cliente, Servicio, Reserva
from excepciones import (
    SoftwareFJError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    EstadoInvalidoError
)
from logger_config import logger


class SistemaGestionSoftwareFJ:
    """Controlador principal de la lógica de negocio de Software FJ."""

    def __init__(self):
        # Almacenamiento en memoria mediante diccionarios y listas (sin base de datos)
        self._clientes: Dict[str, Cliente] = {}
        self._servicios: Dict[str, Servicio] = {}
        self._reservas: Dict[str, Reserva] = {}
        logger.info("Sistema de Gestión Software FJ inicializado en memoria con éxito.")

    # =========================================================================
    # GESTIÓN DE CLIENTES (Ejemplo de try / except / else con validaciones)
    # =========================================================================
    def registrar_cliente(self, identificador: str, nombre: str, email: str, telefono: str) -> Optional[Cliente]:
        """
        Registra un nuevo cliente aplicando validación de duplicados y sintaxis.
        Demuestra el uso de try / except / else y logging estructurado.
        """
        logger.debug(f"Iniciando intento de registro de cliente ID: {identificador}")
        try:
            if identificador in self._clientes:
                raise ClienteInvalidoError(f"Ya existe un cliente registrado con el ID '{identificador}'.")

            nuevo_cliente = Cliente(
                identificador=identificador,
                nombre_completo=nombre,
                email=email,
                telefono=telefono
            )
        except ClienteInvalidoError as error_cliente:
            logger.error(f"Fallo al registrar cliente [{identificador}]: {error_cliente}")
            return None
        except Exception as error_inesperado:
            logger.critical(f"Error imprevisto en creación de cliente [{identificador}]: {error_inesperado}", exc_info=True)
            return None
        else:
            # Se ejecuta únicamente si la creación del cliente fue exitosa (sin excepciones)
            self._clientes[identificador] = nuevo_cliente
            logger.info(f"Cliente registrado exitosamente: {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente

    # =========================================================================
    # GESTIÓN DE SERVICIOS (Ejemplo de try / except y encadenamiento)
    # =========================================================================
    def registrar_servicio(self, servicio: Servicio) -> bool:
        """
        Registra un servicio en el catálogo de Software FJ.
        Implementa encadenamiento de excepciones ante tipos de datos erróneos.
        """
        try:
            if not isinstance(servicio, Servicio):
                # Generamos una excepción TypeError interna y la encadenamos a una de dominio
                raise TypeError(f"El objeto proporcionado ({type(servicio)}) no hereda de la clase abstracta Servicio.")

            if servicio.identificador in self._servicios:
                raise ServicioInvalidoError(f"El código de servicio '{servicio.identificador}' ya se encuentra en uso.")

            self._servicios[servicio.identificador] = servicio
            logger.info(f"Servicio incorporado al catálogo: {servicio.describir_servicio()}")
            return True

        except TypeError as tipo_err:
            # DEMOSTRACIÓN DE ENCADENAMIENTO DE EXCEPCIONES: raise ... from err
            try:
                raise ServicioInvalidoError(f"Incompatibilidad de tipo en servicio: {str(tipo_err)}") from tipo_err
            except ServicioInvalidoError as encadenada:
                logger.error(f"Excepción encadenada capturada: {encadenada} | Causa raíz: {encadenada.__cause__}")
            return False

        except ServicioInvalidoError as serv_err:
            logger.error(f"Error de validación al registrar servicio: {serv_err}")
            return False

    # =========================================================================
    # GESTIÓN DE RESERVAS (Ejemplo completo de try / except / else / finally)
    # =========================================================================
    def crear_reserva(self, id_reserva: str, id_cliente: str, id_servicio: str, duracion: float, descuento: float = 0.0) -> Optional[Reserva]:
        """
        Crea una reserva integrando cliente y servicio.
        Demuestra la estructura completa: try / except / else / finally.
        """
        logger.debug(f"Procesando solicitud de reserva '{id_reserva}' para Cliente '{id_cliente}' y Servicio '{id_servicio}'")
        reserva_creada = None
        operacion_exitosa = False

        try:
            if id_reserva in self._reservas:
                raise ReservaInvalidaError(f"El ID de reserva '{id_reserva}' ya existe en el sistema.")

            if id_cliente not in self._clientes:
                raise ClienteInvalidoError(f"No existe ningún cliente registrado con el ID '{id_cliente}'.")

            if id_servicio not in self._servicios:
                raise ServicioInvalidoError(f"No existe ningún servicio con el código '{id_servicio}'.")

            cliente = self._clientes[id_cliente]
            servicio = self._servicios[id_servicio]

            if not servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no se encuentra disponible para nuevas reservas.")

            # Instanciación y validación interna de parámetros
            reserva_creada = Reserva(
                identificador=id_reserva,
                cliente=cliente,
                servicio=servicio,
                duracion=duracion,
                descuento=descuento
            )

        except (ClienteInvalidoError, ServicioInvalidoError, ServicioNoDisponibleError, ReservaInvalidaError) as error_dominio:
            logger.warning(f"Rechazo controlado en creación de reserva [{id_reserva}]: {error_dominio}")
            reserva_creada = None

        except Exception as error_critico:
            # Encadenamiento ante fallo crítico de bajo nivel
            logger.critical(f"Falla inesperada en reserva [{id_reserva}]: {error_critico}", exc_info=True)
            reserva_creada = None

        else:
            # Solo si todo fue correcto
            self._reservas[id_reserva] = reserva_creada
            operacion_exitosa = True
            logger.info(f"Reserva creada con éxito: {reserva_creada.obtener_resumen()}")

        finally:
            # DEMOSTRACIÓN DE BLOQUE FINALLY: siempre se ejecuta para auditoría o limpieza
            resultado_str = "EXITOSA" if operacion_exitosa else "FALLIDA"
            logger.debug(f"[AUDITORÍA FINALLY] Solicitud de Reserva '{id_reserva}' concluida con estado: {resultado_str}")

        return reserva_creada

    # =========================================================================
    # ACCIONES DE ESTADO: CONFIRMAR Y CANCELAR (try / finally)
    # =========================================================================
    def confirmar_reserva(self, id_reserva: str) -> bool:
        """Confirma una reserva existente con control de excepciones y bloque try/finally."""
        try:
            if id_reserva not in self._reservas:
                raise ReservaInvalidaError(f"No se localizó la reserva '{id_reserva}'.")
            reserva = self._reservas[id_reserva]
            reserva.confirmar()
            return True
        except EstadoInvalidoError as err_estado:
            logger.error(f"Fallo de confirmación: {err_estado}")
            return False
        except ReservaInvalidaError as err_res:
            logger.error(f"Error de referencia de reserva: {err_res}")
            return False
        finally:
            logger.debug(f"[AUDITORÍA FINALLY] Intento de confirmación finalizado para reserva: {id_reserva}")

    def cancelar_reserva(self, id_reserva: str, motivo: str = "Solicitud del cliente") -> bool:
        """Cancela una reserva con manejo de transiciones inválidas."""
        try:
            if id_reserva not in self._reservas:
                raise ReservaInvalidaError(f"No existe la reserva '{id_reserva}'.")
            reserva = self._reservas[id_reserva]
            reserva.cancelar(motivo)
            return True
        except EstadoInvalidoError as err_estado:
            logger.error(f"Transición prohibida al cancelar: {err_estado}")
            return False
        except Exception as ex:
            logger.error(f"Error al cancelar reserva: {ex}")
            return False
        finally:
            logger.debug(f"[AUDITORÍA FINALLY] Proceso de cancelación concluido para reserva: {id_reserva}")

    # =========================================================================
    # CONSULTAS
    # =========================================================================
    def listar_clientes(self) -> List[Cliente]:
        return list(self._clientes.values())

    def listar_servicios(self) -> List[Servicio]:
        return list(self._servicios.values())

    def listar_reservas(self) -> List[Reserva]:
        return list(self._reservas.values())
