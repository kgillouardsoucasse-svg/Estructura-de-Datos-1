from math import inf, isfinite


def dijkstra(grafo, origen):
    if origen not in grafo:
        raise ValueError("El origen no existe en el grafo")
    for vecinos in grafo.values():
        for vecino, peso in vecinos.items():
            if vecino not in grafo:
                raise ValueError("Falta declarar un vertice vecino")
            if not isfinite(peso) or peso < 0:
                raise ValueError("Dijkstra requiere pesos finitos no negativos")

    distancias = {v: inf for v in grafo}
    anteriores = {v: None for v in grafo}
    pendientes = set(grafo)
    distancias[origen] = 0

    while pendientes:
        actual = min(pendientes, key=distancias.get)
        if distancias[actual] == inf:
            break  
        pendientes.remove(actual)
        for vecino, peso in grafo[actual].items():
            nueva = distancias[actual] + peso
            if vecino in pendientes and nueva < distancias[vecino]:
                distancias[vecino] = nueva
                anteriores[vecino] = actual
    return distancias, anteriores


def reconstruir_camino(anteriores, distancias, destino):
    if distancias[destino] == inf:
        return []
    camino = []
    while destino is not None:
        camino.append(destino)
        destino = anteriores[destino]
    return camino[::-1]


if __name__ == "__main__":
    grafo = {
        "A": {"B": 4, "C": 1},
        "B": {"D": 1},
        "C": {"B": 2, "D": 5},
        "D": {"E": 3},
        "E": {},
    }
    print("DIJKSTRA | Grafo dirigido | Origen: A")
    print("Aristas: A->B(4), A->C(1), C->B(2),")
    print("         C->D(5), B->D(1), D->E(3)")
    distancias, anteriores = dijkstra(grafo, "A")
    for destino in grafo:
        ruta = " -> ".join(reconstruir_camino(anteriores, distancias, destino))
        print(f"A -> {destino}: costo {distancias[destino]}, ruta {ruta}")
