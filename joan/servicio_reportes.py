from base_datos import get_connection
from datetime import datetime, timedelta

class ReporteService:
    """Servicio para generación de reportes."""
    
    # ===== REPORTES DE VENTAS =====
    
    @staticmethod
    @staticmethod
    def ventas_diarias(fecha=None):
        """Reporte de ventas diarias detallado para la tabla."""
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT v.numero_factura, c.nombre as cliente, v.total, v.metodo_pago
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            WHERE DATE(v.fecha) = ? AND v.estado = 1
            ORDER BY v.fecha DESC
        """, (fecha,))
        
        result = cursor.fetchall()
        conn.close()
        
        return result
    
    @staticmethod
    def ventas_mensuales(año=None, mes=None):
        """Reporte de ventas mensuales detallado para la tabla."""
        if not año:
            año = datetime.now().year
        if not mes:
            mes = datetime.now().month
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT v.numero_factura, v.fecha, v.total
            FROM ventas v
            WHERE strftime('%Y', v.fecha) = ? AND strftime('%m', v.fecha) = ? AND v.estado = 1
            ORDER BY v.fecha DESC
        """, (str(año), str(mes).zfill(2)))
        
        result = cursor.fetchall()
        conn.close()
        
        return result
    
    @staticmethod
    def ventas_por_producto(fecha_inicio=None, fecha_fin=None):
        """Reporte de ventas por producto."""
        if not fecha_inicio:
            fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not fecha_fin:
            fecha_fin = datetime.now().strftime("%Y-%m-%d")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.nombre, SUM(d.cantidad) as cantidad_vendida, SUM(d.subtotal) as total
            FROM detalles_venta d
            JOIN productos p ON d.id_producto = p.id_producto
            JOIN ventas v ON d.id_venta = v.id_venta
            WHERE DATE(v.fecha) BETWEEN ? AND ? AND v.estado = 1
            GROUP BY p.id_producto
            ORDER BY cantidad_vendida DESC
        """, (fecha_inicio, fecha_fin))
        
        datos = cursor.fetchall()
        conn.close()
        
        return datos
    
    @staticmethod
    def ventas_por_cliente(fecha_inicio=None, fecha_fin=None):
        """Reporte de ventas por cliente."""
        if not fecha_inicio:
            fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not fecha_fin:
            fecha_fin = datetime.now().strftime("%Y-%m-%d")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.nombre, COUNT(*) as cantidad_compras, SUM(v.total) as total
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            WHERE DATE(v.fecha) BETWEEN ? AND ? AND v.estado = 1
            GROUP BY c.id_cliente
            ORDER BY total DESC
        """, (fecha_inicio, fecha_fin))
        
        datos = cursor.fetchall()
        conn.close()
        
        return datos
    
    @staticmethod
    def ventas_por_cajero(fecha_inicio=None, fecha_fin=None):
        """Reporte de ventas por cajero."""
        if not fecha_inicio:
            fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not fecha_fin:
            fecha_fin = datetime.now().strftime("%Y-%m-%d")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.nombre, COUNT(*) as cantidad_ventas, SUM(v.total) as total
            FROM ventas v
            JOIN usuarios u ON v.id_cajero = u.id_usuario
            WHERE DATE(v.fecha) BETWEEN ? AND ? AND v.estado = 1
            GROUP BY u.id_usuario
            ORDER BY total DESC
        """, (fecha_inicio, fecha_fin))
        
        datos = cursor.fetchall()
        conn.close()
        
        return datos
    
    # ===== REPORTES DE INVENTARIO =====
    
    @staticmethod
    @staticmethod
    def inventario_actual():
        """Reporte del inventario actual mapeado a las columnas de la UI."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nombre as producto, stock, precio_compra as costo_unitario, (stock * precio_compra) as valor_total
            FROM productos
            WHERE estado = 1
            ORDER BY nombre
        """)
        
        datos = cursor.fetchall()
        conn.close()
        
        return datos
    
    @staticmethod
    def productos_bajo_stock():
        """Reporte de productos con bajo stock."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nombre, stock, stock_minimo, (stock_minimo - stock) as deficit
            FROM productos
            WHERE stock <= stock_minimo AND estado = 1
            ORDER BY deficit DESC
        """)
        
        datos = cursor.fetchall()
        conn.close()
        
        return datos
    
    @staticmethod
    @staticmethod
    def productos_mas_vendidos(limite=10):
        """Reporte de productos más vendidos con ingresos mapeado a las columnas de la UI."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.nombre, SUM(d.cantidad) as cantidad_vendida, SUM(d.subtotal) as ingresos
            FROM detalles_venta d
            JOIN productos p ON d.id_producto = p.id_producto
            JOIN ventas v ON d.id_venta = v.id_venta
            WHERE v.estado = 1
            GROUP BY p.id_producto
            ORDER BY cantidad_vendida DESC
            LIMIT ?
        """, (limite,))
        
        datos = cursor.fetchall()
        conn.close()
        
        return datos
    
    # ===== REPORTES FINANCIEROS =====
    
    @staticmethod
    def ingresos_diarios(fecha=None):
        """Reporte de ingresos diarios."""
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(total) as total_ingresos, COUNT(*) as cantidad_ventas
            FROM ventas
            WHERE DATE(fecha) = ? AND estado = 1
        """, (fecha,))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'fecha': fecha,
            'total_ingresos': result['total_ingresos'] if result['total_ingresos'] else 0,
            'cantidad_ventas': result['cantidad_ventas'] if result['cantidad_ventas'] else 0
        }
    
    @staticmethod
    def ingresos_mensuales(año=None, mes=None):
        """Reporte de ingresos mensuales."""
        if not año:
            año = datetime.now().year
        if not mes:
            mes = datetime.now().month
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(total) as total_ingresos, COUNT(*) as cantidad_ventas
            FROM ventas
            WHERE strftime('%Y', fecha) = ? AND strftime('%m', fecha) = ? AND estado = 1
        """, (str(año), str(mes).zfill(2)))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'mes': f"{año}-{mes:02d}",
            'total_ingresos': result['total_ingresos'] if result['total_ingresos'] else 0,
            'cantidad_ventas': result['cantidad_ventas'] if result['cantidad_ventas'] else 0
        }
    
    @staticmethod
    def ganancias_por_producto(fecha_inicio=None, fecha_fin=None):
        """Reporte de ganancias por producto."""
        if not fecha_inicio:
            fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not fecha_fin:
            fecha_fin = datetime.now().strftime("%Y-%m-%d")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.nombre, 
                   SUM(d.cantidad) as cantidad_vendida,
                   SUM(d.cantidad * p.precio_compra) as costo_total,
                   SUM(d.subtotal) as ingresos_total,
                   (SUM(d.subtotal) - SUM(d.cantidad * p.precio_compra)) as ganancia
            FROM detalles_venta d
            JOIN productos p ON d.id_producto = p.id_producto
            JOIN ventas v ON d.id_venta = v.id_venta
            WHERE DATE(v.fecha) BETWEEN ? AND ? AND v.estado = 1
            GROUP BY p.id_producto
            ORDER BY ganancia DESC
        """, (fecha_inicio, fecha_fin))
        
        datos = cursor.fetchall()
        conn.close()
        
        return datos

    @staticmethod
    def resumen_financiero():
        """Obtiene un resumen financiero consolidado para el dashboard financiero."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Total ventas (activas)
        cursor.execute("SELECT SUM(total) as total_ventas, COUNT(*) as num_transacciones FROM ventas WHERE estado = 1")
        r_ventas = cursor.fetchone()
        total_ventas = r_ventas['total_ventas'] or 0.0
        num_transacciones = r_ventas['num_transacciones'] or 0
        
        # 2. Total de ingresos (subtotal de ventas activas)
        cursor.execute("SELECT SUM(subtotal) as total_ingresos FROM ventas WHERE estado = 1")
        total_ingresos = cursor.fetchone()['total_ingresos'] or 0.0
        
        # 3. Total de costos (basado en precio_compra de los productos vendidos)
        cursor.execute("""
            SELECT SUM(d.cantidad * p.precio_compra) as total_costos
            FROM detalles_venta d
            JOIN productos p ON d.id_producto = p.id_producto
            JOIN ventas v ON d.id_venta = v.id_venta
            WHERE v.estado = 1
        """)
        total_costos = cursor.fetchone()['total_costos'] or 0.0
        
        # 4. Número de productos vendidos
        cursor.execute("SELECT SUM(cantidad) as num_productos FROM detalles_venta d JOIN ventas v ON d.id_venta = v.id_venta WHERE v.estado = 1")
        num_productos = cursor.fetchone()['num_productos'] or 0
        
        # 5. Valor total del inventario actual (a precio de venta)
        cursor.execute("SELECT SUM(stock * precio_venta) as valor_inventario FROM productos WHERE estado = 1")
        valor_inventario = cursor.fetchone()['valor_inventario'] or 0.0
        
        conn.close()
        
        return {
            'total_ventas': total_ventas,
            'total_ingresos': total_ingresos,
            'total_costos': total_costos,
            'num_transacciones': num_transacciones,
            'num_productos': num_productos,
            'valor_inventario': valor_inventario
        }

