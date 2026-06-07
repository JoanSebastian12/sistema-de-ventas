from base_datos import get_connection

class ClienteService:
    """Servicio para gestión de clientes."""
    
    @staticmethod
    def create_cliente(nombre, documento, telefono="", email="", direccion=""):
        """Crea un nuevo cliente."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO clientes (nombre, documento, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, documento, telefono, email, direccion))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    @staticmethod
    def get_cliente(id_cliente):
        """Obtiene información de un cliente."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = ?", (id_cliente,))
        cliente = cursor.fetchone()
        
        conn.close()
        return cliente
    
    @staticmethod
    def get_all_clientes():
        """Obtiene todos los clientes."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM clientes ORDER BY nombre")
        clientes = cursor.fetchall()
        
        conn.close()
        return clientes
    
    @staticmethod
    def search_cliente(busqueda):
        """Busca clientes por nombre o documento."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM clientes 
            WHERE nombre LIKE ? OR documento LIKE ?
            ORDER BY nombre
        """, (f"%{busqueda}%", f"%{busqueda}%"))
        
        clientes = cursor.fetchall()
        
        conn.close()
        return clientes
    
    @staticmethod
    def update_cliente(id_cliente, nombre, telefono, email, direccion):
        """Actualiza datos de un cliente."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE clientes SET nombre = ?, telefono = ?, email = ?, direccion = ?
            WHERE id_cliente = ?
        """, (nombre, telefono, email, direccion, id_cliente))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_historial_compras(id_cliente):
        """Obtiene el historial de compras de un cliente."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT v.id_venta, v.numero_factura, v.fecha, v.total
            FROM ventas v
            WHERE v.id_cliente = ?
            ORDER BY v.fecha DESC
        """, (id_cliente,))
        
        compras = cursor.fetchall()
        
        conn.close()
        return compras
