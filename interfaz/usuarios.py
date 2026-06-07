import tkinter as tk
from tkinter import ttk, messagebox
from autenticacion import AuthService

class UsuariosUI:
    """Interfaz de gestión de usuarios."""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        
        # Marco principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = ttk.Label(main_frame, text="Gestión de Usuarios", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Buscar Usuario", padding=10)
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(search_frame, text="Búsqueda:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.buscar())
        
        ttk.Button(search_frame, text="Limpiar", command=self.limpiar_busqueda).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Nuevo Usuario", command=self.nuevo_usuario).pack(side=tk.RIGHT, padx=5)
        
        # Frame de tabla
        table_frame = ttk.LabelFrame(main_frame, text="Usuarios", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crear tabla
        columns = ("Usuario", "Nombre", "Rol", "Email", "Estado")
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<Double-1>", lambda e: self.editar_usuario())
        
        # Cargar usuarios
        self.cargar_usuarios()
    
    def cargar_usuarios(self):
        """Carga la lista de usuarios."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        usuarios = AuthService.get_all_usuarios()
        
        for usuario in usuarios:
            self.tree.insert("", tk.END, values=(
                usuario['usuario'],
                usuario['nombre'],
                usuario['rol'],
                usuario['email'] or "-",
                "Activo" if usuario['estado'] == 1 else "Inactivo"
            ))
    
    def buscar(self):
        """Busca usuarios."""
        busqueda = self.search_entry.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        usuarios = AuthService.get_all_usuarios()
        
        if busqueda:
            usuarios = [u for u in usuarios if busqueda.lower() in u['usuario'].lower() or 
                                               busqueda.lower() in u['nombre'].lower()]
        
        for usuario in usuarios:
            self.tree.insert("", tk.END, values=(
                usuario['usuario'],
                usuario['nombre'],
                usuario['rol'],
                usuario['email'] or "-",
                "Activo" if usuario['estado'] == 1 else "Inactivo"
            ))
    
    def limpiar_busqueda(self):
        """Limpia la búsqueda."""
        self.search_entry.delete(0, tk.END)
        self.cargar_usuarios()
    
    def nuevo_usuario(self):
        """Abre ventana para crear nuevo usuario."""
        ventana = tk.Toplevel(self.parent)
        ventana.title("Nuevo Usuario")
        ventana.geometry("400x400")
        
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Usuario:").pack(pady=5)
        usuario_entry = ttk.Entry(frame, width=30)
        usuario_entry.pack(pady=5)
        
        ttk.Label(frame, text="Nombre:").pack(pady=5)
        nombre_entry = ttk.Entry(frame, width=30)
        nombre_entry.pack(pady=5)
        
        ttk.Label(frame, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(frame, width=30)
        email_entry.pack(pady=5)
        
        ttk.Label(frame, text="Contraseña:").pack(pady=5)
        password_entry = ttk.Entry(frame, width=30, show="*")
        password_entry.pack(pady=5)
        
        ttk.Label(frame, text="Rol:").pack(pady=5)
        rol_var = tk.StringVar(value="Cajero")
        rol_combo = ttk.Combobox(frame, textvariable=rol_var, 
                                values=["Administrador", "Cajero", "Supervisor"], 
                                width=27, state="readonly")
        rol_combo.pack(pady=5)
        
        def guardar():
            if not all([usuario_entry.get(), nombre_entry.get(), password_entry.get()]):
                messagebox.showerror("Error", "Completa todos los campos obligatorios")
                return
            
            if AuthService.create_user(
                usuario_entry.get(),
                password_entry.get(),
                nombre_entry.get(),
                email_entry.get(),
                rol_var.get()
            ):
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                ventana.destroy()
                self.cargar_usuarios()
            else:
                err = getattr(AuthService, 'last_error', None)
                msg = f"Error al crear usuario: {err}" if err else "El usuario ya existe"
                messagebox.showerror("Error", msg)
        
        ttk.Button(frame, text="Guardar", command=guardar).pack(pady=20)
    
    def editar_usuario(self):
        """Abre ventana para editar usuario."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un usuario")
            return
        
        item = self.tree.item(selection[0])
        usuario_nombre = item['values'][0]
        
        usuarios = AuthService.get_all_usuarios()
        usuario = next((u for u in usuarios if u['usuario'] == usuario_nombre), None)
        
        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado")
            return
        
        ventana = tk.Toplevel(self.parent)
        ventana.title("Editar Usuario")
        ventana.geometry("400x400")
        
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Usuario:", font=("Arial", 10, "bold")).pack(pady=5)
        ttk.Label(frame, text=usuario['usuario']).pack(pady=5)
        
        ttk.Label(frame, text="Nombre:").pack(pady=5)
        nombre_entry = ttk.Entry(frame, width=30)
        nombre_entry.insert(0, usuario['nombre'])
        nombre_entry.pack(pady=5)
        
        ttk.Label(frame, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(frame, width=30)
        email_entry.insert(0, usuario['email'] or "")
        email_entry.pack(pady=5)
        
        ttk.Label(frame, text="Rol:").pack(pady=5)
        rol_var = tk.StringVar(value=usuario['rol'])
        rol_combo = ttk.Combobox(frame, textvariable=rol_var, 
                                values=["Administrador", "Cajero", "Supervisor"], 
                                width=27, state="readonly")
        rol_combo.pack(pady=5)
        
        ttk.Label(frame, text="Estado:").pack(pady=5)
        estado_var = tk.StringVar(value="Activo" if usuario['estado'] == 1 else "Inactivo")
        estado_combo = ttk.Combobox(frame, textvariable=estado_var, 
                                   values=["Activo", "Inactivo"], 
                                   width=27, state="readonly")
        estado_combo.pack(pady=5)
        
        def guardar():
            ok = AuthService.update_user(
                usuario['id_usuario'],
                nombre_entry.get(),
                email_entry.get(),
                rol_var.get(),
                1 if estado_var.get() == "Activo" else 0
            )
            if ok:
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                ventana.destroy()
                self.cargar_usuarios()
            else:
                err = getattr(AuthService, 'last_error', None)
                msg = f"Error al actualizar usuario: {err}" if err else "No se pudo actualizar el usuario"
                messagebox.showerror("Error", msg)
        
        ttk.Button(frame, text="Guardar", command=guardar).pack(pady=20)
