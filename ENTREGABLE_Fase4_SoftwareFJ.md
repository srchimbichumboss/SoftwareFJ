# Informe Final – Fase 4: Manejo de Excepciones y Programación Orientada a Objetos
## Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ
### Curso: Programación (Código: 213023)

---

### PORTADA

**Universidad Nacional Abierta y a Distancia – UNAD**  
**Vicerrectoría Académica y de Investigación – VIACI**  
**Escuela de Ciencias Básicas, Tecnología e Ingeniería – ECBTI**  
**Programa:** Ingeniería de Sistemas  
**Curso:** Programación (Código 213023)  
**Fase:** Fase 4 – Manejo de Excepciones  
**Número de Grupo:** [Número de Grupo, ej. 213023_XX]  

**Integrantes del Equipo de Trabajo:**
1. **[Nombre Completo Integrante 1 - Líder / srchimbichumboss]** - Código: [Número Documento]
2. **[Nombre Completo Integrante 2]** - Código: [Número Documento]
3. **[Nombre Completo Integrante 3]** - Código: [Número Documento]
4. **[Nombre Completo Integrante 4]** - Código: [Número Documento]
5. **[Nombre Completo Integrante 5]** - Código: [Número Documento]

**Tutor de Curso:** [Nombre del Tutor Asignado]  
**Fecha de Entrega:** Noviembre de 2026  

---

### 1. INTRODUCCIÓN

En la ingeniería de software moderna, la estabilidad y la robustez de las aplicaciones representan atributos de calidad tan fundamentales como la lógica de negocio misma. Los entornos de producción demandan arquitecturas capaces de mitigar fallos en tiempo de ejecución, procesar entradas erróneas y recuperarse de estados anómalos sin interrumpir la operación del sistema. La Programación Orientada a Objetos (POO), combinada con una política sistemática de gestión de excepciones, proporciona las herramientas estructurales para alcanzar dicho nivel de resiliencia.

El presente informe expone el diseño, desarrollo e integración del sistema integral de gestión para la empresa **Software FJ**, especializada en la oferta de servicios corporativos tales como reservas de salas, alquiler de equipos tecnológicos y asesorías especializadas en arquitectura y ciberseguridad. En estricto cumplimiento con la guía de actividades de la Fase 4, la solución se concibió bajo una arquitectura en capas en lenguaje **Python**, prescindiendo de motores de bases de datos relacionales y sustentando la persistencia y trazabilidad de eventos exclusivamente en estructuras de objetos en memoria y un subsistema de auditoría basado en archivos de logs (`software_fj.log`).

El núcleo de la solución articula los pilares de la POO: **abstracción** mediante clases base abstractas, **encapsulación** rigurosa con propiedades validadas, **herencia y polimorfismo** en la especialización de servicios con cálculo dinámico de costos sobrecargados, y un **manejo avanzado de excepciones** estructurado en jerarquías personalizadas, bloques de captura defensiva (`try/except/else/finally`), encadenamiento causal de errores (`raise ... from`) y registro persistente de logs. Finalmente, se evidencia el trabajo colaborativo del equipo mediante el uso profesional de **GitHub**, documentando ramas, pull requests e issues asignados equitativamente.

---

### 2. OBJETIVOS

#### 2.1 Objetivo General
Desarrollar e implementar un sistema integral orientado a objetos para la gestión de clientes, servicios y reservas de la empresa Software FJ, aplicando principios de abstracción, herencia, polimorfismo, encapsulación y manejo robusto de excepciones para garantizar la estabilidad y continuidad operativa del sistema en un entorno sin base de datos.

#### 2.2 Objetivos Específicos
1. Diseñar una jerarquía de clases sólida fundamentada en clases abstractas (`EntidadBase`, `Servicio`) y clases derivadas (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`, `Cliente`, `Reserva`).
2. Implementar mecanismos de encapsulación estricta a través de decoradores `@property` y validadores en setters para blindar la integridad de los datos personales y parámetros de negocio.
3. Construir una jerarquía de excepciones personalizadas derivadas de `Exception` para clasificar y gestionar de forma semántica los errores de datos, servicios, transiciones de estado y cálculos financieros.
4. Aplicar de forma exhaustiva las estructuras de control `try/except`, `try/except/else`, `try/finally` y encadenamiento de excepciones (`raise ... from err`), asegurando que la aplicación continúe ejecutándose ante cualquier fallo.
5. Configurar un subsistema de auditoría con la biblioteca estándar `logging` que almacene eventos informativos, advertencias y excepciones en el archivo físico `software_fj.log`.
6. Diseñar y ejecutar una batería de al menos 10 simulaciones (válidas e inválidas) que evidencien la tolerancia a fallos del sistema.
7. Gestionar el ciclo de vida del desarrollo en un repositorio de GitHub bajo estándares profesionales: ramas funcionales por integrante, commits semánticos, pull requests e issues.

---

### 3. ENLACE AL REPOSITORIO DE TRABAJO COLABORATIVO EN GITHUB

El repositorio oficial del proyecto, con su historial completo de ramas por integrante, commits estructurados, pull requests y gestión de issues, se encuentra publicado y accesible de forma pública:

🔗 **Repositorio GitHub:** [https://github.com/srchimbichumboss/SoftwareFJ](https://github.com/srchimbichumboss/SoftwareFJ)  
🔗 **Gestión de Issues:** [https://github.com/srchimbichumboss/SoftwareFJ/issues](https://github.com/srchimbichumboss/SoftwareFJ/issues)

---

### 4. ARQUITECTURA DEL SISTEMA Y DISEÑO ORIENTADO A OBJETOS

#### 4.1 Principios de POO Implementados

```
               +----------------------------------+
               |        EntidadBase (ABC)         |
               +----------------------------------+
               | - _identificador: str            |
               | - _fecha_creacion: datetime      |
               +----------------------------------+
               | + obtener_resumen()* : str       |
               +----------------------------------+
                                 ^
          +----------------------+----------------------+
          |                                             |
+----------------------------------+          +----------------------------------+
|             Cliente              |          |          Servicio (ABC)          |
+----------------------------------+          +----------------------------------+
| - _nombre_completo: str          |          | - _nombre: str                   |
| - _email: str                    |          | - _tarifa_base: float            |
| - _telefono: str                 |          | - _disponible: bool              |
+----------------------------------+          +----------------------------------+
| + nombre_completo (getter/setter)|          | + describir_servicio()* : str    |
| + email (getter/setter)          |          | + validar_parametros()* : bool   |
| + telefono (getter/setter)       |          | + calcular_costo() : float       |
+----------------------------------+          +----------------------------------+
                                                                ^
                     +-------------------+----------------------+--------------------+
                     |                   |                                           |
+-----------------------------+ +-----------------------------+ +----------------------------------+
|        ReservaSala          | |       AlquilerEquipo        | |      AsesoriaEspecializada       |
+-----------------------------+ +-----------------------------+ +----------------------------------+
| - _tipo_sala: str           | | - _marca_modelo: str        | | - _area_conocimiento: str        |
| - _capacidad_personas: int  | | - _seguro_incluido: bool    | | - _nivel_consultor: str          |
| - _incluye_proyector: bool  | +-----------------------------+ +----------------------------------+
+-----------------------------+
```

1. **Abstracción:** Implementada a través del módulo `abc` de Python (`ABC`, `@abstractmethod`). Las clases `EntidadBase` y `Servicio` no pueden ser instanciadas directamente; definen contratos obligatorios (`obtener_resumen`, `describir_servicio`, `validar_parametros`, `_calcular_subtotal_especifico`) que garantizan homogeneidad en todas las entidades.
2. **Encapsulación:** En la clase `Cliente`, los atributos `_nombre_completo`, `_email` y `_telefono` están protegidos. La modificación de estos atributos solo es posible mediante setters que validan longitudes mínimas, expresiones regulares para correos electrónicos válidos y comprobación de dígitos numéricos, disparando `ClienteInvalidoError` si las reglas no se cumplen.
3. **Herencia y Polimorfismo:** Tres clases especializadas heredan de `Servicio`:
   - `ReservaSala`: Valida duración en horas (1 a 12h), capacidad (2 a 200 personas) y calcula recargos por uso de proyector.
   - `AlquilerEquipo`: Valida duraciones en días (1 a 90 días) y gestiona el costo diario sumado a la póliza de seguro de hardware.
   - `AsesoriaEspecializada`: Aplica factores multiplicadores según el rango del consultor (`JUNIOR` 1.0x, `SEMI_SENIOR` 1.3x, `SENIOR` 1.8x).
4. **Sobrecarga de Métodos:** El método `calcular_costo(duracion, porcentaje_descuento=0.0, porcentaje_impuesto=0.19)` implementa sobrecarga mediante argumentos por defecto e inspección de parámetros opcionales, permitiendo invocarlo con solo la duración, con porcentajes de descuento comercial o con impuestos personalizados.
5. **Entidad Agregadora (Reserva):** Integra un cliente, un servicio polimórfico, la duración y la máquina de estados finita:
   $$\text{PENDIENTE} \longrightarrow \text{CONFIRMADA} \longrightarrow \text{PROCESADA}$$
   $$\text{PENDIENTE / CONFIRMADA} \longrightarrow \text{CANCELADA}$$
   Cualquier transición ilegal (por ejemplo, intentar cancelar una reserva ya procesada o confirmar una no disponible) es interceptada por `EstadoInvalidoError`.

---

### 5. MANEJO ROBUSTO DE EXCEPCIONES Y REGISTRO DE LOGS

#### 5.1 Jerarquía de Excepciones Personalizadas (`excepciones.py`)
Se construyó un árbol semántico de excepciones para tipificar cualquier anomalía del sistema:

```
Exception (Python Built-in)
   └── SoftwareFJError (Clase base de dominio)
         ├── ClienteInvalidoError (Errores en sintaxis o datos del cliente)
         ├── ServicioInvalidoError (Parámetros o tipos inválidos en servicios)
         ├── ServicioNoDisponibleError (Servicio fuera de servicio o agotado)
         ├── CalculoInconsistenteError (Duraciones negativas o descuentos excesivos)
         └── ReservaInvalidaError (Fallos generales en el proceso de reserva)
               └── EstadoInvalidoError (Transiciones de estado prohibidas)
```

#### 5.2 Estructuras de Control Avanzadas

- **Uso de `try / except / else` (`gestor_sistema.py`):**
  Al registrar clientes y crear reservas, el bloque `else` garantiza que las colecciones en memoria solo se actualicen si la instanciación y las validaciones se ejecutaron libres de error:
  ```python
  try:
      nuevo_cliente = Cliente(id, nombre, email, telefono)
  except ClienteInvalidoError as err:
      logger.error(f"Fallo al registrar cliente: {err}")
  else:
      self._clientes[id] = nuevo_cliente
      logger.info(f"Cliente registrado exitosamente: {nuevo_cliente}")
  ```

- **Uso de `try / finally` (`gestor_sistema.py`):**
  Implementado en los métodos de confirmación, cancelación y creación de reservas para garantizar la ejecución de rutinas de auditoría y liberación de contexto independientemente de si la operación tuvo éxito o disparó excepciones:
  ```python
  try:
      # Lógica de operación
  finally:
      logger.debug(f"[AUDITORÍA FINALLY] Proceso concluido para reserva: {id_reserva}")
  ```

- **Encadenamiento de Excepciones (`raise ... from err`):**
  Demostrado en el método `registrar_servicio()`. Cuando un objeto espurio es ingresado al catálogo, se captura la excepción interna de tipo `TypeError` y se reemite una excepción semántica de dominio `ServicioInvalidoError`, conservando la causa raíz original mediante `__cause__`:
  ```python
  except TypeError as tipo_err:
      raise ServicioInvalidoError(f"Incompatibilidad de tipo: {tipo_err}") from tipo_err
  ```

#### 5.3 Configuración del Sistema de Logging (`logger_config.py`)
Se configuró un logger dual que canaliza eventos en formato estructurado a la consola y al archivo permanente `software_fj.log`:
- Formato: `%(asctime)s | %(levelname)-8s | [%(name)s] [%(filename)s:%(lineno)d] | %(message)s`
- Niveles: `DEBUG` (trazas de auditoría), `INFO` (operaciones exitosas), `WARNING` (rechazos de negocio controlados) y `ERROR / CRITICAL` (excepciones capturadas y fallos de tipo).

---

### 6. BATERÍA DE SIMULACIONES Y VALIDACIÓN DE ESTABILIDAD

Se desarrollaron y ejecutaron **11 simulaciones completas** que ponen a prueba todas las capas del sistema. En ningún caso la aplicación colapsó; todos los errores fueron interceptados y documentados en logs.

#### 6.1 Matriz de Casos de Prueba Ejecutados

| # | Escenario de Prueba | Tipo | Entrada / Acción | Excepción / Resultado Gestionado | Estado del Sistema |
|---|---|---|---|---|---|
| **1** | Registro de Cliente Válido | Válido | ID: `CLI-001`, Tel: `3104567890`, Correo: `carlos.mendoza@email.com` | `Cliente` creado exitosamente y almacenado en memoria. | **Estable** |
| **2** | Registro con Email Inválido | Inválido | Email: `correo_sin_arroba_ni_dominio` | `ClienteInvalidoError` capturada. Rechazo seguro sin detención. | **Estable** |
| **3** | Registro con Teléfono Inválido | Inválido | Teléfono: `123` (< 7 dígitos) | `ClienteInvalidoError` capturada y registrada en log. | **Estable** |
| **4** | Registro de 3 Servicios Polimórficos | Válido | Sala Auditorio, Laptop ThinkPad P16 y Asesoría Cloud Senior | Tres servicios especializados agregados al catálogo. | **Estable** |
| **5** | Creación de Servicio con Parámetro Inválido | Inválido | `ReservaSala` con capacidad = `999` personas | `ServicioInvalidoError` (Rango legal: 2-200). Objeto no instanciado. | **Estable** |
| **6** | Registro de Objeto No Servicio (Encadenamiento) | Inválido | String arbitrario enviado a `registrar_servicio()` | **Encadenamiento:** `TypeError` $\rightarrow$ `ServicioInvalidoError` (`raise from`). | **Estable** |
| **7** | Creación de Reserva Válida con Sobrecarga | Válido | Sala 4 horas, descuento comercial del 10% | Reserva `RES-001` creada en estado `PENDIENTE`. Total: \$219,555. | **Estable** |
| **8** | Reserva con Duración Fuera de Regla | Inválido | Sala por `24.0` horas (Máximo permitido: 12h) | `ServicioInvalidoError` interceptado en `crear_reserva()`. | **Estable** |
| **9** | Reserva de Servicio NO Disponible | Inválido | Equipo con `disponible = False` | `ServicioNoDisponibleError` capturada. Retorna `None`. | **Estable** |
| **10** | Transición Ilegal de Estado | Inválido | Cancelar reserva `RES-001` tras haber sido `PROCESADA` | `EstadoInvalidoError` capturada; operación abortada de forma segura. | **Estable** |
| **11** | Cancelación Válida en Reserva Pendiente | Válido | Cancelar reserva `RES-004` en estado `PENDIENTE` | Transición exitosa a `CANCELADA`. Motivo registrado en log. | **Estable** |

#### 6.2 Fragmento de Trazas del Archivo de Logs (`software_fj.log`)
```text
2026-11-22 17:49:28 | INFO     | [SoftwareFJ] [gestor_sistema.py:32] | Sistema de Gestión Software FJ inicializado en memoria con éxito.
2026-11-22 17:49:28 | INFO     | [SoftwareFJ] [gestor_sistema.py:62] | Cliente registrado exitosamente: Cliente: Carlos Mendoza Gómez (ID: CLI-001) - Email: carlos.mendoza@email.com - Tel: 3104567890
2026-11-22 17:49:28 | ERROR    | [SoftwareFJ] [gestor_sistema.py:54] | Fallo al registrar cliente [CLI-002]: [ERR_CLIENTE_INVALIDO] Formato de correo electrónico inválido: 'correo_sin_arroba_ni_dominio'.
2026-11-22 17:49:28 | ERROR    | [SoftwareFJ] [gestor_sistema.py:54] | Fallo al registrar cliente [CLI-003]: [ERR_CLIENTE_INVALIDO] Teléfono inválido '123'. Debe tener al menos 7 dígitos numéricos.
2026-11-22 17:49:28 | INFO     | [SoftwareFJ] [gestor_sistema.py:82] | Servicio incorporado al catálogo: Sala [AUDITORIO] 'Sala Magna Innovación' | Capacidad: 50 personas | Proyector: Sí | Tarifa/h: $45,000.00
2026-11-22 17:49:28 | INFO     | [SoftwareFJ] [gestor_sistema.py:82] | Servicio incorporado al catálogo: Equipo Hardware 'Workstation Portátil ThinkPad P16' (Lenovo ThinkPad P16 Gen 2 - 64GB RAM) | Seguro: Incluido | Tarifa/día: $85,000.00
2026-11-22 17:49:28 | INFO     | [SoftwareFJ] [gestor_sistema.py:82] | Servicio incorporado al catálogo: Asesoría en 'Cloud & DevOps' | Nivel: SENIOR | Tarifa base/h: $120,000.00 (Factor: 1.8x)
2026-11-22 17:49:28 | ERROR    | [SoftwareFJ] [simulaciones.py:107] | Captura en capa de simulación: [ERR_SERVICIO_INVALIDO] Capacidad de sala fuera de rango permitido (2-200): 999
2026-11-22 17:49:28 | ERROR    | [SoftwareFJ] [gestor_sistema.py:90] | Excepción encadenada capturada: [ERR_SERVICIO_INVALIDO] Incompatibilidad de tipo en servicio: El objeto proporcionado (<class 'str'>) no hereda de la clase abstracta Servicio. | Causa raíz: El objeto proporcionado (<class 'str'>) no hereda de la clase abstracta Servicio.
2026-11-22 17:49:28 | INFO     | [SoftwareFJ] [gestor_sistema.py:147] | Reserva creada con éxito: Reserva [RES-001] Estado: PENDIENTE | Cliente: Carlos Mendoza Gómez | Servicio: Sala Magna Innovación (4.0 unidades) | Total: $219,555.00
2026-11-22 17:49:28 | WARNING  | [SoftwareFJ] [gestor_sistema.py:135] | Rechazo controlado en creación de reserva [RES-002-ERR]: [ERR_SERVICIO_INVALIDO] La duración para salas debe ser entre 1 y 12 horas. Solicitado: 24.0 hrs.
2026-11-22 17:49:28 | WARNING  | [SoftwareFJ] [gestor_sistema.py:135] | Rechazo controlado en creación de reserva [RES-003-ERR]: [ERR_SERVICIO_NO_DISPONIBLE] El servicio 'Workstation Portátil ThinkPad P16' no se encuentra disponible para nuevas reservas.
2026-11-22 17:49:28 | INFO     | [SoftwareFJ] [modelos.py:333] | Reserva RES-001 ha sido CONFIRMADA con éxito.
2026-11-22 17:49:28 | INFO     | [SoftwareFJ] [modelos.py:348] | Reserva RES-001 PROCESADA y ejecutada satisfactoriamente.
2026-11-22 17:49:28 | ERROR    | [SoftwareFJ] [gestor_sistema.py:185] | Transición prohibida al cancelar: [ERR_ESTADO_TRANSICION_ILEGAL] Operación inválida: La reserva 'RES-001' ya se encuentra PROCESADA y no puede cancelarse.
2026-11-22 17:49:28 | INFO     | [SoftwareFJ] [gestor_sistema.py:147] | Reserva creada con éxito: Reserva [RES-004] Estado: PENDIENTE | Cliente: Carlos Mendoza Gómez | Servicio: Consultoría en Arquitectura Cloud AWS (3.0 unidades) | Total: $732,564.00
2026-11-22 17:49:28 | WARNING  | [SoftwareFJ] [modelos.py:341] | Reserva RES-004 cancelada (Estado previo: PENDIENTE). Motivo: Reprogramación por cliente
```

---

### 7. EVIDENCIAS DE TRABAJO COLABORATIVO Y GITHUB PROFESIONAL

En concordancia con el Criterio 4 de la rúbrica de evaluación (30 puntos), el repositorio evidencia una distribución equitativa de tareas, ramas independientes por estudiante, commits descriptivos, pull requests e issues:

#### 7.1 Distribución de Roles, Ramas e Issues

| Integrante | Rol en el Proyecto | Rama de Trabajo | Issue Asignado |
|---|---|---|---|
| **Integrante 1** | Arquitecto de Excepciones y Logging | `developer/integrante-1-excepciones` | [Issue #1](https://github.com/srchimbichumboss/SoftwareFJ/issues/1): Diseño de excepciones personalizadas y logging |
| **Integrante 2** | Modelador de Entidades Base | `developer/integrante-2-modelos-base` | [Issue #2](https://github.com/srchimbichumboss/SoftwareFJ/issues/2): Clases abstractas EntidadBase y encapsulación Cliente |
| **Integrante 3** | Desarrollador de Servicios Polimórficos | `developer/integrante-3-servicios-polimorficos` | [Issue #3](https://github.com/srchimbichumboss/SoftwareFJ/issues/3): Especialización polimórfica y sobrecarga |
| **Integrante 4** | Ingeniero de Control y Reservas | `developer/integrante-4-gestor-reservas` | [Issue #4](https://github.com/srchimbichumboss/SoftwareFJ/issues/4): Gestor central con try/except/else/finally |
| **Integrante 5 (Líder)** | Aseguramiento de Calidad y Pruebas | `developer/integrante-5-simulaciones-logs` | [Issue #5](https://github.com/srchimbichumboss/SoftwareFJ/issues/5): Batería de simulaciones, consola y README |

#### 7.2 Pull Requests Integrados en Rama `main`
- **PR #1:** `developer/integrante-1-excepciones` $\rightarrow$ `main` (Sistema de Excepciones y Logging).
- **PR #2:** `developer/integrante-2-modelos-base` $\rightarrow$ `main` (Entidades y Encapsulación de Clientes).
- **PR #3:** `developer/integrante-3-servicios-polimorficos` $\rightarrow$ `main` (Servicios Polimórficos y Tarifas).
- **PR #4:** `developer/integrante-4-gestor-reservas` $\rightarrow$ `main` (Lógica de Negocio y Flujo de Reservas).
- **PR #5:** `developer/integrante-5-simulaciones-logs` $\rightarrow$ `main` (Suite de Pruebas y Documentación Final).

---

### 8. CONCLUSIONES

1. **La encapsulación y las excepciones personalizadas garantizan la consistencia de los datos:** Al delegar la validación de integridad a los setters y levantar excepciones de negocio tipificadas (`ClienteInvalidoError`, `ServicioInvalidoError`), se impide que objetos inconsistentes entren al ciclo de vida del sistema, manteniendo la pureza de la memoria sin requerir restricciones foráneas de bases de datos.
2. **El polimorfismo reduce el acoplamiento y facilita la extensibilidad:** La definición de un contrato abstracto en la clase `Servicio` permite que el motor de reservas gestione salas, equipos y asesorías de forma unificada. Para incorporar un nuevo servicio en el futuro (ej. licencias de software), solo se requiere extender la clase abstracta sin alterar el controlador `SistemaGestionSoftwareFJ`.
3. **El encadenamiento de excepciones preserva la trazabilidad forense:** El empleo de la sintaxis `raise DominioError from err_interno` permite transformar fallos de infraestructura o de tipo en excepciones claras para el usuario final, manteniendo intacto el registro de la causa raíz (`__cause__`) en el archivo de logs para propósitos de depuración técnica.
4. **La estructura `try/except/else/finally` asegura un ciclo de vida limpio:** El bloque `else` previene estados parciales o corrupciones en las colecciones en memoria, mientras que `finally` garantiza la ejecución incondicional de rutinas de auditoría y liberación de recursos, aportando alta confiabilidad a la arquitectura.
5. **El control de versiones estructurado es indispensable en proyectos colaborativos:** La metodología de Git basada en ramas por funcionalidad, convenciones de commits semánticos y pull requests minimiza colisiones de código y permite una trazabilidad transparente del aporte individual de cada estudiante, elevando el estándar de entrega a nivel profesional.

---

### 9. REFERENCIAS BIBLIOGRÁFICAS (Normas APA 7ma Edición)

- Deitel, P. J., & Deitel, H. M. (2020). *Python for programmers with big data and artificial intelligence*. Pearson.
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design patterns: Elements of reusable object-oriented software*. Addison-Wesley.
- Lutz, M. (2013). *Learning Python* (5th ed.). O'Reilly Media.
- Python Software Foundation. (2024). *Errors and exceptions — Python 3.12 documentation*. Python.org. https://docs.python.org/3/tutorial/errors.html
- Python Software Foundation. (2024). *Logging facility for Python*. Python.org. https://docs.python.org/3/library/logging.html
- Universidad Nacional Abierta y a Distancia. (2026). *Guía de actividades y rúbrica de evaluación – Fase 4: Manejo de excepciones (Curso Programación 213023)*. Vicerrectoría Académica y de Investigación (VIACI).
