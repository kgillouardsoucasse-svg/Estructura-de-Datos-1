def ordenar_seleccion(tiempos):
    datos = tiempos.copy()
    n = len(datos)

    for i in range(n - 1):
        indice_menor = i

        for j in range(i + 1, n):
            if datos[j] < datos[indice_menor]:
                indice_menor = j

        if indice_menor != i:
            datos[i], datos[indice_menor] = datos[indice_menor], datos[i]

    return datos


if __name__ == "__main__":
    tiempos = [15.2, 12.8, 14.5, 11.9, 13.6]
    print("Ejercicio 3: tiempos de carrera — método de selección")
    print("Tiempos originales (segundos):", tiempos)
    print("Tiempos ordenados (segundos):", ordenar_seleccion(tiempos))
