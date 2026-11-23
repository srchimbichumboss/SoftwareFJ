"""
Módulo de Excepciones Personalizadas para Software FJ.
Implementa una jerarquía orientada a objetos para la gestión de errores del sistema.
"""

class SoftwareFJError(Exception):
    """Clase base para todas las excepciones del dominio de Software FJ."""
    def __init__(self, mensaje: str, codigo_error: str = "ERR_GENERICO"):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo_error = codigo_error

    def __str__(self):
        return f"[{self.codigo_error}] {self.mensaje}"


class ClienteInvalidoError(SoftwareFJError):
    """Lanzada cuando los datos del cliente no cumplen con las validaciones de negocio."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_CLIENTE_INVALIDO")


class ServicioInvalidoError(SoftwareFJError):
    """Lanzada cuando los parámetros o configuración de un servicio son inválidos."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_SERVICIO_INVALIDO")


class ServicioNoDisponibleError(SoftwareFJError):
    """Lanzada cuando se intenta reservar un servicio que se encuentra fuera de disponibilidad o cupo."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_SERVICIO_NO_DISPONIBLE")


class ReservaInvalidaError(SoftwareFJError):
    """Lanzada ante inconsistencias en la creación, confirmación o procesamiento de una reserva."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_RESERVA_INVALIDA")


class EstadoInvalidoError(ReservaInvalidaError):
    """Lanzada cuando se intenta una transición de estado ilegal en una reserva (ej. cancelar una ya cancelada)."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.codigo_error = "ERR_ESTADO_TRANSICION_ILEGAL"


class CalculoInconsistenteError(SoftwareFJError):
    """Lanzada ante errores matemáticos o de cálculo de tarifas y descuentos."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_CALCULO_INCONSISTENTE")
