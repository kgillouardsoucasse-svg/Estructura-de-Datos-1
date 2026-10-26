class Nodo:
    contador = 1

    def __init__(self, dato):
        self.id = Nodo.contador
        Nodo.contador += 1
        self.INFO = dato
        self.LIGA = None


class ListaEnlazada:
    def __init__(self):
        self.inicios = {"Principal": None, "Rama": None}

    def recorrer(self, camino):
        actual = self.inicios[camino]

        while actual is not None:
            yield actual
            actual = actual.LIGA

    def insertar(self, camino, dato, posicion):
        nodos = list(self.recorrer(camino))

        if not 1 <= posicion <= len(nodos) + 1:
            print(f"La posición debe estar entre 1 y {len(nodos) + 1}.")
            return

        nuevo = Nodo(dato)

        if posicion == 1:
            nuevo.LIGA = self.inicios[camino]
            self.inicios[camino] = nuevo
        else:
            anterior = nodos[posicion - 2]
            nuevo.LIGA = anterior.LIGA
            anterior.LIGA = nuevo

        print(f"Nodo N{nuevo.id} insertado en la posición {posicion}.")

    def eliminar(self, camino, dato):
        anterior = None
        actual = self.inicios[camino]

        while actual is not None:
            if actual.INFO == dato:
                if anterior is None:
                    self.inicios[camino] = actual.LIGA
                else:
                    anterior.LIGA = actual.LIGA

                print(f"Nodo N{actual.id} retirado de {camino}.")

                if any(
                    nodo is actual
                    for nombre in self.inicios
                    for nodo in self.recorrer(nombre)
                ):
                    print("El nodo sigue siendo accesible desde el otro camino.")

                return

            anterior = actual
            actual = actual.LIGA

        print("No se encontró un nodo con ese valor.")

    def nodos_existentes(self):
        nodos = {}

        for camino in self.inicios:
            for nodo in self.recorrer(camino):
                nodos[nodo.id] = nodo

        return nodos

    def mostrar(self):
        print("\n--- RECORRIDOS ---")

        for camino in self.inicios:
            elementos = [
                f"[N{nodo.id} | INFO: {nodo.INFO}]"
                for nodo in self.recorrer(camino)
            ]

            print(f"{camino}: " + " -> ".join(elementos + ["None"]))

        nodos = self.nodos_existentes()

        if not nodos:
            print("La lista está vacía.")
            return

        print("\n--- ENLACES DE CADA NODO ---")

        for identificador in sorted(nodos):
            nodo = nodos[identificador]
            destino = f"N{nodo.LIGA.id}" if nodo.LIGA else "None"
            print(f"N{nodo.id}: INFO = {nodo.INFO}, LIGA -> {destino}")

        print("\nUn mismo identificador N indica el mismo nodo, no una copia.")

    def crear_rama(self, dato, id_destino):
        destino = self.nodos_existentes().get(id_destino)

        if destino is None:
            print("El nodo destino no existe.")
            return

        nuevo = Nodo(dato)
        nuevo.LIGA = destino
        self.inicios["Rama"] = nuevo

        print(f"Rama creada: N{nuevo.id} -> N{destino.id}.")
        print("La entrada Rama reemplaza cualquier rama anterior.")

    def cambiar_enlace(self, id_origen, id_destino):
        nodos = self.nodos_existentes()
        origen = nodos.get(id_origen)
        destino = nodos.get(id_destino)

        if origen is None or destino is None:
            print("El nodo origen o el nodo destino no existe.")
            return

        # Evitar ciclos para que los recorridos terminen en None.
        actual = destino

        while actual is not None:
            if actual is origen:
                print("No se permite ese enlace porque crearía un ciclo.")
                return

            actual = actual.LIGA

        origen.LIGA = destino

        print(f"Enlace actualizado: N{origen.id}.LIGA -> N{destino.id}.")
        print("Los nodos que queden sin acceso dejarán de mostrarse.")


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingresa un número entero válido.")


def leer_id(mensaje):
    while True:
        texto = input(mensaje).strip().upper()

        if texto.startswith("N"):
            texto = texto[1:]

        try:
            identificador = int(texto)

            if identificador > 0:
                return identificador
        except ValueError:
            pass

        print("Escribe un identificador válido, por ejemplo N2 o 2.")


def elegir_camino(lista):
    if lista.inicios["Rama"] is None:
        return "Principal"

    while True:
        print("\n¿En qué camino deseas trabajar?")
        print("1. Principal")
        print("2. Rama")

        opcion = input("Elija un camino: ").strip()

        if opcion == "1":
            return "Principal"

        if opcion == "2":
            return "Rama"

        print("Selecciona 1 o 2.")


def main():
    lista = ListaEnlazada()

    print("LISTAS SIMPLEMENTE ENLAZADAS")
    print("La lista comienza vacía.")
    print("Las posiciones empiezan en 1.")
    print("Los nodos compartidos pueden afectar ambos recorridos.")

    while True:
        print("\n- MENÚ")
        print("1. Insertar al principio")
        print("2. Insertar en medio (por posición)")
        print("3. Insertar al final")
        print("4. Eliminar un nodo")
        print("5. Mostrar lista")
        print("6. Crear rama que apunte a un nodo existente")
        print("7. Hacer que un nodo apunte a otro nodo")
        print("0. Salir")

        opcion = input("Elija una opción: ").strip()

        if opcion == "0":
            print("Programa terminado.")
            break

        elif opcion in ("1", "2", "3"):
            camino = elegir_camino(lista)
            dato = leer_entero("Ingresa el valor del nuevo nodo: ")
            cantidad = len(list(lista.recorrer(camino)))

            if opcion == "1":
                posicion = 1
            elif opcion == "2":
                posicion = leer_entero(
                    f"Posición donde insertar (1 a {cantidad + 1}): "
                )
            else:
                posicion = cantidad + 1

            lista.insertar(camino, dato, posicion)
            lista.mostrar()

        elif opcion == "4":
            camino = elegir_camino(lista)

            if lista.inicios[camino] is None:
                print("El camino seleccionado está vacío.")
                continue

            dato = leer_entero("Valor del nodo que deseas eliminar: ")
            lista.eliminar(camino, dato)
            lista.mostrar()

        elif opcion == "5":
            lista.mostrar()

        elif opcion == "6":
            if not lista.nodos_existentes():
                print("Primero inserta un nodo.")
                continue

            lista.mostrar()
            dato = leer_entero("Valor del nuevo nodo de la rama: ")
            destino = leer_id("Identificador del nodo destino (ejemplo N2): ")

            lista.crear_rama(dato, destino)
            lista.mostrar()

        elif opcion == "7":
            if not lista.nodos_existentes():
                print("Primero inserta nodos.")
                continue

            lista.mostrar()
            origen = leer_id("Identificador del nodo origen: ")
            destino = leer_id("Identificador del nodo destino: ")

            lista.cambiar_enlace(origen, destino)
            lista.mostrar()

        else:
            print("Opción inválida. Selecciona una opción del 0 al 7.")


if __name__ == "__main__":
    main()
