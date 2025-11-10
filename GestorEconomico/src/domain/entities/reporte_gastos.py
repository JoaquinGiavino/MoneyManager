from dataclasses import dataclass
from datetime import date
from typing import Dict
from .categoria import Categoria

@dataclass
class ReporteGastos:
    total: float
    por_categoria: Dict[Categoria, float]
    fecha_inicio: date
    fecha_fin: date
    
    def generar_resumen(self) -> str:
        resumen = f"📊 Reporte de Gastos\n"
        resumen += f"Período: {self.fecha_inicio} al {self.fecha_fin}\n"
        resumen += f"Total gastado: ${self.total:.2f}\n\n"
        resumen += "Desglose por categoría:\n"
        
        for categoria, monto in self.por_categoria.items():
            porcentaje = (monto / self.total * 100) if self.total > 0 else 0
            resumen += f"  • {categoria.nombre}: ${monto:.2f} ({porcentaje:.1f}%)\n"
        
        return resumen