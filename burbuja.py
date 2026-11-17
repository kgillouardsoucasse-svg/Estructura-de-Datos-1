def ordenar_burbuja(calificaciones):
    datos = calificaciones.copy()
    n = len(datos)

    for i in range(n - 1):
        hubo_intercambio = False
        for j in range(n - 1 - i):
            if datos[j] > datos[j + 1]:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                hubo_intercambio = True

        if not hubo_intercambio:
            break

    return datos


if __name__ == "__main__":
    calificaciones = [85, 70, 95, 60, 90, 75]
    print("Ejercicio 1: calificaciones — método burbuja")
    print("Calificaciones originales:", calificaciones)
    print("Calificaciones ordenadas:", ordenar_burbuja(calificaciones))
