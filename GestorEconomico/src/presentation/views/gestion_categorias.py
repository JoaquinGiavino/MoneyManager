import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.domain.entities import Categoria

class GestionCategoriasView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.categorias = []
        self.create_widgets()
        self.cargar_categorias()
    
    def create_widgets(self):
        # Colores modernos
        self.primary_color = '#4361ee'
        self.success_color = '#4cc9f0'
        self.danger_color = '#f72585'
        self.warning_color = '#f8961e'
        self.card_bg = '#ffffff'
        self.light_bg = '#f8f9fa'
        
        # Container principal
        main_frame = tk.Frame(self, bg=self.card_bg)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, 
                             text="🏷️ GESTIÓN DE CATEGORÍAS",
                             font=('Arial', 16, 'bold'),
                             fg=self.primary_color,
                             bg=self.card_bg)
        title_label.pack(pady=(0, 20))
        
        # Frame para formulario de nueva categoría
        form_frame = tk.LabelFrame(main_frame, 
                                 text="➕ NUEVA CATEGORÍA PERSONALIZADA",
                                 font=('Arial', 10, 'bold'),
                                 bg=self.card_bg,
                                 padx=15, pady=15)
        form_frame.pack(fill='x', pady=(0, 20))
        
        # Grid para formulario
        tk.Label(form_frame, text="Nombre:", font=('Arial', 9, 'bold'), 
                bg=self.card_bg).grid(row=0, column=0, sticky='w', pady=8)
        self.nombre_entry = tk.Entry(form_frame, width=30, font=('Arial', 10))
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        
        tk.Label(form_frame, text="Presupuesto mensual:", font=('Arial', 9, 'bold'), 
                bg=self.card_bg).grid(row=1, column=0, sticky='w', pady=8)
        
        presupuesto_frame = tk.Frame(form_frame, bg=self.card_bg)
        presupuesto_frame.grid(row=1, column=1, sticky='w', padx=10, pady=8)
        
        self.presupuesto_entry = tk.Entry(presupuesto_frame, width=15, font=('Arial', 10))
        self.presupuesto_entry.pack(side='left')
        self.presupuesto_entry.insert(0, "0.00")
        
        tk.Label(presupuesto_frame, text="$", font=('Arial', 10, 'bold'), 
                bg=self.card_bg).pack(side='left', padx=(8, 0))
        
        # Botón crear
        crear_btn = tk.Button(form_frame, 
                            text="➕ CREAR CATEGORÍA",
                            bg=self.primary_color,
                            fg='white',
                            font=('Arial', 10, 'bold'),
                            padx=20,
                            pady=8,
                            borderwidth=0,
                            command=self.crear_categoria)
        crear_btn.grid(row=2, column=0, columnspan=2, pady=15)
        
        # Lista de categorías existentes
        list_frame = tk.LabelFrame(main_frame,
                                 text="📋 CATEGORÍAS EXISTENTES", 
                                 font=('Arial', 10, 'bold'),
                                 bg=self.card_bg,
                                 padx=15, pady=15)
        list_frame.pack(fill='both', expand=True)
        
        # Treeview para categorías
        columns = ("Nombre", "Presupuesto", "Tipo", "Icono")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("Nombre", text="NOMBRE")
        self.tree.heading("Presupuesto", text="PRESUPUESTO MENSUAL")
        self.tree.heading("Tipo", text="TIPO")
        self.tree.heading("Icono", text="ICONO")
        
        self.tree.column("Nombre", width=200)
        self.tree.column("Presupuesto", width=150)
        self.tree.column("Tipo", width=120)
        self.tree.column("Icono", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame para botones de acción
        action_frame = tk.Frame(list_frame, bg=self.card_bg)
        action_frame.pack(fill='x', pady=10)
        
        editar_btn = tk.Button(action_frame,
                             text="✏️ EDITAR PRESUPUESTO",
                             bg=self.warning_color,
                             fg='white',
                             font=('Arial', 9, 'bold'),
                             padx=15,
                             pady=6,
                             command=self.editar_presupuesto)
        editar_btn.pack(side='left', padx=5)
        
        eliminar_btn = tk.Button(action_frame,
                               text="🗑️ ELIMINAR",
                               bg=self.danger_color, 
                               fg='white',
                               font=('Arial', 9, 'bold'),
                               padx=15,
                               pady=6,
                               command=self.eliminar_categoria)
        eliminar_btn.pack(side='left', padx=5)
        
        actualizar_btn = tk.Button(action_frame,
                                 text="🔄 ACTUALIZAR LISTA",
                                 bg='#6c757d',
                                 fg='white',
                                 font=('Arial', 9, 'bold'),
                                 padx=15,
                                 pady=6,
                                 command=self.cargar_categorias)
        actualizar_btn.pack(side='right', padx=5)
    
    def cargar_categorias(self):
        """Cargar categorías en el treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.categorias = self.controller.obtener_categorias()
        
        for categoria in self.categorias:
            tipo = "Personalizada" if categoria.es_personalizada else "Predefinida"
            self.tree.insert("", "end", values=(
                categoria.nombre,
                f"${categoria.presupuesto_mensual:,.2f}",
                tipo,
                categoria.icono
            ), tags=(categoria.id,))
    
    def crear_categoria(self):
        """Crear nueva categoría"""
        nombre = self.nombre_entry.get().strip()
        presupuesto_str = self.presupuesto_entry.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "❌ El nombre de la categoría es obligatorio")
            return
            
        # Validar que no existe una categoría con el mismo nombre
        categorias_existentes = self.controller.obtener_categorias()
        if any(cat.nombre.lower() == nombre.lower() for cat in categorias_existentes):
            messagebox.showerror("Error", "❌ Ya existe una categoría con ese nombre")
            return
        
        try:
            presupuesto = float(presupuesto_str)
            if presupuesto < 0:
                raise ValueError("El presupuesto no puede ser negativo")
        except ValueError:
            messagebox.showerror("Error", "❌ El presupuesto debe ser un número válido")
            return
        
        if self.controller.crear_categoria(nombre, presupuesto):
            messagebox.showinfo("Éxito", "✅ Categoría creada correctamente")
            self.nombre_entry.delete(0, tk.END)
            self.presupuesto_entry.delete(0, tk.END)
            self.presupuesto_entry.insert(0, "0.00")
            self.cargar_categorias()
            # Actualizar el combobox en el formulario de gastos
            if hasattr(self.controller.vista_principal, 'formulario'):
                self.controller.vista_principal.formulario.actualizar_categorias(self.categorias)
        else:
            messagebox.showerror("Error", "❌ No se pudo crear la categoría")
    
    def editar_presupuesto(self):
        """Editar presupuesto de categoría seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "⚠️ Por favor selecciona una categoría")
            return
            
        item = seleccion[0]
        categoria_id = self.tree.item(item, 'tags')[0]
        valores = self.tree.item(item, 'values')
        nombre_categoria = valores[0]
        
        categoria = next((cat for cat in self.categorias if cat.id == int(categoria_id)), None)
        
        if not categoria:
            return
            
        # Diálogo para nuevo presupuesto
        nuevo_presupuesto = simpledialog.askfloat(
            "Editar Presupuesto",
            f"💵 Nuevo presupuesto mensual para '{nombre_categoria}':",
            initialvalue=categoria.presupuesto_mensual,
            minvalue=0
        )
        
        if nuevo_presupuesto is not None:
            if self.controller.actualizar_presupuesto(int(categoria_id), nuevo_presupuesto):
                messagebox.showinfo("Éxito", "✅ Presupuesto actualizado correctamente")
                self.cargar_categorias()
            else:
                messagebox.showerror("Error", "❌ No se pudo actualizar el presupuesto")
    
    def eliminar_categoria(self):
        """Eliminar categoría seleccionada - IMPLEMENTACIÓN REAL"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "⚠️ Por favor selecciona una categoría")
            return
            
        item = seleccion[0]
        valores = self.tree.item(item, 'values')
        categoria_id = self.tree.item(item, 'tags')[0]
        nombre_categoria = valores[0]
        tipo_categoria = valores[2]
        
        categoria = next((cat for cat in self.categorias if cat.id == int(categoria_id)), None)
        
        if not categoria:
            return
            
        if not categoria.es_personalizada:
            messagebox.showwarning("Advertencia", "❌ No se pueden eliminar categorías predefinidas del sistema")
            return
            
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar la categoría?\n\n"
            f"🏷️ Categoría: {nombre_categoria}\n"
            f"💰 Presupuesto: ${categoria.presupuesto_mensual:,.2f}\n\n"
            f"⚠️ Esta acción no se puede deshacer."
        )
        
        if confirmacion:
            if self.controller.eliminar_categoria(int(categoria_id)):
                messagebox.showinfo("Éxito", "✅ Categoría eliminada correctamente")
                self.cargar_categorias()
                # Actualizar combobox en formulario de gastos
                if hasattr(self.controller.vista_principal, 'formulario'):
                    self.controller.vista_principal.formulario.actualizar_categorias(self.categorias)
            else:
                # Mensaje específico sobre por qué no se pudo eliminar
                messagebox.showerror("Error", 
                    "❌ No se pudo eliminar la categoría.\n\n"
                    "Posibles causas:\n"
                    "• La categoría tiene gastos asociados\n"
                    "• La categoría no existe\n"
                    "• Error de base de datos")