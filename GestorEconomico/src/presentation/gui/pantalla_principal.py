import tkinter as tk
from tkinter import ttk
from src.presentation.views import FormularioGastoView, ListaGastosView, GraficoTendenciasView
from src.presentation.views.gestion_categorias import GestionCategoriasView

class PantallaPrincipal(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_modern_style()
        self.create_widgets()
    
    def setup_modern_style(self):
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Colores 
        self.primary_color = '#4361ee'
        self.secondary_color = '#3a0ca3'
        self.success_color = '#4cc9f0'
        self.danger_color = '#f72585'
        self.warning_color = '#f8961e'
        self.light_bg = '#f8f9fa'
        self.dark_bg = '#212529'
        self.card_bg = '#ffffff'
        
        # Configurar estilos básicos
        style.configure('Card.TFrame', background=self.card_bg, relief='raised', borderwidth=1)
        
        # Configurar notebook
        style.configure('Modern.TNotebook', background=self.light_bg)
        style.configure('Modern.TNotebook.Tab', 
                    background='#e9ecef',
                    foreground='#6c757d',
                    padding=[20, 10],
                    font=('Arial', 10, 'bold'))
        
        style.map('Modern.TNotebook.Tab',
                background=[('selected', self.primary_color),
                        ('active', self.secondary_color)],
                foreground=[('selected', 'white'),
                        ('active', 'white')])
    
    def create_widgets(self):
        # Header
        self.create_modern_header()
        
        # Notebook con pestañas 
        self.create_modern_notebook()
        
        # Footer con estadísticas
        self.create_modern_footer()
    
    def create_modern_header(self):
        header_frame = tk.Frame(self, bg=self.primary_color, height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Título principal
        title_frame = tk.Frame(header_frame, bg=self.primary_color)
        title_frame.pack(side='left', padx=30, pady=20)
        
        title_label = tk.Label(title_frame, 
                            text="💰 Gestor Económico",
                            font=('Arial', 20, 'bold'),
                            fg='white',
                            bg=self.primary_color)
        title_label.pack(side='left')
        
        # Badge de versión
        version_badge = tk.Label(title_frame,
                                text="v1.0",
                                font=('Arial', 10, 'bold'),
                                fg='white',
                                bg=self.warning_color,
                                padx=8,
                                pady=2)
        version_badge.pack(side='left', padx=(10, 0))
        
        # Estadísticas rápidas en el header
        stats_frame = tk.Frame(header_frame, bg=self.primary_color)
        stats_frame.pack(side='right', padx=30, pady=20)
        
        # Aquí irían estadísticas rápidas (se actualizarán dinámicamente)
        self.month_total_label = tk.Label(stats_frame,
                                        text="Mes Actual: $0.00",
                                        font=('Arial', 10, 'bold'),
                                        fg='white',
                                        bg=self.primary_color)
        self.month_total_label.pack(side='right', padx=(15, 0))
    
    def create_modern_notebook(self):
        # Frame principal del notebook
        notebook_container = tk.Frame(self, bg=self.light_bg)
        notebook_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Notebook moderno
        self.notebook = ttk.Notebook(notebook_container, style='Modern.TNotebook')
        
        # Pestaña de Gestión de Gastos
        gastos_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.setup_gastos_tab(gastos_frame)
        
        # Pestaña de Análisis
        analisis_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.setup_analisis_tab(analisis_frame)
        
        # NUEVA: Pestaña de Gestión de Categorías
        categorias_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.setup_categorias_tab(categorias_frame)
        
        self.notebook.add(gastos_frame, text="💸 GESTIÓN DE GASTOS")
        self.notebook.add(analisis_frame, text="📊 ANÁLISIS")
        self.notebook.add(categorias_frame, text="🏷️ CATEGORÍAS")  # Nueva pestaña
        
        self.notebook.pack(fill='both', expand=True)
        
        
    def setup_categorias_tab(self, parent):
        """Configurar pestaña de gestión de categorías"""
        main_container = tk.Frame(parent, bg=self.card_bg)
        main_container.pack(fill='both', expand=True, padx=2, pady=2)
        
        self.gestion_categorias = GestionCategoriasView(main_container, self.controller)
        self.gestion_categorias.pack(fill='both', expand=True, padx=10, pady=10)
        
    def setup_gastos_tab(self, parent):
        # Container principal
        main_container = tk.Frame(parent, bg=self.card_bg)
        main_container.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Layout en dos columnas
        left_frame = tk.Frame(main_container, bg=self.card_bg)
        left_frame.pack(side='left', fill='both', padx=(0, 10), pady=10)
        
        right_frame = tk.Frame(main_container, bg=self.card_bg)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0), pady=10)
        
        # Formulario en tarjeta
        form_card = tk.Frame(left_frame, bg=self.card_bg, relief='raised', bd=1)
        form_card.pack(fill='both', padx=5, pady=5)
        
        self.formulario = FormularioGastoView(form_card, self.controller, [])
        self.formulario.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Lista de gastos en tarjeta
        list_card = tk.Frame(right_frame, bg=self.card_bg, relief='raised', bd=1)
        list_card.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.lista_gastos = ListaGastosView(list_card, self.controller)
        self.lista_gastos.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_analisis_tab(self, parent):
        main_frame = tk.Frame(parent, bg=self.card_bg)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.grafico = GraficoTendenciasView(main_frame, self.controller)
        self.grafico.pack(fill='both', expand=True)
    
    def create_modern_footer(self):
        footer_frame = tk.Frame(self, bg=self.dark_bg, height=40)
        footer_frame.pack(fill='x', side='bottom', padx=0, pady=0)
        footer_frame.pack_propagate(False)
        
        # Información del footer
        footer_text = tk.Label(footer_frame,
                            text="💰 Gestor Económico | Control Total de tus Finanzas",
                            font=('Arial', 9),
                            fg='#adb5bd',
                            bg=self.dark_bg)
        footer_text.pack(side='left', padx=20, pady=10)
        
        # Estado del sistema
        status_text = tk.Label(footer_frame,
                            text="✅ Joaquin Giavino",
                            font=('Arial', 9),
                            fg=self.success_color,
                            bg=self.dark_bg)
        status_text.pack(side='right', padx=20, pady=10)
    
    def actualizar_categorias(self, categorias):
        self.formulario.actualizar_categorias(categorias)
    
    def mostrar_gastos(self, gastos):
        self.lista_gastos.actualizar_gastos(gastos)
        
        # Actualizar estadísticas del header
        total_mes = sum(gasto.monto for gasto in gastos)
        self.month_total_label.config(text=f"Mes Actual: ${total_mes:,.2f}")
    
    def mostrar_notificacion(self, mensaje: str):
        from tkinter import messagebox
        messagebox.showinfo("💎 Gestor Económico", mensaje)