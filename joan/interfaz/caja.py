import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from servicio_caja import CajaService

class CajaUI:
    """Interfaz de control de caja."""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        
        # Marco principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = ttk.Label(main_frame, text="Control de Caja", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Frame de estado
        estado_frame = ttk.LabelFrame(main_frame, text="Estado de Cajas", padding=10)
        estado_frame.pack(fill=tk.X, pady=10)
        
        # Verificar si hay caja abierta
        cajas_abiertas = CajaService.get_cajas_abiertas(self.user['id_usuario'])
        
        if cajas_abiertas:
            caja = cajas_abiertas[0]
            
            ttk.Label(estado_frame, text="Caja Abierta", font=("Arial", 12, "bold"), foreground="green").pack()
            ttk.Label(estado_frame, text=f"Monto Inicial: ${caja['monto_inicial']:.2f}").pack()
            ttk.Label(estado_frame, text=f"Abierta desde: {caja['fecha_apertura']}").pack()
            
            # Frame para cerrar caja
            cerrar_frame = ttk.LabelFrame(main_frame, text="Cerrar Caja", padding=10)
            cerrar_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(cerrar_frame, text="Monto Final:").pack(side=tk.LEFT, padx=5)
            monto_final_entry = ttk.Entry(cerrar_frame, width=15)
            monto_final_entry.pack(side=tk.LEFT, padx=5)
            
            def cerrar_caja():
                try:
                    monto_final = float(monto_final_entry.get())
                    resultado = CajaService.cerrar_caja(caja['id_caja'], monto_final)
                    
                    if resultado:
                        mensaje = f"""Caja cerrada correctamente
                        
Monto Inicial: ${caja['monto_inicial']:.2f}
Monto Final: ${monto_final:.2f}
Total de Ventas: ${resultado['total_ventas']:.2f}
Diferencia: ${monto_final - caja['monto_inicial'] - resultado['total_ventas']:.2f}
                        """
                        messagebox.showinfo("Éxito", mensaje)
                        # Recargar interfaz
                        for widget in main_frame.winfo_children():
                            widget.destroy()
                        CajaUI(main_frame, user)
                except ValueError:
                    messagebox.showerror("Error", "Monto debe ser un número válido")
            
            ttk.Button(cerrar_frame, text="Cerrar Caja", command=cerrar_caja).pack(side=tk.LEFT, padx=5)
        
        else:
            ttk.Label(estado_frame, text="No hay caja abierta", font=("Arial", 12), foreground="red").pack()
            
            # Frame para abrir caja
            abrir_frame = ttk.LabelFrame(main_frame, text="Abrir Nueva Caja", padding=10)
            abrir_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(abrir_frame, text="Monto Inicial:").pack(side=tk.LEFT, padx=5)
            monto_inicial_entry = ttk.Entry(abrir_frame, width=15)
            monto_inicial_entry.pack(side=tk.LEFT, padx=5)
            
            def abrir_caja():
                try:
                    monto_inicial = float(monto_inicial_entry.get())
                    
                    if CajaService.abrir_caja(self.user['id_usuario'], monto_inicial):
                        messagebox.showinfo("Éxito", "Caja abierta correctamente")
                        # Recargar interfaz
                        for widget in main_frame.winfo_children():
                            widget.destroy()
                        CajaUI(main_frame, user)
                    else:
                        messagebox.showerror("Error", "No se pudo abrir la caja")
                except ValueError:
                    messagebox.showerror("Error", "Monto debe ser un número válido")
            
            ttk.Button(abrir_frame, text="Abrir Caja", command=abrir_caja).pack(side=tk.LEFT, padx=5)
        
        # Historial de cajas
        historial_frame = ttk.LabelFrame(main_frame, text="Historial de Cajas", padding=10)
        historial_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("Fecha Apertura", "Monto Inicial", "Monto Final", "Diferencia", "Estado")
        tree = ttk.Treeview(historial_frame, columns=columns, height=15, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(historial_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar historial
        cajas = CajaService.get_all_cajas()
        for caja in cajas[-20:]:  # Últimas 20 cajas
            diferencia = caja['monto_final'] - caja['monto_inicial'] - caja['total_ventas'] if caja['monto_final'] else 0
            tree.insert("", tk.END, values=(
                caja['fecha_apertura'],
                f"${caja['monto_inicial']:.2f}",
                f"${caja['monto_final']:.2f}" if caja['monto_final'] else "-",
                f"${diferencia:.2f}" if caja['monto_final'] else "-",
                caja['estado']
            ))
