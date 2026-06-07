from base_datos import get_connection
from datetime import datetime

class InventarioService:
    """Servicio para control de inventario."""
    
    @staticmethod
    def registrar_movimiento(id_producto, tipo, cantidad, descripcion=""):
        """Registra un movimiento de inventario y actualiza el stock."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Obtener stock actual
        cursor.execute("SELECT stock FROM productos WHERE id_producto = ?", (id_producto,))
        result = cursor.fetchone()
        stock_actual = result['stock'] if result else 0
        
        # Calcular nuevo stock según tipo de movimiento
        if tipo == "entrada":
            nuevo_stock = stock_actual + cantidad
        elif tipo == "salida":
            nuevo_stock = max(0, stock_actual - cantidad)
        elif tipo == "ajuste":
            nuevo_stock = cantidad
        else:
            conn.close()
            return False
        
        try:
            # Registrar movimiento
            cursor.execute("""
                INSERT INTO movimientos_inventario (id_producto, tipo, cantidad, descripcion)
                VALUES (?, ?, ?, ?)
            """, (id_producto, tipo, cantidad, descripcion))
            
            # Actualizar stock
            cursor.execute("""
                UPDATE productos SET stock = ? WHERE id_producto = ?
            """, (nuevo_stock, id_producto))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    @staticmethod
    def get_movimientos(id_producto=None):
        """Obtiene los movimientos de inventario."""
        conn = get_connection()
        cursor = conn.cursor()
        
        if id_producto:
            cursor.execute("""
                SELECT m.*, p.nombre FROM movimientos_inventario m
                JOIN productos p ON m.id_producto = p.id_producto
                WHERE m.id_producto = ?
                ORDER BY m.fecha DESC
            """, (id_producto,))
        else:
            cursor.execute("""
                SELECT m.*, p.nombre FROM movimientos_inventario m
                JOIN productos p ON m.id_producto = p.id_producto
                ORDER BY m.fecha DESC
            """)
        
        movimientos = cursor.fetchall()
        
        conn.close()
        return movimientos
    
    @staticmethod
    def get_productos_bajo_stock():
        """Obtiene productos con stock bajo."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_producto, nombre, stock, stock_minimo 
            FROM productos 
            WHERE stock <= stock_minimo AND estado = 1
            ORDER BY stock ASC
        """)
        
        productos = cursor.fetchall()
        
        conn.close()
        return productos
    
    @staticmethod
    def get_resumen_inventario():
        """Obtiene resumen del inventario actual."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Total de productos
        cursor.execute("SELECT COUNT(*) as total FROM productos WHERE estado = 1")
        total_productos = cursor.fetchone()['total']
        
        # Productos con bajo stock
        cursor.execute("SELECT COUNT(*) as total FROM productos WHERE stock <= stock_minimo AND estado = 1")
        bajo_stock = cursor.fetchone()['total']
        
        # Valor total del inventario
        cursor.execute("SELECT SUM(stock * precio_venta) as valor FROM productos WHERE estado = 1")
        valor_total = cursor.fetchone()['valor'] or 0
        
        conn.close()
        
        return {
            'total_productos': total_productos,
            'bajo_stock': bajo_stock,
            'valor_inventario': valor_total
        }
