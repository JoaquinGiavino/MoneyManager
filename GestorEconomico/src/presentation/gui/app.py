import tkinter as tk
from tkinter import messagebox
from .controller import ControllerGastos
from .pantalla_principal import PantallaPrincipal

class GestionGastosApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_app()
        
    def setup_app(self):
        self.root.title("💰 Sistema de Gestión de Gastos Personales")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        self.center_window()
        
        # Inicializar controlador
        self.controller = ControllerGastos()
        
        # Crear interfaz principal
        self.vista_principal = PantallaPrincipal(self.root, self.controller)
        self.vista_principal.pack(fill="both", expand=True)
        
        # Configurar controller con la vista
        self.controller.vista_principal = self.vista_principal
        
        # Cargar datos iniciales
        self.cargar_datos_iniciales()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def cargar_datos_iniciales(self):
        try:
            categorias = self.controller.obtener_categorias()
            self.vista_principal.actualizar_categorias(categorias)
            
            self.controller.actualizar_vistas()
            
            print("✅ Datos iniciales cargados correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos iniciales: {str(e)}")
    
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error en la aplicación: {e}")