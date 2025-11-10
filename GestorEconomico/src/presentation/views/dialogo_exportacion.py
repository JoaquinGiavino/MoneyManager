import tkinter as tk
from tkinter import ttk, messagebox

class ExportacionDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Exportar Datos")
        self.geometry("300x200")
        self.resizable(False, False)
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(self, text="Seleccione el formato de exportación:", 
                font=("Arial", 10)).pack(pady=20)
        
        self.formato_var = tk.StringVar(value="csv")
        
        formatos = [("CSV", "csv"), ("JSON", "json"), ("XML", "xml")]
        
        for texto, valor in formatos:
            ttk.Radiobutton(self, text=texto, variable=self.formato_var, 
                        value=valor).pack(pady=5)
        
        ttk.Button(self, text="Exportar", command=self.exportar).pack(pady=20)
        ttk.Button(self, text="Cancelar", command=self.destroy).pack()
    
    def exportar(self):
        try:
            formato = self.formato_var.get()
            contenido = self.controller.exportar_datos(formato)
            
            print(f"Datos exportados en formato {formato.upper()}:")
            print(contenido[:200] + "..." if len(contenido) > 200 else contenido)
            
            messagebox.showinfo("Éxito", f"Datos exportados en formato {formato.upper()}")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")