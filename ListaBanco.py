
from collections import deque


class Banco:
    def __init__(self):
        self.cola_principal = deque()
        self.prioridad_1 = deque()
        self.prioridad_2 = deque()
        self.prioridad_3 = deque()
        self.historial_llegadas = []
        self.historial_atencion = []

    def agregar_cliente(self, nombre, edad, discapacidad=False):

        if edad >= 60 and discapacidad:
            tipo = "Tercera edad y discapacidad"
            prioridad = 1
        elif edad >= 60:
            tipo = "Tercera edad"
            prioridad = 2
        elif discapacidad:
            tipo = "Discapacidad"
            prioridad = 2
        else:
            tipo = "Cliente regular"
            prioridad = 3

        cliente = {
            "nombre": nombre,
            "edad": edad,
            "tipo": tipo,
            "prioridad": prioridad
        }

        self.cola_principal.append(cliente)
        self.historial_llegadas.append(cliente)

    def mostrar_llegadas(self):
        print("\n========== ORDEN DE LLEGADA ==========")

        for numero, cliente in enumerate(self.historial_llegadas, start=1):
            print(
                f"{numero}. {cliente['nombre']} - "
                f"{cliente['edad']} años - "
                f"{cliente['tipo']} - "
                f"Prioridad {cliente['prioridad']}"
            )

    def organizar_colas(self):
        while self.cola_principal:
            cliente = self.cola_principal.popleft()

            if cliente["prioridad"] == 1:
                self.prioridad_1.append(cliente)
            elif cliente["prioridad"] == 2:
                self.prioridad_2.append(cliente)
            else:
                self.prioridad_3.append(cliente)

    def atender_cliente(self):

        if self.prioridad_1:
            cliente = self.prioridad_1.popleft()
        elif self.prioridad_2:
            cliente = self.prioridad_2.popleft()
        elif self.prioridad_3:
            cliente = self.prioridad_3.popleft()
        else:
            return

        self.historial_atencion.append(cliente)

    def atender_todos(self):
        self.organizar_colas()

        while self.prioridad_1 or self.prioridad_2 or self.prioridad_3:
            self.atender_cliente()

    def mostrar_atencion(self):
        print("\n========== ORDEN DE ATENCION ==========")

        for numero, cliente in enumerate(self.historial_atencion, start=1):
            print(
                f"{numero}. {cliente['nombre']} - "
                f"{cliente['edad']} años - "
                f"{cliente['tipo']} - "
                f"Prioridad {cliente['prioridad']}"
            )

        print("\nTodos los clientes han sido atendidos.")


# SIMULACION DEL BANCO

banco = Banco()

banco.agregar_cliente("Carlos", 25)
banco.agregar_cliente("Ana", 70)
banco.agregar_cliente("Luis", 35, True)
banco.agregar_cliente("Pedro", 65, True)
banco.agregar_cliente("Maria", 28)
banco.agregar_cliente("Elena", 75, True)
banco.agregar_cliente("Jose", 60)
banco.agregar_cliente("Sofia", 19)
banco.agregar_cliente("Lucia", 42, True)
banco.agregar_cliente("Miguel", 33)

banco.mostrar_llegadas()
banco.atender_todos()
banco.mostrar_atencion()
