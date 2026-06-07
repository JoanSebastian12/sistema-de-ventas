import tkinter as tk
from tkinter import ttk, messagebox
from autenticacion import AuthService

class LoginUI:
    """Interfaz de login."""
    
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        
        # Marco principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, text="Sistema de Gestión de Ventas", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(main_frame, text="Iniciar Sesión", font=("Arial", 14))
        subtitle_label.pack(pady=10)
        
        # Login frame
        login_frame = ttk.Frame(main_frame)
        login_frame.pack(pady=30)
        
        # Usuario
        ttk.Label(login_frame, text="Usuario:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.usuario_entry = ttk.Entry(login_frame, width=30, font=("Arial", 11))
        self.usuario_entry.grid(row=0, column=1, pady=10, padx=10)
        self.usuario_entry.focus()
        
        # Contraseña
        ttk.Label(login_frame, text="Contraseña:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.password_entry = ttk.Entry(login_frame, width=30, font=("Arial", 11), show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        login_btn = ttk.Button(button_frame, text="Ingresar", command=self.login)
        login_btn.pack(side=tk.LEFT, padx=10)
        
        # Información de ayuda
        info_label = ttk.Label(main_frame, text="Usuario de prueba: admin | Contraseña: admin123", 
                              font=("Arial", 9, "italic"), foreground="gray")
        info_label.pack(pady=20)
        
        # Bind Enter key
        self.usuario_entry.bind("<Return>", lambda e: self.login())
        self.password_entry.bind("<Return>", lambda e: self.login())
    
    def login(self):
        """Realiza el login."""
        usuario = self.usuario_entry.get()
        contraseña = self.password_entry.get()
        
        if not usuario or not contraseña:
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return
        
        user = AuthService.login(usuario, contraseña)
        
        if user:
            messagebox.showinfo("Éxito", f"Bienvenido {user['nombre']}")
            self.callback(user)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.password_entry.delete(0, tk.END)
            self.usuario_entry.focus()
