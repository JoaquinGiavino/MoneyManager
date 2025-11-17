import os
from datetime import datetime
from typing import List
from src.domain.entities import Gasto
from .exportador_csv import ExportadorCSV

class GestorExportacion:
    def __init__(self):
        self.exportadores = {
            "csv": ExportadorCSV()
        }
    
    def obtener_formatos_soportados(self) -> List[str]:
        return ["csv"]
    
    def exportar(self, gastos: List[Gasto], formato: str) -> str:
        if formato != "csv":
            raise ValueError("Solo se soporta formato CSV")
        
        return self.exportadores["csv"].exportar(gastos)
    
    def exportar_a_archivo(self, gastos: List[Gasto], formato: str, ruta_archivo: str) -> None:
        if formato != "csv":
            raise ValueError("Solo se soporta formato CSV")
        
        contenido = self.exportadores["csv"].exportar(gastos)
        
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
    
    def obtener_nombre_archivo_sugerido(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"gastos_excel_{timestamp}.csv"
    
    def obtener_estadisticas_exportacion(self, gastos: List[Gasto]) -> dict:
        if not gastos:
            return {}
        
        total = sum(gasto.monto for gasto in gastos)
        categorias = len(set(gasto.categoria.nombre for gasto in gastos))
        fecha_min = min(gasto.fecha for gasto in gastos)
        fecha_max = max(gasto.fecha for gasto in gastos)
        
        return {
            "total_gastos": len(gastos),
            "total_monto": total,
            "categorias_unicas": categorias,
            "periodo": f"{fecha_min} a {fecha_max}",
            "promedio_gasto": total / len(gastos) if gastos else 0
        }