def warshall(adyacencia, reflexivo=True):
  
    n = len(adyacencia)
    if any(len(fila) != n for fila in adyacencia):
        raise ValueError("La matriz debe ser cuadrada")
    if any(x not in (0, 1) for fila in adyacencia for x in fila):
        raise ValueError("La matriz solo admite 0 y 1")
    alcance = [[bool(x) for x in fila] for fila in adyacencia]
    if reflexivo:
        for i in range(n):
            alcance[i][i] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                alcance[i][j] = alcance[i][j] or (
                    alcance[i][k] and alcance[k][j]
                )
    return alcance


def mostrar(matriz):
    print("      A  B  C  D")
    for nombre, fila in zip("ABCD", matriz):
        print(f"   {nombre}  " + "  ".join(str(int(x)) for x in fila))


if __name__ == "__main__":
    matriz = [[0, 1, 0, 0], [0, 0, 1, 0],
              [0, 0, 0, 1], [0, 0, 0, 0]]
    print("WARSHALL | Aristas: A->B, B->C, C->D")
    print("Matriz de adyacencia inicial:")
    mostrar(matriz)
    print("Alcanzabilidad (incluye caminos de longitud cero):")
    resultado = warshall(matriz)
    mostrar(resultado)
    print(f"Existe camino de A a D: {resultado[0][3]}")
    print(f"Existe camino de D a A: {resultado[3][0]}")
