from typing import List
from src.domain.entities import Gasto
from src.domain.interfaces import Exportable

class ExportadorCSV(Exportable):
    def exportar(self, gastos: List[Gasto]) -> str:
        if not gastos:
            return "Fecha;Descripción;Monto;Categoría;Moneda\n"
        
        lines = []
        
        # Agregar BOM para Excel con UTF-8
        lines.append('\ufeff')  # BOM para Excel
        
        # Encabezados en español
        lines.append("Fecha;Descripción;Monto;Categoría;Moneda")
        
        for gasto in gastos:
            # Escapar descripción si tiene punto y coma
            descripcion = gasto.descripcion
            if ';' in descripcion or '"' in descripcion:
                descripcion = descripcion.replace('"', '""')
                descripcion = f'"{descripcion}"'
            
            # Escapar categoría si tiene punto y coma
            categoria = gasto.categoria.nombre
            if ';' in categoria or '"' in categoria:
                categoria = categoria.replace('"', '""')
                categoria = f'"{categoria}"'
            
            # Formatear monto con coma decimal (formato español)
            monto_formateado = str(gasto.monto).replace('.', ',')
            
            line = [
                gasto.fecha.strftime("%d/%m/%Y"),  # Formato fecha español
                descripcion,
                monto_formateado,
                categoria,
                gasto.moneda.value
            ]
            lines.append(';'.join(line))
        
        return '\n'.join(lines)