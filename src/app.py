#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autor: Sergio Israel Jacobo Velasquez
Fecha: 2026-04-15
Descripción: Carga build/libops.so con ctypes, prueba funciones C/ASM y benchmark.
"""

import argparse
import ctypes
import os
import random
import sys
import time


def _repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lib_path():
    return os.path.join(_repo_root(), "build", "libops.so")


def _load_lib():
    path = _lib_path()
    if not os.path.isfile(path):
        print(f"No existe {path}. Ejecuta: make", file=sys.stderr)
        sys.exit(1)
    lib = ctypes.CDLL(path)

    for name in ("suma_c", "suma_asm", "resta", "maximo"):
        fn = getattr(lib, name)
        fn.argtypes = (ctypes.c_int, ctypes.c_int)
        fn.restype = ctypes.c_int

    lib.suma_arreglo.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    lib.suma_arreglo.restype = ctypes.c_int
    return lib


def cmd_run():
    lib = _load_lib()
    a, b = 17, 5
    print("=== Integración Python + C + ARM64 ===")
    print(f"suma_c({a}, {b})     = {lib.suma_c(a, b)}")
    print(f"suma_asm({a}, {b})   = {lib.suma_asm(a, b)}")
    print(f"resta({a}, {b})      = {lib.resta(a, b)}")
    print(f"maximo({a}, {b})     = {lib.maximo(a, b)}")

    nums = (ctypes.c_int * 6)(3, 7, 2, 9, 1, 4)
    n = 6
    esperado = sum(nums[i] for i in range(n))
    got = lib.suma_arreglo(nums, n)
    print(f"suma_arreglo(...)    = {got} (esperado {esperado})")
    if got != esperado:
        sys.exit(2)
    print("OK: resultados consistentes.")


def _bench(label, loops, py_fn, c_fn, asm_fn):
    t0 = time.perf_counter()
    for _ in range(loops):
        py_fn()
    t_py = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    for _ in range(loops):
        c_fn()
    t_c = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    for _ in range(loops):
        asm_fn()
    t_asm = (time.perf_counter() - t0) * 1000.0

    print(f"{label}")
    print(f"  Python : {t_py:10.3f} ms")
    print(f"  C      : {t_c:10.3f} ms")
    print(f"  ASM    : {t_asm:10.3f} ms")
    print()


def cmd_bench():
    lib = _load_lib()
    loops = 200_000
    a, b = 12345, 678

    def py_suma():
        return a + b

    def c_suma():
        return lib.suma_c(a, b)

    def asm_suma():
        return lib.suma_asm(a, b)

    _bench("Suma escalar (a+b)", loops, py_suma, c_suma, asm_suma)

    def py_resta():
        return a - b

    def c_resta():
        return lib.suma_c(a, -b)

    def asm_resta():
        return lib.resta(a, b)

    _bench("Resta escalar (a-b)", loops, py_resta, c_resta, asm_resta)

    n = 4096
    data = [random.randint(-1000, 1000) for _ in range(n)]
    arr = (ctypes.c_int * n)(*data)
    esperado = sum(data)

    def py_arr():
        s = 0
        for v in data:
            s += v
        return s

    def c_arr():
        s = 0
        for v in data:
            s = lib.suma_c(s, v)
        return s

    def asm_arr():
        return lib.suma_arreglo(arr, n)

    loops_arr = 2000
    t0 = time.perf_counter()
    for _ in range(loops_arr):
        py_arr()
    t_py = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    for _ in range(loops_arr):
        c_arr()
    t_c = (time.perf_counter() - t0) * 1000.0

    t0 = time.perf_counter()
    for _ in range(loops_arr):
        asm_arr()
    t_asm = (time.perf_counter() - t0) * 1000.0

    if asm_arr() != esperado:
        print("ERROR: suma_arreglo no coincide con Python.", file=sys.stderr)
        sys.exit(2)

    print("Suma de arreglo (Python vs acumulador C vs suma_arreglo ASM)")
    print(f"  Python : {t_py:10.3f} ms")
    print(f"  C      : {t_c:10.3f} ms")
    print(f"  ASM    : {t_asm:10.3f} ms")


def main():
    p = argparse.ArgumentParser(description="Proyecto Python + C + ARM64")
    p.add_argument("mode", nargs="?", default="run", choices=("run", "bench"))
    args = p.parse_args()
    if args.mode == "run":
        cmd_run()
    else:
        cmd_bench()


if __name__ == "__main__":
    main()
