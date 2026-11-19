def shell_sort(numeros):
    datos = list(numeros)
    salto = len(datos) // 2
    while salto > 0:
        for i in range(salto, len(datos)):
            actual = datos[i]
            j = i
            while j >= salto and datos[j - salto] > actual:
                datos[j] = datos[j - salto]
                j -= salto
            datos[j] = actual
        salto //= 2
    return datos


if __name__ == "__main__":
    from interfaz import ejecutar_metodo
    ejecutar_metodo("ShellSort", shell_sort)
