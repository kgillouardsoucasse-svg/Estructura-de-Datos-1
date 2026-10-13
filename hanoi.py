import platform
import sys
from pathlib import Path
from time import perf_counter


def resolver_hanoi(n, origen="A", auxiliar="B", destino="C", mostrar=False):
    if n < 1:
        raise ValueError("El número de discos debe ser mayor que cero.")

    if n == 1:
        if mostrar:
            print(f"Disco 1: {origen} -> {destino}")
        return 1

    movimientos = resolver_hanoi(n - 1, origen, destino, auxiliar, mostrar)
    if mostrar:
        print(f"Disco {n}: {origen} -> {destino}")
    movimientos += 1
    movimientos += resolver_hanoi(n - 1, auxiliar, origen, destino, mostrar)
    return movimientos


def medir_tiempo(n, repeticiones=1):
    inicio = perf_counter()
    for _ in range(repeticiones):
        movimientos = resolver_hanoi(n)
    segundos = (perf_counter() - inicio) / repeticiones
    return movimientos, segundos


def estimar_tiempo(n, movimientos_base, segundos_base):
    movimientos = 2 ** n - 1
    segundos = segundos_base * movimientos / movimientos_base
    return movimientos, segundos


def main():
    if "--mostrar" in sys.argv:
        resolver_hanoi(5, mostrar=True)
        return

    lineas = [
        f"Python: {platform.python_version()}",
        f"Sistema: {platform.system()} {platform.release()}",
        "Tiempos sin imprimir movimientos. 64 discos: solo estimación.",
        "",
    ]
    for n, repeticiones in [(5, 1000), (10, 1000), (30, 1)]:
        print(f"Resolviendo {n} discos ({repeticiones} ejecución/es)...", flush=True)
        movimientos, segundos = medir_tiempo(n, repeticiones)
        linea = (
            f"{n} discos | {movimientos:,} movimientos | {segundos:.9f} s "
            f"| MEDIDO | repeticiones: {repeticiones}"
        )
        print(linea, flush=True)
        lineas.append(linea)

    movimientos_64, segundos_64 = estimar_tiempo(64, movimientos, segundos)
    anios_64 = segundos_64 / (365.25 * 24 * 60 * 60)
    linea = (
        f"64 discos | {movimientos_64:,} movimientos | {segundos_64:.3f} s "
        f"| ESTIMADO: {anios_64:,.2f} años"
    )
    print(linea, flush=True)
    lineas.append(linea)
    Path(__file__).with_name("resultados.txt").write_text(
        "\n".join(lineas) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
