import argparse
from collections import deque
from typing import List, Optional


class Nodo:

    def __init__(self, dato: int):
        self.dato = dato
        self.izquierdo: Optional["Nodo"] = None
        self.derecho: Optional["Nodo"] = None


class Arbol:

    def __init__(self):
        self.raiz: Optional[Nodo] = None

    def esta_vacio(self) -> bool:
        return self.raiz is None

    def insertar(self, dato: int) -> bool:
        if self.raiz is None:
            self.raiz = Nodo(dato)
            return True
        actual = self.raiz
        while True:
            if dato == actual.dato:
                return False
            if dato < actual.dato:
                if actual.izquierdo is None:
                    actual.izquierdo = Nodo(dato)
                    return True
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = Nodo(dato)
                    return True
                actual = actual.derecho

    def buscar(self, dato: int) -> bool:
        actual = self.raiz
        while actual is not None:
            if dato == actual.dato:
                return True
            actual = actual.izquierdo if dato < actual.dato else actual.derecho
        return False

    def eliminar(self, dato: int) -> bool:
        self.raiz, eliminado = self._eliminar(self.raiz, dato)
        return eliminado

    def _eliminar(self, nodo: Optional[Nodo], dato: int):
        if nodo is None:
            return None, False
        if dato < nodo.dato:
            nodo.izquierdo, eliminado = self._eliminar(nodo.izquierdo, dato)
        elif dato > nodo.dato:
            nodo.derecho, eliminado = self._eliminar(nodo.derecho, dato)
        else:
            if nodo.izquierdo is None:
                return nodo.derecho, True
            if nodo.derecho is None:
                return nodo.izquierdo, True
            sucesor = nodo.derecho
            while sucesor.izquierdo is not None:
                sucesor = sucesor.izquierdo
            nodo.dato = sucesor.dato
            nodo.derecho, _ = self._eliminar(nodo.derecho, sucesor.dato)
            eliminado = True
        return nodo, eliminado

    def inorden(self) -> List[int]:
        return self._recorrer("inorden")

    def preorden(self) -> List[int]:
        return self._recorrer("preorden")

    def postorden(self) -> List[int]:
        return self._recorrer("postorden")

    def _recorrer(self, orden: str) -> List[int]:
        resultado = []

        def visitar(nodo):
            if nodo is None:
                return
            if orden == "preorden":
                resultado.append(nodo.dato)
            visitar(nodo.izquierdo)
            if orden == "inorden":
                resultado.append(nodo.dato)
            visitar(nodo.derecho)
            if orden == "postorden":
                resultado.append(nodo.dato)

        visitar(self.raiz)
        return resultado

    def por_niveles(self) -> List[int]:
        if self.raiz is None:
            return []
        pendientes = deque([self.raiz])
        resultado = []
        while pendientes:
            nodo = pendientes.popleft()
            resultado.append(nodo.dato)
            if nodo.izquierdo is not None:
                pendientes.append(nodo.izquierdo)
            if nodo.derecho is not None:
                pendientes.append(nodo.derecho)
        return resultado

    def minimo(self) -> Optional[int]:
        actual = self.raiz
        if actual is None:
            return None
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual.dato

    def maximo(self) -> Optional[int]:
        actual = self.raiz
        if actual is None:
            return None
        while actual.derecho is not None:
            actual = actual.derecho
        return actual.dato

    def altura(self) -> int:
        def medir(nodo):
            if nodo is None:
                return 0
            return 1 + max(medir(nodo.izquierdo), medir(nodo.derecho))

        return medir(self.raiz)

    def contar_nodos(self) -> int:
        def contar(nodo):
            if nodo is None:
                return 0
            return 1 + contar(nodo.izquierdo) + contar(nodo.derecho)

        return contar(self.raiz)

    def mostrar(self) -> str:
        if self.raiz is None:
            return "(árbol vacío)"
        lineas = []

        def dibujar(nodo, nivel):
            if nodo is None:
                return
            dibujar(nodo.derecho, nivel + 1)
            lineas.append("    " * nivel + str(nodo.dato))
            dibujar(nodo.izquierdo, nivel + 1)

        dibujar(self.raiz, 0)
        return "\n".join(lineas)


def demostracion():
    arbol = Arbol()
    datos = [50, 30, 70, 20, 40, 60, 80]
    for dato in datos:
        arbol.insertar(dato)
    print("ADA6 - Árbol binario de búsqueda")
    print("Insertar:", datos)
    print("Dibujo girado (derecha arriba):\n" + arbol.mostrar())
    print("Inorden:", arbol.inorden())
    print("Preorden:", arbol.preorden())
    print("Postorden:", arbol.postorden())
    print("Por niveles:", arbol.por_niveles())
    print("Buscar 40:", arbol.buscar(40))
    print("Buscar 99:", arbol.buscar(99))
    print("Insertar 40 otra vez:", arbol.insertar(40))
    print("Nodos:", arbol.contar_nodos(), "| Altura en niveles:", arbol.altura())
    print("Mínimo:", arbol.minimo(), "| Máximo:", arbol.maximo())
    for dato, caso in [(20, "hoja"), (30, "un hijo"), (50, "dos hijos")]:
        print("Eliminar", dato, "(" + caso + "):", arbol.eliminar(dato))
        print("Inorden:", arbol.inorden())
    print("Árbol final:\n" + arbol.mostrar())


def menu():
    arbol = Arbol()
    while True:
        print("\n--- Árbol binario de búsqueda ---")
        print("1. Insertar\n2. Buscar\n3. Eliminar\n4. Recorridos")
        print("5. Estadísticas\n6. Mostrar árbol\n0. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            print("Programa finalizado.")
            return
        if opcion in ("1", "2", "3"):
            try:
                dato = int(input("Introduce un número entero: "))
            except ValueError:
                print("Entrada inválida: escribe un número entero.")
                continue
            if opcion == "1":
                print("Insertado." if arbol.insertar(dato) else "El dato ya existe.")
            elif opcion == "2":
                print("Encontrado." if arbol.buscar(dato) else "No encontrado.")
            else:
                print("Eliminado." if arbol.eliminar(dato) else "El dato no existe.")
        elif opcion == "4":
            print("Inorden:", arbol.inorden())
            print("Preorden:", arbol.preorden())
            print("Postorden:", arbol.postorden())
            print("Por niveles:", arbol.por_niveles())
        elif opcion == "5":
            print("Vacío:", arbol.esta_vacio())
            print("Cantidad de nodos:", arbol.contar_nodos())
            print("Altura en niveles:", arbol.altura())
            print("Mínimo:", arbol.minimo(), "| Máximo:", arbol.maximo())
        elif opcion == "6":
            print(arbol.mostrar())
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="Ejecuta el ejemplo preparado")
    args = parser.parse_args()
    try:
        demostracion() if args.demo else menu()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma finalizado.")
