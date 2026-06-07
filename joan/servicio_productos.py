from base_datos import get_connection

class ProductoService:
    """Servicio para gestión de productos."""
    
    @staticmethod
    def create_producto(codigo_producto, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, categoria):
        """Crea un nuevo producto."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO productos 
                (codigo_producto, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, categoria, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (codigo_producto, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, categoria, 1))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    @staticmethod
    def get_producto(id_producto):
        """Obtiene información de un producto."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM productos WHERE id_producto = ? AND estado = 1", (id_producto,))
        producto = cursor.fetchone()
        
        conn.close()
        return producto
    
    @staticmethod
    def get_all_productos():
        """Obtiene todos los productos activos."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM productos WHERE estado = 1 ORDER BY nombre")
        productos = cursor.fetchall()
        
        conn.close()
        return productos
    
    @staticmethod
    def search_producto(busqueda):
        """Busca productos por nombre o código."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM productos 
            WHERE (nombre LIKE ? OR codigo_producto LIKE ?) AND estado = 1
            ORDER BY nombre
        """, (f"%{busqueda}%", f"%{busqueda}%"))
        
        productos = cursor.fetchall()
        
        conn.close()
        return productos
    
    @staticmethod
    def update_producto(id_producto, nombre, descripcion, precio_compra, precio_venta, stock_minimo, categoria):
        """Actualiza datos de un producto."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE productos SET nombre = ?, descripcion = ?, precio_compra = ?, 
            precio_venta = ?, stock_minimo = ?, categoria = ?
            WHERE id_producto = ?
        """, (nombre, descripcion, precio_compra, precio_venta, stock_minimo, categoria, id_producto))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete_producto(id_producto):
        """Elimina un producto (lógico)."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE productos SET estado = 0 WHERE id_producto = ?", (id_producto,))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_productos_bajo_stock():
        """Obtiene productos con stock bajo."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM productos 
            WHERE stock <= stock_minimo AND estado = 1
            ORDER BY stock ASC
        """)
        
        productos = cursor.fetchall()
        
        conn.close()
        return productos
    
    @staticmethod
    def get_stock(id_producto):
        """Obtiene el stock actual de un producto."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT stock FROM productos WHERE id_producto = ?", (id_producto,))
        result = cursor.fetchone()
        
        conn.close()
        return result['stock'] if result else 0
