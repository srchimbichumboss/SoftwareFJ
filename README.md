# Software FJ - Sistema de Reservas y Gestión

Proyecto práctico para la materia **Programación (213023) - Fase 4 (POO)** de la UNAD.

**Estudiante:** Thomas Fernando Mengual Arciniegas  
**Tutor:** Ángel Alberto Varón Quimbayo  
**Ingeniería de Sistemas - UNAD 2026**

---

## 📌 ¿De qué trata el proyecto?

Es una aplicación en Python para gestionar clientes, servicios (salas, alquiler de equipos y asesorías) y reservas para una empresa llamada **Software FJ**.

Como pide la guía:
- No usa base de datos: todo se maneja en memoria con listas y diccionarios de objetos.
- Aplica los 4 pilares de la programación orientada a objetos (Abstracción, Encapsulamiento, Herencia y Polimorfismo).
- Maneja excepciones con clases propias (`try/except/else/finally` y encadenamiento con `raise ... from`).
- Guarda un registro de todo lo que pasa en `software_fj.log`.
- Incluye 11 simulaciones automáticas con casos válidos y casos donde los datos están mal para comprobar que el programa no se cae.

---

## 📁 Archivos del proyecto

- `main.py`: Menú principal interactivo por consola.
- `modelos.py`: Las clases principales (`EntidadBase`, `Cliente`, `Servicio`, `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`, `Reserva`).
- `gestor_sistema.py`: La lógica para registrar clientes, crear servicios, hacer reservas y cancelarlas.
- `excepciones.py`: Las excepciones personalizadas del sistema.
- `logger_config.py`: Configuración del log para que salga en consola y en el archivo `software_fj.log`.
- `simulaciones.py`: Las 11 pruebas automáticas.
- `software_fj.log`: Archivo donde quedan guardadas las acciones y los errores capturados.
- `Fase4_Thomas_Mengual_SoftwareFJ.docx`: Documento formal del trabajo.

---

## 🚀 Cómo correr el proyecto

### 1. Requisitos
Tener instalado Python 3.8 o superior. No se necesitan librerías externas para correr el programa (usa la librería estándar de Python).

### 2. Probar las simulaciones automáticas
Para ver las 11 pruebas corriendo solas (muestra casos buenos y errores controlados):
```bash
python main.py --simulacion
```

### 3. Usar el menú interactivo
Para crear clientes y reservas manualmente:
```bash
python main.py
```

---

## 🧪 Resumen de las pruebas (11 casos)

1. Registro de cliente normal -> Funciona y crea el ID.
2. Cliente con correo sin `@` -> Captura error y no se cae.
3. Cliente con teléfono corto -> Captura error y sigue funcionando.
4. Creación de sala, equipo y asesoría -> Servicios creados con sus tarifas.
5. Sala con capacidad de 999 personas -> Error de validación (máximo 200).
6. Pasar un dato incorrecto al registrar servicio -> Error de tipo encadenado (`raise from`).
7. Reserva con 10% de descuento -> Calcula bien el total con IVA y descuento.
8. Reservar sala por más de 12 horas -> Error controlado (máximo 12h).
9. Reservar un servicio que está desactivado -> Error controlado de servicio no disponible.
10. Cancelar una reserva que ya fue procesada -> No lo permite porque ya pasó de estado.
11. Cancelar una reserva pendiente -> La cancela correctamente y libera el cupo.

---

## 👤 Autor
Desarrollado de manera individual por:  
**Thomas Fernando Mengual Arciniegas**  
GitHub: [@srchimbichumboss](https://github.com/srchimbichumboss)
