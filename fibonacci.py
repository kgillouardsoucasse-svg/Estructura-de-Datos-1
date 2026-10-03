def fibonacci(cantidad):
    serie = []
    actual, siguiente = 0, 1

    for _ in range(cantidad):
        serie.append(actual)
        # Python calcula ambos valores antes de hacer la asignación.
        actual, siguiente = siguiente, actual + siguiente

    return serie


def main():
    print("Serie de Fibonacci")

    while True:
        try:
            cantidad = int(input("¿Cuántos términos deseas mostrar? "))
            if cantidad <= 0:
                print("Ingresa un número entero mayor que cero.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Ingresa un número entero, por ejemplo: 8.")

    serie = fibonacci(cantidad)
    print("Serie de Fibonacci:")
    print(*serie)


if __name__ == "__main__":
    main()
