from pila import Pila


OPERADORES = {"+", "-", "*", "/", "^"}


def aplicar_operador(operador, izquierdo, derecho):
    if operador == "+":
        return izquierdo + derecho
    if operador == "-":
        return izquierdo - derecho
    if operador == "*":
        return izquierdo * derecho
    if operador == "/":
        if derecho == 0:
            raise ValueError("No se puede dividir entre cero.")
        return izquierdo / derecho
    if operador == "^":
        return izquierdo ** derecho
    raise ValueError(f"Operador no reconocido: {operador}")


def evaluar_expresion(expresion, notacion):
    if notacion not in ("posfija", "prefija"):
        raise ValueError("La notación debe ser posfija o prefija.")

    tokens = expresion.split()
    if not tokens:
        raise ValueError("Escribe una expresión.")

    pila = Pila()
    recorrido = tokens if notacion == "posfija" else reversed(tokens)

    for token in recorrido:
        if token in OPERADORES:
            if pila.tamano() < 2:
                raise ValueError(f"Faltan operandos para el operador '{token}'.")

            primero = pila.desapilar()
            segundo = pila.desapilar()
            
            if notacion == "posfija":
                izquierdo, derecho = segundo, primero
            else:
                izquierdo, derecho = primero, segundo

            resultado = aplicar_operador(token, izquierdo, derecho)
            pila.apilar(resultado)
        else:
            try:
                numero = float(token)
            except ValueError:
                raise ValueError(
                    f"Elemento no válido: '{token}'. Separa los elementos con espacios."
                ) from None
            pila.apilar(numero)

    if pila.tamano() != 1:
        raise ValueError("Sobran operandos o faltan operadores.")
    return pila.desapilar()


def main():
    print("EVALUADOR DE EXPRESIONES CON PILAS")
    print("Operadores: +, -, *, / y ^ (potencia).")
    print("Separa los elementos con espacios. Usa punto para los decimales.")

    while True:
        print("\n1. Notación posfija\n2. Notación prefija\n3. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion == "3":
            print("Programa terminado.")
            break
        if opcion not in ("1", "2"):
            print("Opción no válida.")
            continue

        notacion = "posfija" if opcion == "1" else "prefija"
        expresion = input(f"Expresión {notacion}: ")
        try:
            resultado = evaluar_expresion(expresion, notacion)
            print(f"Resultado: {resultado:g}")
        except (ValueError, OverflowError, ZeroDivisionError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
