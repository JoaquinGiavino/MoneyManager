from typing import List
from src.domain.entities import Gasto
from src.domain.interfaces import Exportable

class ExportadorCSV(Exportable):
    def exportar(self, gastos: List[Gasto]) -> str:
        if not gastos:
            return "Fecha,Descripcion,Monto,Categoria,Moneda\n"
        
        lines = ["Fecha,Descripcion,Monto,Categoria,Moneda"]
        
        for gasto in gastos:
            # Escapar la descripción si tiene comas
            descripcion = gasto.descripcion
            if ',' in descripcion or '"' in descripcion:
                descripcion = descripcion.replace('"', '""')
                descripcion = f'"{descripcion}"'
            
            line = [
                gasto.fecha.isoformat(),
                descripcion,
                str(gasto.monto),
                gasto.categoria.nombre,
                gasto.moneda.value
            ]
            lines.append(','.join(line))
        
        return '\n'.join(lines)