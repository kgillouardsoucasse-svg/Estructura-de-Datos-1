def quick_sort(numeros):
    datos = list(numeros)
    if len(datos) < 2:
        return datos
    pendientes = [(0, len(datos) - 1)]
    while pendientes:
        izquierda, derecha = pendientes.pop()
        i, j = izquierda, derecha
        pivote = datos[(izquierda + derecha) // 2]
        while i <= j:
            while datos[i] < pivote:
                i += 1
            while datos[j] > pivote:
                j -= 1
            if i <= j:
                datos[i], datos[j] = datos[j], datos[i]
                i += 1
                j -= 1
        if izquierda < j:
            pendientes.append((izquierda, j))
        if i < derecha:
            pendientes.append((i, derecha))
    return datos


if __name__ == "__main__":
    from interfaz import ejecutar_metodo
    ejecutar_metodo("QuickSort", quick_sort)
