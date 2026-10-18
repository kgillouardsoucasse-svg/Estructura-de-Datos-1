from pila import Pila


class Navegador:
    def __init__(self):
        self.historial = Pila()
        self.adelante = Pila()

    def visitar(self, sitio):
        sitio = sitio.strip()
        if not sitio:
            raise ValueError("El nombre o la dirección del sitio no puede estar vacío.")
        self.historial.apilar(sitio)
        self.adelante.vaciar()
        return self.actual()

    def actual(self):
        if self.historial.esta_vacia():
            return None
        return self.historial.cima()

    def retroceder(self):
        if self.historial.tamano() <= 1:
            raise ValueError("No hay un sitio anterior al que regresar.")
        self.adelante.apilar(self.historial.desapilar())
        return self.actual()

    def avanzar(self):
        if self.adelante.esta_vacia():
            raise ValueError("No hay un sitio siguiente al que avanzar.")
        self.historial.apilar(self.adelante.desapilar())
        return self.actual()

    def mostrar_historial(self):
        if self.historial.esta_vacia():
            print("Todavía no has visitado sitios.")
            return
        print("\nHistorial de la ruta actual (del más antiguo al más reciente):")
        sitios = self.historial.elementos()
        for indice, sitio in enumerate(sitios, start=1):
            marca = " <- actual / cima" if indice == len(sitios) else ""
            print(f"{indice}. {sitio}{marca}")
        pendientes = self.adelante.elementos()
        if pendientes:
            print("Sitios disponibles para avanzar:")
            for sitio in reversed(pendientes):
                print(f"- {sitio}")


def main():
    navegador = Navegador()
    print("HISTORIAL DE NAVEGACIÓN CON PILAS")
    print("Simulación: escribe nombres o direcciones; no se abren páginas reales.")

    while True:
        print(f"\nSitio actual: {navegador.actual() or '(ninguno)'}")
        print("1. Visitar sitio\n2. Retroceder\n3. Avanzar\n4. Ver historial\n5. Salir")
        opcion = input("Elige una opción: ").strip()
        try:
            if opcion == "1":
                sitio = input("Sitio que quieres visitar: ")
                print(f"Visitando: {navegador.visitar(sitio)}")
            elif opcion == "2":
                print(f"Regresaste a: {navegador.retroceder()}")
            elif opcion == "3":
                print(f"Avanzaste a: {navegador.avanzar()}")
            elif opcion == "4":
                navegador.mostrar_historial()
            elif opcion == "5":
                print("Programa terminado.")
                break
            else:
                print("Opción no válida.")
        except ValueError as error:
            print(f"Aviso: {error}")


if __name__ == "__main__":
    main()
