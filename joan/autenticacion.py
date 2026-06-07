from hashlib import sha256
from base_datos import get_connection
from datetime import datetime

class AuthService:
    """Servicio de autenticación y manejo de usuarios."""

    # Último error ocurrido en operaciones (útil para mensajes detallados en la UI)
    last_error = None
    
    @staticmethod
    def hash_password(password):
        """Cifra una contraseña."""
        return sha256(password.encode()).hexdigest()
    
    @staticmethod
    def login(usuario, contraseña):
        """Intenta iniciar sesión. Retorna usuario si es exitoso, None si falla."""
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = AuthService.hash_password(contraseña)
        
        cursor.execute("""
            SELECT * FROM usuarios 
            WHERE usuario = ? AND contraseña = ? AND estado = 1
        """, (usuario, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            # Registrar último acceso
            cursor.execute("""
                UPDATE usuarios SET ultimo_acceso = ? WHERE id_usuario = ?
            """, (datetime.now(), user['id_usuario']))
            
            # Registrar en auditoría
            cursor.execute("""
                INSERT INTO auditoria (id_usuario, evento, descripcion)
                VALUES (?, ?, ?)
            """, (user['id_usuario'], "Inicio de sesión", f"Usuario {usuario} inició sesión"))
            
            conn.commit()
        
        conn.close()
        return user
    
    @staticmethod
    def create_user(*args):
        """Crea un nuevo usuario.

        Soporta dos firmas históricas:
        - create_user(nombre, usuario, contraseña, rol)
        - create_user(usuario, contraseña, nombre, email, rol)  <-- usada por la UI
        """
        conn = get_connection()
        cursor = conn.cursor()

        # Normalizar parámetros
        if len(args) == 4:
            nombre, usuario, contraseña, rol = args
            email = None
        elif len(args) == 5:
            usuario, contraseña, nombre, email, rol = args
        else:
            return False

        password_hash = AuthService.hash_password(contraseña)

        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, usuario, email, contraseña, rol, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nombre, usuario, email, password_hash, rol, 1))

            conn.commit()
            conn.close()
            AuthService.last_error = None
            return True
        except Exception as e:
            AuthService.last_error = str(e)
            conn.close()
            return False
    
    @staticmethod
    def get_user(id_usuario):
        """Obtiene información de un usuario."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        user = cursor.fetchone()
        
        conn.close()
        return user
    
    @staticmethod
    def get_all_users():
        """Obtiene todos los usuarios."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios ORDER BY fecha_creacion DESC")
        users = cursor.fetchall()

        conn.close()
        return users

    # Alias en español esperado por la interfaz
    @staticmethod
    def get_all_usuarios():
        return AuthService.get_all_users()
    
    @staticmethod
    def update_user(*args):
        """Actualiza datos de un usuario.

        Soporta dos firmas:
        - update_user(id_usuario, nombre, rol, estado)
        - update_user(id_usuario, nombre, email, rol, estado)  <-- usada por la UI
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            if len(args) == 4:
                id_usuario, nombre, rol, estado = args
                # actualizar sin email
                cursor.execute("""
                    UPDATE usuarios SET nombre = ?, rol = ?, estado = ?
                    WHERE id_usuario = ?
                """, (nombre, rol, estado, id_usuario))
            elif len(args) == 5:
                id_usuario, nombre, email, rol, estado = args
                cursor.execute("""
                    UPDATE usuarios SET nombre = ?, email = ?, rol = ?, estado = ?
                    WHERE id_usuario = ?
                """, (nombre, email, rol, estado, id_usuario))
            else:
                conn.close()
                AuthService.last_error = "Parámetros inválidos para update_user"
                return False

            conn.commit()
            conn.close()
            AuthService.last_error = None
            return True
        except Exception as e:
            AuthService.last_error = str(e)
            conn.close()
            return False
    
    @staticmethod
    def change_password(id_usuario, new_password):
        """Cambia la contraseña de un usuario."""
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = AuthService.hash_password(new_password)
        
        cursor.execute("""
            UPDATE usuarios SET contraseña = ?
            WHERE id_usuario = ?
        """, (password_hash, id_usuario))
        
        conn.commit()
        conn.close()
