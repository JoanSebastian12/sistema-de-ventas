using System;
using System.Collections.Generic;

class Program
{
    // Variables globales (listas paralelas para simular base de datos sin POO)
    static List<string> nombres = new List<string>();
    static List<decimal> precios = new List<decimal>();
    static List<int> stocks = new List<int>();
    
    // Estadísticas
    static decimal totalVentasCaja = 0m;
    static int cantidadVentasRealizadas = 0;
    static List<int> unidadesVendidasPorProducto = new List<int>(); // Para producto más vendido

    static void Main(string[] args)
    {
        int opcion;
        do
        {
            ImprimirEncabezado("SISTEMA GESTOR DE VENTAS E INVENTARIO (MINI-POS)");
            Console.WriteLine("1. Registrar nuevo producto en inventario");
            Console.WriteLine("2. Consultar inventario completo");
            Console.WriteLine("3. Registrar una venta");
            Console.WriteLine("4. Ver reporte de caja y estadísticas diarias");
            Console.WriteLine("5. Salir");
            Console.WriteLine("====================================================");
            
            opcion = LeerEntero("Seleccione una opción (1-5): ", 1, 5);

            switch (opcion)
            {
                case 1:
                    RegistrarProducto();
                    break;
                case 2:
                    ConsultarInventario();
                    break;
                case 3:
                    RegistrarVenta();
                    break;
                case 4:
                    MostrarReporteCaja();
                    break;
                case 5:
                    Console.WriteLine("\nSaliendo del sistema... ¡Hasta luego!");
                    break;
            }

            if (opcion != 5)
            {
                Console.WriteLine("\nPresione cualquier tecla para continuar...");
                Console.ReadKey();
            }

        } while (opcion != 5);
    }

    static void RegistrarProducto()
    {
        ImprimirEncabezado("REGISTRAR NUEVO PRODUCTO");
        
        string nombre = "";
        while (string.IsNullOrWhiteSpace(nombre))
        {
            Console.Write("Ingrese el nombre del producto: ");
            nombre = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(nombre))
            {
                Console.WriteLine("[ERROR] El nombre no puede estar vacío.");
            }
        }

        // Validación de nombres duplicados
        bool existe = false;
        foreach (string n in nombres)
        {
            if (n.Equals(nombre, StringComparison.OrdinalIgnoreCase))
            {
                existe = true;
                break;
            }
        }

        if (existe)
        {
            Console.WriteLine("[ERROR] Ya existe un producto registrado con ese nombre.");
            return;
        }

        decimal precio = LeerDecimal("Ingrese el precio unitario ($): ", 0.01m); // Mayor a cero
        int stock = LeerEntero("Ingrese el stock inicial (cantidad disponible): ", 0, int.MaxValue); // Mayor o igual a cero

        nombres.Add(nombre);
        precios.Add(precio);
        stocks.Add(stock);
        unidadesVendidasPorProducto.Add(0); // Inicializar sus ventas en 0

        Console.WriteLine("\n[OK] Producto registrado con éxito.");
    }

    static void ConsultarInventario()
    {
        ImprimirEncabezado("INVENTARIO COMPLETO");

        if (nombres.Count == 0)
        {
            Console.WriteLine("No hay productos registrados en el inventario.");
            return;
        }

        for (int i = 0; i < nombres.Count; i++)
        {
            string alerta = stocks[i] < 5 ? " [ALERTA: BAJO STOCK]" : "";
            Console.WriteLine($"{i + 1}. {nombres[i]} | Precio: {precios[i]:C} | Stock: {stocks[i]}{alerta}");
        }
    }

    static void RegistrarVenta()
    {
        ImprimirEncabezado("REGISTRAR VENTA");

        if (nombres.Count == 0)
        {
            Console.WriteLine("No hay productos registrados para vender.");
            return;
        }

        // Mostrar lista
        for (int i = 0; i < nombres.Count; i++)
        {
            string alerta = stocks[i] < 5 ? " [ALERTA: BAJO STOCK]" : "";
            Console.WriteLine($"{i + 1}. {nombres[i]} | Precio: {precios[i]:C} | Stock: {stocks[i]}{alerta}");
        }
        Console.WriteLine();

        int indice = LeerEntero($"Seleccione el número del producto a vender (1-{nombres.Count}): ", 1, nombres.Count) - 1;
        
        int cantidad = 0;
        bool cantidadValida = false;
        while (!cantidadValida)
        {
            cantidad = LeerEntero("Ingrese la cantidad a comprar: ", 1, int.MaxValue);
            
            if (cantidad > stocks[indice])
            {
                Console.WriteLine($"[ERROR] Stock insuficiente. Solo quedan {stocks[indice]} unidades en inventario.\n");
            }
            else
            {
                cantidadValida = true;
            }
        }

        Console.Write("¿Aplica descuento de cliente frecuente (10%)? (S/N): ");
        string respuestaDescuento = Console.ReadLine();
        bool tieneDescuento = respuestaDescuento != null && respuestaDescuento.Trim().Equals("S", StringComparison.OrdinalIgnoreCase);

        decimal montoIva;
        decimal montoDescuento;
        decimal totalPagar = CalcularFactura(precios[indice], cantidad, tieneDescuento, out montoIva, out montoDescuento);
        decimal subtotal = precios[indice] * cantidad;

        // Actualizar datos
        stocks[indice] -= cantidad;
        totalVentasCaja += totalPagar;
        cantidadVentasRealizadas++;
        unidadesVendidasPorProducto[indice] += cantidad;

        // Imprimir Ticket
        ImprimirEncabezado("TICKET DE VENTA");
        Console.WriteLine($" Producto:             {nombres[indice]} (x{cantidad})");
        Console.WriteLine($" Subtotal:             {subtotal:C}");
        if (tieneDescuento)
        {
            Console.WriteLine($" Descuento (10%):     -{montoDescuento:C}");
        }
        Console.WriteLine($" IVA (19%):            +{montoIva:C}");
        Console.WriteLine(" ---------------------------------------------------");
        Console.WriteLine($" TOTAL A PAGAR:        {totalPagar:C}");
        Console.WriteLine("====================================================");
        Console.WriteLine($"\n[OK] Venta efectuada con éxito. Stock actualizado: {stocks[indice]} unidades.");
    }

    static void MostrarReporteCaja()
    {
        ImprimirEncabezado("REPORTE DE CAJA Y ESTADÍSTICAS");
        
        Console.WriteLine($"Total de ventas realizadas en la sesión: {cantidadVentasRealizadas}");
        Console.WriteLine($"Total acumulado ingresado a caja en dinero: {totalVentasCaja:C}");
        
        decimal promedio = cantidadVentasRealizadas > 0 ? totalVentasCaja / cantidadVentasRealizadas : 0;
        Console.WriteLine($"Promedio de dinero por venta: {promedio:C}");

        if (nombres.Count > 0)
        {
            int maxVentas = -1;
            string productoMax = "";
            for (int i = 0; i < nombres.Count; i++)
            {
                if (unidadesVendidasPorProducto[i] > maxVentas)
                {
                    maxVentas = unidadesVendidasPorProducto[i];
                    productoMax = nombres[i];
                }
            }
            if (maxVentas > 0)
            {
                Console.WriteLine($"Producto con mayor cantidad de unidades vendidas: {productoMax} ({maxVentas} unidades)");
            }
            else
            {
                Console.WriteLine("Producto con mayor cantidad de unidades vendidas: N/A (No hay ventas)");
            }
        }
        else
        {
            Console.WriteLine("Producto con mayor cantidad de unidades vendidas: N/A (No hay productos)");
        }
    }

    // --- Métodos Obligatorios ---

    static int LeerEntero(string mensaje, int min, int max)
    {
        int valor;
        while (true)
        {
            Console.Write(mensaje);
            string entrada = Console.ReadLine();
            
            if (int.TryParse(entrada, out valor))
            {
                if (valor >= min && valor <= max)
                {
                    return valor;
                }
                else
                {
                    Console.WriteLine($"[ERROR] Opción fuera de rango. Ingrese un valor entre {min} y {max}.\n");
                }
            }
            else
            {
                Console.WriteLine("[ERROR] Entrada no válida. Debe ingresar un número entero.\n");
            }
        }
    }

    static decimal LeerDecimal(string mensaje, decimal min)
    {
        decimal valor;
        while (true)
        {
            Console.Write(mensaje);
            string entrada = Console.ReadLine();
            
            if (decimal.TryParse(entrada, out valor))
            {
                if (valor >= min)
                {
                    return valor;
                }
                else
                {
                    Console.WriteLine($"[ERROR] Valor fuera de rango. Ingrese un decimal mayor o igual a {min}.\n");
                }
            }
            else
            {
                Console.WriteLine("[ERROR] Entrada no válida. Debe ingresar un número decimal.\n");
            }
        }
    }

    static decimal CalcularFactura(decimal precio, int cantidad, bool tieneDescuento, out decimal montoIva, out decimal montoDescuento)
    {
        decimal subtotal = precio * cantidad;
        montoDescuento = 0m;
        
        if (tieneDescuento)
        {
            montoDescuento = subtotal * 0.10m; // 10%
        }
        
        decimal baseGrabable = subtotal - montoDescuento;
        montoIva = baseGrabable * 0.19m; // 19%
        
        return baseGrabable + montoIva;
    }

    static void ImprimirEncabezado(string titulo)
    {
        Console.Clear();
        Console.WriteLine("====================================================");
        int padding = (52 - titulo.Length) / 2;
        if (padding > 0)
        {
            Console.WriteLine(new string(' ', padding) + titulo);
        }
        else
        {
            Console.WriteLine(titulo);
        }
        Console.WriteLine("====================================================");
    }
}
