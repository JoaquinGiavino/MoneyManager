import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import date

class GraficoTendenciasView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_modern_widgets()
    
    def create_modern_widgets(self):
        # Colores modernos
        self.primary_color = '#4361ee'
        self.success_color = '#4cc9f0'
        self.danger_color = '#f72585'
        self.warning_color = '#f8961e'
        self.card_bg = '#ffffff'
        
        main_container = tk.Frame(self, bg=self.card_bg)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header de análisis
        header_frame = tk.Frame(main_container, bg=self.card_bg)
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(header_frame,
                            text="📊 PANEL DE ANÁLISIS",
                            font=('Arial', 16, 'bold'),
                            fg=self.primary_color,
                            bg=self.card_bg)
        title_label.pack(side='left')
        
        # Controles de análisis
        controls_frame = tk.Frame(main_container, bg=self.card_bg)
        controls_frame.pack(fill='x', pady=(0, 20))
        
        # Botones de acción modernos
        actions_frame = tk.Frame(controls_frame, bg=self.card_bg)
        actions_frame.pack(side='left')
        
        self.create_analysis_button(actions_frame, "📈 REPORTE MENSUAL", 
                                self.generar_reporte, self.primary_color)
        
        self.create_analysis_button(actions_frame, "🔄 COMPARAR MESES", 
                                self.comparar_meses, self.success_color)
        
        self.create_analysis_button(actions_frame, "📋 RESUMEN", 
                                self.generar_resumen, self.warning_color)
        
        # Área de resultados moderna
        results_container = tk.Frame(main_container, bg=self.card_bg, relief='raised', bd=1)
        results_container.pack(fill='both', expand=True)
        
        # Header de resultados
        results_header = tk.Frame(results_container, bg='#e9ecef', height=40)
        results_header.pack(fill='x')
        results_header.pack_propagate(False)
        
        tk.Label(results_header, text="📋 RESULTADOS DEL ANÁLISIS",
                font=('Arial', 11, 'bold'),
                fg='#495057',
                bg='#e9ecef').pack(side='left', padx=15, pady=10)
        
        # Área de texto con scroll
        text_frame = tk.Frame(results_container, bg=self.card_bg)
        text_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.info_text = scrolledtext.ScrolledText(text_frame, 
                                                width=80, 
                                                height=20, 
                                                font=('Consolas', 10),
                                                bg='#f8f9fa',
                                                fg='#212529')
        self.info_text.pack(fill='both', expand=True)
        self.info_text.insert("1.0", "💎 BIENVENIDO AL PANEL DE ANÁLISIS\n\n"
                                "Selecciona una opción para generar reportes detallados "
                                "sobre tus hábitos de gasto.\n\n"
                                "📊 **Opciones disponibles:**\n"
                                "• 📈 Reporte Mensual: Análisis completo del mes actual\n"
                                "• 🔄 Comparar Meses: Comparativa con el mes anterior\n"
                                "• 📋 Resumen Ejecutivo: Vista rápida de tus finanzas\n\n"
                                "¡Toma el control de tus finanzas! 💪")
        self.info_text.config(state="disabled")
    
    def create_analysis_button(self, parent, text, command, color):
        btn = tk.Button(parent,
                    text=text,
                    font=('Arial', 10, 'bold'),
                    fg='white',
                    bg=color,
                    borderwidth=0,
                    padx=20,
                    pady=12,
                    command=command)
        btn.pack(side='left', padx=(0, 10))
        return btn
    
    def generar_reporte(self):
        try:
            hoy = date.today()
            self.info_text.config(state="normal")
            self.info_text.delete("1.0", tk.END)
            
            # Mostrar indicador de carga
            self.info_text.insert("1.0", "⏳ Generando reporte mensual...\n")
            self.info_text.update()
            
            reporte = self.controller.generar_reporte_mensual(hoy.month, hoy.year)
            
            # Limpiar y mostrar resultados
            self.info_text.delete("1.0", tk.END)
            
            # Encabezado moderno
            self.info_text.insert("1.0", "📊 REPORTE MENSUAL DETALLADO\n\n")
            self.info_text.insert(tk.END, "="*50 + "\n")
            self.info_text.insert(tk.END, f"📅 Período: {reporte.fecha_inicio.strftime('%d/%m/%Y')} "
                                        f"al {reporte.fecha_fin.strftime('%d/%m/%Y')}\n")
            self.info_text.insert(tk.END, f"💰 Total Gastado: ${reporte.total:,.2f}\n")
            self.info_text.insert(tk.END, "="*50 + "\n\n")
            
            # Desglose por categoría
            self.info_text.insert(tk.END, "🏷️ DESGLOSE POR CATEGORÍA:\n\n")
            
            for categoria, monto in reporte.por_categoria.items():
                porcentaje = (monto / reporte.total * 100) if reporte.total > 0 else 0
                bar = "█" * int(porcentaje / 5)  # Barra de progreso simple
                
                self.info_text.insert(tk.END, 
                                    f"  {categoria.icono} {categoria.nombre:<15} "
                                    f"${monto:>8.2f} ({porcentaje:5.1f}%) {bar}\n")
            
            self.info_text.insert(tk.END, "\n" + "="*50 + "\n")
            self.info_text.insert(tk.END, "💡 **Análisis completado exitosamente** ✅\n")
            
            self.info_text.config(state="disabled")
            
        except Exception as e:
            self.mostrar_error(f"Error al generar reporte: {str(e)}")
    
    def comparar_meses(self):
        try:
            hoy = date.today()
            self.info_text.config(state="normal")
            self.info_text.delete("1.0", tk.END)
            
            # Indicador de carga
            self.info_text.insert("1.0", "⏳ Comparando meses...\n")
            self.info_text.update()
            
            mes_actual = hoy.month
            año_actual = hoy.year
            
            mes_anterior = mes_actual - 1 if mes_actual > 1 else 12
            año_anterior = año_actual if mes_actual > 1 else año_actual - 1
            
            comparacion = self.controller.comparar_meses(
                mes_actual, año_actual, mes_anterior, año_anterior
            )
            
            # Limpiar y mostrar resultados
            self.info_text.delete("1.0", tk.END)
            
            self.info_text.insert("1.0", "🔄 COMPARATIVA MENSUAL\n\n")
            self.info_text.insert(tk.END, "="*50 + "\n")
            
            # Datos del mes actual
            self.info_text.insert(tk.END, f"📈 MES ACTUAL ({mes_actual}/{año_actual}):\n")
            self.info_text.insert(tk.END, f"   Total: ${comparacion.mes_actual_total:,.2f}\n\n")
            
            # Datos del mes anterior
            self.info_text.insert(tk.END, f"📉 MES ANTERIOR ({mes_anterior}/{año_anterior}):\n")
            self.info_text.insert(tk.END, f"   Total: ${comparacion.mes_anterior_total:,.2f}\n\n")
            
            # Análisis comparativo
            self.info_text.insert(tk.END, "📊 ANÁLISIS COMPARATIVO:\n")
            
            if comparacion.diferencia_total > 0:
                tendencia = "🔴 AUMENTO"
                icono = "📈"
            else:
                tendencia = "🟢 DISMINUCIÓN" 
                icono = "📉"
            
            self.info_text.insert(tk.END, f"   {icono} Tendencia: {tendencia}\n")
            self.info_text.insert(tk.END, f"   💰 Diferencia: ${abs(comparacion.diferencia_total):,.2f}\n")
            self.info_text.insert(tk.END, f"   📊 Porcentaje: {comparacion.porcentaje_cambio:+.1f}%\n\n")
            
            # Recomendación
            self.info_text.insert(tk.END, "💡 RECOMENDACIÓN:\n")
            if comparacion.porcentaje_cambio > 10:
                self.info_text.insert(tk.END, "   ⚠️  Considera revisar tus gastos, "
                                            "estás gastando significativamente más.\n")
            elif comparacion.porcentaje_cambio < -10:
                self.info_text.insert(tk.END, "   ✅ ¡Excelente! Estás gastando menos que el mes anterior.\n")
            else:
                self.info_text.insert(tk.END, "   🔄 Tus gastos se mantienen estables. "
                                            "¡Sigue así!\n")
            
            self.info_text.insert(tk.END, "\n" + "="*50 + "\n")
            self.info_text.config(state="disabled")
            
        except Exception as e:
            self.mostrar_error(f"Error al comparar meses: {str(e)}")
    
    def generar_resumen(self):
        try:
            hoy = date.today()
            self.info_text.config(state="normal")
            self.info_text.delete("1.0", tk.END)
            
            gastos = self.controller.obtener_gastos_mes_actual()
            total_mes = sum(gasto.monto for gasto in gastos)
            
            self.info_text.insert("1.0", "📋 RESUMEN EJECUTIVO\n\n")
            self.info_text.insert(tk.END, "="*50 + "\n")
            self.info_text.insert(tk.END, f"📅 Resumen del {hoy.strftime('%B %Y')}\n")
            self.info_text.insert(tk.END, "="*50 + "\n\n")
            
            # Estadísticas rápidas
            self.info_text.insert(tk.END, "🚀 ESTADÍSTICAS RÁPIDAS:\n\n")
            self.info_text.insert(tk.END, f"   📊 Total de gastos: {len(gastos)}\n")
            self.info_text.insert(tk.END, f"   💰 Total mensual: ${total_mes:,.2f}\n")
            
            if gastos:
                promedio = total_mes / len(gastos)
                max_gasto = max(gastos, key=lambda x: x.monto)
                min_gasto = min(gastos, key=lambda x: x.monto)
                
                self.info_text.insert(tk.END, f"   📈 Promedio por gasto: ${promedio:,.2f}\n")
                self.info_text.insert(tk.END, f"   🔺 Gasto más alto: ${max_gasto.monto:,.2f} "
                                            f"({max_gasto.descripcion})\n")
                self.info_text.insert(tk.END, f"   🔻 Gasto más bajo: ${min_gasto.monto:,.2f} "
                                            f"({min_gasto.descripcion})\n\n")
            
            # Distribución por categoría
            self.info_text.insert(tk.END, "🏷️ DISTRIBUCIÓN POR CATEGORÍA:\n\n")
            
            categorias = {}
            for gasto in gastos:
                cat_nombre = gasto.categoria.nombre
                if cat_nombre not in categorias:
                    categorias[cat_nombre] = 0
                categorias[cat_nombre] += gasto.monto
            
            for cat_nombre, total in categorias.items():
                porcentaje = (total / total_mes * 100) if total_mes > 0 else 0
                self.info_text.insert(tk.END, f"   • {cat_nombre}: ${total:,.2f} ({porcentaje:.1f}%)\n")
            
            self.info_text.insert(tk.END, "\n" + "="*50 + "\n")
            self.info_text.insert(tk.END, "🎯 **Resumen generado exitosamente** ✅\n")
            
            self.info_text.config(state="disabled")
            
        except Exception as e:
            self.mostrar_error(f"Error al generar resumen: {str(e)}")
    
    def mostrar_error(self, mensaje):
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", f"❌ ERROR\n\n{mensaje}\n\n"
                                "⚠️ Por favor, intenta nuevamente.")
        self.info_text.config(state="disabled")
        messagebox.showerror("Error de Análisis", mensaje)