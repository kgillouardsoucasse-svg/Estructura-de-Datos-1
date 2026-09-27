from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
DEPARTAMENTOS = ["Ropa", "Deportes", "Juguetería"]


def crear_arreglo():
    return [[None for _ in DEPARTAMENTOS] for _ in MESES]


def validar_posicion(mes, departamento):
    if not 0 <= mes < len(MESES) or not 0 <= departamento < len(DEPARTAMENTOS):
        raise ValueError("El mes o el departamento está fuera de rango.")


def insertar_venta(ventas, mes, departamento, monto):
    validar_posicion(mes, departamento)
    try:
        importe = Decimal(str(monto).strip().replace(",", "."))
        if not importe.is_finite() or importe < 0:
            raise ValueError("El importe debe ser un número finito mayor o igual a cero.")
        importe = importe.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except InvalidOperation as error:
        raise ValueError("Escribe un importe válido, por ejemplo 1250.50.") from error
    ventas[mes][departamento] = importe


def buscar_venta(ventas, mes, departamento):
    validar_posicion(mes, departamento)
    return ventas[mes][departamento]


def eliminar_venta(ventas, mes, departamento):
    validar_posicion(mes, departamento)
    if ventas[mes][departamento] is None:
        return False
    ventas[mes][departamento] = None
    return True


def mostrar_ventas(ventas):
    tabla = [["Mes"] + DEPARTAMENTOS]
    for nombre, fila in zip(MESES, ventas):
        tabla.append([nombre] + ["--" if monto is None else f"{monto:.2f}" for monto in fila])
    anchos = [max(len(fila[columna]) for fila in tabla) for columna in range(4)]
    for numero, fila in enumerate(tabla):
        print(" | ".join(celda.ljust(ancho) for celda, ancho in zip(fila, anchos)))
        if numero == 0:
            print("-+-".join("-" * ancho for ancho in anchos))
    print("-- = sin venta registrada")


def elegir_opcion(etiqueta, opciones):
    for numero, nombre in enumerate(opciones, start=1):
        print(f"{numero}. {nombre}")
    while True:
        try:
            numero = int(input(f"Selecciona {etiqueta}: "))
            if 1 <= numero <= len(opciones):
                return numero - 1
        except ValueError:
            pass
        print(f"Escribe un número entero entre 1 y {len(opciones)}.")


def main():
    ventas = crear_arreglo()
    while True:
        print("\nREGISTRO DE VENTAS")
        print("1. Insertar o actualizar venta")
        print("2. Buscar venta")
        print("3. Eliminar venta")
        print("4. Mostrar tabla completa")
        print("5. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "5":
            print("Programa finalizado.")
            break
        if opcion == "4":
            mostrar_ventas(ventas)
            continue
        if opcion not in ("1", "2", "3"):
            print("Opción inválida. Elige del 1 al 5.")
            continue

        mes = elegir_opcion("el mes", MESES)
        departamento = elegir_opcion("el departamento", DEPARTAMENTOS)
        referencia = f"{MESES[mes]} / {DEPARTAMENTOS[departamento]}"

        if opcion == "1":
            if buscar_venta(ventas, mes, departamento) is not None:
                respuesta = input("Ya existe una venta. ¿Reemplazarla? (s/n): ").strip().lower()
                if respuesta != "s":
                    print("Operación cancelada.")
                    continue
            while True:
                monto = input("Importe de la venta (sin separador de miles): ")
                try:
                    insertar_venta(ventas, mes, departamento, monto)
                    print(f"Venta guardada: {referencia} = {ventas[mes][departamento]:.2f}")
                    break
                except ValueError as error:
                    print(error)
        elif opcion == "2":
            monto = buscar_venta(ventas, mes, departamento)
            if monto is None:
                print(f"No hay venta registrada en {referencia}.")
            else:
                print(f"Venta encontrada: {referencia} = {monto:.2f}")
        elif opcion == "3":
            if eliminar_venta(ventas, mes, departamento):
                print(f"Venta eliminada: {referencia}.")
            else:
                print(f"No hay venta registrada en {referencia}.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma finalizado.") 
