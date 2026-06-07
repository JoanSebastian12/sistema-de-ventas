import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from servicio_inventario import InventarioService
from interfaz.productos import ProductosUI
from interfaz.clientes import ClientesUI
from interfaz.punto_venta import VentasUI
from interfaz.inventario import InventarioUI
from interfaz.caja import CajaUI
from interfaz.reportes import ReportesUI
from interfaz.usuarios import UsuariosUI

class DashboardUI:
    """Dashboard principal del sistema."""
    
    def __init__(self, parent, user, logout_callback):
        self.parent = parent
        self.user = user
        self.logout_callback = logout_callback
        
        # Crear interfaz principal
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz principal."""
        # Barra superior con información del usuario
        top_frame = ttk.Frame(self.parent, relief=tk.RAISED, borderwidth=1)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        user_label = ttk.Label(top_frame, text=f"Usuario: {self.user['nombre']} ({self.user['rol']})", 
                              font=("Arial", 11, "bold"))
        user_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        logout_btn = ttk.Button(top_frame, text="Cerrar Sesión", command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Frame principal con menú y contenido
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Menú lateral
        self.menu_frame = ttk.Frame(main_frame, width=200, relief=tk.SUNKEN, borderwidth=1)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # Título del menú
        menu_title = ttk.Label(self.menu_frame, text="Menú Principal", font=("Arial", 12, "bold"))
        menu_title.pack(pady=10, padx=5)
        
        # Botones del menú
        self.crear_botones_menu()
        
        # Frame de contenido
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Mostrar dashboard inicial
        self.mostrar_dashboard()
    
    def crear_botones_menu(self):
        """Crea los botones del menú según el rol del usuario."""
        rol = self.user['rol']
        
        # Botones comunes para todos
        ttk.Button(self.menu_frame, text="Dashboard", command=self.mostrar_dashboard, width=20).pack(pady=5, padx=5)
        
        # Menú según rol
        if rol == "Administrador":
            ttk.Button(self.menu_frame, text="Gestión de Usuarios", command=self.abrir_usuarios, width=20).pack(pady=5, padx=5)
            ttk.Button(self.menu_frame, text="Gestión de Productos", command=self.abrir_productos, width=20).pack(pady=5, padx=5)
            ttk.Button(self.menu_frame, text="Gestión de Clientes", command=self.abrir_clientes, width=20).pack(pady=5, padx=5)
            ttk.Button(self.menu_frame, text="Inventario", command=self.abrir_inventario, width=20).pack(pady=5, padx=5)
            ttk.Button(self.menu_frame, text="Punto de Venta", command=self.abrir_ventas, width=20).pack(pady=5, padx=5)
            ttk.Button(self.menu_frame, text="Control de Caja", command=self.abrir_caja, width=20).pack(pady=5, padx=5)
            ttk.Button(self.menu_frame, text="Reportes", command=self.abrir_reportes, width=20).pack(pady=5, padx=5)
        
        elif rol == "Cajero":
            ttk.Button(self.menu_frame, text="Punto de Venta", command=self.abrir_ventas, width=20).pack(pady=5, padx=5)
            ttk.Button(self.menu_frame, text="Control de Caja", command=self.abrir_caja, width=20).pack(pady=5, padx=5)
            ttk.Button(self.menu_frame, text="Gestión de Clientes", command=self.abrir_clientes, width=20).pack(pady=5, padx=5)
        
        elif rol == "Supervisor":
            ttk.Button(self.menu_frame, text="Inventario", command=self.abrir_inventario, width=20).pack(pady=5, padx=5)
            ttk.Button(self.menu_frame, text="Reportes", command=self.abrir_reportes, width=20).pack(pady=5, padx=5)
    
    def mostrar_dashboard(self):
        """Muestra el dashboard inicial."""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Título
        title = ttk.Label(self.content_frame, text="Dashboard", font=("Arial", 18, "bold"))
        title.pack(pady=10)
        
        # Resumen de inventario
        resumen = InventarioService.get_resumen_inventario()
        
        # Alerta de Stock Crítico
        if resumen['bajo_stock'] > 0:
            alert_frame = tk.Frame(self.content_frame, bg="#FDEDEC", highlightbackground="#F1948A", highlightthickness=1, bd=0)
            alert_frame.pack(fill=tk.X, padx=10, pady=5)
            
            alert_icon = tk.Label(alert_frame, text="⚠️", font=("Arial", 14), bg="#FDEDEC", fg="#C0392B")
            alert_icon.pack(side=tk.LEFT, padx=10, pady=10)
            
            alert_text = f"¡Atención! Tienes {resumen['bajo_stock']} producto(s) con stock igual o inferior al mínimo."
            alert_label = tk.Label(alert_frame, text=alert_text, font=("Arial", 10, "bold"), bg="#FDEDEC", fg="#C0392B", justify=tk.LEFT)
            alert_label.pack(side=tk.LEFT, padx=5, pady=10)
            
            if self.user['rol'] in ["Administrador", "Supervisor"]:
                alert_btn = tk.Button(alert_frame, text="Ver Inventario", font=("Arial", 9, "bold"), bg="#E6B0AA", fg="#78281F", activebackground="#C0392B", activeforeground="white", relief=tk.FLAT, command=self.abrir_inventario)
                alert_btn.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # Frame de información
        info_frame = ttk.LabelFrame(self.content_frame, text="Información General", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        info_text = f"""
Bienvenido, {self.user['nombre']}
Rol: {self.user['rol']}
Fecha y Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

═════════════════════════════════════════

RESUMEN DE INVENTARIO:

Total de productos: {resumen['total_productos']}
Productos con stock bajo: {resumen['bajo_stock']}
Valor total del inventario: ${resumen['valor_inventario']:,.2f}

═════════════════════════════════════════

Usa el menú lateral para acceder a las 
diferentes funcionalidades del sistema.
        """
        
        info_label = ttk.Label(info_frame, text=info_text, font=("Arial", 11), justify=tk.LEFT)
        info_label.pack(fill=tk.BOTH, expand=True)
    
    def abrir_productos(self):
        """Abre la interfaz de productos."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        ProductosUI(self.content_frame, self.user)
    
    def abrir_clientes(self):
        """Abre la interfaz de clientes."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        ClientesUI(self.content_frame, self.user)
    
    def abrir_ventas(self):
        """Abre la interfaz de ventas."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        VentasUI(self.content_frame, self.user)
    
    def abrir_inventario(self):
        """Abre la interfaz de inventario."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        InventarioUI(self.content_frame, self.user)
    
    def abrir_caja(self):
        """Abre la interfaz de caja."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        CajaUI(self.content_frame, self.user)
    
    def abrir_reportes(self):
        """Abre la interfaz de reportes."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        ReportesUI(self.content_frame, self.user)
    
    def abrir_usuarios(self):
        """Abre la interfaz de usuarios."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        UsuariosUI(self.content_frame, self.user)
    
    def logout(self):
        """Cierra la sesión."""
        if messagebox.askyesno("Confirmar", "¿Deseas cerrar sesión?"):
            self.logout_callback()
