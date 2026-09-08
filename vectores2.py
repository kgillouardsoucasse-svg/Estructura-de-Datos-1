import random
import statistics

numeros = []


for i in range(50):
    numero = random.randint(1, 100)
    numeros.append(numero)

print("Numeros:")
print(numeros)


media = statistics.mean(numeros) 
mediana = statistics.median(numeros)
moda = statistics.multimode(numeros)
varianza = statistics.pvariance(numeros)
desviacion = statistics.pstdev(numeros)
 
print("Media =", media)
print("Mediana =", mediana)
print("Moda =", moda)
print("Varianza =", varianza)
print("Desviacion estandar =", desviacion)