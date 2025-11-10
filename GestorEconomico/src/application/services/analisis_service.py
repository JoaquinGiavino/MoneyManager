from typing import List, Dict
from src.domain.entities import Gasto, TipoAlerta
from src.domain.interfaces import AnalisisStrategy

class AnalizadorGastos:
    def __init__(self, estrategias: List[AnalisisStrategy]):
        self.estrategias = {type(estrategia).__name__: estrategia for estrategia in estrategias}
    
    def calcular_promedios(self, gastos: List[Gasto]) -> Dict[str, float]:
        if not gastos:
            return {}
        
        promedios = {}
        categorias = set(gasto.categoria.nombre for gasto in gastos)
        
        for categoria in categorias:
            gastos_categoria = [g for g in gastos if g.categoria.nombre == categoria]
            if gastos_categoria:
                promedio = sum(g.monto for g in gastos_categoria) / len(gastos_categoria)
                promedios[categoria] = promedio
        
        return promedios
    
    def verificar_alertas(self, gastos: List[Gasto]) -> List[TipoAlerta]:
        alertas = []
        
        if not gastos:
            return alertas
        
        gastos_por_categoria = {}
        for gasto in gastos:
            cat_nombre = gasto.categoria.nombre
            if cat_nombre not in gastos_por_categoria:
                gastos_por_categoria[cat_nombre] = 0
            gastos_por_categoria[cat_nombre] += gasto.monto
        
        for gasto in gastos:
            total_categoria = gastos_por_categoria.get(gasto.categoria.nombre, 0)
            presupuesto = gasto.categoria.presupuesto_mensual
            
            if presupuesto > 0 and total_categoria > presupuesto:
                alertas.append(TipoAlerta.PRESUPUESTO_EXCEDIDO)
                break
        
        if len(gastos) > 0:
            alertas.append(TipoAlerta.NUEVO_GASTO)
        
        return alertas
    
    def ejecutar_analisis_completo(self, gastos: List[Gasto]) -> Dict[str, dict]:
        resultados = {}
        
        for nombre, estrategia in self.estrategias.items():
            resultados[nombre] = estrategia.analizar(gastos)
        
        return resultados