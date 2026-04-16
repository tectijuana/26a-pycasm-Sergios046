/*
 * Autor: Sergio Israel Jacobo Velasquez
 * Fecha: 2026-04-15
 * Descripción: Rutinas AArch64 (ARM64). ABI: argumentos w0/w1, retorno w0.
 */

        .text
        .align  2

        .global suma_asm
        .type   suma_asm, %function
suma_asm:
        add     w0, w0, w1
        ret

        .global resta
        .type   resta, %function
resta:
        sub     w0, w0, w1
        ret

        .global maximo
        .type   maximo, %function
maximo:
        cmp     w0, w1
        csel    w0, w0, w1, ge
        ret

        .global suma_arreglo
        .type   suma_arreglo, %function
suma_arreglo:
        mov     w2, wzr
        mov     w3, wzr
.Lloop:
        cmp     w2, w1
        b.ge    .Lend
        ldr     w5, [x0, w2, uxtw #2]
        add     w3, w3, w5
        add     w2, w2, #1
        b       .Lloop
.Lend:
        mov     w0, w3
        ret
