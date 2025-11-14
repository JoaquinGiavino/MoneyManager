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
        self.create_modern_widgets()
    
    def create_modern_widgets(self):
        # Colores modernos
        self.primary_color = '#4361ee'
        self.success_color = '#4cc9f0'
        self.danger_color = '#f72585'
        self.card_bg = '#ffffff'
        self.light_gray = '#f8f9fa'
        
        # Container principal
        main_container = tk.Frame(self, bg=self.card_bg)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título del formulario
        title_label = tk.Label(main_container,
                            text="➕ NUEVO GASTO",
                            font=('Arial', 14, 'bold'),
                            fg=self.primary_color,
                            bg=self.card_bg,
                            pady=10)
        title_label.pack(fill='x')
        
        # Campo Descripción
        desc_frame = self.create_modern_input_field(main_container, "Descripción del Gasto:", 0)
        self.descripcion_entry = self.create_modern_entry(desc_frame)
        self.descripcion_entry.pack(fill='x', pady=5)
        self.descripcion_entry.focus()
        
        # Campo Monto
        monto_frame = self.create_modern_input_field(main_container, "Monto ($):", 1)
        monto_input_frame = tk.Frame(monto_frame, bg=self.card_bg)
        monto_input_frame.pack(fill='x', pady=5)
        
        self.monto_entry = self.create_modern_entry(monto_input_frame, width=15)
        self.monto_entry.insert(0, "0.00")
        self.monto_entry.pack(side='left')
        
        # Badge de moneda
        currency_badge = tk.Label(monto_input_frame,
                                text="ARS",
                                font=('Arial', 9, 'bold'),
                                fg='white',
                                bg=self.primary_color,
                                padx=8,
                                pady=2)
        currency_badge.pack(side='left', padx=(8, 0))
        
        # Campo Categoría
        cat_frame = self.create_modern_input_field(main_container, "Categoría:", 2)
        self.categoria_combo = self.create_modern_combobox(cat_frame)
        self.categoria_combo.pack(fill='x', pady=5)
        if self.categorias:
            self.categoria_combo.set(self.categorias[0].nombre)
        
        # Campo Fecha
        fecha_frame = self.create_modern_input_field(main_container, "Fecha:", 3)
        fecha_input_frame = tk.Frame(fecha_frame, bg=self.card_bg)
        fecha_input_frame.pack(fill='x', pady=5)
        
        self.fecha_entry = self.create_modern_entry(fecha_input_frame, width=12)
        self.fecha_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        self.fecha_entry.pack(side='left')
        
        # Botón de hoy
        today_btn = tk.Button(fecha_input_frame,
                            text="Hoy",
                            font=('Arial', 8),
                            fg=self.primary_color,
                            bg=self.light_gray,
                            borderwidth=1,
                            relief='solid',
                            command=self.set_today_date)
        today_btn.pack(side='left', padx=(8, 0))
        
        # Botón de acción principal
        btn_container = tk.Frame(main_container, bg=self.card_bg)
        btn_container.pack(fill='x', pady=20)
        
        self.agregar_btn = tk.Button(btn_container,
                                    text="➕ AGREGAR GASTO",
                                    font=('Arial', 12, 'bold'),
                                    fg='white',
                                    bg=self.primary_color,
                                    borderwidth=0,
                                    padx=30,
                                    pady=12,
                                    command=self.agregar_gasto)
        self.agregar_btn.pack(fill='x')
        
        # Bind Enter key para agregar gasto
        self.descripcion_entry.bind('<Return>', lambda e: self.agregar_gasto())
        self.monto_entry.bind('<Return>', lambda e: self.agregar_gasto())
        self.fecha_entry.bind('<Return>', lambda e: self.agregar_gasto())
    
    def create_modern_input_field(self, parent, label_text, row):
        container = tk.Frame(parent, bg=self.card_bg)
        container.pack(fill='x', pady=8)
        
        label = tk.Label(container,
                        text=label_text,
                        font=('Arial', 10, 'bold'),
                        fg='#495057',
                        bg=self.card_bg,
                        anchor='w')
        label.pack(fill='x')
        
        return container
    
    def create_modern_entry(self, parent, width=30, **kwargs):
        entry = tk.Entry(parent,
                        width=width,
                        font=('Arial', 10),
                        relief='solid',
                        bg=self.light_gray,
                        fg='#212529',
                        bd=1,
                        **kwargs)
        return entry
    
    def create_modern_combobox(self, parent):
        combo = ttk.Combobox(parent,
                        values=[cat.nombre for cat in self.categorias],
                        state="readonly",
                        font=('Arial', 10))
        
        return combo
    
    def set_today_date(self):
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, date.today().strftime("%d/%m/%Y"))
    
    def agregar_gasto(self):
        try:
            descripcion = self.descripcion_entry.get().strip()
            monto_str = self.monto_entry.get().strip()
            fecha_str = self.fecha_entry.get().strip()
            categoria_nombre = self.categoria_combo.get()
            
            # Validaciones
            ValidadorDatos.validar_descripcion(descripcion)
            monto = float(monto_str)
            ValidadorDatos.validar_monto(monto)
            fecha = FormatoRegional.parsear_fecha(fecha_str)
            ValidadorDatos.validar_fecha(fecha)
            
            categoria = next((cat for cat in self.categorias if cat.nombre == categoria_nombre), None)
            if not categoria:
                raise ValidacionError("Categoría no válida")
            
            # Efecto visual de carga
            self.agregar_btn.config(text="⏳ PROCESANDO...", bg='#6c757d')
            self.update()
            
            # Agregar gasto
            success = self.controller.agregar_gasto(descripcion, monto, fecha, categoria)
            
            if success:
                # Efecto de éxito
                self.agregar_btn.config(text="✅ GASTO AGREGADO", bg=self.success_color)
                self.after(1000, self.reset_form)
            else:
                raise Exception("No se pudo agregar el gasto")
            
        except (ValueError, ValidacionError) as e:
            self.show_error_message(str(e))
        except Exception as e:
            self.show_error_message(f"Error al agregar gasto: {str(e)}")
        finally:
            self.after(1500, self.reset_button)
    
    def reset_form(self):
        self.descripcion_entry.delete(0, tk.END)
        self.monto_entry.delete(0, tk.END)
        self.monto_entry.insert(0, "0.00")
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        self.descripcion_entry.focus()
    
    def reset_button(self):
        self.agregar_btn.config(text="➕ AGREGAR GASTO", bg=self.primary_color)
    
    def show_error_message(self, message):
        self.agregar_btn.config(text="❌ ERROR", bg=self.danger_color)
        messagebox.showerror("Error de Validación", f"❌ {message}")
    
    def actualizar_categorias(self, categorias):
        self.categorias = categorias
        self.categoria_combo['values'] = [cat.nombre for cat in categorias]
        if categorias:
            self.categoria_combo.set(categorias[0].nombre)