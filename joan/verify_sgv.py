import sys
import os

# Añadir el directorio del proyecto al path
sys.path.append(r"c:\Users\USER\Desktop\joan")

print("--- Iniciando verificación del Sistema de Gestión de Ventas (SGV) ---")

try:
    print("1. Cargando base_datos.py...")
    import base_datos
    base_datos.create_tables()
    base_datos.insert_admin_user()
    base_datos.insert_consumidor_final()
    print("   [OK] Base de datos inicializada correctamente.")
except Exception as e:
    print(f"   [ERROR] Error al inicializar base de datos: {e}")
    sys.exit(1)

try:
    print("2. Probando todos los métodos de ReporteService...")
    from servicio_reportes import ReporteService
    
    # 2.1 resumen_financiero
    resumen = ReporteService.resumen_financiero()
    print(f"   [OK] Método resumen_financiero ejecutado con éxito. Resumen: {resumen}")
    
    # 2.2 ventas_diarias
    v_diarias = ReporteService.ventas_diarias()
    print(f"   [OK] Método ventas_diarias ejecutado con éxito. Encontrados: {len(v_diarias)} registros.")
    if len(v_diarias) > 0:
        # Intentar convertir a dict para simular la UI
        d = dict(v_diarias[0])
        print(f"        Muestra registro: {d}")
        
    # 2.3 ventas_mensuales
    v_mensuales = ReporteService.ventas_mensuales()
    print(f"   [OK] Método ventas_mensuales ejecutado con éxito. Encontrados: {len(v_mensuales)} registros.")
    
    # 2.4 inventario_actual
    inv = ReporteService.inventario_actual()
    print(f"   [OK] Método inventario_actual ejecutado con éxito. Encontrados: {len(inv)} registros.")
    if len(inv) > 0:
        d = dict(inv[0])
        print(f"        Muestra registro: {d}")
        
    # 2.5 productos_mas_vendidos
    mas_vendidos = ReporteService.productos_mas_vendidos()
    print(f"   [OK] Método productos_mas_vendidos ejecutado con éxito. Encontrados: {len(mas_vendidos)} registros.")
    
except Exception as e:
    print(f"   [ERROR] Error al validar ReporteService: {e}")
    sys.exit(1)

try:
    print("3. Probando lógica de creación de venta y descuentos...")
    from servicio_ventas import VentaService
    from servicio_productos import ProductoService
    
    # Obtener un producto o agregar uno ficticio si no hay
    productos = ProductoService.get_all_productos()
    if not productos:
        print("   Agregando producto de prueba...")
        ProductoService.create_producto("TEST-001", "Producto Test", "Desc Test", 10.0, 20.0, 100, 5, "Test")
        productos = ProductoService.get_all_productos()
        
    producto = productos[0]
    detalles = [{
        'id_producto': producto['id_producto'],
        'nombre': producto['nombre'],
        'cantidad': 2,
        'precio_unitario': producto['precio_venta']
    }]
    
    print("   Registrando venta con 10% de descuento...")
    resultado = VentaService.crear_venta(1, 1, 'Efectivo', detalles, 10.0)
    
    if resultado:
        print("   [OK] Venta creada exitosamente.")
        print(f"   Resultado Venta: {resultado}")
        print(f"   Ticket generado en: {resultado['ruta_ticket']}")
        
        # Validar existencia del archivo del ticket
        if os.path.exists(resultado['ruta_ticket']):
            print(f"   [OK] El archivo del ticket existe.")
            with open(resultado['ruta_ticket'], 'r', encoding='utf-8') as f:
                print("   --- Contenido del Ticket ---")
                print(f.read())
                print("   ----------------------------")
        else:
            print("   [ERROR] El archivo del ticket NO fue creado.")
            sys.exit(1)
    else:
        print("   [ERROR] La venta retornó None.")
        sys.exit(1)
except Exception as e:
    print(f"   [ERROR] Error durante prueba de venta/descuentos: {e}")
    sys.exit(1)

print("\n--- ¡Todas las verificaciones lógicas pasaron exitosamente! ---")
