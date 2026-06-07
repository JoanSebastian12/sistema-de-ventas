import tkinter as tk
from tkinter import ttk, messagebox
from servicio_productos import ProductoService

class ProductosUI:
    """Interfaz de gestión de productos."""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.productos = []
        
        # Marco principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = ttk.Label(main_frame, text="Gestión de Productos", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Buscar Producto", padding=10)
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(search_frame, text="Búsqueda:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.buscar())
        
        ttk.Button(search_frame, text="Limpiar", command=self.limpiar_busqueda).pack(side=tk.LEFT, padx=5)
        
        if self.user['rol'] == "Administrador":
            ttk.Button(search_frame, text="Nuevo Producto", command=self.nuevo_producto).pack(side=tk.RIGHT, padx=5)
        
        # Frame de tabla
        table_frame = ttk.LabelFrame(main_frame, text="Productos", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crear tabla
        columns = ("Código", "Nombre", "Precio Venta", "Stock", "Stock Mín.", "Categoría")
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if self.user['rol'] == "Administrador":
            self.tree.bind("<Double-1>", lambda e: self.editar_producto())
        
        # Cargar productos
        self.cargar_productos()
    
    def cargar_productos(self):
        """Carga la lista de productos."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.productos = ProductoService.get_all_productos()
        
        for producto in self.productos:
            self.tree.insert("", tk.END, values=(
                producto['codigo_producto'],
                producto['nombre'],
                f"${producto['precio_venta']:.2f}",
                producto['stock'],
                producto['stock_minimo'],
                producto['categoria'] or "-"
            ))
    
    def buscar(self):
        """Busca productos."""
        busqueda = self.search_entry.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if busqueda:
            productos = ProductoService.search_producto(busqueda)
        else:
            productos = ProductoService.get_all_productos()
        
        for producto in productos:
            self.tree.insert("", tk.END, values=(
                producto['codigo_producto'],
                producto['nombre'],
                f"${producto['precio_venta']:.2f}",
                producto['stock'],
                producto['stock_minimo'],
                producto['categoria'] or "-"
            ))
    
    def limpiar_busqueda(self):
        """Limpia la búsqueda."""
        self.search_entry.delete(0, tk.END)
        self.cargar_productos()
    
    def nuevo_producto(self):
        """Abre ventana para crear nuevo producto."""
        ventana = tk.Toplevel(self.parent)
        ventana.title("Nuevo Producto")
        ventana.geometry("400x400")
        
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos
        ttk.Label(frame, text="Código:").pack(pady=5)
        codigo_entry = ttk.Entry(frame, width=30)
        codigo_entry.pack(pady=5)
        
        ttk.Label(frame, text="Nombre:").pack(pady=5)
        nombre_entry = ttk.Entry(frame, width=30)
        nombre_entry.pack(pady=5)
        
        ttk.Label(frame, text="Descripción:").pack(pady=5)
        desc_entry = ttk.Entry(frame, width=30)
        desc_entry.pack(pady=5)
        
        ttk.Label(frame, text="Precio Compra:").pack(pady=5)
        precio_compra_entry = ttk.Entry(frame, width=30)
        precio_compra_entry.pack(pady=5)
        
        ttk.Label(frame, text="Precio Venta:").pack(pady=5)
        precio_venta_entry = ttk.Entry(frame, width=30)
        precio_venta_entry.pack(pady=5)
        
        ttk.Label(frame, text="Stock:").pack(pady=5)
        stock_entry = ttk.Entry(frame, width=30)
        stock_entry.pack(pady=5)
        
        ttk.Label(frame, text="Stock Mínimo:").pack(pady=5)
        stock_min_entry = ttk.Entry(frame, width=30)
        stock_min_entry.pack(pady=5)
        
        ttk.Label(frame, text="Categoría:").pack(pady=5)
        categoria_entry = ttk.Entry(frame, width=30)
        categoria_entry.pack(pady=5)
        
        def guardar():
            if not all([codigo_entry.get(), nombre_entry.get(), precio_compra_entry.get(), 
                       precio_venta_entry.get(), stock_entry.get()]):
                messagebox.showerror("Error", "Completa todos los campos obligatorios")
                return
            
            try:
                precio_compra = float(precio_compra_entry.get())
                precio_venta = float(precio_venta_entry.get())
                stock = int(stock_entry.get())
                stock_min = int(stock_min_entry.get()) if stock_min_entry.get() else 5
                
                if precio_venta <= precio_compra:
                    messagebox.showerror("Error", "Precio venta debe ser mayor que precio compra")
                    return
                
                ProductoService.create_producto(
                    codigo_entry.get(),
                    nombre_entry.get(),
                    desc_entry.get(),
                    precio_compra,
                    precio_venta,
                    stock,
                    stock_min,
                    categoria_entry.get()
                )
                
                messagebox.showinfo("Éxito", "Producto creado correctamente")
                ventana.destroy()
                self.cargar_productos()
            except ValueError:
                messagebox.showerror("Error", "Verifica los valores numéricos")
        
        ttk.Button(frame, text="Guardar", command=guardar).pack(pady=20)
    
    def editar_producto(self):
        """Abre ventana para editar producto."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un producto")
            return
        
        item = self.tree.item(selection[0])
        codigo = item['values'][0]
        
        # Encontrar producto por código
        producto = next((p for p in self.productos if p['codigo_producto'] == codigo), None)
        
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        ventana = tk.Toplevel(self.parent)
        ventana.title("Editar Producto")
        ventana.geometry("400x350")
        
        frame = ttk.Frame(ventana, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Nombre:").pack(pady=5)
        nombre_entry = ttk.Entry(frame, width=30)
        nombre_entry.insert(0, producto['nombre'])
        nombre_entry.pack(pady=5)
        
        ttk.Label(frame, text="Descripción:").pack(pady=5)
        desc_entry = ttk.Entry(frame, width=30)
        desc_entry.insert(0, producto['descripcion'] or "")
        desc_entry.pack(pady=5)
        
        ttk.Label(frame, text="Precio Compra:").pack(pady=5)
        precio_compra_entry = ttk.Entry(frame, width=30)
        precio_compra_entry.insert(0, str(producto['precio_compra']))
        precio_compra_entry.pack(pady=5)
        
        ttk.Label(frame, text="Precio Venta:").pack(pady=5)
        precio_venta_entry = ttk.Entry(frame, width=30)
        precio_venta_entry.insert(0, str(producto['precio_venta']))
        precio_venta_entry.pack(pady=5)
        
        ttk.Label(frame, text="Stock Mínimo:").pack(pady=5)
        stock_min_entry = ttk.Entry(frame, width=30)
        stock_min_entry.insert(0, str(producto['stock_minimo']))
        stock_min_entry.pack(pady=5)
        
        ttk.Label(frame, text="Categoría:").pack(pady=5)
        categoria_entry = ttk.Entry(frame, width=30)
        categoria_entry.insert(0, producto['categoria'] or "")
        categoria_entry.pack(pady=5)
        
        def guardar():
            try:
                ProductoService.update_producto(
                    producto['id_producto'],
                    nombre_entry.get(),
                    desc_entry.get(),
                    float(precio_compra_entry.get()),
                    float(precio_venta_entry.get()),
                    int(stock_min_entry.get()),
                    categoria_entry.get()
                )
                
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                ventana.destroy()
                self.cargar_productos()
            except ValueError:
                messagebox.showerror("Error", "Verifica los valores")
        
        ttk.Button(frame, text="Guardar", command=guardar).pack(pady=20)
