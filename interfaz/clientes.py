import tkinter as tk
from tkinter import ttk, messagebox
from servicio_clientes import ClienteService

class ClientesUI:
    """Interfaz de gestión de clientes."""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        
        # Marco principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = ttk.Label(main_frame, text="Gestión de Clientes", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Buscar Cliente", padding=10)
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(search_frame, text="Búsqueda:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.buscar())
        
        ttk.Button(search_frame, text="Limpiar", command=self.limpiar_busqueda).pack(side=tk.LEFT, padx=5)
        
        if self.user['rol'] in ["Administrador", "Cajero"]:
            ttk.Button(search_frame, text="Nuevo Cliente", command=self.nuevo_cliente).pack(side=tk.RIGHT, padx=5)
        
        # Frame de tabla
        table_frame = ttk.LabelFrame(main_frame, text="Clientes", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crear tabla
        columns = ("Nombre", "Documento", "Teléfono", "Email", "Dirección")
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<Double-1>", lambda e: self.ver_historial())
        
        # Cargar clientes
        self.cargar_clientes()
    
    def cargar_clientes(self):
        """Carga la lista de clientes."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        clientes = ClienteService.get_all_clientes()
        
        for cliente in clientes:
            self.tree.insert("", tk.END, values=(
                cliente['nombre'],
                cliente['documento'],
                cliente['telefono'] or "-",
                cliente['email'] or "-",
                cliente['direccion'] or "-"
            ))
    
    def buscar(self):
        """Busca clientes."""
        busqueda = self.search_entry.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if busqueda:
            clientes = ClienteService.search_cliente(busqueda)
        else:
            clientes = ClienteService.get_all_clientes()
        
        for cliente in clientes:
            self.tree.insert("", tk.END, values=(
                cliente['nombre'],
                cliente['documento'],
                cliente['telefono'] or "-",
                cliente['email'] or "-",
                cliente['direccion'] or "-"
            ))
    
    def limpiar_busqueda(self):
        """Limpia la búsqueda."""
        self.search_entry.delete(0, tk.END)
        self.cargar_clientes()
    
    def nuevo_cliente(self):
        """Abre ventana para crear nuevo cliente."""
        ventana = tk.Toplevel(self.parent)
        ventana.title("Nuevo Cliente")
        ventana.geometry("400x350")
        
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Nombre:").pack(pady=5)
        nombre_entry = ttk.Entry(frame, width=30)
        nombre_entry.pack(pady=5)
        
        ttk.Label(frame, text="Documento:").pack(pady=5)
        documento_entry = ttk.Entry(frame, width=30)
        documento_entry.pack(pady=5)
        
        ttk.Label(frame, text="Teléfono:").pack(pady=5)
        telefono_entry = ttk.Entry(frame, width=30)
        telefono_entry.pack(pady=5)
        
        ttk.Label(frame, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(frame, width=30)
        email_entry.pack(pady=5)
        
        ttk.Label(frame, text="Dirección:").pack(pady=5)
        direccion_entry = ttk.Entry(frame, width=30)
        direccion_entry.pack(pady=5)
        
        def guardar():
            if not nombre_entry.get() or not documento_entry.get():
                messagebox.showerror("Error", "Nombre y Documento son obligatorios")
                return
            
            if ClienteService.create_cliente(
                nombre_entry.get(),
                documento_entry.get(),
                telefono_entry.get(),
                email_entry.get(),
                direccion_entry.get()
            ):
                messagebox.showinfo("Éxito", "Cliente creado correctamente")
                ventana.destroy()
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", "El documento ya existe")
        
        ttk.Button(frame, text="Guardar", command=guardar).pack(pady=20)
    
    def ver_historial(self):
        """Ver historial de compras del cliente seleccionado."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        documento = item['values'][1]
        
        clientes = ClienteService.get_all_clientes()
        cliente = next((c for c in clientes if c['documento'] == documento), None)
        
        if not cliente:
            return
        
        historial = ClienteService.get_historial_compras(cliente['id_cliente'])
        
        ventana = tk.Toplevel(self.parent)
        ventana.title(f"Historial de {cliente['nombre']}")
        ventana.geometry("600x400")
        
        frame = ttk.Frame(ventana, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"Historial de {cliente['nombre']}", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Crear tabla
        columns = ("Factura", "Fecha", "Total")
        tree = ttk.Treeview(frame, columns=columns, height=15, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for venta in historial:
            tree.insert("", tk.END, values=(
                venta['numero_factura'],
                venta['fecha'],
                f"${venta['total']:.2f}"
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
