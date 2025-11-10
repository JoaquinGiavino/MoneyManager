from typing import List, Dict
from src.domain.entities import Gasto
from src.domain.interfaces import AnalisisStrategy

class AnalisisTotal(AnalisisStrategy):
    def analizar(self, gastos: List[Gasto]) -> Dict:
        total = sum(gasto.monto for gasto in gastos)
        promedio = total / len(gastos) if gastos else 0
        
        return {
            "total_gastado": total,
            "cantidad_gastos": len(gastos),
            "promedio_por_gasto": promedio,
            "gasto_maximo": max(gasto.monto for gasto in gastos) if gastos else 0,
            "gasto_minimo": min(gasto.monto for gasto in gastos) if gastos else 0
        }