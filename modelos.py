"""
Módulo de Modelos Orientados a Objetos para Software FJ.
Implementa principios de:
- Abstracción (EntidadBase, Servicio con ABC)
- Encapsulación (atributos privados/protegidos, decoradores @property y setters con validación)
- Herencia (ReservaSala, AlquilerEquipo, AsesoriaEspecializada heredan de Servicio)
- Polimorfismo (sobrescritura de calcular_costo, describir_servicio, validar_parametros)
- Sobrecarga de métodos mediante parámetros opcionales y control de firma flexible
"""
from abc import ABC, abstractmethod
from datetime import datetime
import re
from typing import Optional

from excepciones import (
    ClienteInvalidoError,
    ServicioInvalidoError,
    CalculoInconsistenteError,
    EstadoInvalidoError
)
from logger_config import logger


# =====================================================================
# CLASE ABSTRACTA: ENTIDAD BASE
# =====================================================================
class EntidadBase(ABC):
    """Clase abstracta que define los atributos y comportamientos comunes a todas las entidades del sistema."""

    def __init__(self, identificador: str):
        if not identificador or not str(identificador).strip():
            raise ValueError("El identificador de la entidad no puede ser vacío.")
        self._identificador = str(identificador).strip()
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self) -> str:
        return self._identificador

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Contrato abstracto para obtener una descripción textual de la entidad."""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(ID: {self._identificador})"


# =====================================================================
# CLASE CLIENTE CON ENCAPSULACIÓN ROBUSTA
# =====================================================================
class Cliente(EntidadBase):
    """Entidad Cliente con validaciones estrictas y encapsulación de datos personales."""

    def __init__(self, identificador: str, nombre_completo: str, email: str, telefono: str):
        super().__init__(identificador)
        # Encapsulación mediante setters con validaciones
        self.nombre_completo = nombre_completo
        self.email = email
        self.telefono = telefono

    @property
    def nombre_completo(self) -> str:
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido '{valor}'. Debe contener al menos 3 caracteres.")
        self._nombre_completo = valor.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not valor or not re.match(patron, valor.strip()):
            raise ClienteInvalidoError(f"Formato de correo electrónico inválido: '{valor}'.")
        self._email = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        valor_limpio = re.sub(r"\D", "", str(valor))
        if len(valor_limpio) < 7:
            raise ClienteInvalidoError(f"Teléfono inválido '{valor}'. Debe tener al menos 7 dígitos numéricos.")
        self._telefono = valor_limpio

    def obtener_resumen(self) -> str:
        return f"Cliente: {self._nombre_completo} (ID: {self._identificador}) - Email: {self._email} - Tel: {self._telefono}"


# =====================================================================
# CLASE ABSTRACTA: SERVICIO
# =====================================================================
class Servicio(EntidadBase):
    """Clase abstracta de servicio que establece el contrato polimórfico para los servicios de Software FJ."""

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(identificador)
        if tarifa_base <= 0:
            raise ServicioInvalidoError(f"La tarifa base del servicio debe ser mayor a 0. Valor recibido: {tarifa_base}")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    # -------------------------------------------------------------
    # MÉTODOS ABSTRACTOS POLIMÓRFICOS
    # -------------------------------------------------------------
    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna la ficha técnica y características del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion: float, **kwargs) -> bool:
        """Verifica que la duración y parámetros específicos sean válidos para este tipo de servicio."""
        pass

    # -------------------------------------------------------------
    # MÉTODO SOBRECARGADO (Variantes: base, con descuento, con impuesto/cupon)
    # -------------------------------------------------------------
    def calcular_costo(self, duracion: float, porcentaje_descuento: float = 0.0, porcentaje_impuesto: float = 0.19) -> float:
        """
        Calcula el costo total del servicio con sobrecarga funcional:
        - Variante 1: Solo con duración (aplica impuesto por defecto).
        - Variante 2: Con descuento opcional.
        - Variante 3: Con impuestos personalizados.
        """
        if duracion <= 0:
            raise CalculoInconsistenteError(f"La duración debe ser positiva. Valor recibido: {duracion}")

        if not (0.0 <= porcentaje_descuento <= 0.80):
            raise CalculoInconsistenteError(f"El porcentaje de descuento debe estar entre 0% y 80%. Recibido: {porcentaje_descuento * 100}%")

        if porcentaje_impuesto < 0.0:
            raise CalculoInconsistenteError(f"El porcentaje de impuesto no puede ser negativo: {porcentaje_impuesto * 100}%")

        # Cálculo base dependiente de la especialización
        subtotal_base = self._calcular_subtotal_especifico(duracion)

        # Aplicación de descuento
        monto_descuento = subtotal_base * porcentaje_descuento
        subtotal_con_descuento = subtotal_base - monto_descuento

        # Aplicación de impuesto (IVA)
        total = subtotal_con_descuento * (1.0 + porcentaje_impuesto)
        return round(total, 2)

    @abstractmethod
    def _calcular_subtotal_especifico(self, duracion: float) -> float:
        """Implementación interna del subtotal según el tipo de servicio."""
        pass

    def obtener_resumen(self) -> str:
        return f"{self._nombre} [Base: ${self._tarifa_base:,.2f} | Disp: {self._disponible}]"


# =====================================================================
# SERVICIO DERIVADO 1: RESERVA DE SALAS
# =====================================================================
class ReservaSala(Servicio):
    """Servicio especializado de salas de juntas y auditorios para eventos corporativos."""

    TIPOS_PERMITIDOS = {"REUNIONES", "CAPACITACION", "AUDITORIO"}

    def __init__(self, identificador: str, nombre: str, tarifa_por_hora: float, tipo_sala: str, capacidad_personas: int, incluye_proyector: bool = True):
        super().__init__(identificador, nombre, tarifa_por_hora)
        tipo_normalizado = tipo_sala.strip().upper()
        if tipo_normalizado not in self.TIPOS_PERMITIDOS:
            raise ServicioInvalidoError(f"Tipo de sala '{tipo_sala}' inválido. Tipos permitidos: {self.TIPOS_PERMITIDOS}")
        if capacidad_personas < 2 or capacidad_personas > 200:
            raise ServicioInvalidoError(f"Capacidad de sala fuera de rango permitido (2-200): {capacidad_personas}")

        self._tipo_sala = tipo_normalizado
        self._capacidad_personas = capacidad_personas
        self._incluye_proyector = incluye_proyector

    def validar_parametros(self, duracion: float, **kwargs) -> bool:
        if duracion < 1.0 or duracion > 12.0:
            raise ServicioInvalidoError(f"La duración para salas debe ser entre 1 y 12 horas. Solicitado: {duracion} hrs.")
        return True

    def _calcular_subtotal_especifico(self, duracion: float) -> float:
        costo_horas = self._tarifa_base * duracion
        recargo_equipo = 25000.0 if self._incluye_proyector else 0.0
        return costo_horas + recargo_equipo

    def describir_servicio(self) -> str:
        return (f"Sala [{self._tipo_sala}] '{self._nombre}' | Capacidad: {self._capacidad_personas} personas | "
                f"Proyector: {'Sí' if self._incluye_proyector else 'No'} | Tarifa/h: ${self._tarifa_base:,.2f}")


# =====================================================================
# SERVICIO DERIVADO 2: ALQUILER DE EQUIPOS
# =====================================================================
class AlquilerEquipo(Servicio):
    """Servicio especializado de alquiler de hardware (laptops, servidores, estaciones de trabajo)."""

    def __init__(self, identificador: str, nombre: str, tarifa_por_dia: float, marca_modelo: str, seguro_incluido: bool = True):
        super().__init__(identificador, nombre, tarifa_por_dia)
        if not marca_modelo or len(marca_modelo.strip()) < 2:
            raise ServicioInvalidoError("La marca/modelo del equipo debe ser especificada.")
        self._marca_modelo = marca_modelo.strip()
        self._seguro_incluido = seguro_incluido

    def validar_parametros(self, duracion: float, **kwargs) -> bool:
        # Duración en días para equipos
        if duracion < 1.0 or duracion > 90.0:
            raise ServicioInvalidoError(f"El alquiler de equipos debe ser entre 1 y 90 días. Solicitado: {duracion} días.")
        return True

    def _calcular_subtotal_especifico(self, duracion: float) -> float:
        costo_dias = self._tarifa_base * duracion
        costo_poliza = 15000.0 * duracion if self._seguro_incluido else 0.0
        return costo_dias + costo_poliza

    def describir_servicio(self) -> str:
        return (f"Equipo Hardware '{self._nombre}' ({self._marca_modelo}) | "
                f"Seguro: {'Incluido' if self._seguro_incluido else 'Sin seguro'} | Tarifa/día: ${self._tarifa_base:,.2f}")


# =====================================================================
# SERVICIO DERIVADO 3: ASESORÍA ESPECIALIZADA
# =====================================================================
class AsesoriaEspecializada(Servicio):
    """Servicio de consultoría y asesoría técnica en desarrollo de software y ciberseguridad."""

    NIVELES_PERMITIDOS = {"JUNIOR": 1.0, "SEMI_SENIOR": 1.3, "SENIOR": 1.8}

    def __init__(self, identificador: str, nombre: str, tarifa_base_hora: float, area_conocimiento: str, nivel_consultor: str = "SENIOR"):
        super().__init__(identificador, nombre, tarifa_base_hora)
        nivel_norm = nivel_consultor.strip().upper()
        if nivel_norm not in self.NIVELES_PERMITIDOS:
            raise ServicioInvalidoError(f"Nivel de consultor '{nivel_consultor}' no reconocido. Permitidos: {list(self.NIVELES_PERMITIDOS.keys())}")
        self._area_conocimiento = area_conocimiento.strip()
        self._nivel_consultor = nivel_norm

    def validar_parametros(self, duracion: float, **kwargs) -> bool:
        if duracion < 0.5 or duracion > 40.0:
            raise ServicioInvalidoError(f"La duración de asesoría debe oscilar entre 0.5 y 40 horas. Solicitado: {duracion} hrs.")
        return True

    def _calcular_subtotal_especifico(self, duracion: float) -> float:
        multiplicador = self.NIVELES_PERMITIDOS[self._nivel_consultor]
        return (self._tarifa_base * multiplicador) * duracion

    def describir_servicio(self) -> str:
        return (f"Asesoría en '{self._area_conocimiento}' | Nivel: {self._nivel_consultor} | "
                f"Tarifa base/h: ${self._tarifa_base:,.2f} (Factor: {self.NIVELES_PERMITIDOS[self._nivel_consultor]}x)")


# =====================================================================
# CLASE RESERVA: INTEGRA CLIENTE, SERVICIO, DURACIÓN Y ESTADOS
# =====================================================================
class Reserva(EntidadBase):
    """Representa una reserva de servicio realizada por un cliente en Software FJ."""

    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"
    ESTADO_PROCESADA = "PROCESADA"

    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion: float, descuento: float = 0.0):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente):
            raise ClienteInvalidoError("La reserva requiere un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ServicioInvalidoError("La reserva requiere un objeto Servicio válido.")

        # Validaciones de reglas de negocio
        servicio.validar_parametros(duracion)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._descuento = descuento
        self._estado = self.ESTADO_PENDIENTE
        self._costo_total = servicio.calcular_costo(duracion, porcentaje_descuento=descuento)

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    @property
    def duracion(self) -> float:
        return self._duracion

    def confirmar(self):
        """Confirma la reserva pasando de PENDIENTE a CONFIRMADA."""
        if self._estado != self.ESTADO_PENDIENTE:
            raise EstadoInvalidoError(f"No se puede confirmar la reserva '{self._identificador}' en estado actual: '{self._estado}'. Debe estar PENDIENTE.")
        if not self._servicio.disponible:
            raise ServicioInvalidoError(f"No se puede confirmar: el servicio '{self._servicio.nombre}' no se encuentra disponible actualmente.")
        self._estado = self.ESTADO_CONFIRMADA
        logger.info(f"Reserva {self._identificador} ha sido CONFIRMADA con éxito.")

    def cancelar(self, motivo: str = "Solicitud del cliente"):
        """Cancela la reserva."""
        if self._estado in (self.ESTADO_CANCELADA, self.ESTADO_PROCESADA):
            raise EstadoInvalidoError(f"Operación inválida: La reserva '{self._identificador}' ya se encuentra {self._estado} y no puede cancelarse.")
        estado_previo = self._estado
        self._estado = self.ESTADO_CANCELADA
        logger.warning(f"Reserva {self._identificador} cancelada (Estado previo: {estado_previo}). Motivo: {motivo}")

    def procesar(self):
        """Procesa y da por completada la reserva."""
        if self._estado != self.ESTADO_CONFIRMADA:
            raise EstadoInvalidoError(f"No se puede procesar la reserva '{self._identificador}'. Se requiere estado CONFIRMADA (Estado actual: {self._estado}).")
        self._estado = self.ESTADO_PROCESADA
        logger.info(f"Reserva {self._identificador} PROCESADA y ejecutada satisfactoriamente.")

    def obtener_resumen(self) -> str:
        return (f"Reserva [{self._identificador}] Estado: {self._estado} | Cliente: {self._cliente.nombre_completo} | "
                f"Servicio: {self._servicio.nombre} ({self._duracion} unidades) | Total: ${self._costo_total:,.2f}")
