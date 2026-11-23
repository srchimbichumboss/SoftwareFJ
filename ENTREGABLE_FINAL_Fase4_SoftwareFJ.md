# Sistema De Gestión Software Y Fundamentos De Arquitectura En Python
## Fase 4 - Programación Orientada A Objetos (POO)

**Autor Único:** Thomas Fernando Mengual Arciniegas  
**Asesor / Tutor:** Ángel Alberto Varón Quimbayo  
**Universidad Nacional Abierta y a Distancia (UNAD)**  
**Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)**  
**Programa:** Ingeniería de Sistemas  
**Año:** 2026  

---

### TABLA DE CONTENIDO
1. Introducción
2. Justificación
3. Objetivos  
   3.1. Objetivo General  
   3.2. Objetivos Específicos  
4. Desarrollo del Sistema Software FJ (POO)  
   4.1. Diseño de Clases y Encapsulación  
   4.2. Servicios Polimórficos y Tarifas  
   4.3. Manejo de Excepciones y Encadenamiento  
   4.4. Archivo de Logs y Trazabilidad  
   4.5. Batería de 11 Simulaciones  
5. Repositorio y Control de Versiones en GitHub  
6. Conclusiones  
7. Referencias Bibliográficas  

---

### Resumen
El presente informe consolida el desarrollo integral, en modalidad 100% individual. El proyecto aborda la confluencia entre la ingeniería de software orientada a objetos (POO) y los fundamentos de la arquitectura de computadores, utilizando el lenguaje de programación Python como entorno moderno de implementación. Se presenta la arquitectura completa del sistema corporativo Software FJ para la gestión de clientes, servicios especializados (salas de conferencias, alquiler tecnológico y asesorías) y reservas, aplicando abstracción rigurosa mediante módulos nativos (abc), encapsulación con validación de estados (@property/@setter), polimorfismo en el cálculo tarifario con sobrecarga flexible, jerarquía propia de excepciones con encadenamiento explícito (raise ... from) y trazabilidad persistente mediante logging dual en consola y archivo de auditoría. Adicionalmente, se presenta el modelamiento en Python de los principios de Von Neumann (registros de CPU, banderas de acarreo/Carry Flag, operaciones lógicas bit a bit y ciclos de instrucción), demostrando cómo los conceptos de arquitectura se manifiestan en entornos de desarrollo modernos.

### Abstract
This report consolidates comprehensive development, in a 100% individual modality. The project addresses the convergence between object-oriented software engineering (OOP) and the fundamentals of computer architecture, using the Python programming language as a modern implementation environment. The complete architecture of the corporate system FJ Software is presented for client management, specialized services (conference rooms, technology rental, and consulting), and reservations, applying rigorous abstraction through native modules (abc), encapsulation with state validation (@property/@setter), polymorphism in tariff calculation with flexible overload, its own hierarchy of exceptions with explicit chaining (raise ... from), and persistent traceability through dual logging in console and audit file. Additionally, Python modeling of Von Neumann's principles (CPU registers, carry flags/Carry Flags, bitwise logical operations, and instruction cycles) is presented, demonstrating how architectural concepts manifest themselves in modern development environments.

---

### Introducción
La comprensión integral de los sistemas computacionales exige el dominio tanto de las capas de abstracción de alto nivel (paradigma orientado a objetos) como de los mecanismos fundamentales mediante los cuales la CPU y la memoria procesan la información. En este informe, concebido y ejecutado en su totalidad por un único autor.

---

### Objetivos

#### Objetivo General
Desarrollar una solución robusta y profesional en Python aplicando los principios de la Programación Orientada a Objetos (POO), manejo integral de excepciones y auditoría persistente, complementado con el análisis y modelamiento de la arquitectura de computadores.

#### Objetivos Específicos
- Implementar abstracción y contratos estrictos con el módulo abc (EntidadBase, Servicio).
- Garantizar la integridad de datos mediante encapsulación y validación en setters (@property) para la clase Cliente.
- Desarrollar polimorfismo y sobrecarga tarifaria en tres servicios: ReservaSala, AlquilerEquipo y Asesoria Especializada.
- Diseñar una jerarquía orientada a objetos de excepciones personalizadas con manejo multicapa y encadenamiento (raise ... from).
- Configurar logging dual en software_fj.log y consola para auditoría permanente de operaciones y errores.
- Ejecutar y documentar 11 simulaciones automatizadas de prueba demostrando estabilidad total del sistema.
- Modelar en Python los fundamentos de hardware: registros de CPU, control del Carry Flag en operaciones aritméticas y compuertas lógicas bit a bit.

---

### Modelamiento De Arquitectura De Computadores En Python

#### Planteamiento del problema
El hardware de un computador opera bajo el modelo clásico de Von Neumann: Unidad de Control (CU), Unidad Aritmeticológica (ALU), registros internos de alta velocidad, memoria principal y buses de interconexión. A continuación, se demuestra cómo estos conceptos de bajo nivel se traducen y comprenden directamente mediante la semántica de Python:

#### Operaciones Aritméticas y Control de Carry Flag
En la ALU, al sumar o restar dos operandos en un registro de 8 bits (capacidad 00h a FFh / 0 a 255), si el resultado excede el ancho de palabra, el hardware enciende la bandera de acarreo (Carry Flag = 1). En Python, este principio se modela rigurosamente:

```python
def suma_hex_con_carry(a_hex: int, b_hex: int):
    suma = a_hex + b_hex
    carry = 1 if suma > 0xFF else 0
    resultado_8bits = suma & 0xFF
    print(f'Operacion: {a_hex:02X}h + {b_hex:02X}h = {resultado_8bits:02X}h | Carry Flag: {carry}')
    return resultado_8bits, carry

# Ejemplo: FFh + 01h = 100h (desborda 8 bits -> resultado 00h con Carry = 1)
suma_hex_con_carry(0xFF, 0x01)
```

---

### Sistema Integral Software FJ (POO)
Software FJ es una solución corporativa orientada a objetos para la gestión de reservas empresariales. El autor diseñó el sistema bajo una arquitectura modular limpia compuesta por 6 módulos especializados:

| Módulo | Responsabilidad Principal | Mecanismos POO |
|---|---|---|
| `excepciones.py` | Jerarquía de excepciones de dominio | Herencia de Exception, clases personalizadas |
| `logger_config.py` | Subsistema de logging persistente | Dual-handler: Consola + `software_fj.log` |
| `modelos.py` | Entidades, reglas de negocio y cálculo | `abc.ABC`, `@abstractmethod`, `@property`, polimorfismo |
| `gestor_sistema.py` | Controlador de reservas y transiciones | `try/except/else/finally`, `raise ... from` |
| `simulaciones.py` | Batería automatizada de pruebas | 11 casos de prueba (válidos e inválidos) |
| `main.py` | Punto de entrada y CLI interactivo | Menú navegable por consola y flags |

---

### Batería De 11 Simulaciones Automatizadas
Se ejecutó la suite de pruebas mediante el comando `python main.py --simulacion`, obteniendo 100% de éxito y estabilidad:

| # | Caso de Prueba | Tipo | Resultado Obtenido |
|---|---|---|---|
| 1 | Registro válido de cliente corporativo | Válido | Cliente registrado con UUID y log INFO |
| 2 | Cliente con email inválido (sin @) | Inválido | ClienteInvalidoError capturada con éxito |
| 3 | Cliente con teléfono menor a 7 dígitos | Inválido | ClienteInvalidoError capturada |
| 4 | Creación de 3 servicios polimórficos | Válido | Sala, Equipo y Asesoría registrados |
| 5 | Sala con capacidad fuera de rango (999) | Inválido | ServicioInvalidoError (rango 2-200) |
| 6 | Inyección de objeto espurio (no Servicio) | Inválido | Encadenamiento: TypeError -> ServicioInvalidoError |
| 7 | Reserva con descuento corporativo (10%) | Válido | Cálculo preciso de subtotal, descuento e IVA |
| 8 | Reserva de sala excediendo 12 horas | Inválido | ServicioInvalidoError rechazado controladamente |
| 9 | Reserva de servicio no disponible | Inválido | ServicioNoDisponibleError capturada |
| 10 | Cancelación sobre reserva ya PROCESADA | Inválido | EstadoInvalidoError (transición prohibida) |
| 11 | Cancelación legítima de reserva PENDIENTE | Válido | Estado cambiado a CANCELADA y log registrado |

---

### Repositorio GitHub Y Trabajo Individual
**Enlace oficial:** [https://github.com/srchimbichumboss/SoftwareFJ](https://github.com/srchimbichumboss/SoftwareFJ)  
Desarrollo y entrega 100% individual por Thomas Fernando Mengual Arciniegas.

---

### Conclusiones
1. La articulación de conceptos de arquitectura de computadores mediante Python demuestra que las reglas de bajo nivel (carry, desbordamiento, máscaras bitwise) son los cimientos sobre los cuales se construyen los lenguajes de alto nivel.
2. La arquitectura modular de Software FJ garantiza un código desacoplado, mantenible y extensible, con un manejo de excepciones que previene caídas inesperadas.
3. El desarrollo individual permitió asegurar una coherencia técnica total en cada archivo del sistema.

---

### Referencias Bibliográficas
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.
- Hamacher, C., Vranesic, Z., Zaky, S., & Manjikian, N. (2012). Computer Organization and Embedded Systems (6th ed.). McGraw-Hill Education.
- Lutz, M. (2013). Learning Python: Powerful Object-Oriented Programming (5th ed.). O'Reilly Media.
- Patterson, D. A., & Hennessy, J. L. (2020). Computer Organization and Design: The Hardware/Software Interface (6th ed.). Morgan Kaufmann.
- Python Software Foundation. (2024). Python 3.12 Documentation (abc, logging, exceptions). https://docs.python.org/3/
- Universidad Nacional Abierta y a Distancia. (2026). Guía de actividades y rúbrica de evaluación - Fase 4. UNAD.
