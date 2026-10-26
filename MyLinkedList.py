class _Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class MyLinkedList:

    def __init__(self, iterable=None):
        self._head = None
        self._tail = None
        self._size = 0
        if iterable is not None:
            for value in iterable:
                self.append(value)

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def prepend(self, value):
        node = _Node(value)
        node.next = self._head
        self._head = node
        if self._size == 0:
            self._tail = node
        self._size += 1

    def append(self, value):
        node = _Node(value)
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1

    def _check_index(self, index, allow_end=False):
        if not isinstance(index, int):
            raise TypeError("El índice debe ser un entero.")
        limit = self._size if allow_end else self._size - 1
        if index < 0 or index > limit:
            raise IndexError("Índice fuera de rango.")

    def _node_at(self, index):
        self._check_index(index)
        current = self._head
        for _ in range(index):
            current = current.next
        return current

    def insert(self, index, value):
        self._check_index(index, allow_end=True)
        if index == 0:
            self.prepend(value)
        elif index == self._size:
            self.append(value)
        else:
            previous = self._node_at(index - 1)
            node = _Node(value)
            node.next = previous.next
            previous.next = node
            self._size += 1

    def get(self, index):
        return self._node_at(index).data

    def set(self, index, value):
        self._node_at(index).data = value

    def search(self, value):
        current = self._head
        index = 0
        while current is not None:
            if current.data == value:
                return index
            current = current.next
            index += 1
        return -1

    def delete(self, index):
        self._check_index(index)
        if index == 0:
            removed = self._head
            self._head = removed.next
            if self._size == 1:
                self._tail = None
        else:
            previous = self._node_at(index - 1)
            removed = previous.next
            previous.next = removed.next
            if removed is self._tail:
                self._tail = previous
        self._size -= 1
        return removed.data

    def remove(self, value):
        index = self.search(value)
        if index == -1:
            raise ValueError("El valor no se encuentra en la lista.")
        return self.delete(index)

    def clear(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __iter__(self):
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def __contains__(self, value):
        return self.search(value) != -1

    def __str__(self):
        return " -> ".join(str(value) for value in self) + (
            " -> None" if self._size else "None"
        )
