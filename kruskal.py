from math import isfinite


def kruskal(vertices, aristas):
    vertices = list(vertices)
    aristas = list(aristas)
    if len(set(vertices)) != len(vertices):
        raise ValueError("Hay vertices repetidos")
    padre = {v: v for v in vertices}
    rango = {v: 0 for v in vertices}
    for u, v, peso in aristas:
        if u not in padre or v not in padre:
            raise ValueError("Una arista usa un vertice no declarado")
        if not isfinite(peso):
            raise ValueError("Los pesos deben ser finitos")

    def buscar(v):
        while padre[v] != v:
            padre[v] = padre[padre[v]]
            v = padre[v]
        return v

    elegidas, costo, componentes = [], 0, len(vertices)
    for u, v, peso in sorted(aristas, key=lambda arista: arista[2]):
        raiz_u, raiz_v = buscar(u), buscar(v)
        if raiz_u == raiz_v:
            continue  
        if rango[raiz_u] < rango[raiz_v]:
            raiz_u, raiz_v = raiz_v, raiz_u
        padre[raiz_v] = raiz_u
        if rango[raiz_u] == rango[raiz_v]:
            rango[raiz_u] += 1
        elegidas.append((u, v, peso))
        costo += peso
        componentes -= 1
    return elegidas, costo, componentes


if __name__ == "__main__":
    aristas = [("A", "B", 4), ("A", "C", 1), ("B", "C", 2),
               ("B", "D", 1), ("C", "D", 5), ("D", "E", 3)]
    print("KRUSKAL | Grafo no dirigido | Vertices: A B C D E")
    print("Aristas: A-B(4), A-C(1), B-C(2),")
    print("         B-D(1), C-D(5), D-E(3)")
    elegidas, costo, componentes = kruskal("ABCDE", aristas)
    print("Aristas del arbol de expansion minima:")
    for u, v, peso in elegidas:
        print(f"  {u} -- {v} : {peso}")
    print(f"Costo total: {costo}")
    print(f"Componentes: {componentes}")
    print(f"Aristas seleccionadas: {len(elegidas)} = V - 1")
