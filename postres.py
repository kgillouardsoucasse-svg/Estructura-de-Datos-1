from dataclasses import dataclass, field
import unicodedata


def limpiar(texto):
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("El nombre no puede estar vacío.")
    return unicodedata.normalize("NFC", " ".join(texto.split()))


def clave(texto):
    return limpiar(texto).casefold()


def orden(texto):
    nombre = clave(texto)
    tabla = str.maketrans("áéíóúü", "aeiouu")
    return nombre.translate(tabla).replace("ñ", "n~"), nombre


@dataclass
class Nodo:
    ingrediente: str
    siguiente: "Nodo" = None


class ListaIngredientes:
    def __init__(self, ingredientes=()):
        self.cabeza = None  
        for ingrediente in ingredientes:
            self.agregar(ingrediente)

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.ingrediente
            actual = actual.siguiente

    def agregar(self, ingrediente):
        nuevo = Nodo(limpiar(ingrediente))
        if self.cabeza is None:
            self.cabeza = nuevo
            return
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def eliminar(self, ingrediente):
        buscado = clave(ingrediente)
        anterior, actual = None, self.cabeza
        while actual is not None:
            if clave(actual.ingrediente) == buscado:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                actual.siguiente = None
                return True
            anterior, actual = actual, actual.siguiente
        return False

    def quitar_repetidos(self):
        vistos = set()
        anterior, actual = None, self.cabeza
        eliminados = 0
        while actual is not None:
            siguiente = actual.siguiente
            nombre = clave(actual.ingrediente)
            if nombre in vistos:
                anterior.siguiente = siguiente
                actual.siguiente = None
                eliminados += 1
            else:
                vistos.add(nombre)
                anterior = actual
            actual = siguiente
        return eliminados


@dataclass
class Postre:
    nombre: str
    ingredientes: ListaIngredientes = field(default_factory=ListaIngredientes)


def buscar(POSTRES, nombre):
    buscado = clave(nombre)
    for postre in POSTRES:
        if clave(postre.nombre) == buscado:
            return postre
    raise ValueError("El postre no existe.")


def consultar(POSTRES, nombre):  
    postre = buscar(POSTRES, nombre)
    valores = list(postre.ingredientes)
    print(postre.nombre + ": " + (", ".join(valores) if valores
                                  else "Sin ingredientes."))


def insertar_ingredientes(POSTRES, nombre, ingredientes):  
    postre = buscar(POSTRES, nombre)
    nuevos = [limpiar(valor) for valor in ingredientes]
    if not nuevos:
        raise ValueError("Debe ingresar al menos un ingrediente.")
    for ingrediente in nuevos:
        postre.ingredientes.agregar(ingrediente)


def eliminar_ingrediente(POSTRES, nombre, ingrediente):  
    postre = buscar(POSTRES, nombre)
    if not postre.ingredientes.eliminar(ingrediente):
        raise ValueError("El ingrediente no existe en ese postre.")


def alta_postre(POSTRES, nombre, ingredientes):  
    nombre = limpiar(nombre)
    if any(clave(p.nombre) == clave(nombre) for p in POSTRES):
        raise ValueError("El postre ya existe.")
    nuevo = Postre(nombre, ListaIngredientes(ingredientes))
    posicion = 0
    while posicion < len(POSTRES):
        if orden(POSTRES[posicion].nombre) > orden(nombre):
            break
        posicion += 1
    POSTRES.insert(posicion, nuevo)


def baja_postre(POSTRES, nombre): 
    postre = buscar(POSTRES, nombre)
    actual = postre.ingredientes.cabeza
    postre.ingredientes.cabeza = None
    while actual is not None:
        siguiente = actual.siguiente
        actual.siguiente = None
        actual = siguiente
    POSTRES.remove(postre)


def eliminar_repetidos(POSTRES): 
    unicos, por_nombre = [], {}
    postres_eliminados = ingredientes_eliminados = 0
    for postre in POSTRES:
        nombre = clave(postre.nombre)
        if nombre in por_nombre:
            destino = por_nombre[nombre].ingredientes
            for ingrediente in postre.ingredientes:
                destino.agregar(ingrediente)
            postres_eliminados += 1
        else:
            por_nombre[nombre] = postre
            unicos.append(postre)
    for postre in unicos:
        ingredientes_eliminados += postre.ingredientes.quitar_repetidos()
    POSTRES[:] = sorted(unicos, key=lambda p: orden(p.nombre))
    return postres_eliminados, ingredientes_eliminados


def datos_ejemplo():
    POSTRES = []
    alta_postre(POSTRES, "Flan", ["Leche", "Huevo", "Azúcar"])
    alta_postre(POSTRES, "Arroz con leche", ["Arroz", "Leche", "Canela"])
    alta_postre(POSTRES, "Gelatina", [])
    return POSTRES


def demostracion_repetidos():
    ejemplo = [
        Postre("Flan", ListaIngredientes(["Leche", "Huevo", "Leche"])),
        Postre("flan", ListaIngredientes(["Azúcar", "Huevo"])),
        Postre("Gelatina", ListaIngredientes()),
    ]
    print("Antes:")
    for p in ejemplo:
        print(p.nombre, "->", list(p.ingredientes))
    resultado = eliminar_repetidos(ejemplo)
    print("Después:")
    for p in ejemplo:
        print(p.nombre, "->", list(p.ingredientes))
    print("Postres eliminados:", resultado[0])
    print("Ingredientes repetidos eliminados:", resultado[1])


def leer_ingredientes(permitir_vacio=False):
    texto = input("Ingredientes separados por comas: ")
    if permitir_vacio and not texto.strip():
        return []
    return [limpiar(parte) for parte in texto.split(",")]


def main():
    POSTRES = datos_ejemplo()
    while True:
        print("\n1. Consultar ingredientes\n2. Insertar ingredientes"
              "\n3. Eliminar un ingrediente\n4. Dar de alta un postre"
              "\n5. Dar de baja un postre\n6. Eliminar repetidos"
              "\n7. Mostrar todos\n8. Demostración de repetidos\n0. Salir")
        try:
            opcion = input("Opción: ").strip()
            if opcion == "0":
                break
            if opcion in {"1", "2", "3", "4", "5"}:
                nombre = input("Nombre del postre: ")
                if opcion == "1":
                    consultar(POSTRES, nombre)
                elif opcion == "2":
                    insertar_ingredientes(POSTRES, nombre, leer_ingredientes())
                    print("Ingredientes agregados.")
                elif opcion == "3":
                    ingrediente = input("Ingrediente que desea eliminar: ")
                    eliminar_ingrediente(POSTRES, nombre, ingrediente)
                    print("Ingrediente eliminado.")
                elif opcion == "4":
                    alta_postre(POSTRES, nombre, leer_ingredientes(True))
                    print("Postre registrado.")
                else:
                    baja_postre(POSTRES, nombre)
                    print("Postre y sus ingredientes eliminados.")
            elif opcion == "6":
                p, i = eliminar_repetidos(POSTRES)
                print(f"Eliminados: {p} postres y {i} ingredientes repetidos.")
            elif opcion == "7":
                if not POSTRES:
                    print("No hay postres registrados.")
                for postre in POSTRES:
                    consultar(POSTRES, postre.nombre)
            elif opcion == "8":
                demostracion_repetidos()
            else:
                print("Opción inválida.")
        except ValueError as error:
            print("Error:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
            break


if __name__ == "__main__":
    main()
