from timeit import repeat


def fibonacci_iterativo(n):
    anterior, actual = 0, 1
    for _ in range(n):
        anterior, actual = actual, anterior + actual
    return anterior


def fibonacci_recursivo(n):
    
    if n <= 1:  # Casos base: F(0) = 0 y F(1) = 1.
        return n

    # AQUÍ ESTÁ LA RECURSIVIDAD: la función se llama a sí misma.
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


def medir_tiempo(funcion, n):
    tiempos = repeat(lambda: funcion(n), repeat=5, number=10)
    return min(tiempos) / 10


def main():
    print("FIBONACCI: SOLUCIÓN ITERATIVA Y RECURSIVA")
    print("La sucesión comienza: 0, 1, 1, 2, 3, 5, 8, 13...")
    print("La posición inicial es 0; por ejemplo, F(10) = 55.")
    print("Se limita n a 30 porque la recursión simple repite cálculos.")

    while True:
        entrada = input("\nEscribe una posición de 0 a 30, o 'salir': ").strip()
        if entrada.lower() == "salir":
            print("Programa terminado.")
            break

        try:
            n = int(entrada)
        except ValueError:
            print("Entrada inválida. Escribe un número entero.")
            continue

        if not 0 <= n <= 30:
            print("El número debe estar entre 0 y 30.")
            continue

        resultado_iterativo = fibonacci_iterativo(n)
        resultado_recursivo = fibonacci_recursivo(n)
        print("Midiendo tiempos...")
        tiempo_iterativo = medir_tiempo(fibonacci_iterativo, n)
        tiempo_recursivo = medir_tiempo(fibonacci_recursivo, n)

        print(f"\n{'Método':<12} {'Resultado':>12} {'Tiempo (segundos)':>20}")
        print(f"{'Iterativo':<12} {resultado_iterativo:>12} {tiempo_iterativo:>20.9f}")
        print(f"{'Recursivo':<12} {resultado_recursivo:>12} {tiempo_recursivo:>20.9f}")
        print("Tiempo por llamada: mejor lote de 5, con 10 llamadas por lote.")
        print("Los tiempos pueden cambiar según el equipo y su carga.")


if __name__ == "__main__":
    main()
