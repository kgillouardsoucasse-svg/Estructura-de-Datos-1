import random
import time

alumnos = 500
materias = 6

nombres_materias = [
    "Matemáticas",
    "Español",
    "Inglés",
    "Historia",
    "Programación",
    "Física"
]


por_alumno = []

for i in range(alumnos):
    fila = []

    for j in range(materias):
        fila.append(random.randint(0, 10))

    por_alumno.append(fila)

por_materia = []

for j in range(materias):
    fila = []

    for i in range(alumnos):
        fila.append(por_alumno[i][j])

    por_materia.append(fila)


print("\nTABLA DE CALIFICACIONES")
print("-" * (10 + materias * 15))

print(f"{'Alumno':<10}", end="")

for j in range(materias):
    print(f"{nombres_materias[j]:<15}", end="")

print()
print("-" * (10 + materias * 15))

for i in range(alumnos):
    print(f"{i + 1:<10}", end="")

    for j in range(materias):
        print(f"{por_alumno[i][j]:<15}", end="")

    print()

print("-" * (10 + materias * 15))


inicio = time.perf_counter()

for i in range(100000):
    calificacion1 = por_alumno[320][4]

tiempo1 = time.perf_counter() - inicio


inicio = time.perf_counter()

for i in range(100000):
    calificacion2 = por_materia[4][320]

tiempo2 = time.perf_counter() - inicio


print("\nDATO SOLICITADO")
print("+----------+--------------------+--------------+")
print("| Alumno   | Materia            | Calificación |")
print("+----------+--------------------+--------------+")

materia_buscada = "5 - " + nombres_materias[4]

print(f"| {321:<8} | {materia_buscada:<18} | {calificacion1:<12} |")
print("+----------+--------------------+--------------+")


print("\nTIEMPO DE 100000 CONSULTAS")
print("+--------------------+--------------------+")
print("| Organización       | Tiempo en segundos |")
print("+--------------------+--------------------+")
print(f"| {'Por alumno':<18} | {tiempo1:<18.8f} |")
print(f"| {'Por materia':<18} | {tiempo2:<18.8f} |")
print("+--------------------+--------------------+")

if tiempo1 < tiempo2:
    print("\nEn esta ejecución fue más rápida la matriz por alumno.")
elif tiempo2 < tiempo1:
    print("\nEn esta ejecución fue más rápida la matriz por materia.")
else:
    print("\nLas dos matrices tardaron lo mismo.") 
