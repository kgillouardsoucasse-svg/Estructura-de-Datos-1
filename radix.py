def radix_sort(numeros):
    datos = list(numeros)
    if not datos:
        return datos
    minimo = min(datos)
    datos = [numero - minimo for numero in datos]
    maximo = max(datos)
    posicion = 1
    while maximo // posicion > 0:
        cubetas = [[] for _ in range(10)]
        for numero in datos:
            digito = (numero // posicion) % 10
            cubetas[digito].append(numero)
        datos = [numero for cubeta in cubetas for numero in cubeta]
        posicion *= 10
    return [numero + minimo for numero in datos]


if __name__ == "__main__":
    from interfaz import ejecutar_metodo
    ejecutar_metodo("Radix", radix_sort)
