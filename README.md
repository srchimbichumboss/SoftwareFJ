# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

**Universidad Nacional Abierta y a Distancia (UNAD)**  
**Curso:** Programación (Código 213023) - **Fase 4**  
**Escuela:** Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)  
**Programa:** Ingeniería de Sistemas  

---

## 📌 1. Descripción General del Proyecto

Software FJ es una solución orientada a objetos en **Python** diseñada para gestionar clientes, servicios (salas, alquiler de equipos y asesorías especializadas) y reservas corporativas sin utilizar motores de bases de datos relacionales, manteniendo la persistencia y auditoría exclusivamente a través de estructuras en memoria y un sistema de logging en archivo.

El proyecto implementa de manera estricta los requerimientos de la **Fase 4 (Rúbrica de 150 puntos)**:
- **Abstracción**: Clases abstractas `EntidadBase` y `Servicio` implementadas con el módulo `abc` de Python (`ABC`, `@abstractmethod`).
- **Encapsulación**: Atributos protegidos/privados en la clase `Cliente`, `Servicio` y `Reserva`, gestionados mediante `@property` y `@setter` con validaciones rigurosas.
- **Herencia y Polimorfismo**: Tres servicios especializados (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) que heredan de `Servicio` y sobrescriben los métodos `describir_servicio()`, `validar_parametros()` y `_calcular_subtotal_especifico()`.
- **Sobrecarga de Métodos**: Método `calcular_costo()` con parámetros opcionales y flexibles para tarifas base, descuentos e impuestos.
- **Manejo Robusto de Excepciones**: Jerarquía de excepciones personalizadas, uso explícito de `try/except`, `try/except/else`, `try/finally` y **encadenamiento de excepciones (`raise ... from err`)**.
- **Archivo de Logs**: Registro persistente y detallado en `software_fj.log`.
- **Batería de 10+ Simulaciones**: Demostración de estabilidad ante entradas erróneas y casos de borde.

---

## 📁 2. Estructura del Repositorio y Arquitectura

```text
SoftwareFJ/
│
├── excepciones.py       # Jerarquía orientada a objetos de excepciones personalizadas
├── logger_config.py     # Configuración centralizada del logger (consola + software_fj.log)
├── modelos.py           # Clases EntidadBase, Cliente, Servicio, ReservaSala, AlquilerEquipo, AsesoriaEspecializada, Reserva
├── gestor_sistema.py    # Controlador del sistema con try/except, else, finally y encadenamiento
├── simulaciones.py      # Batería de 11 simulaciones completas (casos válidos e inválidos)
├── main.py              # Punto de entrada principal con menú interactivo por consola
├── software_fj.log      # Archivo persistente de auditoría y traza de errores
└── README.md            # Documentación técnica del proyecto
```

---

## 🏗️ 3. Diagrama de Clases y Jerarquía

```
               +----------------------+
               |  EntidadBase (ABC)   |
               +----------------------+
               | - identificador      |
               | - fecha_creacion     |
               +----------------------+
                          ^
         +----------------+----------------+
         |                                 |
+-----------------+               +-----------------+
|     Cliente     |               |  Servicio (ABC) |
+-----------------+               +-----------------+
| - nombre        |               | - nombre        |
| - email         |               | - tarifa_base   |
| - telefono      |               | - disponible    |
+-----------------+               +-----------------+
                                           ^
         +-------------------+-------------+-------------------+
         |                   |                                 |
+-----------------+ +--------------------+         +------------------------+
|  ReservaSala    | |   AlquilerEquipo   |         | AsesoriaEspecializada  |
+-----------------+ +--------------------+         +------------------------+
| - tipo_sala     | | - marca_modelo     |         | - area_conocimiento    |
| - capacidad     | | - seguro_incluido  |         | - nivel_consultor      |
+-----------------+ +--------------------+         +------------------------+
```

---

## ⚙️ 4. Guía de Ejecución

### Prerrequisitos
- Python 3.8 o superior instalado en el sistema.

### Ejecución de Simulaciones Automáticas (10+ Casos)
Para evidenciar el cumplimiento del Criterio 2 de la rúbrica ante el tutor:
```bash
python main.py --simulacion
```

### Ejecución del Menú Interactivo de la Aplicación
```bash
python main.py
```

---

## 🧪 5. Resumen de las 10+ Simulaciones Ejecutadas

| # | Caso de Prueba | Tipo | Resultado / Excepción Gestionada | Estado del Sistema |
|---|----------------|------|-----------------------------------|--------------------|
| 1 | Registro válido de cliente | Válido | Cliente registrado con ID y fecha | Estable |
| 2 | Registro con email inválido | Inválido | `ClienteInvalidoError` capturada | Estable (Continúa) |
| 3 | Registro con teléfono < 7 dígitos | Inválido | `ClienteInvalidoError` capturada | Estable (Continúa) |
| 4 | Creación de 3 servicios polimórficos | Válido | Sala, Equipo y Asesoría incorporados | Estable |
| 5 | Creación de Sala con capacidad 999 | Inválido | `ServicioInvalidoError` (Rango 2-200) | Estable (Continúa) |
| 6 | Registro de objeto espurio (no Servicio) | Inválido | **Encadenamiento**: `TypeError` -> `ServicioInvalidoError` con `from` | Estable |
| 7 | Reserva con descuento 10% (Sobrecarga) | Válido | Cálculo automático de IVA y descuento | Estable |
| 8 | Reserva de Sala por 24 horas | Inválido | `ServicioInvalidoError` (Máx 12 hrs para salas) | Estable (Continúa) |
| 9 | Reserva de servicio NO disponible | Inválido | `ServicioNoDisponibleError` capturada | Estable (Continúa) |
| 10 | Cancelación de reserva ya PROCESADA | Inválido | `EstadoInvalidoError` (Transición ilegal) | Estable (Continúa) |
| 11 | Cancelación válida de reserva PENDIENTE | Válido | Transición PENDIENTE -> CANCELADA | Estable |

---

## 👥 6. Información para Trabajo Colaborativo en GitHub (Criterio 4)

Para obtener los **30 puntos del Nivel Alto** en Trabajo Colaborativo y Uso Profesional de GitHub:
1. **Crear el repositorio en GitHub**: `SoftwareFJ-Fase4-GrupoXX`.
2. **Subir los archivos base** a la rama `main`.
3. **Crear ramas individuales por cada uno de los 5 integrantes**:
   - `feature/excepciones-personalizadas` (Estudiante 1)
   - `feature/modelos-entidades-cliente` (Estudiante 2)
   - `feature/servicios-polimorficos` (Estudiante 3)
   - `feature/gestor-reservas-estados` (Estudiante 4)
   - `feature/simulaciones-logging` (Estudiante 5)
4. **Hacer Pull Requests (PR)** desde cada rama hacia `main` con descripciones claras.
5. Asignar **Issues** en GitHub para cada uno de los módulos anteriores.
