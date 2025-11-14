import tkinter as tk
from tkinter import messagebox, filedialog
import os
from datetime import datetime

class ExportacionDialog:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.ejecutar_exportacion_simple()

    def ejecutar_exportacion_simple(self):
        try:
            # 1. Obtener gastos primero
            gastos = self.controller.obtener_gastos_mes_actual()
            
            if not gastos:
                messagebox.showinfo("Info", "No hay gastos para exportar")
                return

            # 2. Preguntar formato con messagebox
            formato = self.preguntar_formato_simple()
            if not formato:
                return

            # 3. Preguntar ubicación
            archivo = filedialog.asksaveasfilename(
                title="Guardar archivo de gastos",
                defaultextension=f".{formato}",
                initialfile=f"gastos_{datetime.now().strftime('%Y%m%d')}.{formato}",
                filetypes=[(f"Archivos {formato.upper()}", f"*.{formato}")]
            )
            
            if not archivo:
                return

            # 4. Exportar
            self.guardar_archivo(formato, archivo, gastos)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def preguntar_formato_simple(self):
        # Crear ventana mini para selección
        win = tk.Toplevel(self.parent)
        win.title("Formato de Exportación")
        win.geometry("250x120")
        win.resizable(False, False)
        
        # Centrar
        win.transient(self.parent)
        win.grab_set()
        
        tk.Label(win, text="Selecciona formato:", font=('Arial', 10)).pack(pady=10)
        
        formato_var = tk.StringVar(value="csv")
        
        # Frame para botones de formato
        frame_format = tk.Frame(win)
        frame_format.pack(pady=5)
        
        tk.Radiobutton(frame_format, text="CSV", variable=formato_var, value="csv").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame_format, text="JSON", variable=formato_var, value="json").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame_format, text="XML", variable=formato_var, value="xml").pack(side=tk.LEFT, padx=10)
        
        resultado = [None]
        
        def aceptar():
            resultado[0] = formato_var.get()
            win.destroy()
        
        def cancelar():
            win.destroy()
        
        # Frame para botones de acción
        frame_buttons = tk.Frame(win)
        frame_buttons.pack(pady=10)
        
        tk.Button(frame_buttons, text="Aceptar", command=aceptar, width=8).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Cancelar", command=cancelar, width=8).pack(side=tk.LEFT, padx=5)
        
        # Centrar ventana
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (125)
        y = (win.winfo_screenheight() // 2) - (60)
        win.geometry(f"+{x}+{y}")
        
        self.parent.wait_window(win)
        return resultado[0]

    def guardar_archivo(self, formato, archivo_path, gastos):
        try:
            if formato == "csv":
                contenido = self.exportar_csv(gastos)
            elif formato == "json":
                contenido = self.exportar_json(gastos)
            elif formato == "xml":
                contenido = self.exportar_xml(gastos)
            else:
                raise ValueError(f"Formato no soportado: {formato}")

            # Escribir archivo
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(contenido)

            # Mostrar éxito
            nombre_archivo = os.path.basename(archivo_path)
            messagebox.showinfo(
                "Éxito", 
                f"✅ Exportado correctamente!\n\n"
                f"Archivo: {nombre_archivo}\n"
                f"Gastos exportados: {len(gastos)}\n"
                f"Formato: {formato.upper()}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")

    def exportar_csv(self, gastos):
        lines = []
        
        lines.append('\ufeff')  # BOM para Excel
        
        # Encabezados con tildes correctas
        lines.append("Fecha;Descripción;Monto;Categoría;Moneda")
        
        for gasto in gastos:
            # Escapar caracteres especiales
            descripcion = gasto.descripcion
            # Si tiene punto y coma o comillas, encerrar entre comillas
            if ';' in descripcion or '"' in descripcion:
                descripcion = descripcion.replace('"', '""')  # Escapar comillas
                descripcion = f'"{descripcion}"'
            
            categoria = gasto.categoria.nombre
            if ';' in categoria or '"' in categoria:
                categoria = categoria.replace('"', '""')
                categoria = f'"{categoria}"'
            
            
            monto_formateado = str(gasto.monto).replace('.', ',')  # Coma decimal
            
            line = [
                gasto.fecha.isoformat(),
                descripcion,
                monto_formateado,
                categoria,
                gasto.moneda.value
            ]
            lines.append(';'.join(line))
        
        return '\n'.join(lines)

    def exportar_json(self, gastos):
        """Exportar a JSON"""
        import json
        
        datos = {
            "fecha_exportacion": datetime.now().isoformat(),
            "total_gastos": len(gastos),
            "gastos": []
        }
        
        for gasto in gastos:
            gasto_data = {
                "fecha": gasto.fecha.isoformat(),
                "descripcion": gasto.descripcion,
                "monto": gasto.monto,
                "categoria": gasto.categoria.nombre,
                "moneda": gasto.moneda.value
            }
            datos["gastos"].append(gasto_data)
        
        return json.dumps(datos, indent=2, ensure_ascii=False)

    def exportar_xml(self, gastos):
        """Exportar a XML"""
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<gastos>',
            f'  <fecha_exportacion>{datetime.now().isoformat()}</fecha_exportacion>',
            f'  <total>{len(gastos)}</total>'
        ]
        
        for gasto in gastos:
            xml_lines.extend([
                '  <gasto>',
                f'    <fecha>{gasto.fecha}</fecha>',
                f'    <descripcion>{self.escape_xml(gasto.descripcion)}</descripcion>',
                f'    <monto>{gasto.monto}</monto>',
                f'    <categoria>{self.escape_xml(gasto.categoria.nombre)}</categoria>',
                f'    <moneda>{gasto.moneda.value}</moneda>',
                '  </gasto>'
            ])
        
        xml_lines.append('</gastos>')
        return '\n'.join(xml_lines)

    def escape_xml(self, text):
        """Escapar caracteres especiales para XML"""
        if not text:
            return ""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')