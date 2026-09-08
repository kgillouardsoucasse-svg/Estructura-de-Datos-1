def factorial2(n):
    resultado = 1

    for i in range(1, n + 1):
        resultado *= i

    return resultado


a = 100000
print(factorial2(a))
