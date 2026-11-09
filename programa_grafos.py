import argparse
import heapq
import itertools
import webbrowser
from html import escape
from pathlib import Path


# Cada arista contiene: origen, destino y costo de traslado en pesos.
# Las rutas son bidireccionales; no necesariamente representan colindancias.
CONEXIONES = [
    ("Jalisco", "Nayarit", 400),
    ("Jalisco", "Zacatecas", 550),
    ("Jalisco", "Aguascalientes", 350),
    ("Jalisco", "Guanajuato", 500),
    ("Jalisco", "Michoacán", 450),
    ("Jalisco", "Colima", 300),
    ("Nayarit", "Zacatecas", 600),
    ("Zacatecas", "Aguascalientes", 250),
    ("Aguascalientes", "Guanajuato", 450),
    ("Guanajuato", "Michoacán", 300),
    ("Michoacán", "Colima", 400),
]


def crear_grafo(conexiones):
    """Construye una lista de adyacencia con diccionarios anidados."""
    grafo = {}
    for origen, destino, costo in conexiones:
        if costo <= 0:
            raise ValueError("Los costos deben ser positivos.")
        grafo.setdefault(origen, {})[destino] = costo
        grafo.setdefault(destino, {})[origen] = costo
    return grafo


def recorrido_sin_repetir(grafo, inicio):
    """Backtracking: busca el camino hamiltoniano de menor costo desde inicio."""
    mejor_ruta = None
    mejor_costo = float("inf")

    def explorar(ruta, visitados, costo):
        nonlocal mejor_ruta, mejor_costo
        if costo >= mejor_costo:
            return
        if len(visitados) == len(grafo):
            mejor_ruta, mejor_costo = ruta.copy(), costo
            return
        for vecino, precio in grafo[ruta[-1]].items():
            if vecino not in visitados:
                ruta.append(vecino)
                visitados.add(vecino)
                explorar(ruta, visitados, costo + precio)
                visitados.remove(vecino)
                ruta.pop()

    explorar([inicio], {inicio}, 0)
    return mejor_ruta, mejor_costo


def recorrido_con_repeticion(grafo, inicio):
    """Dijkstra sobre (ubicación, estados visitados, hubo repetición).

    Llegar a un mismo lugar con distintos estados visitados representa una
    situación diferente. Se termina al visitar todos y repetir al menos uno.
    """
    inicial = (inicio, frozenset([inicio]), False)
    distancias = {inicial: 0}
    anteriores = {inicial: None}
    desempate = itertools.count()
    pendientes = [(0, next(desempate), inicial)]

    while pendientes:
        costo, _, situacion = heapq.heappop(pendientes)
        if costo != distancias[situacion]:
            continue
        actual, visitados, repetido = situacion
        if len(visitados) == len(grafo) and repetido:
            ruta = []
            cursor = situacion
            while cursor is not None:
                ruta.append(cursor[0])
                cursor = anteriores[cursor]
            return ruta[::-1], costo

        for vecino, precio in grafo[actual].items():
            siguiente = (
                vecino,
                visitados | {vecino},
                repetido or vecino in visitados,
            )
            nuevo_costo = costo + precio
            if nuevo_costo < distancias.get(siguiente, float("inf")):
                distancias[siguiente] = nuevo_costo
                anteriores[siguiente] = situacion
                heapq.heappush(
                    pendientes, (nuevo_costo, next(desempate), siguiente)
                )
    return None, float("inf")


def mostrar_recorrido(titulo, grafo, resultado):
    ruta, costo = resultado
    print("\n" + titulo)
    if ruta is None:
        print("No existe un recorrido que cumpla esta condición.")
        return
    print(" -> ".join(ruta))
    for origen, destino in zip(ruta, ruta[1:]):
        print(f"  {origen} -> {destino}: ${grafo[origen][destino]:,} MXN")
    repetidos = list(dict.fromkeys(e for e in ruta if ruta.count(e) > 1))
    print("Estados repetidos: " + (", ".join(repetidos) or "ninguno"))
    print(f"Costo total: ${costo:,} MXN")


def dibujar_grafo(conexiones, archivo):
    """Dibuja nodos, relaciones y pesos en SVG, sin instalar paquetes."""
    posiciones = {
        "Jalisco": (470, 320),
        "Nayarit": (170, 160),
        "Zacatecas": (470, 110),
        "Aguascalientes": (770, 160),
        "Guanajuato": (770, 460),
        "Michoacán": (470, 530),
        "Colima": (170, 460),
    }
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="650" '
        'viewBox="0 0 960 650" role="img" aria-labelledby="titulo descripcion">',
        '<title id="titulo">Grafo de siete estados mexicanos</title>',
        '<desc id="descripcion">Rutas bidireccionales con costos ficticios '
        'en pesos mexicanos. La ubicación de los nodos es esquemática.</desc>',
        '<rect width="960" height="650" fill="#f5f7fb"/>',
        '<g font-family="Arial, sans-serif" text-anchor="middle">',
        '<text x="480" y="39" font-size="25" font-weight="bold" '
        'fill="#14324c">ADA7 · Programa de grafos</text>',
        '<text x="480" y="65" font-size="15" fill="#4b6074">'
        '7 estados · 11 conexiones · Costos ficticios en MXN</text>',
    ]
    # Primero las aristas; después los nodos, para mantener legibles los nombres.
    for origen, destino, costo in conexiones:
        x1, y1 = posiciones[origen]
        x2, y2 = posiciones[destino]
        x, y = (x1 + x2) / 2, (y1 + y2) / 2
        svg.extend([
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            'stroke="#8496ab" stroke-width="2.5"/>',
            f'<rect x="{x-29}" y="{y-13}" width="58" height="26" '
            'rx="8" fill="#ffffff" stroke="#d2dce8"/>',
            f'<text x="{x}" y="{y+5}" font-size="15" '
            f'fill="#14324c">${costo}</text>',
        ])
    for estado, (x, y) in posiciones.items():
        color = "#0f766e" if estado == "Jalisco" else "#173f65"
        svg.extend([
            f'<rect x="{x-85}" y="{y-24}" width="170" height="48" '
            f'rx="24" fill="{color}"/>',
            f'<text x="{x}" y="{y+6}" font-size="17" '
            f'fill="white">{escape(estado)}</text>',
        ])
    svg.extend([
        '<text x="480" y="601" font-size="15" fill="#4b6074">'
        'Cada línea permite viajar en ambos sentidos.</text>',
        '<text x="480" y="625" font-size="13" fill="#4b6074">'
        'Modelo didáctico: no es un mapa ni una cotización de transporte.</text>',
        '</g></svg>',
    ])
    archivo.write_text("\n".join(svg), encoding="utf-8")


def main():
    grafo = crear_grafo(CONEXIONES)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inicio", choices=sorted(grafo), default="Jalisco")
    parser.add_argument("--ver", action="store_true", help="Abrir el dibujo del grafo")
    parser.add_argument("--consola", action="store_true", help="Usar la versión de texto")
    args = parser.parse_args()

    if not args.consola:
        from interfaz_grafos import iniciar_interfaz
        iniciar_interfaz(args.inicio)
        return

    print("ADA7 - PROGRAMA DE GRAFOS")
    print("Grafo no dirigido y ponderado; costos ficticios en MXN.")
    print(f"Inicio: {args.inicio}. El regreso al inicio no es obligatorio.")
    print("\nESTADOS Y SUS RELACIONES")
    for estado, vecinos in grafo.items():
        relaciones = ", ".join(f"{v} (${c:,})" for v, c in vecinos.items())
        print(f"  {estado}: {relaciones}")

    mostrar_recorrido(
        "A) RECORRIDO SIN REPETIR ESTADOS", grafo,
        recorrido_sin_repetir(grafo, args.inicio),
    )
    mostrar_recorrido(
        "B) RECORRIDO REPITIENDO AL MENOS UN ESTADO", grafo,
        recorrido_con_repeticion(grafo, args.inicio),
    )
    archivo = Path(__file__).resolve().with_name("grafo_estados.svg")
    dibujar_grafo(CONEXIONES, archivo)
    print(f"\nDibujo generado: {archivo.name}")
    print("Ábrelo en tu navegador o ejecuta este programa con --ver.")
    if args.ver:
        webbrowser.open(archivo.as_uri())


if __name__ == "__main__":
    main()
