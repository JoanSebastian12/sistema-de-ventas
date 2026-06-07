from base_datos import get_connection
from datetime import datetime

class CajaService:
    """Servicio para control de caja."""
    
    @staticmethod
    def abrir_caja(id_usuario, monto_inicial):
        """Abre una caja para un usuario."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar si hay caja abierta
            cursor.execute("""
                SELECT * FROM cajas WHERE id_usuario = ? AND estado = 'abierta'
            """, (id_usuario,))
            
            if cursor.fetchone():
                conn.close()
                return None  # Ya hay caja abierta
            
            cursor.execute("""
                INSERT INTO cajas (id_usuario, monto_inicial, estado)
                VALUES (?, ?, ?)
            """, (id_usuario, monto_inicial, 'abierta'))
            
            id_caja = cursor.lastrowid
            
            # Registrar en auditoría
            cursor.execute("""
                INSERT INTO auditoria (id_usuario, evento, descripcion)
                VALUES (?, ?, ?)
            """, (id_usuario, 'Apertura de caja', f'Monto inicial: {monto_inicial}'))
            
            conn.commit()
            conn.close()
            
            return {'id_caja': id_caja, 'monto_inicial': monto_inicial}
        except Exception as e:
            conn.close()
            return None
    
    @staticmethod
    def get_caja_abierta(id_usuario):
        """Obtiene la caja abierta de un usuario."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM cajas WHERE id_usuario = ? AND estado = 'abierta'
        """, (id_usuario,))
        
        caja = cursor.fetchone()
        
        conn.close()
        return caja

    @staticmethod
    def get_cajas_abiertas(id_usuario):
        """Obtiene las cajas abiertas de un usuario."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM cajas WHERE id_usuario = ? AND estado = 'abierta' ORDER BY fecha_apertura DESC
        """, (id_usuario,))
        
        cajas = cursor.fetchall()
        
        conn.close()
        return cajas

    @staticmethod
    def get_all_cajas():
        """Obtiene todas las cajas."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM cajas ORDER BY fecha_apertura DESC
        """)
        cajas = cursor.fetchall()
        
        conn.close()
        return cajas
    
    @staticmethod
    def cerrar_caja(id_caja, monto_final):
        """Cierra una caja."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener caja
            cursor.execute("SELECT * FROM cajas WHERE id_caja = ?", (id_caja,))
            caja = cursor.fetchone()
            
            if not caja:
                conn.close()
                return None
            
            # Calcular total de ventas
            cursor.execute("""
                SELECT SUM(total) as total FROM ventas
                WHERE id_cajero = ? AND DATE(fecha) = DATE(?)
            """, (caja['id_usuario'], caja['fecha_apertura']))
            
            result = cursor.fetchone()
            total_ventas = result['total'] if result['total'] else 0
            
            # Actualizar caja
            cursor.execute("""
                UPDATE cajas SET fecha_cierre = ?, monto_final = ?, total_ventas = ?, estado = 'cerrada'
                WHERE id_caja = ?
            """, (datetime.now(), monto_final, total_ventas, id_caja))
            
            # Registrar en auditoría
            cursor.execute("""
                INSERT INTO auditoria (id_usuario, evento, descripcion)
                VALUES (?, ?, ?)
            """, (caja['id_usuario'], 'Cierre de caja', f'Total ventas: {total_ventas}'))
            
            conn.commit()
            conn.close()
            
            diferencia = monto_final - (caja['monto_inicial'] + total_ventas)
            
            return {
                'monto_inicial': caja['monto_inicial'],
                'total_ventas': total_ventas,
                'monto_esperado': caja['monto_inicial'] + total_ventas,
                'monto_final': monto_final,
                'diferencia': diferencia
            }
        except Exception as e:
            conn.close()
            return None
    
    @staticmethod
    def get_movimientos_caja(id_caja):
        """Obtiene movimientos de una caja (ventas)."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.id_usuario, v.numero_factura, v.fecha, v.total, v.metodo_pago
            FROM cajas c
            JOIN ventas v ON c.id_usuario = v.id_cajero
            WHERE c.id_caja = ? AND DATE(v.fecha) = DATE(c.fecha_apertura)
            ORDER BY v.fecha
        """, (id_caja,))
        
        movimientos = cursor.fetchall()
        
        conn.close()
        return movimientos
    
    @staticmethod
    def get_resumen_cajas_dia(fecha):
        """Obtiene resumen de todas las cajas de un día."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.id_caja, u.nombre as usuario, c.monto_inicial, c.monto_final, 
                   c.total_ventas, c.fecha_apertura, c.fecha_cierre
            FROM cajas c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE DATE(c.fecha_apertura) = ?
            ORDER BY c.fecha_apertura
        """, (fecha,))
        
        cajas = cursor.fetchall()
        
        conn.close()
        return cajas
