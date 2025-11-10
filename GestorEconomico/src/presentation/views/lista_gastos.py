import tkinter as tk
from tkinter import ttk, messagebox
from src.presentation.utils import FormatoRegional
from .dialogo_exportacion import ExportacionDialog

class ListaGastosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(self, text="📋 Gastos del Mes Actual", 
                font=("Arial", 12, "bold")).pack(pady=10, anchor="w")
        
        controles_frame = ttk.Frame(self)
        controles_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(controles_frame, text="Actualizar", 
                command=self.controller.actualizar_vistas).pack(side="left")
        
        ttk.Button(controles_frame, text="Exportar", 
                command=self.mostrar_dialogo_exportacion).pack(side="left", padx=(5, 0))
        
        # BOTÓN NUEVO PARA ELIMINAR
        ttk.Button(controles_frame, text="Eliminar Seleccionado", 
                command=self.eliminar_gasto_seleccionado, 
                style="Danger.TButton").pack(side="left", padx=(5, 0))
        
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # AGREGAR COLUMNA OCULTA PARA ID
        columns = ("ID", "Fecha", "Descripción", "Monto", "Categoría")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Monto", text="Monto")
        self.tree.heading("Categoría", text="Categoría")
        
        # OCULTAR COLUMNA ID
        self.tree.column("ID", width=0, stretch=False)
        self.tree.column("Fecha", width=100, anchor="center")
        self.tree.column("Descripción", width=250)
        self.tree.column("Monto", width=100, anchor="e")
        self.tree.column("Categoría", width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # BIND PARA DOBLE CLIC
        self.tree.bind("<Double-1>", self.on_double_click)
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def actualizar_gastos(self, gastos):
        self.tree.delete(*self.tree.get_children())
        
        for gasto in gastos:
            self.tree.insert("", "end", values=(
                gasto.id,  # AGREGAR ID OCULTO
                FormatoRegional.formatear_fecha(gasto.fecha),
                gasto.descripcion,
                FormatoRegional.formatear_moneda(gasto.monto, gasto.moneda),
                gasto.categoria.nombre
            ))
    
    def eliminar_gasto_seleccionado(self):
        """Eliminar el gasto seleccionado en la lista"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona un gasto para eliminar")
            return
        
        item = seleccion[0]
        valores = self.tree.item(item, 'values')
        gasto_id = int(valores[0])  # ID está en la primera columna (oculta)
        descripcion = valores[2]
        monto = valores[3]
        categoria = valores[4]
        
        # Confirmar eliminación
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
        """Manejar doble clic para eliminar"""
        # Solo eliminar si se hace clic en un ítem (no en área vacía)
        item = self.tree.identify('item', event.x, event.y)
        if item:
            self.eliminar_gasto_seleccionado()
    
    def mostrar_dialogo_exportacion(self):
        dialogo = ExportacionDialog(self, self.controller)
        self.wait_window(dialogo)