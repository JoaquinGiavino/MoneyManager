import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from src.presentation.utils import ValidadorDatos, FormatoRegional
from src.core.exceptions import ValidacionError

class FormularioGastoView(ttk.Frame):
    def __init__(self, parent, controller, categorias):
        super().__init__(parent)
        self.controller = controller
        self.categorias = categorias
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(self, text="➕ Agregar Nuevo Gasto", 
                font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self, text="Descripción:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.descripcion_entry = ttk.Entry(self, width=30, font=("Arial", 10))
        self.descripcion_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.descripcion_entry.focus()
        
        ttk.Label(self, text="Monto:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        monto_frame = ttk.Frame(self)
        monto_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.monto_entry = ttk.Entry(monto_frame, width=15, font=("Arial", 10))
        self.monto_entry.insert(0, "0.00")
        self.monto_entry.pack(side="left")
        
        ttk.Label(monto_frame, text="ARS").pack(side="left", padx=(5, 0))
        
        ttk.Label(self, text="Categoría:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.categoria_combo = ttk.Combobox(self, values=[cat.nombre for cat in self.categorias], 
                                        state="readonly", width=27)
        self.categoria_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        if self.categorias:
            self.categoria_combo.set(self.categorias[0].nombre)
        
        ttk.Label(self, text="Fecha:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.fecha_entry = ttk.Entry(self, width=12, font=("Arial", 10))
        self.fecha_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        self.fecha_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        self.agregar_btn = ttk.Button(self, text="Agregar Gasto", 
                                    command=self.agregar_gasto, style="Accent.TButton")
        self.agregar_btn.grid(row=5, column=0, columnspan=2, pady=15)
        
        self.grid_columnconfigure(1, weight=1)
    
    def agregar_gasto(self):
        try:
            descripcion = self.descripcion_entry.get().strip()
            monto_str = self.monto_entry.get().strip()
            fecha_str = self.fecha_entry.get().strip()
            categoria_nombre = self.categoria_combo.get()
            
            ValidadorDatos.validar_descripcion(descripcion)
            monto = float(monto_str)
            ValidadorDatos.validar_monto(monto)
            fecha = FormatoRegional.parsear_fecha(fecha_str)
            ValidadorDatos.validar_fecha(fecha)
            
            categoria = next((cat for cat in self.categorias if cat.nombre == categoria_nombre), None)
            if not categoria:
                raise ValidacionError("Categoría no válida")
            
            self.controller.agregar_gasto(descripcion, monto, fecha, categoria)
            
            self.descripcion_entry.delete(0, tk.END)
            self.monto_entry.delete(0, tk.END)
            self.monto_entry.insert(0, "0.00")
            self.descripcion_entry.focus()
            
            messagebox.showinfo("Éxito", "✅ Gasto agregado correctamente")
            
        except (ValueError, ValidacionError) as e:
            messagebox.showerror("Error de Validación", f"❌ {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error al agregar gasto: {str(e)}")
    
    def actualizar_categorias(self, categorias):
        self.categorias = categorias
        self.categoria_combo["values"] = [cat.nombre for cat in categorias]
        if categorias:
            self.categoria_combo.set(categorias[0].nombre)