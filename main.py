from cola import Cola


def main():
    fila = Cola()
    for alumno in ("Ana", "Bruno", "Carla"):
        fila.encolar(alumno)

    print(fila)
    print("Atendiendo a:", fila.desencolar())
    print("Siguiente:", fila.frente())
    print("Elementos restantes:", fila.tamano())
    print(fila)


if __name__ == "__main__":
    main()
