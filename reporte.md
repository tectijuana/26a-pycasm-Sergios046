---
title: "Integración Python, C y ARM64 Assembly"
subtitle: "Lenguajes de Interfaz — Proyecto práctico"
author: "Sergio Israel Jacobo Velasquez"
date: "15 de abril de 2026"
lang: es-MX
---

# Portada académica

| Dato | Información |
|------|-------------|
| **Alumno** | Sergio Israel Jacobo Velasquez |
| **Carrera** | Ingeniería en Sistemas Computacionales (ISC) |
| **Materia** | Lenguajes de Interfaz |
| **Horario** | 5:00 – 6:00 |
| **Profesor** | Rene Solis Reyes |
| **Nombre de la práctica** | Proyecto integración Python + C + ARM64 Assembly |
| **Fecha** | 15 de abril de 2026 |

---

# 1. Introducción

Este trabajo integra **Python** (orquestación y medición), **C** (puente en `src/bridge.c`) y **ARM64 Assembly** (rutinas en `src/ops.s`) mediante una biblioteca compartida `build/libops.so` cargada con **`ctypes`**.

En sistemas **x86_64** (por ejemplo WSL) la compilación usa **`HOST_STUB_ASM`** para conservar la misma interfaz sin ejecutar código ARM nativo en una CPU incompatible. El archivo ensamblador real se compila en **`build/libops.aarch64.so`** con **`make cross-aarch64`**.

# 2. Objetivo

- Demostrar interoperabilidad **Python ↔ C ↔ ASM** con **`.so`** y **`ctypes`**.
- Aplicar el **ABI** AArch64 para enteros de 32 bits: argumentos en **`w0` / `w1`** (y siguientes), retorno en **`w0`**.
- Comparar **rendimiento** entre Python, rutas C (`suma_c`) y rutas ASM (`suma_asm`, `resta`, `suma_arreglo`).
- Documentar el uso de **Make**, **GDB** y evidencias (**asciinema**, capturas).

# 3. Explicación por capas

## 3.1 Python (`src/app.py`)

Carga `build/libops.so` con `ctypes.CDLL`, declara `argtypes` y `restype` para cada función exportada, valida resultados numéricos y ejecuta un **benchmark** en tres columnas: Python puro, enfoque C vía `ctypes` y enfoque ASM / rutas equivalentes.

## 3.2 C (`src/bridge.c`)

Implementa **`suma_c`**. Cuando no se usa `HOST_STUB_ASM`, las funciones **`suma_asm`**, **`resta`**, **`maximo`** y **`suma_arreglo`** provienen de **`ops.s`**. Con `HOST_STUB_ASM`, se incluyen implementaciones equivalentes en C para permitir pruebas locales en hardware no AArch64.

## 3.3 ARM64 Assembly (`src/ops.s`)

- **`suma_asm`:** suma de enteros con `add` sobre `w0` y `w1`.
- **`resta`:** resta con `sub`.
- **`maximo`:** comparación y selección condicional.
- **`suma_arreglo`:** recorrido de arreglo con cargas `ldr` y acumulación, optimizando el acceso en un solo bucle a nivel de rutina exportada.

# 4. Benchmark

Ejecución: **`make bench`**. Se comparan tiempos de Python, rutas C y rutas ASM usando `time.perf_counter()` en el script.

**Tabla modelo (copiar tiempos de tu equipo):**

| Prueba | Python (ms) | C (ms) | ASM (ms) |
|--------|----------------|--------|----------|
| Suma escalar |  |  |  |
| Resta escalar |  |  |  |
| Suma de arreglo |  |  |  |

Interpretación esperada: el arrastre de **`ctypes`** puede hacer que la columna C no siempre “gane” frente a Python en operaciones mínimas; en **suma de arreglo**, la rutina agregada en la biblioteca suele mostrar ventaja frente a acumular con muchas llamadas desde Python.

# 5. Uso de GDB

1. Compilar con **`-g`** (ya incluido en el `Makefile`).
2. `make debug` o `gdb -q --args python3 src/app.py`.
3. Colocar breakpoints: `break suma_c` (en AArch64 también `break suma_asm`).
4. `run`, inspección con `info registers`, `disassemble`, avance con `stepi` / `nexti`.
5. Inspección de memoria cuando aplique: `x/16xw` sobre direcciones válidas mostradas por GDB.

# 6. Evidencias

Se organizan en el repositorio:

- **`evidencias/screenshots/`:** imágenes de terminal (compilar, ejecutar, benchmark) y GDB.
- **`evidencias/asciinema/`:** archivo **`.cast`** y/o enlace de subida.
- **`evidencias/notas.md`:** resumen y checklist para el profesor.

Opcional: captura de `file build/libops.aarch64.so` tras **`make cross-aarch64`**.

# 7. Conclusiones

La integración multi-lenguaje es viable y medible con herramientas estándar. Assembly ARM64 aporta control fino sobre registros y bucles; el costo de cruzar capas (**Python → C → ASM**) debe considerarse al analizar resultados. Para trabajo futuro: pruebas en **hardware AArch64 nativo** (p. ej. Raspberry Pi) y profiling adicional (`perf`) si el entorno lo permite.
