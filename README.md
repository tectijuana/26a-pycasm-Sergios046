# Proyecto ARM64 + Python + C

**Materia:** Lenguajes de Interfaz  
**Carrera:** Ingeniería en Sistemas Computacionales (ISC)  
**Profesor:** Rene Solis Reyes  
**Horario:** 5:00 – 6:00  
**Alumno:** Sergio Israel Jacobo Velasquez  
**Fecha:** 2026-04-15

## Descripción

Integración de **Python** (interfaz y pruebas), **C** (`src/bridge.c`) y **ARM64 Assembly** (`src/ops.s`) mediante una biblioteca compartida `build/libops.so` cargada con **`ctypes`**.

| Componente | Rol |
|------------|-----|
| `src/app.py` | Carga la `.so`, pruebas funcionales y benchmark Python vs C vs ASM |
| `src/bridge.c` | Puente C: `suma_c` y enlace a rutinas ASM (o equivalente con `HOST_STUB_ASM`) |
| `src/ops.s` | Rutinas AArch64: `suma_asm`, `resta`, `maximo`, `suma_arreglo` |
| `Makefile` | Compilación, `run`, `bench`, `debug`, `cross-aarch64` |

## Estructura

```
Proyecto_ARM64_Python/
├── src/
│   ├── app.py
│   ├── bridge.c
│   └── ops.s
├── build/                 # generado (libops.so; no imprescindible en git)
├── evidencias/
│   ├── screenshots/
│   ├── asciinema/
│   └── notas.md
├── Makefile
├── README.md
├── reporte.md             # fuente del reporte
├── reporte.pdf            # generar con: make reporte-pdf
```

## Entornos

| Entorno | Comportamiento de `make` |
|--------|---------------------------|
| **WSL / Linux x86_64** | Compila `bridge.c` con `-DHOST_STUB_ASM` → misma API; permite `make run` / `make bench` con el Python del sistema. |
| **Ubuntu ARM64 / Raspberry Pi** | Enlaza `bridge.c` + `ops.s` (ensamblador nativo). |
| **Artefacto ARM64 en PC x86** | `make cross-aarch64` → `build/libops.aarch64.so` (incluye `ops.s` real). |

## Dependencias

```bash
sudo apt update
sudo apt install -y gcc make python3 gdb
sudo apt install -y gcc-aarch64-linux-gnu    # opcional: cross-aarch64
sudo apt install -y pandoc texlive-xetex     # opcional: make reporte-pdf
```

## Compilación y ejecución

```bash
make clean
make
make run
make bench
```

Otros objetivos:

```bash
make debug              # GDB con python3 src/app.py
make cross-aarch64      # build/libops.aarch64.so
make reporte-pdf        # reporte.pdf desde reporte.md
```

## Depuración (GDB)

```bash
make debug
```

Ejemplos: `break suma_c`, `run`, `info registers`, `disassemble suma_c`, `continue`, `quit`.

## Evidencias (rúbrica)

Guardar en `evidencias/screenshots/` las capturas; en `evidencias/asciinema/` el archivo `.cast` o el enlace de subida; revisar `evidencias/notas.md`.

## Reporte PDF / HTML

**Opción A — PDF (recomendada):**

```bash
sudo apt install -y pandoc texlive-xetex
make reporte-pdf
```

**Opción B — HTML y luego “Imprimir a PDF” desde Chrome/Firefox:**

```bash
sudo apt install -y pandoc
make reporte-html
```

Abre `reporte.html` → Imprimir → Guardar como PDF → `reporte.pdf`.

**Opción C:** abre `reporte.md` en Word/LibreOffice y exporta a `reporte.pdf`.

## GitHub Classroom

```bash
git status
git add -A
git commit -m "Entrega final: Python + C + ARM64 (Sergio Israel Jacobo Velasquez)"
git push -u origin main
```


