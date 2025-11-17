import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
from src.presentation.utils import FormatoRegional

class ListaGastosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_modern_widgets()
    
    def create_modern_widgets(self):
        self.primary_color = '#4361ee'
        self.success_color = '#4cc9f0'
        self.danger_color = '#f72585'
        self.card_bg = '#ffffff'
        
        main_container = tk.Frame(self, bg=self.card_bg)
        main_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.create_controls_header(main_container)
        self.create_modern_treeview(main_container)
        self.create_list_footer(main_container)
    
    def create_controls_header(self, parent):
        controls_frame = tk.Frame(parent, bg=self.card_bg)
        controls_frame.pack(fill='x', padx=0, pady=(0, 10))
        
        title_label = tk.Label(controls_frame,
                            text="📋 GASTOS REGISTRADOS",
                            font=('Arial', 12, 'bold'),
                            fg=self.primary_color,
                            bg=self.card_bg)
        title_label.pack(side='left', padx=10, pady=10)
        
        buttons_frame = tk.Frame(controls_frame, bg=self.card_bg)
        buttons_frame.pack(side='right', padx=10, pady=10)
        
        refresh_btn = tk.Button(buttons_frame,
                            text="🔄 Actualizar",
                            font=('Arial', 9, 'bold'),
                            fg='white',
                            bg='#6c757d',
                            borderwidth=0,
                            padx=15,
                            pady=8,
                            command=self.controller.actualizar_vistas)
        refresh_btn.pack(side='left', padx=(0, 8))
        
        export_btn = tk.Button(buttons_frame,
                            text="📊 Exportar Excel",
                            font=('Arial', 9, 'bold'),
                            fg='white',
                            bg=self.primary_color,
                            borderwidth=0,
                            padx=15,
                            pady=8,
                            command=self.exportar_a_excel)
        export_btn.pack(side='left', padx=(0, 8))
        
        delete_btn = tk.Button(buttons_frame,
                            text="🗑️ Eliminar",
                            font=('Arial', 9, 'bold'),
                            fg='white',
                            bg=self.danger_color,
                            borderwidth=0,
                            padx=15,
                            pady=8,
                            command=self.eliminar_gasto_seleccionado)
        delete_btn.pack(side='left')
    
    def create_modern_treeview(self, parent):
        tree_container = tk.Frame(parent, bg='#dee2e6')
        tree_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        tree_frame = tk.Frame(tree_container, bg=self.card_bg)
        tree_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        columns = ("ID", "Fecha", "Descripción", "Monto", "Categoría")
        
        self.tree = ttk.Treeview(tree_frame, 
                            columns=columns, 
                            show="headings",
                            height=15)
        
        self.tree.column("ID", width=0, stretch=False, anchor='center')
        self.tree.column("Fecha", width=100, anchor='center')
        self.tree.column("Descripción", width=250, anchor='w')
        self.tree.column("Monto", width=120, anchor='e')
        self.tree.column("Categoría", width=120, anchor='center')
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="📅 FECHA")
        self.tree.heading("Descripción", text="📝 DESCRIPCIÓN")
        self.tree.heading("Monto", text="💰 MONTO")
        self.tree.heading("Categoría", text="🏷️ CATEGORÍA")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind("<Double-1>", self.on_double_click)
    
    def create_list_footer(self, parent):
        footer_frame = tk.Frame(parent, bg='#f8f9fa')
        footer_frame.pack(fill='x', side='bottom', pady=(10, 0))
        
        self.stats_label = tk.Label(footer_frame,
                                text="Total: 0 gastos | $0.00",
                                font=('Arial', 9, 'bold'),
                                fg=self.primary_color,
                                bg='#f8f9fa')
        self.stats_label.pack(side='left', padx=10, pady=5)
        
        self.count_label = tk.Label(footer_frame,
                                text="Mostrando: 0 items",
                                font=('Arial', 9),
                                fg='#6c757d',
                                bg='#f8f9fa')
        self.count_label.pack(side='right', padx=10, pady=5)
    
    def exportar_a_excel(self):
        try:
            gastos = self.controller.obtener_gastos_mes_actual()
            
            if not gastos:
                messagebox.showinfo("Info", "No hay gastos para exportar")
                return

            archivo = filedialog.asksaveasfilename(
                title="Exportar gastos a Excel",
                defaultextension=".csv",
                initialfile=f"gastos_excel_{datetime.now().strftime('%Y%m%d')}.csv",
                filetypes=[
                    ("Archivos CSV para Excel", "*.csv"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if not archivo:
                return

            self.controller.gestor_exportacion.exportar_a_archivo(gastos, "csv", archivo)
            
            nombre_archivo = os.path.basename(archivo)
            messagebox.showinfo(
                "✅ Exportación exitosa", 
                f"Gastos exportados correctamente a:\n{nombre_archivo}\n\n"
                f"• {len(gastos)} gastos exportados\n"
                f"• Archivo listo para abrir en Excel"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
    
    def actualizar_gastos(self, gastos):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for gasto in gastos:
            values = (
                gasto.id,
                FormatoRegional.formatear_fecha(gasto.fecha),
                gasto.descripcion,
                FormatoRegional.formatear_moneda(gasto.monto, gasto.moneda),
                gasto.categoria.nombre
            )
            
            self.tree.insert("", "end", values=values)
        
        total_gastos = len(gastos)
        total_monto = sum(gasto.monto for gasto in gastos)
        
        self.stats_label.config(text=f"Total: {total_gastos} gastos | ${total_monto:,.2f}")
        self.count_label.config(text=f"Mostrando: {total_gastos} items")
    
    def eliminar_gasto_seleccionado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona un gasto para eliminar")
            return
        
        item = seleccion[0]
        valores = self.tree.item(item, 'values')
        gasto_id = int(valores[0])
        descripcion = valores[2]
        monto = valores[3]
        categoria = valores[4]
        
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar este gasto?\n\n"
            f"📝 Descripción: {descripcion}\n"
            f"💰 Monto: {monto}\n"
            f"🏷️ Categoría: {categoria}\n\n"
            f"⚠️ Esta acción no se puede deshacer."
        )
        
        if confirmacion:
            try:
                if self.controller.eliminar_gasto(gasto_id):
                    messagebox.showinfo("Éxito", "✅ Gasto eliminado correctamente")
                else:
                    messagebox.showerror("Error", "❌ No se pudo eliminar el gasto")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error al eliminar gasto: {str(e)}")
    
    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        if item:
            self.eliminar_gasto_seleccionado()