from cola import Cola

SERVICIOS = {1: "Pólizas", 2: "Siniestros", 3: "Pagos"}


class SistemaSeguros:
    def __init__(self):
        self.colas = {numero: Cola() for numero in SERVICIOS}
        self.siguiente_turno = {numero: 1 for numero in SERVICIOS}

    def validar_servicio(self, servicio):
        if servicio not in self.colas:
            raise ValueError("Servicio inválido. Usa 1, 2 o 3.")

    def registrar_cliente(self, servicio):
        self.validar_servicio(servicio)
        turno = self.siguiente_turno[servicio]
        self.colas[servicio].encolar(turno)
        self.siguiente_turno[servicio] += 1
        return turno

    def atender_cliente(self, servicio):
        self.validar_servicio(servicio)
        if self.colas[servicio].esta_vacia():
            return None
        return self.colas[servicio].desencolar()


def interpretar_comando(texto):
    texto = texto.strip().upper()
    if texto == "S":
        return "S", None
    if not texto or texto[0] not in ("C", "A"):
        raise ValueError("Comando inválido. Usa C1, A1 o S para salir.")
    numero = texto[1:].strip()
    if not numero.isascii() or not numero.isdecimal():
        raise ValueError("Escribe C o A seguida del número de servicio, por ejemplo C1.")
    if numero not in ("1", "2", "3"):
        raise ValueError("Servicio inválido. Usa 1, 2 o 3.")
    return texto[0], int(numero)


def main():
    sistema = SistemaSeguros()
    print("COLAS DE ATENCIÓN - COMPAÑÍA DE SEGUROS")
    for numero, nombre in SERVICIOS.items():
        print(f"{numero}: {nombre}")
    print("C + servicio: llegada. A + servicio: atender. S: salir.")
    print("Ejemplos: C1, C 2, A1, A 3")

    while True:
        try:
            comando, servicio = interpretar_comando(input("Comando: "))
            if comando == "S":
                print("Simulación finalizada.")
                break
            nombre = SERVICIOS[servicio]
            if comando == "C":
                turno = sistema.registrar_cliente(servicio)
                print(f"Servicio {servicio} ({nombre}): turno asignado {turno}.")
            else:
                turno = sistema.atender_cliente(servicio)
                if turno is None:
                    print(f"Servicio {servicio} ({nombre}): no hay clientes en espera.")
                else:
                    print(f"Servicio {servicio} ({nombre}): llamando al turno {turno}.")
        except ValueError as error:
            print(error)
        except (EOFError, KeyboardInterrupt):
            print("\nSimulación finalizada.")
            break


if __name__ == "__main__":
    main()
