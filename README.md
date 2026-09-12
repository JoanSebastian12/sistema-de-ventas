# Gestor de Ventas e Inventario (Mini-POS)

**Estudiante:** Joan Sebastian Rosania Logreira

## Descripción del Proyecto

es una aplicación de consola desarrollada en C# (.NET 8) que actúa como un sistema de punto de venta (POS) y control de inventario básico para una tienda local de comercio de barrio. 

permite registrar productos, consultar el inventario, realizar ventas calculando IVA (19%) y descuentos (10%), además de mostrar un reporte de caja diario.



## Tecnologías Utilizadas
- C# y .NET 8
- Manejo de listas (`List<T>`) para almacenar datos en memoria.
- Métodos `TryParse` para manejo seguro de excepciones.

## Instrucciones de Ejecución

Para ejecutar este proyecto

1. Clona el repositorio desde GitHub:
   ```bash
   git clone <url_del_repositorio>
   ```

2. Navega a la carpeta del proyecto:
   ```bash
   cd GestorVentasUnidad1
   ```

3. Ejecuta la aplicación utilizando .NET CLI:
   ```bash
   dotnet run
   ```

## Ejemplos de la Aplicación en Ejecución

### Manejo de Errores de Entrada
El sistema protege contra entradas inválidas de manera robusta:
```text
====================================================
   SISTEMA GESTOR DE VENTAS E INVENTARIO (MINI-POS)
====================================================
1. Registrar nuevo producto en inventario
2. Consultar inventario completo
3. Registrar una venta
4. Ver reporte de caja y estadísticas diarias
5. Salir
====================================================
Seleccione una opción (1-5): abc
[ERROR] Entrada no válida. Debe ingresar un número entero.

Seleccione una opción (1-5): 9
[ERROR] Opción fuera de rango. Ingrese un valor entre 1 y 5.
```

### Registro de Venta Exitoso
Cálculo correcto de stock, IVA y descuentos:
```text
====================================================
                  TICKET DE VENTA
====================================================
 Producto:             Café Colombiano 500g (x2)
 Subtotal:             $ 36.000,00
 Descuento (10%):     -$  3.600,00
 IVA (19%):            +$  6.156,00
 ---------------------------------------------------
 TOTAL A PAGAR:        $ 38.556,00
====================================================

[OK] Venta efectuada con éxito. Stock actualizado: 8 unidades.
```
