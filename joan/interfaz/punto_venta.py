import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from servicio_productos import ProductoService
from servicio_clientes import ClienteService
from servicio_ventas import VentaService

class VentasUI:
    """Interfaz de Punto de Venta."""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.carrito = []
        self.cliente_actual = None
        
        # Marco principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = ttk.Label(main_frame, text="Punto de Venta (POS)", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Frame superior: búsqueda de productos
        search_frame = ttk.LabelFrame(main_frame, text="Agregar Productos", padding=10)
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(search_frame, text="Búsqueda:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda e: self.buscar_producto())
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_producto).pack(side=tk.LEFT, padx=5)
        
        # Frame de productos encontrados
        self.productos_frame = ttk.LabelFrame(main_frame, text="Productos", padding=10)
        self.productos_frame.pack(fill=tk.X, pady=10)
        
        columns = ("Código", "Nombre", "Precio", "Stock")
        self.productos_tree = ttk.Treeview(self.productos_frame, columns=columns, height=5, show="headings")
        
        for col in columns:
            self.productos_tree.heading(col, text=col)
            self.productos_tree.column(col, width=100)
        
        self.productos_tree.pack(fill=tk.BOTH)
        self.productos_tree.bind("<Double-1>", lambda e: self.agregar_al_carrito())
        
        # Frame de cantidad
        qty_frame = ttk.Frame(search_frame)
        qty_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(qty_frame, text="Cantidad:").pack(side=tk.LEFT, padx=5)
        self.cantidad_entry = ttk.Entry(qty_frame, width=5)
        self.cantidad_entry.insert(0, "1")
        self.cantidad_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(qty_frame, text="Agregar", command=self.agregar_al_carrito).pack(side=tk.LEFT, padx=5)
        
        # Frame de carrito
        carrito_frame = ttk.LabelFrame(main_frame, text="Carrito de Compra", padding=10)
        carrito_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("Producto", "Cantidad", "Precio Unit.", "Subtotal", "")
        self.carrito_tree = ttk.Treeview(carrito_frame, columns=columns, height=10, show="headings")
        
        for col in columns:
            self.carrito_tree.heading(col, text=col)
            if col == "":
                self.carrito_tree.column(col, width=50)
            else:
                self.carrito_tree.column(col, width=100)
        
        self.carrito_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.carrito_tree.bind("<Double-1>", lambda e: self.eliminar_del_carrito())
        
        # Frame de totales
        totales_frame = ttk.LabelFrame(main_frame, text="Totales", padding=10)
        totales_frame.pack(fill=tk.X, pady=10)
        
        self.subtotal_label = ttk.Label(totales_frame, text="Subtotal: $0.00", font=("Arial", 11))
        self.subtotal_label.pack(anchor=tk.E, padx=10, pady=5)
        
        self.descuento_label = ttk.Label(totales_frame, text="Descuento: $0.00", font=("Arial", 11))
        self.descuento_label.pack(anchor=tk.E, padx=10, pady=5)
        
        self.impuestos_label = ttk.Label(totales_frame, text="Impuestos (19%): $0.00", font=("Arial", 11))
        self.impuestos_label.pack(anchor=tk.E, padx=10, pady=5)
        
        self.total_label = ttk.Label(totales_frame, text="Total: $0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(anchor=tk.E, padx=10, pady=5)
        
        # Frame de cliente y pago
        checkout_frame = ttk.LabelFrame(main_frame, text="Checkout", padding=10)
        checkout_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(checkout_frame, text="Cliente:").pack(side=tk.LEFT, padx=5)
        self.cliente_var = tk.StringVar(value="Consumidor Final")
        cliente_combo = ttk.Combobox(checkout_frame, textvariable=self.cliente_var, width=30, state="readonly")
        cliente_combo.pack(side=tk.LEFT, padx=5)
        self.actualizar_clientes()
        
        ttk.Label(checkout_frame, text="Método de Pago:").pack(side=tk.LEFT, padx=5)
        self.metodo_var = tk.StringVar(value="Efectivo")
        metodo_combo = ttk.Combobox(checkout_frame, textvariable=self.metodo_var, 
                                     values=["Efectivo", "Tarjeta", "Transferencia", "Mixto"], 
                                     width=15, state="readonly")
        metodo_combo.pack(side=tk.LEFT, padx=5)

        ttk.Label(checkout_frame, text="Descuento (%):").pack(side=tk.LEFT, padx=5)
        self.descuento_var = tk.StringVar(value="0")
        self.descuento_entry = ttk.Entry(checkout_frame, textvariable=self.descuento_var, width=5)
        self.descuento_entry.pack(side=tk.LEFT, padx=5)
        self.descuento_var.trace_add("write", lambda *args: self.actualizar_carrito())
        
        ttk.Button(checkout_frame, text="Finalizar Venta", command=self.finalizar_venta).pack(side=tk.RIGHT, padx=5)

    
    def buscar_producto(self):
        """Busca productos."""
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        
        busqueda = self.search_entry.get()
        
        if busqueda:
            productos = ProductoService.search_producto(busqueda)
        else:
            productos = ProductoService.get_all_productos()
        
        for producto in productos:
            self.productos_tree.insert("", tk.END, values=(
                producto['codigo_producto'],
                producto['nombre'],
                f"${producto['precio_venta']:.2f}",
                producto['stock']
            ))
    
    def agregar_al_carrito(self):
        """Agrega producto al carrito."""
        selection = self.productos_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un producto")
            return
        
        try:
            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "Cantidad debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número")
            return
        
        item = self.productos_tree.item(selection[0])
        codigo = item['values'][0]
        
        productos = ProductoService.get_all_productos()
        producto = next((p for p in productos if p['codigo_producto'] == codigo), None)
        
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        if cantidad > producto['stock']:
            messagebox.showerror("Error", "Stock insuficiente")
            return
        
        # Agregar al carrito
        self.carrito.append({
            'id_producto': producto['id_producto'],
            'nombre': producto['nombre'],
            'cantidad': cantidad,
            'precio_unitario': producto['precio_venta']
        })
        
        self.actualizar_carrito()
    
    def actualizar_carrito(self):
        """Actualiza la vista del carrito."""
        for item in self.carrito_tree.get_children():
            self.carrito_tree.delete(item)
        
        subtotal = 0
        for detalle in self.carrito:
            subtotal_item = detalle['cantidad'] * detalle['precio_unitario']
            subtotal += subtotal_item
            
            self.carrito_tree.insert("", tk.END, values=(
                detalle['nombre'],
                detalle['cantidad'],
                f"${detalle['precio_unitario']:.2f}",
                f"${subtotal_item:.2f}",
                "X"
            ))
        
        # Obtener descuento de la UI de forma segura
        descuento_porcentaje = 0.0
        try:
            val = self.descuento_var.get()
            if val:
                descuento_porcentaje = float(val)
                if descuento_porcentaje < 0:
                    descuento_porcentaje = 0.0
                elif descuento_porcentaje > 100:
                    descuento_porcentaje = 100.0
        except ValueError:
            pass
            
        descuento_monto = subtotal * (descuento_porcentaje / 100.0)
        subtotal_con_descuento = subtotal - descuento_monto
        impuestos = subtotal_con_descuento * 0.19
        total = subtotal_con_descuento + impuestos
        
        self.subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
        self.descuento_label.config(text=f"Descuento ({descuento_porcentaje:.1f}%): ${descuento_monto:.2f}")
        self.impuestos_label.config(text=f"Impuestos (19%): ${impuestos:.2f}")
        self.total_label.config(text=f"Total: ${total:.2f}")
    
    def eliminar_del_carrito(self):
        """Elimina producto del carrito."""
        selection = self.carrito_tree.selection()
        if not selection:
            return
        
        index = self.carrito_tree.index(selection[0])
        self.carrito.pop(index)
        self.actualizar_carrito()
    
    def actualizar_clientes(self):
        """Actualiza lista de clientes."""
        clientes = ClienteService.get_all_clientes()
        nombres = [f"{c['nombre']} ({c['documento']})" for c in clientes]
        
        # Actualizar combobox si existe
        for widget in self.parent.winfo_children():
            if isinstance(widget, ttk.Combobox) and widget.get() == "Consumidor Final":
                widget['values'] = nombres
                break
    
    def finalizar_venta(self):
        """Finaliza la venta."""
        if not self.carrito:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        # Obtener cliente
        cliente_nombre = self.cliente_var.get()
        clientes = ClienteService.get_all_clientes()
        cliente = next((c for c in clientes if f"{c['nombre']} ({c['documento']})" == cliente_nombre or c['nombre'] == cliente_nombre), None)
        
        if not cliente:
            messagebox.showerror("Error", "Cliente no válido")
            return
            
        # Obtener descuento
        descuento_porcentaje = 0.0
        try:
            val = self.descuento_var.get()
            if val:
                descuento_porcentaje = float(val)
                if descuento_porcentaje < 0 or descuento_porcentaje > 100:
                    raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El descuento debe ser un número entre 0 y 100")
            return
        
        # Crear venta
        resultado = VentaService.crear_venta(
            cliente['id_cliente'],
            self.user['id_usuario'],
            self.metodo_var.get(),
            self.carrito,
            descuento_porcentaje
        )
        
        if resultado:
            messagebox.showinfo("Éxito", f"Venta registrada.\nFactura: {resultado['numero_factura']}\nTotal: ${resultado['total']:.2f}")
            
            # Abrir ticket automáticamente en Windows
            import os
            try:
                os.startfile(resultado['ruta_ticket'])
            except Exception:
                try:
                    import subprocess
                    subprocess.Popen(['notepad.exe', resultado['ruta_ticket']])
                except Exception:
                    pass
            
            self.carrito = []
            self.descuento_var.set("0")
            self.cantidad_entry.delete(0, tk.END)
            self.cantidad_entry.insert(0, "1")
            self.search_entry.delete(0, tk.END)
            self.actualizar_carrito()
            self.buscar_producto()
        else:
            messagebox.showerror("Error", "Error al registrar la venta")
