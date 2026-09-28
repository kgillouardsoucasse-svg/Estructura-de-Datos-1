# Estructura-de-Datos-1

JAVA Y PYTHON

# Registro de ventas mensuales en Java

Programa de consola que almacena las ventas mensuales de **Ropa, Deportes y Juguetería** en un arreglo bidimensional de **12 filas por 3 columnas**:

```java
private final BigDecimal[][] ventas = new BigDecimal[12][3];
```

Cada fila corresponde a un mes, de enero a diciembre; cada columna corresponde a un departamento. Cada celda guarda un único importe mensual. Una celda vacía contiene `null`, lo que permite distinguirla de una venta de cero.

Los datos se conservan en memoria durante la ejecución y se pierden al cerrar el programa.

## Compilar y ejecutar

Necesitas un JDK de Java 8 o posterior. No se necesitan bibliotecas externas.

Guarda `Ventas.java` y abre una terminal en la carpeta que lo contiene. Compila y ejecuta:

```sh
javac -encoding UTF-8 Ventas.java
java Ventas
```

El nombre del archivo debe ser `Ventas.java`, respetando la mayúscula, porque la clase pública se llama `Ventas`.

## Funcionamiento de los métodos

| Método | Explicación |
| --- | --- |
| `insertarVenta(int mes, int departamento, BigDecimal monto)` | Valida la posición y el importe. Guarda la venta en `ventas[mes][departamento]`; si ya existe una, la reemplaza. El menú pide confirmación antes de reemplazarla. |
| `buscarVenta(int mes, int departamento)` | Busca una venta por mes y departamento. Devuelve su importe, o `null` si la celda está vacía. |
| `eliminarVenta(int mes, int departamento)` | Cambia el contenido de la celda a `null`. Devuelve `true` si eliminó un registro o `false` si no había venta. |
| `mostrarVentas()` | Recorre el arreglo y muestra los 12 meses y los 3 departamentos en una tabla. Las celdas vacías aparecen como `--`. |
| `validarPosicion(int mes, int departamento)` | Comprueba que el mes y el departamento estén dentro de los límites del arreglo. |
| `elegirOpcion(Scanner entrada, String etiqueta, String[] opciones)` | Muestra opciones numeradas, solicita una selección válida y devuelve su índice. |
| `ejecutarMenu(Scanner entrada)` | Repite el menú y llama a los métodos correspondientes hasta que el usuario elige salir. |
| `main(String[] args)` | Crea el registro de ventas, abre la entrada de consola y ejecuta el menú. |

Internamente, los índices comienzan en cero: enero es `0`, diciembre es `11`, Ropa es `0`, Deportes es `1` y Juguetería es `2`. En el menú, el usuario elige meses del 1 al 12 y departamentos del 1 al 3.

Los importes se representan con `BigDecimal`, una clase estándar de Java para números decimales. Se aceptan importes no negativos, con punto o coma decimal y sin separadores de miles. Se redondean a dos decimales mediante `RoundingMode.HALF_UP`; por ejemplo, `12.345` se guarda como `12.35`.

## Ejemplo de uso del menú

1. Selecciona **1. Insertar o actualizar venta**.
2. Elige **1. Enero** y **1. Ropa**.
3. Introduce `1500.50`.
4. Selecciona **2. Buscar venta**, enero y Ropa: aparecerá `1500.50`.
5. Selecciona **4. Mostrar tabla completa** para consultar el arreglo.
6. Selecciona **3. Eliminar venta**, enero y Ropa. La celda quedará vacía.
7. Selecciona **5. Salir** para finalizar.

## Ejemplo de llamadas a los métodos

Este fragmento puede utilizarse dentro de un método Java, importando `java.math.BigDecimal`:

```java
Ventas registro = new Ventas();
registro.insertarVenta(0, 0, new BigDecimal("1500.50"));
System.out.println(registro.buscarVenta(0, 0));    // 1500.50
System.out.println(registro.eliminarVenta(0, 0)); // true
System.out.println(registro.buscarVenta(0, 0));    // null
```
# Registro de ventas mensuales en Python

Programa de consola que administra las ventas mensuales de los departamentos de **Ropa, Deportes y Juguetería** mediante un arreglo bidimensional de **12 filas por 3 columnas**, representado en Python como una lista de listas.

Cada fila corresponde a un mes, de enero a diciembre, y cada columna corresponde a un departamento. Cada celda guarda un importe mensual. Una celda sin venta registrada contiene `None`, lo que permite distinguirla de una venta de cero.

Los datos se conservan en memoria durante la ejecución y se pierden al cerrar el programa.

## Requisitos y ejecución

- Python 3.6 o posterior.
- El archivo `ventas.py`.
- No requiere instalar bibliotecas externas.

Abre una terminal en la carpeta donde guardaste el programa y ejecuta:

```sh
python ventas.py
```

En Windows también puedes usar `py ventas.py` si tienes instalado el lanzador de Python.

## Estructura del arreglo

```python
ventas = [[None for _ in DEPARTAMENTOS] for _ in MESES]
```

Los índices internos comienzan en cero:

| Elemento | Índices |
| --- | --- |
| Meses | Enero: `0`, febrero: `1`, ..., diciembre: `11` |
| Departamentos | Ropa: `0`, Deportes: `1`, Juguetería: `2` |

Por ejemplo, `ventas[0][0]` contiene la venta de enero del departamento de Ropa.

El menú presenta los meses del 1 al 12 y los departamentos del 1 al 3. El programa convierte la selección del usuario al índice correspondiente.

## Explicación de las funciones

### `crear_arreglo()`

Crea y devuelve el arreglo de 12 filas independientes y 3 columnas. Todas las celdas comienzan con `None`.

### `insertar_venta(ventas, mes, departamento, monto)`

Valida la posición y convierte el importe a `Decimal`. Rechaza valores negativos, no numéricos o no finitos. Redondea el importe a dos decimales y lo guarda en `ventas[mes][departamento]`.

Si la celda ya contiene una venta, la función reemplaza el importe anterior. El menú solicita confirmación antes de llamar a esta función para reemplazar una venta existente.

### `buscar_venta(ventas, mes, departamento)`

Valida la posición y devuelve el importe de la celda indicada. La búsqueda se realiza por mes y departamento. Si no existe una venta registrada, devuelve `None`.

### `eliminar_venta(ventas, mes, departamento)`

Valida la posición y cambia el contenido de la celda a `None`. Devuelve `True` si eliminó una venta o `False` si la celda ya estaba vacía. No elimina la fila ni la columna del arreglo.

### `mostrar_ventas(ventas)`

Recorre el arreglo y muestra una tabla con los 12 meses y los 3 departamentos. Los importes aparecen con dos decimales y las celdas vacías se representan con `--`.

### `validar_posicion(mes, departamento)`

Comprueba que el mes esté entre `0` y `11` y que el departamento esté entre `0` y `2`. Si algún índice está fuera de rango, genera un error `ValueError`.

### `elegir_opcion(etiqueta, opciones)`

Muestra una lista de opciones numeradas y solicita una selección. Repite la solicitud si el usuario no escribe un entero dentro del rango permitido. Devuelve el índice de la opción elegida.

### `main()`

Crea el arreglo y ejecuta el menú principal. Permite insertar o actualizar, buscar, eliminar y mostrar ventas, así como salir del programa.

## Manejo de importes

Se utiliza `Decimal`, de la biblioteca estándar de Python, para representar los importes decimales. El programa acepta punto o coma decimal, sin separadores de miles; por ejemplo, `1500.50` o `1500,50`.

Los importes se redondean a dos decimales con `ROUND_HALF_UP`: `12.345` se guarda como `12.35`. Una venta de `0.00` es válida y se distingue de una celda vacía.

## Ejemplo de uso

1. Selecciona **1. Insertar o actualizar venta**.
2. Elige **1. Enero** y **1. Ropa**.
3. Introduce el importe `1500.50`.
4. Selecciona **2. Buscar venta** y elige enero y Ropa: aparecerá `1500.50`.
5. Selecciona **4. Mostrar tabla completa** para consultar el arreglo.
6. Selecciona **3. Eliminar venta**, enero y Ropa. La celda quedará vacía.
7. Selecciona **5. Salir** para finalizar.

También puedes importar las funciones desde otro archivo ubicado en la misma carpeta:

```python
from ventas import crear_arreglo, insertar_venta, buscar_venta, eliminar_venta

ventas = crear_arreglo()
insertar_venta(ventas, 0, 0, "1500.50")
print(buscar_venta(ventas, 0, 0))    # 1500.50
print(eliminar_venta(ventas, 0, 0))  # True
print(buscar_venta(ventas, 0, 0))    # None
```
