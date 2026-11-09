from math import inf, isfinite


def floyd(matriz):
    n = len(matriz)
    if any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada")
    if any(p != inf and not isfinite(p) for fila in matriz for p in fila):
        raise ValueError("Use pesos finitos o inf")
    dist = [fila[:] for fila in matriz]
    for i in range(n):
        dist[i][i] = min(0, dist[i][i])

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    if any(dist[i][i] < 0 for i in range(n)):
        raise ValueError("El grafo contiene un ciclo negativo")
    return dist


def mostrar(matriz, nombres):
    print("     " + " ".join(f"{v:>5}" for v in nombres))
    for nombre, fila in zip(nombres, matriz):
        valores = ["INF" if p == inf else str(p) for p in fila]
        print(f"{nombre:>3}  " + " ".join(f"{p:>5}" for p in valores))


if __name__ == "__main__":
    matriz = [
        [0, 4, 1, inf, inf],
        [inf, 0, inf, 1, inf],
        [inf, 2, 0, 5, inf],
        [inf, inf, inf, 0, 3],
        [inf, inf, inf, inf, 0],
    ]
    print("FLOYD | Grafo dirigido | INF = sin camino")
    print("Matriz de pesos inicial:")
    mostrar(matriz, "ABCDE")
    print("Distancias minimas entre todos los pares:")
    mostrar(floyd(matriz), "ABCDE")
