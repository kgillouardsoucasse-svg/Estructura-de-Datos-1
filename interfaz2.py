def leer_entero(mensaje, minimo=None):
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Entrada inválida. Escribe un número entero.")
            continue
        if minimo is not None and numero < minimo:
            print(f"Escribe un número mayor o igual que {minimo}.")
            continue
        return numero


def ordenar_una_vez(nombre, metodo):
    cantidad = leer_entero("¿Cuántos números deseas ordenar? ", minimo=1)
    numeros = [leer_entero(f"Número {i + 1}: ") for i in range(cantidad)]
    resultado = metodo(numeros)
    print(f"\nMétodo: {nombre}")
    print(f"Lista original: {numeros}")
    print(f"Lista ordenada: {resultado}\n")


def ejecutar_menu(metodos):
    try:
        while True:
            print("=== MÉTODOS DE ORDENAMIENTO ===")
            for opcion, (nombre, _) in metodos.items():
                print(f"{opcion}. {nombre}")
            print("0. Salir")
            opcion = leer_entero("Elige una opción: ")
            if opcion == 0:
                print("Programa finalizado.")
                return
            if opcion not in metodos:
                print("Opción inválida. Intenta de nuevo.\n")
                continue
            nombre, metodo = metodos[opcion]
            ordenar_una_vez(nombre, metodo)
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma finalizado por interrupción de la entrada.")


def ejecutar_metodo(nombre, metodo):
    ejecutar_menu({1: (nombre, metodo)})


if __name__ == "__main__":
    # Permite abrir también este archivo directamente y ver el menú completo.
    from shellsort import shell_sort
    from quicksort import quick_sort
    from heapsort import heap_sort
    from radix import radix_sort

    ejecutar_menu({
        1: ("ShellSort", shell_sort),
        2: ("QuickSort", quick_sort),
        3: ("HeapSort", heap_sort),
        4: ("Radix", radix_sort),
    })
