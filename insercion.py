def ordenar_insercion(precios):
    datos = precios.copy()

    for i in range(1, len(datos)):
        actual = datos[i]
        j = i - 1

        while j >= 0 and datos[j] > actual:
            datos[j + 1] = datos[j]
            j -= 1

        datos[j + 1] = actual

    return datos


if __name__ == "__main__":
    precios = [120.50, 45.00, 89.90, 30.00, 150.00]
    ordenados = ordenar_insercion(precios)
    print("Ejercicio 2: precios — método de inserción")
    print("Precios originales:", ", ".join(f"${p:.2f}" for p in precios))
    print("Precios ordenados:", ", ".join(f"${p:.2f}" for p in ordenados))
