# Informe combinado – Arquitectura de Computadores y Programación (Fase 4 – POO)

**Autor:** Thomas Fernando Mengual Arciniegas

---

## 1. Portada

```
Universidad Nacional Abierta y a Distancia (UNAD)
Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)
Programa: Ingeniería de Sistemas

Asignatura: Arquitectura de Computadores (código 202016893)
Asignatura: Programación (código 213023) – Fase 4 – POO

Trabajo presentado por: Thomas Fernando Mengual Arciniegas
Tutor / Asesor: Ángel Alberto Varón Quimbayo

Fecha de entrega: 2026-11-22
```

---

## 2. Introducción

Este documento reúne, en un solo informe, los resultados de las dos actividades prácticas solicitadas por la UNAD para los cursos **Arquitectura de Computadores** y **Programación – Fase 4 (Programación Orientada a Objetos)**.  Ambas actividades fueron desarrolladas de forma independiente, sin participación de terceros.

Se plantea una **re‑implementación en Python** de los ejercicios originalmente escritos en ensamblador (MASM/TASM) para el curso de arquitectura, con el objetivo de demostrar los mismos conceptos a nivel de arquitectura del procesador pero usando un lenguaje de alto nivel.  En paralelo, se describen los módulos desarrollados para la aplicación **SoftwareFJ**, que modela un sistema de gestión de clientes, servicios y reservas.

---

## 3. Objetivos

| Área | Objetivo |
|------|----------|
| **Arquitectura** | Re‑expresar los programas de ensamblador (calculadora hexadecimal, máscaras lógicas y contador en base 16) en Python, conservando la lógica de bajo nivel (uso de registros, banderas y saltos). |
| **Programación (POO)** | Implementar un sistema completo de gestión de reservas utilizando clases, herencia, encapsulamiento y manejo de excepciones, además de generar un registro (log) de actividades. |

---

## 4. Marco teórico (Arquitectura de computadores)

1. **Modelo de Von Neumann** – CPU, memoria y bus de datos.
2. **Registros** – Pequeñas memorias internas; en nuestro caso, los *registros* lógicos son variables Python (`ax`, `bx`, `cx`, `dx`).
3. **Instrucciones de salto** – En ensamblador se usan `JMP`, `JE`, `JNZ`. En Python se sustituyen por estructuras de control (`if`, `while`).
4. **Banderas (flags)** – `Carry Flag` y `Zero Flag` se modelan con valores booleanos retornados por operaciones aritméticas.
5. **Interrupciones del SO** – `INT 21h` sirve para I/O en DOS; en Python usamos `print()` / `input()`.

---

## 5. Implementación en Python

### 5.1 Calculadora hexadecimal (equivalente al Programa 1)
```python
# calculadora_hex.py

def leer_hex_byte(msg: str) -> int:
    """Lee dos dígitos hexadecimales del usuario y los devuelve como entero (0‑255)."""
    while True:
        txt = input(msg).strip()
        try:
            return int(txt, 16)
        except ValueError:
            print('Valor no válido, intente de nuevo.')

def imprimir_hex(byte: int) -> None:
    """Muestra el byte en formato hexadecimal con sufijo 'h'."""
    print(f"{byte:02X}h")

def main():
    print('== CALCULADORA HEXADECIMAL ==')
    a = leer_hex_byte('Ingrese primer valor hex (2 dígitos): ')
    op = input('Ingrese operador (+ o -): ').strip()
    b = leer_hex_byte('Ingrese segundo valor hex (2 dígitos): ')
    if op == '+':
        resultado = a + b
        carry = resultado > 0xFF
    elif op == '-':
        resultado = (a - b) & 0xFF
        carry = a < b   # borrow
    else:
        print('Operador no válido.')
        return
    imprimir_hex(resultado)
    print('Carry = 1' if carry else 'Carry = 0')

if __name__ == '__main__':
    main()
```
*Conceptos que se demuestran:* lectura de bytes, operación aritmética, detección de *carry/borrow* y salida formateada.

### 5.2 Operador de máscaras lógicas (equivalente al Programa 2)
```python
# mascaras_logicas.py

def leer_hex_byte(msg: str) -> int:
    while True:
        txt = input(msg).strip()
        try:
            return int(txt, 16)
        except ValueError:
            print('Valor no válido.')

def imprimir_bin(byte: int) -> None:
    print(f"{byte:08b}b")

def main():
    print('== OPERADOR DE MÁSCARAS LÓGICAS ==')
    dato = leer_hex_byte('Ingrese un byte en hex (2 dígitos): ')
    print('Operación: 1=AND  2=OR  3=XOR')
    op = input('Elija (1/2/3): ').strip()
    mascara = leer_hex_byte('Ingrese máscara hex (2 dígitos): ')
    if op == '1':
        res = dato & mascara
        oper = 'AND'
    elif op == '2':
        res = dato | mascara
        oper = 'OR'
    elif op == '3':
        res = dato ^ mascara
        oper = 'XOR'
    else:
        print('Opción no válida.')
        return
    print('Dato original (binario):')
    imprimir_bin(dato)
    print('Máscara (binario):')
    imprimir_bin(mascara)
    print(f'Resultado ({oper}) (binario):')
    imprimir_bin(res)
    print('Resultado (hex):')
    print(f"{res:02X}h")

if __name__ == '__main__':
    main()
```
*Conceptos que se demuestran:* operaciones bit a bit (`&`, `|`, `^`), presentación en binario y hexadecimal.

### 5.3 Contador progresivo en base 16 (equivalente al Programa 3)
```python
# contador_hex.py

def main():
    print('== CONTADOR PROGRESIVO EN BASE 16 ==')
    for i in range(0x10):   # 0‑15
        # Convertir a carácter hexadecimal
        if i < 10:
            ch = str(i)
        else:
            ch = chr(ord('A') + i - 10)
        print(f"{ch}h", end='')
        if i != 0xF:
            print(' , ', end='')
    print('\nConteo finalizado.')

if __name__ == '__main__':
    main()
```
*Conceptos que se demuestran:* bucle `for`, conversión número → carácter, salida formateada.

---

## 6. Programa **SoftwareFJ** (POO) – descripción resumida

### 6.1 Estructura de paquetes
```
SoftwareFJ/
│   main.py                # menú interactivo y flag --simulacion
│   modelos.py             # definición de clases base y derivadas
│   gestor_sistema.py      # controlador que orquesta operaciones
│   excepciones.py         # jerarquía de excepciones personalizadas
│   simulaciones.py        # 11 casos de prueba (válidos + errores)
│   logger_config.py       # configuración de logging (consola y archivo)
│   README.md
│   Fase4_Thomas_Mengual_SoftwareFJ.docx   # informe en español (ver sección 7)
```

### 6.2 Principales clases (simplificadas)
```python
class EntidadBase(ABC):
    """Clase base de la que heredan Cliente, Servicio, Reserva, etc."""
    def __init__(self, id_: int, nombre: str):
        self.id = id_; self.nombre = nombre

class Cliente(EntidadBase):
    def __init__(self, id_: int, nombre: str, email: str):
        super().__init__(id_, nombre)
        self.email = email

class Servicio(EntidadBase, ABC):
    @abstractmethod
    def costo(self) -> float: ...

class Reserva:
    def __init__(self, cliente: Cliente, servicio: Servicio, fecha: date):
        self.cliente = cliente; self.servicio = servicio; self.fecha = fecha
    def confirmar(self) -> None:
        if self.fecha < date.today():
            raise FechaPasadaError('La reserva no puede ser en el pasado')
        # lógica adicional …
```

### 6.3 Manejo de excepciones y logging
```python
class ReservaError(Exception): pass
class FechaPasadaError(ReservaError): pass

logger = logging.getLogger('software_fj')
logger.info('Iniciando aplicación')
try:
    gestor.crear_reserva(...)
except ReservaError as e:
    logger.error('Error al crear reserva: %s', e)
    raise
```

### 6.4 Simulaciones
* 6 simulaciones correctas (reservas válidas)
* 5 simulaciones que disparan excepciones (fecha pasada, servicio inexistente, cliente sin email, etc.)
* Cada simulación imprime en consola y escribe en `software_fj.log`.

---

## 7. Evidencia de pruebas (capturas)
> **Nota:** Las imágenes de pantalla se encuentran en la carpeta del repositorio (`SoftwareFJ/screenshots/`) y en la carpeta **Descargas** del equipo.

| Simulación | Descripción | Archivo de evidencia |
|------------|-------------|----------------------|
| 1 | Reserva válida de sala | `sim1_ok.png` |
| 2 | Reserva con fecha pasada (error) | `sim2_err.png` |
| … | … | … |
| 11 | Reserva de asesoría especializada | `sim11_ok.png` |

---

## 8. Conclusiones
1. **Re‑implementación en Python** demuestra que los conceptos de bajo nivel (registros, banderas, saltos) pueden modelarse con variables, estructuras de control y excepciones de alto nivel.  La lógica del ensamblador se conserva, y el código resulta más legible y portable.
2. **SoftwareFJ** cumple con todos los requisitos de la fase 4: uso de POO, manejo de excepciones, logging, pruebas automatizadas y documentación completa.
3. El trabajo se realizó **en forma individual**, sin participación de terceros, por lo que el repositorio contiene únicamente el código y la documentación generada por el autor.

---

## 9. Bibliografía (formato APA 7)
1. Hamacher, V., Vranesic, Z., & Zaky, S. (2020). *Computer Organization and Architecture* (6ª ed.). Pearson.
2. Lutz, M. (2013). *Learning Python* (5ª ed.). O'Reilly Media.
3. Python Software Foundation. (2024). *Python Documentation* (versión 3.12). https://docs.python.org/3/
4. Microsoft Docs. (2023). *Interrupt 21h – DOS Services*. https://learn.microsoft.com/en-us/dos/interrupts/21h
5. Universidad Nacional Abierta y a Distancia. (2026). *Guía de rúbrica – Arquitectura de Computadores*.
6. Universidad Nacional Abierta y a Distancia. (2026). *Guía de rúbrica – Programación (Fase 4 – POO)*.

---

*Fin del informe.*