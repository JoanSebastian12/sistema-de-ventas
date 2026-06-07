import tkinter as tk
from tkinter import ttk, messagebox
from servicio_inventario import InventarioService

class InventarioUI:
    """Interfaz de control de inventario."""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        
        # Marco principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = ttk.Label(main_frame, text="Control de Inventario", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Crear notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Inventario Actual
        tab1 = ttk.Frame(notebook, padding=10)
        notebook.add(tab1, text="Inventario Actual")
        
        columns = ("Código", "Nombre", "Stock", "Stock Mín.", "Valor")
        tree1 = ttk.Treeview(tab1, columns=columns, height=20, show="headings")
        
        for col in columns:
            tree1.heading(col, text=col)
            tree1.column(col, width=120)
        
        scrollbar1 = ttk.Scrollbar(tab1, orient=tk.VERTICAL, command=tree1.yview)
        tree1.configure(yscroll=scrollbar1.set)
        
        tree1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar inventario actual
        productos = InventarioService.get_movimientos()
        movimientos_dict = {}
        for mov in productos:
            movimientos_dict[mov['id_producto']] = mov
        
        # Tab 2: Productos con Bajo Stock
        tab2 = ttk.Frame(notebook, padding=10)
        notebook.add(tab2, text="Stock Bajo")
        
        columns2 = ("Nombre", "Stock Actual", "Stock Mín.", "Falta")
        tree2 = ttk.Treeview(tab2, columns=columns2, height=20, show="headings")
        
        for col in columns2:
            tree2.heading(col, text=col)
            tree2.column(col, width=150)
        
        scrollbar2 = ttk.Scrollbar(tab2, orient=tk.VERTICAL, command=tree2.yview)
        tree2.configure(yscroll=scrollbar2.set)
        
        tree2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        bajo_stock = InventarioService.get_productos_bajo_stock()
        for producto in bajo_stock:
            tree2.insert("", tk.END, values=(
                producto['nombre'],
                producto['stock'],
                producto['stock_minimo'],
                producto['stock_minimo'] - producto['stock']
            ))
        
        # Tab 3: Movimientos
        tab3 = ttk.Frame(notebook, padding=10)
        notebook.add(tab3, text="Movimientos")
        
        columns3 = ("Producto", "Tipo", "Cantidad", "Fecha", "Descripción")
        tree3 = ttk.Treeview(tab3, columns=columns3, height=20, show="headings")
        
        for col in columns3:
            tree3.heading(col, text=col)
            tree3.column(col, width=120)
        
        scrollbar3 = ttk.Scrollbar(tab3, orient=tk.VERTICAL, command=tree3.yview)
        tree3.configure(yscroll=scrollbar3.set)
        
        tree3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)
        
        movimientos = InventarioService.get_movimientos()
        for mov in movimientos[:100]:  # Últimos 100 movimientos
            tree3.insert("", tk.END, values=(
                mov['nombre'],
                mov['tipo'],
                mov['cantidad'],
                mov['fecha'],
                mov['descripcion'] or "-"
            ))
