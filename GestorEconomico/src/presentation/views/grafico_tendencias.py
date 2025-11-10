import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import date

class GraficoTendenciasView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(self, text="📈 Análisis y Tendencias", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        controles_frame = ttk.Frame(self)
        controles_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(controles_frame, text="Generar Reporte Mensual",
                command=self.generar_reporte).pack(side="left")
        
        ttk.Button(controles_frame, text="Comparar Meses",
                command=self.comparar_meses).pack(side="left", padx=(5, 0))
        
        self.info_text = scrolledtext.ScrolledText(self, width=80, height=20, font=("Consolas", 10))
        self.info_text.pack(fill="both", expand=True, padx=20, pady=10)
        self.info_text.insert("1.0", "Los resultados del análisis aparecerán aquí...\n\n")
        self.info_text.config(state="disabled")
    
    def generar_reporte(self):
        try:
            hoy = date.today()
            reporte = self.controller.generar_reporte_mensual(hoy.month, hoy.year)
            
            self.info_text.config(state="normal")
            self.info_text.delete("1.0", tk.END)
            self.info_text.insert("1.0", reporte.generar_resumen())
            self.info_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def comparar_meses(self):
        try:
            hoy = date.today()
            mes_actual = hoy.month
            año_actual = hoy.year
            
            mes_anterior = mes_actual - 1 if mes_actual > 1 else 12
            año_anterior = año_actual if mes_actual > 1 else año_actual - 1
            
            comparacion = self.controller.comparar_meses(
                mes_actual, año_actual, mes_anterior, año_anterior
            )
            
            self.info_text.config(state="normal")
            self.info_text.delete("1.0", tk.END)
            self.info_text.insert("1.0", f"📊 Comparación Mensual\n\n")
            self.info_text.insert(tk.END, f"Mes Actual ({mes_actual}/{año_actual}): ")
            self.info_text.insert(tk.END, f"${comparacion.mes_actual_total:.2f}\n")
            
            self.info_text.insert(tk.END, f"Mes Anterior ({mes_anterior}/{año_anterior}): ")
            self.info_text.insert(tk.END, f"${comparacion.mes_anterior_total:.2f}\n\n")
            
            self.info_text.insert(tk.END, f"Diferencia: {str(comparacion)}\n")
            self.info_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al comparar meses: {str(e)}")