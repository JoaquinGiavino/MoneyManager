from typing import List, Dict
from src.domain.entities import Gasto
from src.domain.interfaces import AnalisisStrategy

class AnalisisTendencias(AnalisisStrategy):
    def analizar(self, gastos: List[Gasto]) -> Dict:
        if not gastos:
            return {}
        
        por_mes = {}
        
        for gasto in gastos:
            clave = (gasto.fecha.year, gasto.fecha.month)
            if clave not in por_mes:
                por_mes[clave] = 0.0
            por_mes[clave] += gasto.monto
        
        meses_ordenados = sorted(por_mes.items())
        
        tendencia = {
            "meses": [f"{año}-{mes:02d}" for (año, mes), _ in meses_ordenados],
            "totales": [total for _, total in meses_ordenados],
            "tendencia": "estable"
        }
        
        if len(meses_ordenados) >= 2:
            ultimo = meses_ordenados[-1][1]
            penultimo = meses_ordenados[-2][1]
            
            if ultimo > penultimo * 1.1:
                tendencia["tendencia"] = "ascendente"
            elif ultimo < penultimo * 0.9:
                tendencia["tendencia"] = "descendente"
        
        return tendencia