from MyLinkedList import MyLinkedList


def main():
    lista = MyLinkedList()
    print("¿Está vacía?", lista.is_empty())

    lista.append(10)
    lista.append(20)
    lista.append(30)
    lista.prepend(5)
    lista.insert(2, 15)
    print("Después de insertar:", lista)
    print("Cantidad de elementos:", len(lista))
    print("Posición del 20:", lista.search(20))
    print("Elemento en la posición 2:", lista.get(2))

    lista.set(2, 17)
    print("Después de actualizar:", lista)
    lista.remove(20)
    print("Después de eliminar el valor 20:", lista)
    print("Dato eliminado de la posición 0:", lista.delete(0))
    print("Lista actual:", lista)

    print("Recorrido:")
    for dato in lista:
        print(dato)

    lista.clear()
    print("Después de vaciar:", lista)
    print("¿Está vacía?", lista.is_empty())


if __name__ == "__main__":
    main()
