from base_datos import get_connection
from datetime import datetime
from servicio_inventario import InventarioService

class VentaService:
    """Servicio para gestión de ventas y facturación."""
    
    @staticmethod
    def generar_numero_factura():
        """Genera número de factura único."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM ventas")
        count = cursor.fetchone()['count'] + 1
        
        conn.close()
        
        fecha = datetime.now()
        numero_factura = f"FAC-{fecha.year}{fecha.month:02d}{fecha.day:02d}-{count:05d}"
        
        return numero_factura
    
    @staticmethod
    def crear_venta(id_cliente, id_cajero, metodo_pago, detalles, descuento_porcentaje=0.0):
        """Crea una venta con sus detalles.
        
        detalles es una lista de dicts con: id_producto, cantidad, precio_unitario
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener nombres de cliente y cajero para el ticket
            cursor.execute("SELECT nombre FROM clientes WHERE id_cliente = ?", (id_cliente,))
            r_cliente = cursor.fetchone()
            cliente_nombre = r_cliente['nombre'] if r_cliente else "Consumidor Final"
            
            cursor.execute("SELECT nombre FROM usuarios WHERE id_usuario = ?", (id_cajero,))
            r_cajero = cursor.fetchone()
            cajero_nombre = r_cajero['nombre'] if r_cajero else "Cajero"

            # Calcular totales
            subtotal = sum(det['cantidad'] * det['precio_unitario'] for det in detalles)
            descuento_monto = subtotal * (descuento_porcentaje / 100.0)
            subtotal_con_descuento = subtotal - descuento_monto
            impuestos = subtotal_con_descuento * 0.19  # IVA 19%
            total = subtotal_con_descuento + impuestos
            
            numero_factura = VentaService.generar_numero_factura()
            
            # Insertar venta
            cursor.execute("""
                INSERT INTO ventas (numero_factura, id_cliente, id_cajero, subtotal, descuento, impuestos, total, metodo_pago)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (numero_factura, id_cliente, id_cajero, subtotal, descuento_monto, impuestos, total, metodo_pago))
            
            id_venta = cursor.lastrowid
            
            # Insertar detalles de venta
            for detalle in detalles:
                subtotal_detalle = detalle['cantidad'] * detalle['precio_unitario']
                
                cursor.execute("""
                    INSERT INTO detalles_venta (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_venta, detalle['id_producto'], detalle['cantidad'], detalle['precio_unitario'], subtotal_detalle))
                
                # Descontar inventario
                InventarioService.registrar_movimiento(
                    detalle['id_producto'], 
                    'salida', 
                    detalle['cantidad'],
                    f'Venta factura {numero_factura}'
                )
            
            # Registrar en auditoría
            cursor.execute("""
                INSERT INTO auditoria (id_usuario, evento, descripcion)
                VALUES (?, ?, ?)
            """, (id_cajero, 'Venta realizada', f'Factura {numero_factura} - Total: {total}'))
            
            conn.commit()
            conn.close()
            
            # Generar ticket de venta en texto
            ruta_ticket = VentaService.generar_ticket_texto(
                numero_factura, 
                cliente_nombre, 
                cajero_nombre, 
                subtotal, 
                descuento_monto, 
                impuestos, 
                total, 
                metodo_pago, 
                detalles
            )
            
            return {
                'id_venta': id_venta,
                'numero_factura': numero_factura,
                'subtotal': subtotal,
                'descuento': descuento_monto,
                'impuestos': impuestos,
                'total': total,
                'ruta_ticket': ruta_ticket
            }
        except Exception as e:
            try:
                conn.close()
            except Exception:
                pass
            return None

    @staticmethod
    def generar_ticket_texto(numero_factura, cliente_nombre, cajero_nombre, subtotal, descuento_monto, impuestos, total, metodo_pago, detalles):
        """Genera un archivo de ticket .txt con formato profesional."""
        import os
        
        # Crear directorio 'facturas' si no existe
        if not os.path.exists('facturas'):
            os.makedirs('facturas')
            
        ruta_archivo = os.path.join('facturas', f"{numero_factura}.txt")
        
        fecha_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        lineas = []
        lineas.append("========================================")
        lineas.append("         SISTEMA DE VENTAS - SGV        ")
        lineas.append("========================================")
        lineas.append(f"Factura: {numero_factura}")
        lineas.append(f"Fecha:   {fecha_str}")
        lineas.append(f"Cajero:  {cajero_nombre}")
        lineas.append(f"Cliente: {cliente_nombre}")
        lineas.append("----------------------------------------")
        lineas.append("Cant  Descripción       P.Unit   Subtot")
        lineas.append("----------------------------------------")
        
        for det in detalles:
            # Obtener nombre del producto si viene de la UI
            prod_nombre = det.get('nombre', f"Producto #{det['id_producto']}")
            # Limitar longitud del nombre para el ticket
            if len(prod_nombre) > 16:
                prod_nombre = prod_nombre[:13] + "..."
            
            p_unit = det['precio_unitario']
            cant = det['cantidad']
            sub = cant * p_unit
            
            lineas.append(f"{cant:<4} {prod_nombre:<17} ${p_unit:<7.2f} ${sub:<7.2f}")
            
        lineas.append("----------------------------------------")
        lineas.append(f"Subtotal:                      ${subtotal:>8.2f}")
        if descuento_monto > 0:
            lineas.append(f"Descuento:                    -${descuento_monto:>8.2f}")
        lineas.append(f"IVA (19%):                     ${impuestos:>8.2f}")
        lineas.append(f"TOTAL:                         ${total:>8.2f}")
        lineas.append(f"Método de Pago: {metodo_pago:>23}")
        lineas.append("========================================")
        lineas.append("       ¡GRACIAS POR SU COMPRA!          ")
        lineas.append("========================================")
        
        contenido = "\n".join(lineas)
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido)
            
        return ruta_archivo

    
    @staticmethod
    def get_venta(id_venta):
        """Obtiene información de una venta."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM ventas WHERE id_venta = ?", (id_venta,))
        venta = cursor.fetchone()
        
        conn.close()
        return venta
    
    @staticmethod
    def get_detalles_venta(id_venta):
        """Obtiene detalles de una venta."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT d.*, p.nombre FROM detalles_venta d
            JOIN productos p ON d.id_producto = p.id_producto
            WHERE d.id_venta = ?
        """, (id_venta,))
        
        detalles = cursor.fetchall()
        
        conn.close()
        return detalles
    
    @staticmethod
    def get_ventas_periodo(fecha_inicio, fecha_fin):
        """Obtiene ventas en un período."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT v.*, c.nombre as cliente_nombre, u.nombre as cajero_nombre
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            JOIN usuarios u ON v.id_cajero = u.id_usuario
            WHERE DATE(v.fecha) BETWEEN ? AND ? AND v.estado = 1
            ORDER BY v.fecha DESC
        """, (fecha_inicio, fecha_fin))
        
        ventas = cursor.fetchall()
        
        conn.close()
        return ventas
    
    @staticmethod
    def anular_venta(id_venta):
        """Anula una venta y revierte el inventario."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener detalles de la venta
            cursor.execute("SELECT * FROM detalles_venta WHERE id_venta = ?", (id_venta,))
            detalles = cursor.fetchall()
            
            # Revertir inventario
            for detalle in detalles:
                InventarioService.registrar_movimiento(
                    detalle['id_producto'],
                    'entrada',
                    detalle['cantidad'],
                    f'Anulación de venta id_venta: {id_venta}'
                )
            
            # Marcar venta como anulada
            cursor.execute("UPDATE ventas SET estado = 0 WHERE id_venta = ?", (id_venta,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    @staticmethod
    def get_ventas_por_producto(fecha_inicio=None, fecha_fin=None):
        """Obtiene resumen de ventas por producto."""
        conn = get_connection()
        cursor = conn.cursor()
        
        if fecha_inicio and fecha_fin:
            cursor.execute("""
                SELECT p.nombre, SUM(d.cantidad) as cantidad_vendida, SUM(d.subtotal) as total
                FROM detalles_venta d
                JOIN productos p ON d.id_producto = p.id_producto
                JOIN ventas v ON d.id_venta = v.id_venta
                WHERE DATE(v.fecha) BETWEEN ? AND ? AND v.estado = 1
                GROUP BY p.id_producto
                ORDER BY cantidad_vendida DESC
            """, (fecha_inicio, fecha_fin))
        else:
            cursor.execute("""
                SELECT p.nombre, SUM(d.cantidad) as cantidad_vendida, SUM(d.subtotal) as total
                FROM detalles_venta d
                JOIN productos p ON d.id_producto = p.id_producto
                JOIN ventas v ON d.id_venta = v.id_venta
                WHERE v.estado = 1
                GROUP BY p.id_producto
                ORDER BY cantidad_vendida DESC
            """)
        
        datos = cursor.fetchall()
        
        conn.close()
        return datos
