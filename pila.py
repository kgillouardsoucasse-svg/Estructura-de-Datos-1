class Pila:

    def __init__(self):
        self._elementos = []

    def esta_vacia(self):
        return len(self._elementos) == 0

    def apilar(self, elemento):
        self._elementos.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("No se puede desapilar: la pila está vacía.")
        return self._elementos.pop()

    def cima(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía; no tiene cima.")
        return self._elementos[-1]

    def tamano(self):
        return len(self._elementos)

    def elementos(self):
        return self._elementos.copy()

    def vaciar(self):
        self._elementos.clear() 
