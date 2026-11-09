

from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from programa_grafos import (
    CONEXIONES, crear_grafo, dibujar_grafo, mostrar_recorrido,
    recorrido_con_repeticion, recorrido_sin_repetir,
)

FONDO = "#eef3f8"
TINTA = "#17324d"
GRIS = "#52667a"
VERDE = "#087f72"
NARANJA = "#b85512"
POSICIONES = {
    "Jalisco": (0.50, 0.49), "Nayarit": (0.16, 0.21),
    "Zacatecas": (0.50, 0.10), "Aguascalientes": (0.84, 0.21),
    "Guanajuato": (0.84, 0.77), "Michoacán": (0.50, 0.89),
    "Colima": (0.16, 0.77),
}


class AplicacionGrafos:
    def __init__(self, ventana, inicio="Jalisco"):
        self.ventana = ventana
        self.grafo = crear_grafo(CONEXIONES)
        self.inicio = tk.StringVar(value=inicio)
        self.resultados = []
        self.paneles = []
        ventana.title("ADA7 · Rutas entre estados de México")
        ancho = min(1220, ventana.winfo_screenwidth() - 60)
        alto = min(850, ventana.winfo_screenheight() - 85)
        ventana.geometry(f"{ancho}x{alto}")
        ventana.minsize(1000, 700)
        ventana.configure(bg=FONDO)
        self.configurar_estilo()
        self.construir_interfaz()
        self.calcular()

    def configurar_estilo(self):
        estilo = ttk.Style(self.ventana)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background=FONDO)
        estilo.configure("Card.TFrame", background="white")
        estilo.configure("TLabel", background=FONDO, foreground=TINTA,
                         font=("Segoe UI", 10))
        estilo.configure("Card.TLabel", background="white")
        estilo.configure("Title.TLabel", font=("Segoe UI", 23, "bold"))
        estilo.configure("Muted.TLabel", foreground=GRIS)
        estilo.configure("TButton", font=("Segoe UI", 10), padding=(12, 8))
        estilo.configure("Primary.TButton", foreground="white", background=VERDE)
        estilo.map("Primary.TButton", background=[("active", "#06685e")])
        estilo.configure("TCombobox", padding=6, font=("Segoe UI", 10))
        estilo.configure("TNotebook", background="white", borderwidth=0)
        estilo.configure("TNotebook.Tab", padding=(10, 10), font=("Segoe UI", 10))
        estilo.map("TNotebook.Tab", background=[("selected", "#dceeea")])
        estilo.configure("Treeview", font=("Segoe UI", 9), rowheight=29,
                         background="white", fieldbackground="white")
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), padding=7)

    def construir_interfaz(self):
        principal = ttk.Frame(self.ventana, padding=22)
        principal.pack(fill="both", expand=True)
        ttk.Label(principal, text="México, estado por estado", style="Title.TLabel").pack(anchor="w")
        ttk.Label(principal, text="ADA7  /  Grafos ponderados  /  7 estados · 11 conexiones",
                  style="Muted.TLabel").pack(anchor="w", pady=(3, 16))

        controles = ttk.Frame(principal)
        controles.pack(fill="x", pady=(0, 16))
        ttk.Label(controles, text="Estado de inicio").pack(side="left", padx=(0, 10))
        self.selector = ttk.Combobox(controles, textvariable=self.inicio,
                                     values=sorted(self.grafo), state="readonly", width=19)
        self.selector.pack(side="left")
        self.selector.bind("<<ComboboxSelected>>", lambda _: self.calcular())
        self.boton_calcular = ttk.Button(controles, text="Calcular recorridos",
                                         command=self.calcular, style="Primary.TButton")
        self.boton_calcular.pack(side="left", padx=12)
        ttk.Button(controles, text="Guardar resultados", command=self.guardar_resultados).pack(side="right")

        resumen = ttk.Frame(principal)
        resumen.pack(fill="x", pady=(0, 16))
        self.resumen_a = self.tarjeta(resumen, "A · SIN REPETIR", VERDE)
        self.resumen_b = self.tarjeta(resumen, "B · CON REPETICIÓN", NARANJA)

        cuerpo = ttk.Frame(principal)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(0, weight=1)
        cuerpo.columnconfigure(1, weight=0, minsize=415)
        cuerpo.rowconfigure(0, weight=1)
        izquierda = ttk.Frame(cuerpo, style="Card.TFrame", padding=14)
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        barra = ttk.Frame(izquierda, style="Card.TFrame")
        barra.pack(fill="x")
        ttk.Label(barra, text="Mapa de conexiones", style="Card.TLabel",
                  font=("Segoe UI", 13, "bold")).pack(side="left")
        ttk.Button(barra, text="Exportar grafo", command=self.exportar_grafo).pack(side="right")
        self.canvas = tk.Canvas(izquierda, bg="white", highlightthickness=0, width=560, height=390)
        self.canvas.pack(fill="both", expand=True, pady=8)
        self.canvas.bind("<Configure>", lambda _: self.dibujar())
        self.leyenda = ttk.Label(izquierda, text="", style="Card.TLabel", foreground=GRIS,
                                 wraplength=480, justify="left")
        self.leyenda.pack(anchor="w")

        self.pestanas = ttk.Notebook(cuerpo, width=410)
        self.pestanas.grid(row=0, column=1, sticky="nsew")
        for nombre, color in [("A · Sin repetir", VERDE), ("B · Repetir", NARANJA)]:
            panel = ttk.Frame(self.pestanas, style="Card.TFrame", padding=12)
            self.pestanas.add(panel, text=nombre)
            ruta = ttk.Label(panel, text="", style="Card.TLabel", wraplength=375,
                             justify="left", font=("Segoe UI", 11, "bold"))
            ruta.pack(fill="x", pady=(0, 10))
            repetidos = ttk.Label(panel, text="", style="Card.TLabel", foreground=color,
                                  wraplength=375)
            repetidos.pack(fill="x", pady=(0, 10))
            tabla = self.crear_tabla(panel, ("Paso", "Traslado", "MXN"), (44, 245, 70))
            total = ttk.Label(panel, text="", style="Card.TLabel",
                              font=("Segoe UI", 15, "bold"), foreground=color)
            total.pack(anchor="e", pady=(12, 0))
            self.paneles.append((ruta, repetidos, tabla, total))
        relaciones = ttk.Frame(self.pestanas, style="Card.TFrame", padding=12)
        self.pestanas.add(relaciones, text="Conexiones")
        ttk.Label(relaciones, text="Todas las rutas son bidireccionales.",
                  style="Card.TLabel").pack(anchor="w", pady=(0, 12))
        self.tabla_relaciones = self.crear_tabla(
            relaciones, ("Estado 1", "Estado 2", "MXN"), (145, 145, 70))
        for a, b, costo in CONEXIONES:
            self.tabla_relaciones.insert("", "end", values=(a, b, f"${costo:,}"))
        self.pestanas.bind("<<NotebookTabChanged>>", lambda _: self.dibujar())

        ttk.Label(principal,
                  text="Costos ficticios en MXN · Diagrama esquemático · No es obligatorio regresar al inicio",
                  style="Muted.TLabel").pack(anchor="w", pady=(14, 0))

    def tarjeta(self, padre, titulo, color):
        tarjeta = ttk.Frame(padre, style="Card.TFrame", padding=(18, 12))
        tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Label(tarjeta, text=titulo, style="Card.TLabel", foreground=color,
                  font=("Segoe UI", 10, "bold")).pack(anchor="w")
        valor = ttk.Label(tarjeta, text="", style="Card.TLabel",
                          font=("Segoe UI", 22, "bold"))
        valor.pack(anchor="w", pady=(3, 0))
        return valor

    def crear_tabla(self, padre, encabezados, anchos):
        contenedor = ttk.Frame(padre, style="Card.TFrame")
        contenedor.pack(fill="both", expand=True)
        tabla = ttk.Treeview(contenedor, columns=encabezados, show="headings", height=7)
        barra = ttk.Scrollbar(contenedor, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)
        for nombre, ancho in zip(encabezados, anchos):
            tabla.heading(nombre, text=nombre)
            tabla.column(nombre, width=ancho, minwidth=35,
                         anchor="e" if nombre == "MXN" else "w")
        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def calcular(self):
        inicio = self.inicio.get()
        self.resultados = [recorrido_sin_repetir(self.grafo, inicio),
                           recorrido_con_repeticion(self.grafo, inicio)]
        for indice, (ruta, costo) in enumerate(self.resultados):
            etiqueta, repetidos, tabla, total = self.paneles[indice]
            tabla.delete(*tabla.get_children())
            resumen = [self.resumen_a, self.resumen_b][indice]
            if ruta is None:
                etiqueta.configure(text="No existe un recorrido para esta condición.")
                repetidos.configure(text="")
                total.configure(text="Sin solución")
                resumen.configure(text="Sin solución")
                continue
            etiqueta.configure(text=" → ".join(ruta))
            cuenta = Counter(ruta)
            repeticion = ", ".join(f"{e} ({n} visitas)" for e, n in cuenta.items() if n > 1)
            repetidos.configure(text=f"7 estados visitados · {len(ruta)-1} traslados\n"
                                + (f"Se repite: {repeticion}" if repeticion else "Ningún estado repetido"))
            for paso, (a, b) in enumerate(zip(ruta, ruta[1:]), 1):
                tabla.insert("", "end", values=(paso, f"{a} → {b}", f"${self.grafo[a][b]:,}"))
            total.configure(text=f"Total: ${costo:,} MXN")
            resumen.configure(text=f"${costo:,} MXN")
        self.dibujar()

    def dibujar(self):
        if not self.resultados:
            return
        lienzo = self.canvas
        lienzo.delete("all")
        ancho, alto = lienzo.winfo_width(), lienzo.winfo_height()
        if ancho < 10 or alto < 10:
            return
        indice = self.pestanas.index(self.pestanas.select())
        ruta = self.resultados[indice][0] if indice < 2 else None
        color = VERDE if indice == 0 else NARANJA
        usos = Counter(frozenset((a, b)) for a, b in zip(ruta or [], (ruta or [])[1:]))
        posiciones = {e: (x * ancho, y * alto) for e, (x, y) in POSICIONES.items()}
        # Dibujar las líneas antes de todas las etiquetas evita tapar los costos.
        for a, b, _ in CONEXIONES:
            usada = usos[frozenset((a, b))]
            lienzo.create_line(*posiciones[a], *posiciones[b],
                               fill=color if usada else "#cdd7e1", width=4 if usada else 2,
                               tags="arista")
        for a, b, costo in CONEXIONES:
            x1, y1 = posiciones[a]
            x2, y2 = posiciones[b]
            x, y = (x1 + x2) / 2, (y1 + y2) / 2
            veces = usos[frozenset((a, b))]
            texto = f"${costo}" + (f" ×{veces}" if veces > 1 else "")
            medio = 35 if veces > 1 else 25
            lienzo.create_rectangle(x-medio, y-12, x+medio, y+12, fill="white", outline="")
            lienzo.create_text(x, y, text=texto, fill=color if veces else GRIS,
                               font=("Segoe UI", 10, "bold" if veces else "normal"), tags="costo")
        for estado, (x, y) in posiciones.items():
            orden = [str(i + 1) for i, e in enumerate(ruta or []) if e == estado]
            es_inicio = estado == self.inicio.get()
            medio = min(78, max(59, ancho * .105))
            lienzo.create_oval(x-medio, y-26, x+medio, y+26,
                               fill=color if orden else TINTA,
                               outline="#edb64e" if es_inicio else "white",
                               width=3, tags="nodo")
            lienzo.create_text(x, y-7 if orden else y, text=estado, fill="white",
                               font=("Segoe UI", 10, "bold"), tags="nombre")
            if orden:
                lienzo.create_text(x, y+11, text="Visita " + ", ".join(orden), fill="white",
                                   font=("Segoe UI", 8), tags="orden")
        self.leyenda.configure(
            wraplength=max(300, ancho-12),
            text=("Líneas de color: recorrido seleccionado. ×2: conexión usada dos veces. "
                  "Borde dorado: inicio. El orden se muestra en cada estado."
                  if ruta else "Selecciona A o B para ver su recorrido. Borde dorado: estado inicial."))

    def texto_resultados(self):
        salida = StringIO()
        with redirect_stdout(salida):
            print("ADA7 · Programa de grafos")
            print(f"Inicio: {self.inicio.get()} · Costos ficticios en MXN")
            print("No es obligatorio regresar al inicio.")
            for titulo, resultado in zip(
                    ["A) SIN REPETIR ESTADOS", "B) REPITIENDO AL MENOS UN ESTADO"], self.resultados):
                mostrar_recorrido(titulo, self.grafo, resultado)
            print("\nESTADOS Y RELACIONES (bidireccionales)")
            for a, b, costo in CONEXIONES:
                print(f"{a} <-> {b}: ${costo:,} MXN")
        return salida.getvalue()

    def guardar_resultados(self):
        destino = filedialog.asksaveasfilename(parent=self.ventana, title="Guardar resultados",
                                              defaultextension=".txt", initialfile="resultados_grafos.txt",
                                              filetypes=[("Archivo de texto", "*.txt")])
        if destino:
            try:
                Path(destino).write_text(self.texto_resultados(), encoding="utf-8")
            except OSError as error:
                messagebox.showerror("No se pudo guardar", str(error), parent=self.ventana)

    def exportar_grafo(self):
        destino = filedialog.asksaveasfilename(parent=self.ventana, title="Exportar todas las conexiones",
                                              defaultextension=".svg", initialfile="grafo_estados.svg",
                                              filetypes=[("Imagen SVG", "*.svg")])
        if destino:
            try:
                dibujar_grafo(CONEXIONES, Path(destino))
            except OSError as error:
                messagebox.showerror("No se pudo exportar", str(error), parent=self.ventana)


def iniciar_interfaz(inicio="Jalisco"):
    ventana = tk.Tk()
    AplicacionGrafos(ventana, inicio)
    ventana.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()
