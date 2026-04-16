# Autor: Sergio Israel Jacobo Velasquez
# Fecha: 2026-04-15
# Descripción: Compila build/libops.so (nativo). En x86_64 usa HOST_STUB_ASM.
#              Objetivo cross-aarch64: .so real ARM64 para Raspberry Pi.

export PATH := /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$(PATH)

HOSTARCH := $(shell uname -m)
CC       := $(shell if command -v gcc >/dev/null 2>&1; then echo gcc; elif command -v clang >/dev/null 2>&1; then echo clang; else echo ""; fi)
ifeq ($(strip $(CC)),)
$(error Falta gcc o clang. Ejecuta: sudo apt install -y gcc)
endif

CROSS_CC := $(if $(wildcard /usr/bin/aarch64-linux-gnu-gcc),/usr/bin/aarch64-linux-gnu-gcc,aarch64-linux-gnu-gcc)

CFLAGS  := -std=c11 -O2 -fPIC -Wall -Wextra -g
LDFLAGS := -shared

BUILD_DIR := build
TARGET    := $(BUILD_DIR)/libops.so
AARCH64_SO := $(BUILD_DIR)/libops.aarch64.so

SRC_DIR := src

.PHONY: all run bench debug clean cross-aarch64 reporte-pdf reporte-html

all: $(TARGET)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

ifeq ($(HOSTARCH),aarch64)
$(TARGET): $(SRC_DIR)/bridge.c $(SRC_DIR)/ops.s | $(BUILD_DIR)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $(SRC_DIR)/bridge.c $(SRC_DIR)/ops.s
else
$(TARGET): $(SRC_DIR)/bridge.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -DHOST_STUB_ASM $(LDFLAGS) -o $@ $(SRC_DIR)/bridge.c
endif

run: $(TARGET)
	python3 $(SRC_DIR)/app.py

bench: $(TARGET)
	python3 $(SRC_DIR)/app.py bench

debug: $(TARGET)
	gdb -q --args python3 $(SRC_DIR)/app.py

cross-aarch64: $(BUILD_DIR)
	@command -v $(CROSS_CC) >/dev/null 2>&1 || (echo "Instala: sudo apt install -y gcc-aarch64-linux-gnu" && exit 1)
	$(CROSS_CC) $(CFLAGS) $(LDFLAGS) -o $(AARCH64_SO) $(SRC_DIR)/bridge.c $(SRC_DIR)/ops.s

clean:
	rm -rf $(BUILD_DIR)

# PDF: requiere pandoc + LaTeX (xelatex o pdflatex). Alternativa: make reporte-html y "Imprimir a PDF" en el navegador.
reporte-pdf: reporte.md
	@command -v pandoc >/dev/null 2>&1 || (echo "Instala: sudo apt install -y pandoc texlive-xetex" && exit 1)
	pandoc reporte.md -o reporte.pdf --toc -N \
		-V documentclass=article -V fontsize=12pt \
		--pdf-engine=xelatex 2>/dev/null || \
	pandoc reporte.md -o reporte.pdf --toc -N \
		-V documentclass=article --pdf-engine=pdflatex 2>/dev/null || \
	pandoc reporte.md -o reporte.pdf --toc -N

reporte-html: reporte.md
	@command -v pandoc >/dev/null 2>&1 || (echo "Instala: sudo apt install -y pandoc" && exit 1)
	pandoc reporte.md -s -o reporte.html --toc -N
