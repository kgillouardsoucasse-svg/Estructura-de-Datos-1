import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.NoSuchElementException;
import java.util.Scanner;

/** Registro de ventas mensuales en un arreglo bidimensional de 12 x 3. */
public class Ventas {
    private static final String[] MESES = {
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    };
    private static final String[] DEPARTAMENTOS = {"Ropa", "Deportes", "Juguetería"};

    // Las filas son meses y las columnas son departamentos.
    // null representa una celda sin venta registrada.
    private final BigDecimal[][] ventas = new BigDecimal[12][3];

    private void validarPosicion(int mes, int departamento) {
        if (mes < 0 || mes >= MESES.length
                || departamento < 0 || departamento >= DEPARTAMENTOS.length) {
            throw new IllegalArgumentException("El mes o el departamento está fuera de rango.");
        }
    }

    /** Inserta o actualiza una venta. Los índices comienzan en cero. */
    public void insertarVenta(int mes, int departamento, BigDecimal monto) {
        validarPosicion(mes, departamento);
        if (monto == null || monto.signum() < 0) {
            throw new IllegalArgumentException("El importe debe ser mayor o igual a cero.");
        }
        ventas[mes][departamento] = monto.setScale(2, RoundingMode.HALF_UP);
    }

    /** Devuelve el importe, o null si la celda está vacía. */
    public BigDecimal buscarVenta(int mes, int departamento) {
        validarPosicion(mes, departamento);
        return ventas[mes][departamento];
    }

    /** Vacía una celda; devuelve true si había una venta registrada. */
    public boolean eliminarVenta(int mes, int departamento) {
        validarPosicion(mes, departamento);
        if (ventas[mes][departamento] == null) {
            return false;
        }
        ventas[mes][departamento] = null;
        return true;
    }

    public void mostrarVentas() {
        String[][] tabla = new String[13][4];
        tabla[0] = new String[] {"Mes", "Ropa", "Deportes", "Juguetería"};
        int[] anchos = new int[4];
        for (int mes = 0; mes < MESES.length; mes++) {
            tabla[mes + 1][0] = MESES[mes];
            for (int departamento = 0; departamento < DEPARTAMENTOS.length; departamento++) {
                BigDecimal monto = ventas[mes][departamento];
                tabla[mes + 1][departamento + 1] = monto == null ? "--" : monto.toPlainString();
            }
        }
        for (String[] fila : tabla) {
            for (int columna = 0; columna < fila.length; columna++) {
                anchos[columna] = Math.max(anchos[columna], fila[columna].length());
            }
        }
        for (String[] fila : tabla) {
            for (int columna = 0; columna < fila.length; columna++) {
                if (columna > 0) {
                    System.out.print(" | ");
                }
                System.out.printf("%-" + anchos[columna] + "s", fila[columna]);
            }
            System.out.println();
        }
        System.out.println("-- = sin venta registrada");
    }

    private static int elegirOpcion(Scanner entrada, String etiqueta, String[] opciones) {
        for (int i = 0; i < opciones.length; i++) {
            System.out.println((i + 1) + ". " + opciones[i]);
        }
        while (true) {
            System.out.print("Selecciona " + etiqueta + ": ");
            try {
                int numero = Integer.parseInt(entrada.nextLine().trim());
                if (numero >= 1 && numero <= opciones.length) {
                    return numero - 1;
                }
            } catch (NumberFormatException error) {
                // Se solicita otra entrada si el texto no es un entero.
            }
            System.out.println("Escribe un número entero entre 1 y " + opciones.length + ".");
        }
    }

    private void ejecutarMenu(Scanner entrada) {
        while (true) {
            System.out.println("\nREGISTRO DE VENTAS");
            System.out.println("1. Insertar o actualizar venta");
            System.out.println("2. Buscar venta");
            System.out.println("3. Eliminar venta");
            System.out.println("4. Mostrar tabla completa");
            System.out.println("5. Salir");
            System.out.print("Selecciona una opción: ");
            String opcion = entrada.nextLine().trim();
            if (opcion.equals("5")) {
                return;
            }
            if (opcion.equals("4")) {
                mostrarVentas();
                continue;
            }
            if (!opcion.equals("1") && !opcion.equals("2") && !opcion.equals("3")) {
                System.out.println("Opción inválida. Elige del 1 al 5.");
                continue;
            }
            int mes = elegirOpcion(entrada, "el mes", MESES);
            int departamento = elegirOpcion(entrada, "el departamento", DEPARTAMENTOS);
            String referencia = MESES[mes] + " / " + DEPARTAMENTOS[departamento];
            switch (opcion) {
                case "1":
                    if (buscarVenta(mes, departamento) != null) {
                        System.out.print("Ya existe una venta. ¿Reemplazarla? (s/n): ");
                        if (!entrada.nextLine().trim().equalsIgnoreCase("s")) {
                            System.out.println("Operación cancelada.");
                            break;
                        }
                    }
                    while (true) {
                        System.out.print("Importe de la venta (sin separador de miles): ");
                        String texto = entrada.nextLine().trim().replace(',', '.');
                        try {
                            insertarVenta(mes, departamento, new BigDecimal(texto));
                            System.out.println("Venta guardada: " + referencia + " = "
                                    + buscarVenta(mes, departamento).toPlainString());
                            break;
                        } catch (NumberFormatException | ArithmeticException error) {
                            System.out.println("Escribe un importe válido, por ejemplo 1250.50.");
                        } catch (IllegalArgumentException error) {
                            System.out.println(error.getMessage());
                        }
                    }
                    break;
                case "2":
                    BigDecimal monto = buscarVenta(mes, departamento);
                    if (monto == null) {
                        System.out.println("No hay venta registrada en " + referencia + ".");
                    } else {
                        System.out.println("Venta encontrada: " + referencia + " = " + monto.toPlainString());
                    }
                    break;
                case "3":
                    if (eliminarVenta(mes, departamento)) {
                        System.out.println("Venta eliminada: " + referencia + ".");
                    } else {
                        System.out.println("No hay venta registrada en " + referencia + ".");
                    }
                    break;
                default:
                    break;
            }
        }
    }

    public static void main(String[] args) {
        Ventas registro = new Ventas();
        try (Scanner entrada = new Scanner(System.in)) {
            registro.ejecutarMenu(entrada);
        } catch (NoSuchElementException error) {
            // Permite finalizar si se cierra la entrada de la consola.
        }
        System.out.println("\nPrograma finalizado.");
    }
}
