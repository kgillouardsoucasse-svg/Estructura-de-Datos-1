def _ajustar_monticulo(datos, tamano, raiz):
    while True:
        mayor = raiz
        izquierdo = 2 * raiz + 1
        derecho = 2 * raiz + 2
        if izquierdo < tamano and datos[izquierdo] > datos[mayor]:
            mayor = izquierdo
        if derecho < tamano and datos[derecho] > datos[mayor]:
            mayor = derecho
        if mayor == raiz:
            return
        datos[raiz], datos[mayor] = datos[mayor], datos[raiz]
        raiz = mayor


def heap_sort(numeros):
    datos = list(numeros)
    n = len(datos)
    for raiz in range(n // 2 - 1, -1, -1):
        _ajustar_monticulo(datos, n, raiz)
    for fin in range(n - 1, 0, -1):
        datos[0], datos[fin] = datos[fin], datos[0]
        _ajustar_monticulo(datos, fin, 0)
    return datos


if __name__ == "__main__":
    from interfaz import ejecutar_metodo
    ejecutar_metodo("HeapSort", heap_sort)
