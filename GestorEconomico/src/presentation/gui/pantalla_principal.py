import tkinter as tk
from tkinter import ttk
from src.presentation.views import FormularioGastoView, ListaGastosView, GraficoTendenciasView

class PantallaPrincipal(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        self.configure_style()
        
        notebook = ttk.Notebook(self)
        
        frame_gastos = ttk.Frame(notebook)
        self.setup_gastos_tab(frame_gastos)
        
        frame_analisis = ttk.Frame(notebook)
        self.setup_analisis_tab(frame_analisis)
        
        notebook.add(frame_gastos, text="💸 Gestión de Gastos")
        notebook.add(frame_analisis, text="📊 Análisis")
        
        notebook.pack(fill="both", expand=True)
    
    def configure_style(self):
        """Configurar estilos para la interfaz del Gestor Económico"""
        style = ttk.Style()
        
        # Estilo para botón principal (azul)
        style.configure("Accent.TButton", 
                    foreground="white", 
                    background="#007bff",
                    font=("Arial", 10, "bold"))
        
        # Estilo para botón de peligro (rojo)
        style.configure("Danger.TButton", 
                    foreground="white", 
                    background="#dc3545",
                    font=("Arial", 10, "bold"))
        
        # Efecto hover para botones
        style.map("Accent.TButton",
                background=[('active', '#0056b3')])
        
        style.map("Danger.TButton",
                background=[('active', '#c82333')])
    
    def setup_gastos_tab(self, parent):
        """Configurar pestaña de gestión de gastos"""
        frame_izquierdo = ttk.Frame(parent)
        frame_izquierdo.pack(side="left", fill="y", padx=10, pady=10)
        
        self.formulario = FormularioGastoView(frame_izquierdo, self.controller, [])
        self.formulario.pack(fill="both", expand=True)
        
        frame_derecho = ttk.Frame(parent)
        frame_derecho.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.lista_gastos = ListaGastosView(frame_derecho, self.controller)
        self.lista_gastos.pack(fill="both", expand=True)
    
    def setup_analisis_tab(self, parent):
        """Configurar pestaña de análisis"""
        self.grafico = GraficoTendenciasView(parent, self.controller)
        self.grafico.pack(fill="both", expand=True)
    
    def actualizar_categorias(self, categorias):
        """Actualizar lista de categorías en el formulario"""
        self.formulario.actualizar_categorias(categorias)
    
    def mostrar_gastos(self, gastos):
        """Mostrar lista de gastos en la vista"""
        self.lista_gastos.actualizar_gastos(gastos)
    
    def mostrar_notificacion(self, mensaje: str):
        """Mostrar notificación al usuario"""
        from tkinter import messagebox
        messagebox.showinfo("Notificación Gestor Económico", mensaje)