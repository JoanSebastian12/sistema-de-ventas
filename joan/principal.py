# Sistema de Gestión de Ventas - Proyecto Final
# Autor: Joan Sebastian Rosania Logreira

import tkinter as tk
from base_datos import create_tables, insert_admin_user, insert_consumidor_final
from interfaz.inicio_sesion import LoginUI
from interfaz.panel_principal import DashboardUI

class SistemaVentasApp:
    """Aplicación principal del Sistema de Gestión de Ventas."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Ventas - SGV")
        self.root.geometry("1000x700")
        self.root.minsize(1000, 700)
        
        # Inicializar base de datos
        create_tables()
        insert_admin_user()
        insert_consumidor_final()
        
        self.user_actual = None
        self.mostrar_login()
    
    def mostrar_login(self):
        """Muestra la pantalla de login."""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.login_ui = LoginUI(self.root, self.en_login_exitoso)
    
    def en_login_exitoso(self, usuario):
        """Callback cuando el login es exitoso."""
        self.user_actual = usuario
        self.mostrar_dashboard()
    
    def mostrar_dashboard(self):
        """Muestra el dashboard principal."""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.dashboard_ui = DashboardUI(self.root, self.user_actual, self.cerrar_sesion)
    
    def cerrar_sesion(self):
        """Cierra sesión actual."""
        self.user_actual = None
        self.mostrar_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaVentasApp(root)
    root.mainloop()