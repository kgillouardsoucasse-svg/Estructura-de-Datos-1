def MemoriaEstatica():
    calificaciones = [0] * 5

    for i in range(5):
        calificaciones[i] = int(input("Introduce la calificación: "))

    print("Las calificaciones son:")
    print(calificaciones)

def MemoriaDinamica():
    frutas = []

    frutas.append("Mango")
    frutas.append("Manzana")
    frutas.append("Banana")
    frutas.append("Uvas")

    print("Frutas:")
    print(frutas)
    frutas.pop(0)
    frutas.pop(1)

    frutas.append("Sandia")

    print("Frutas modificadas:")
    print(frutas)

MemoriaEstatica()
MemoriaDinamica() 
