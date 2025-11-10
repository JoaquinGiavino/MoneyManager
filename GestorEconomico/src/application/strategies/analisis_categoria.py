from typing import List, Dict
from src.domain.entities import Gasto
from src.domain.interfaces import AnalisisStrategy

class AnalisisPorCategoria(AnalisisStrategy):
    def analizar(self, gastos: List[Gasto]) -> Dict:
        por_categoria = {}
        
        for gasto in gastos:
            cat_nombre = gasto.categoria.nombre
            if cat_nombre not in por_categoria:
                por_categoria[cat_nombre] = {
                    "total": 0.0,
                    "cantidad": 0,
                    "color": gasto.categoria.color,
                    "icono": gasto.categoria.icono
                }
            
            por_categoria[cat_nombre]["total"] += gasto.monto
            por_categoria[cat_nombre]["cantidad"] += 1
        
        total_general = sum(info["total"] for info in por_categoria.values())
        
        for cat_info in por_categoria.values():
            if total_general > 0:
                cat_info["porcentaje"] = (cat_info["total"] / total_general) * 100
            else:
                cat_info["porcentaje"] = 0
        
        return por_categoria