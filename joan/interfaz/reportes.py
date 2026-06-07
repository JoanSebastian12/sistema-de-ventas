import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
from fpdf import FPDF
from servicio_reportes import ReporteService

class ReportesUI:
    """Interfaz de reportes."""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        
        # Marco principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = ttk.Label(main_frame, text="Reportes", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Crear notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Ventas Diarias
        tab1 = ttk.Frame(notebook, padding=10)
        notebook.add(tab1, text="Ventas Diarias")
        
        ttk.Label(tab1, text="Fecha:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        fecha_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        fecha_entry = ttk.Entry(tab1, textvariable=fecha_var, width=12)
        fecha_entry.pack(side=tk.LEFT, padx=5)
        
        def mostrar_ventas_diarias():
            fecha = fecha_var.get()
            reportes = ReporteService.ventas_diarias(fecha)
            mostrar_reporte(report_frame1, "Ventas Diarias", reportes, ["Número Factura", "Cliente", "Total", "Método Pago"])
        
        ttk.Button(tab1, text="Ver Reporte", command=mostrar_ventas_diarias).pack(side=tk.LEFT, padx=5)
        report_frame1 = ttk.Frame(tab1)
        report_frame1.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 2: Ventas Mensuales
        tab2 = ttk.Frame(notebook, padding=10)
        notebook.add(tab2, text="Ventas Mensuales")
        
        ttk.Label(tab2, text="Año:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        anio_var = tk.StringVar(value=str(datetime.now().year))
        anio_entry = ttk.Entry(tab2, textvariable=anio_var, width=6)
        anio_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(tab2, text="Mes:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        mes_var = tk.StringVar(value=str(datetime.now().month))
        mes_entry = ttk.Entry(tab2, textvariable=mes_var, width=4)
        mes_entry.pack(side=tk.LEFT, padx=5)
        
        def mostrar_ventas_mensuales():
            reportes = ReporteService.ventas_mensuales(int(anio_var.get()), int(mes_var.get()))
            mostrar_reporte(report_frame2, "Ventas Mensuales", reportes, ["Número Factura", "Fecha", "Total"])
        
        ttk.Button(tab2, text="Ver Reporte", command=mostrar_ventas_mensuales).pack(side=tk.LEFT, padx=5)
        report_frame2 = ttk.Frame(tab2)
        report_frame2.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 3: Productos Más Vendidos
        tab3 = ttk.Frame(notebook, padding=10)
        notebook.add(tab3, text="Productos Vendidos")
        
        def mostrar_productos_vendidos():
            reportes = ReporteService.productos_mas_vendidos()
            mostrar_reporte(report_frame3, "Productos Vendidos", reportes, ["Producto", "Cantidad Vendida", "Ingresos"])
        
        ttk.Button(tab3, text="Ver Reporte", command=mostrar_productos_vendidos).pack(side=tk.LEFT, padx=5)
        report_frame3 = ttk.Frame(tab3)
        report_frame3.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 4: Ganancias por Producto
        tab4 = ttk.Frame(notebook, padding=10)
        notebook.add(tab4, text="Ganancias")
        
        def mostrar_ganancias():
            reportes = ReporteService.ganancias_por_producto()
            mostrar_reporte(report_frame4, "Ganancias", reportes, ["Producto", "Costo Total", "Ingresos", "Ganancia"])
        
        ttk.Button(tab4, text="Ver Reporte", command=mostrar_ganancias).pack(side=tk.LEFT, padx=5)
        report_frame4 = ttk.Frame(tab4)
        report_frame4.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 5: Inventario
        tab5 = ttk.Frame(notebook, padding=10)
        notebook.add(tab5, text="Inventario")
        
        def mostrar_inventario():
            reportes = ReporteService.inventario_actual()
            mostrar_reporte(report_frame5, "Inventario", reportes, ["Producto", "Stock", "Costo Unitario", "Valor Total"])
        
        ttk.Button(tab5, text="Ver Reporte", command=mostrar_inventario).pack(side=tk.LEFT, padx=5)
        report_frame5 = ttk.Frame(tab5)
        report_frame5.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 6: Resumen Financiero
        tab6 = ttk.Frame(notebook, padding=10)
        notebook.add(tab6, text="Resumen Financiero")
        
        resumen = ReporteService.resumen_financiero()
        
        resumen_text = f"""
RESUMEN FINANCIERO DEL PERÍODO
═════════════════════════════════════

Total de Ventas: ${resumen['total_ventas']:.2f}
Total de Ingresos: ${resumen['total_ingresos']:.2f}
Total de Costos: ${resumen['total_costos']:.2f}
Ganancia Neta: ${resumen['total_ingresos'] - resumen['total_costos']:.2f}

Número de Transacciones: {resumen['num_transacciones']}
Número de Productos Vendidos: {resumen['num_productos']}

Valor del Inventario: ${resumen['valor_inventario']:.2f}
        """
        
        ttk.Label(tab6, text=resumen_text, font=("Arial", 10), justify=tk.LEFT).pack(fill=tk.BOTH, expand=True)
        ttk.Button(tab6, text="Exportar Resumen a PDF", command=lambda: exportar_resumen_financiero_pdf(resumen)).pack(pady=10)

def exportar_reporte_pdf(titulo, datos, columnas):
    if not datos:
        messagebox.showwarning("Advertencia", "No hay datos para exportar en PDF.")
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")],
        initialfile=f"{titulo.replace(' ', '_')}.pdf"
    )
    if not ruta:
        return

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, titulo, ln=True, align="C")
        pdf.ln(5)

        pdf.set_font("Arial", "B", 10)
        page_width = pdf.w - 2 * pdf.l_margin
        col_width = page_width / len(columnas)

        for col in columnas:
            pdf.cell(col_width, 8, str(col), border=1, align="C")
        pdf.ln()

        pdf.set_font("Arial", "", 9)
        for fila in datos:
            fila_dict = dict(fila) if not isinstance(fila, dict) else fila
            for valor in fila_dict.values():
                pdf.cell(col_width, 8, str(valor), border=1)
            pdf.ln()

        pdf.output(ruta)
        messagebox.showinfo("Éxito", f"Reporte exportado correctamente a {ruta}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar el reporte en PDF:\n{e}")


def exportar_resumen_financiero_pdf(resumen):
    ruta = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")],
        initialfile="Resumen_Financiero.pdf"
    )
    if not ruta:
        return

    try:
        texto = (
            "RESUMEN FINANCIERO DEL PERÍODO\n"
            "═════════════════════════════════════\n\n"
            f"Total de Ventas: ${resumen['total_ventas']:.2f}\n"
            f"Total de Ingresos: ${resumen['total_ingresos']:.2f}\n"
            f"Total de Costos: ${resumen['total_costos']:.2f}\n"
            f"Ganancia Neta: ${resumen['total_ingresos'] - resumen['total_costos']:.2f}\n\n"
            f"Número de Transacciones: {resumen['num_transacciones']}\n"
            f"Número de Productos Vendidos: {resumen['num_productos']}\n\n"
            f"Valor del Inventario: ${resumen['valor_inventario']:.2f}\n"
        )

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Resumen Financiero", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, texto)
        pdf.output(ruta)
        messagebox.showinfo("Éxito", f"Resumen financiero exportado correctamente a {ruta}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar el resumen en PDF:\n{e}")


def mostrar_reporte(frame, titulo, datos, columnas):
    """Helper para mostrar reporte en tabla."""
    # Limpiar frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    if not datos:
        ttk.Label(frame, text="No hay datos para mostrar").pack(pady=20)
        return
    
    # Crear tabla
    tree = ttk.Treeview(frame, columns=columnas, height=15, show="headings")
    
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    # Insertar datos
    for fila in datos:
        fila_dict = dict(fila) if not isinstance(fila, dict) else fila
        valores = [str(v) for v in fila_dict.values()]
        tree.insert("", tk.END, values=valores)
    
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    ttk.Button(frame, text="Exportar reporte a PDF", command=lambda: exportar_reporte_pdf(titulo, datos, columnas)).pack(side=tk.BOTTOM, pady=10)
