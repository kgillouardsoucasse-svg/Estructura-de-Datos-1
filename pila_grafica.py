import tkinter as tk
from tkinter import messagebox


class PilaGrafica:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Funcionamiento de una Pila")
        self.ventana.geometry("760x560")
        self.ventana.config(bg="#eef3ff")

        self.pila = []
        self.max_elementos = 8

        self.crear_interfaz()
        self.dibujar_pila()

    def crear_interfaz(self):
        titulo = tk.Label(
            self.ventana,
            text="Pila en Python",
            font=("Arial", 24, "bold"),
            bg="#eef3ff",
            fg="#1d3557",
        )
        titulo.pack(pady=12)

        descripcion = tk.Label(
            self.ventana,
            text="Una pila trabaja con el principio LIFO: el ultimo en entrar es el primero en salir.",
            font=("Arial", 12),
            bg="#eef3ff",
            fg="#33415c",
        )
        descripcion.pack()

        panel = tk.Frame(self.ventana, bg="#eef3ff")
        panel.pack(pady=14)

        tk.Label(
            panel,
            text="Dato:",
            font=("Arial", 12, "bold"),
            bg="#eef3ff",
            fg="#1d3557",
        ).grid(row=0, column=0, padx=6)

        self.entrada = tk.Entry(panel, width=18, font=("Arial", 12))
        self.entrada.grid(row=0, column=1, padx=6)
        self.entrada.bind("<Return>", lambda event: self.push())

        tk.Button(panel, text="Push / Insertar", command=self.push, bg="#457b9d", fg="white", width=14).grid(
            row=0, column=2, padx=6
        )
        tk.Button(panel, text="Pop / Eliminar", command=self.pop, bg="#e63946", fg="white", width=14).grid(
            row=0, column=3, padx=6
        )
        tk.Button(panel, text="Peek / Ver cima", command=self.peek, bg="#2a9d8f", fg="white", width=14).grid(
            row=0, column=4, padx=6
        )
        tk.Button(panel, text="Limpiar", command=self.limpiar, bg="#6c757d", fg="white", width=10).grid(
            row=0, column=5, padx=6
        )

        cuerpo = tk.Frame(self.ventana, bg="#eef3ff")
        cuerpo.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(cuerpo, width=430, height=350, bg="white", highlightthickness=2, highlightbackground="#b8c0d9")
        self.canvas.grid(row=0, column=0, padx=10)

        info = tk.Frame(cuerpo, bg="#eef3ff")
        info.grid(row=0, column=1, sticky="n", padx=20)

        tk.Label(info, text="Operaciones", font=("Arial", 16, "bold"), bg="#eef3ff", fg="#1d3557").pack(anchor="w")
        tk.Label(
            info,
            text=(
                "Push: agrega un dato a la cima.\n"
                "Pop: elimina el dato de la cima.\n"
                "Peek: muestra el dato superior.\n\n"
                "La pila solo permite trabajar\n"
                "directamente con el ultimo dato."
            ),
            font=("Arial", 12),
            bg="#eef3ff",
            fg="#33415c",
            justify="left",
        ).pack(anchor="w", pady=8)

        self.estado = tk.Label(
            info,
            text="Estado: pila vacia",
            font=("Arial", 12, "bold"),
            bg="#eef3ff",
            fg="#1d3557",
            justify="left",
            wraplength=230,
        )
        self.estado.pack(anchor="w", pady=12)

    def push(self):
        dato = self.entrada.get().strip()

        if not dato:
            messagebox.showwarning("Dato vacio", "Escribe un dato para insertarlo en la pila.")
            return

        if len(self.pila) >= self.max_elementos:
            messagebox.showwarning("Pila llena", "La pila llego al limite de elementos.")
            return

        self.pila.append(dato)
        self.entrada.delete(0, tk.END)
        self.estado.config(text=f"Estado: se inserto '{dato}' en la cima.")
        self.dibujar_pila()

    def pop(self):
        if not self.pila:
            messagebox.showinfo("Pila vacia", "No hay elementos para eliminar.")
            return

        dato = self.pila.pop()
        self.estado.config(text=f"Estado: se elimino '{dato}' de la cima.")
        self.dibujar_pila()

    def peek(self):
        if not self.pila:
            messagebox.showinfo("Pila vacia", "No hay elemento en la cima.")
            return

        dato = self.pila[-1]
        self.estado.config(text=f"Estado: la cima de la pila es '{dato}'.")
        messagebox.showinfo("Cima de la pila", f"El elemento superior es: {dato}")
        self.dibujar_pila()

    def limpiar(self):
        self.pila.clear()
        self.estado.config(text="Estado: pila vacia")
        self.dibujar_pila()

    def dibujar_pila(self):
        self.canvas.delete("all")

        self.canvas.create_text(215, 25, text="Representacion grafica de la pila", font=("Arial", 14, "bold"), fill="#1d3557")
        self.canvas.create_line(105, 320, 325, 320, width=4, fill="#1d3557")
        self.canvas.create_line(105, 80, 105, 320, width=4, fill="#1d3557")
        self.canvas.create_line(325, 80, 325, 320, width=4, fill="#1d3557")

        if not self.pila:
            self.canvas.create_text(215, 200, text="Pila vacia", font=("Arial", 16, "bold"), fill="#6c757d")
            return

        bloque_alto = 28
        espacio = 6
        base_y = 312

        for indice, dato in enumerate(self.pila):
            y2 = base_y - indice * (bloque_alto + espacio)
            y1 = y2 - bloque_alto
            color = "#a8dadc" if indice != len(self.pila) - 1 else "#f4a261"

            self.canvas.create_rectangle(125, y1, 305, y2, fill=color, outline="#1d3557", width=2)
            self.canvas.create_text(215, (y1 + y2) / 2, text=dato, font=("Arial", 12, "bold"), fill="#1d3557")

        cima_y = base_y - (len(self.pila) - 1) * (bloque_alto + espacio) - bloque_alto / 2
        self.canvas.create_text(355, cima_y, text="<-- cima", font=("Arial", 11, "bold"), fill="#e76f51", anchor="w")


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = PilaGrafica(ventana_principal)
    ventana_principal.mainloop()
