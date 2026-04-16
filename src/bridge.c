/*
 * Autor: Sergio Israel Jacobo Velasquez
 * Fecha: 2026-04-15
 * Descripción: Puente C para Python/ctypes. Expone suma_c en C y suma_asm / resta /
 *              maximo / suma_arreglo en ARM64 vía ops.s. Con HOST_STUB_ASM se
 *              compila sin ensamblador (WSL x86_64) manteniendo la misma API.
 */

#include <stddef.h>

int suma_c(int a, int b) { return a + b; }

#ifndef HOST_STUB_ASM

int suma_asm(int a, int b);
int resta(int a, int b);
int maximo(int a, int b);
int suma_arreglo(const int *arr, int n);

#else

int suma_asm(int a, int b) { return a + b; }

int resta(int a, int b) { return a - b; }

int maximo(int a, int b) { return (a > b) ? a : b; }

int suma_arreglo(const int *arr, int n) {
    int acc = 0;
    for (int i = 0; i < n; i++) {
        acc += arr[i];
    }
    return acc;
}

#endif
