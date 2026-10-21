from collections import deque


class Cola:
    def __init__(self, elementos=None):
        self._elementos = deque(elementos if elementos is not None else [])

    def esta_vacia(self):
        return len(self._elementos) == 0

    def encolar(self, elemento):
        self._elementos.append(elemento)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("No se puede desencolar una cola vacía.")
        return self._elementos.popleft()

    def frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")
        return self._elementos[0]

    def tamano(self):
        return len(self._elementos)

    def copiar(self):
        return Cola(self._elementos)

    def a_lista(self):
        return list(self._elementos)
