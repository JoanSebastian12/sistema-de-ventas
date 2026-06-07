import sqlite3
import os
from datetime import datetime

DATABASE = "sistema_ventas.db"

def get_connection():
    """Obtiene conexión a la base de datos."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Crea todas las tablas necesarias."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            email TEXT,
            contraseña TEXT NOT NULL,
            rol TEXT NOT NULL,
            estado INTEGER DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultimo_acceso TIMESTAMP
        )
    """)

    # Tabla de clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            documento TEXT UNIQUE NOT NULL,
            telefono TEXT,
            email TEXT,
            direccion TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_producto TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio_compra REAL NOT NULL,
            precio_venta REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            stock_minimo INTEGER DEFAULT 5,
            categoria TEXT,
            estado INTEGER DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla de movimientos de inventario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos_inventario (
            id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            descripcion TEXT,
            FOREIGN KEY(id_producto) REFERENCES productos(id_producto)
        )
    """)

    # Tabla de ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_factura TEXT UNIQUE NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            id_cliente INTEGER NOT NULL,
            id_cajero INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            descuento REAL DEFAULT 0.0,
            impuestos REAL NOT NULL,
            total REAL NOT NULL,
            metodo_pago TEXT NOT NULL,
            estado INTEGER DEFAULT 1,
            FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY(id_cajero) REFERENCES usuarios(id_usuario)
        )
    """)

    # Tabla de detalles de venta
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalles_venta (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY(id_venta) REFERENCES ventas(id_venta),
            FOREIGN KEY(id_producto) REFERENCES productos(id_producto)
        )
    """)

    # Tabla de control de caja
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cajas (
            id_caja INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            fecha_apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_cierre TIMESTAMP,
            monto_inicial REAL NOT NULL,
            monto_final REAL,
            total_ventas REAL,
            estado TEXT DEFAULT 'abierta',
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
        )
    """)

    # Tabla de auditoría
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auditoria (
            id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            evento TEXT NOT NULL,
            descripcion TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
        )
    """)

    # Migración: agregar columna email si la tabla existe y no tiene la columna
    try:
        cursor.execute("PRAGMA table_info(usuarios)")
        cols = [r[1] for r in cursor.fetchall()]
        if 'email' not in cols:
            try:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN email TEXT")
            except Exception:
                pass
    except Exception:
        pass

    # Migración: agregar columna descuento a la tabla ventas si no existe
    try:
        cursor.execute("PRAGMA table_info(ventas)")
        cols = [r[1] for r in cursor.fetchall()]
        if 'descuento' not in cols:
            try:
                cursor.execute("ALTER TABLE ventas ADD COLUMN descuento REAL DEFAULT 0.0")
            except Exception:
                pass
    except Exception:
        pass

    conn.commit()
    conn.close()

def insert_admin_user():
    """Inserta usuario administrador por defecto si no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        from hashlib import sha256
        password_hash = sha256("admin123".encode()).hexdigest()
        
        cursor.execute("""
            INSERT INTO usuarios (nombre, usuario, email, contraseña, rol, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("Administrador", "admin", None, password_hash, "Administrador", 1))
        
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def insert_consumidor_final():
    """Inserta cliente 'Consumidor Final' si no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO clientes (nombre, documento)
            VALUES (?, ?)
        """, ("Consumidor Final", "0"))
        
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

if __name__ == "__main__":
    create_tables()
    insert_admin_user()
    insert_consumidor_final()
    print("Base de datos inicializada correctamente.")
