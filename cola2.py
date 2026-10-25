class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    def __init__(self):
        self._frente = None
        self._final = None
        self._tamano = 0

    def esta_vacia(self):
        return self._frente is None

    def encolar(self, dato):

        nuevo = Nodo(dato)
        if self.esta_vacia():
            self._frente = nuevo
        else:
            self._final.siguiente = nuevo
        self._final = nuevo
        self._tamano += 1

    def desencolar(self):
       
        if self.esta_vacia():
            raise IndexError("No se puede desencolar: la cola está vacía")

        dato = self._frente.dato
        self._frente = self._frente.siguiente
        self._tamano -= 1
        if self._frente is None:
            self._final = None
        return dato

    def frente(self):
       
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._frente.dato

    def tamano(self):
        return self._tamano

    def __str__(self):
        elementos = []
        actual = self._frente
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return "Frente -> " + " -> ".join(elementos) + " -> Final"
