from cola import Cola


def sumar_colas(cola_a, cola_b):
    if cola_a.tamano() != cola_b.tamano():
        raise ValueError("Las colas deben tener la misma cantidad de elementos.")

    copia_a = cola_a.copiar()
    copia_b = cola_b.copiar()
    resultado = Cola()

    while not copia_a.esta_vacia():
        a = copia_a.desencolar()
        b = copia_b.desencolar()
        if type(a) is not int or type(b) is not int:
            raise TypeError("Las colas deben contener únicamente números enteros.")
        resultado.encolar(a + b)

    return resultado


def main():
    cola_a = Cola([3, 4, 2, 8, 12])
    cola_b = Cola([6, 2, 9, 11, 3])
    resultado = sumar_colas(cola_a, cola_b)

    print("SUMA DE DOS COLAS")
    print(f"{'Cola A':>8} {'Cola B':>8} {'Resultado':>10}")
    for a, b, suma in zip(cola_a.a_lista(), cola_b.a_lista(), resultado.a_lista()):
        print(f"{a:>8} {b:>8} {suma:>10}")
    print("Cola resultado:", resultado.a_lista())


if __name__ == "__main__":
    main()
