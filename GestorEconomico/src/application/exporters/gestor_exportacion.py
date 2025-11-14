import os
from datetime import datetime
from typing import List
from src.domain.entities import Gasto
from .exportador_csv import ExportadorCSV
from .exportador_json import ExportadorJSON
from .exportador_xml import ExportadorXML

class GestorExportacion:
    def __init__(self):
        self.exportadores = {
            "csv": ExportadorCSV(),
            "json": ExportadorJSON(),
            "xml": ExportadorXML()
        }
    
    def obtener_formatos_soportados(self) -> List[str]:
        return list(self.exportadores.keys())
    
    def exportar(self, gastos: List[Gasto], formato: str) -> str:
        if formato not in self.exportadores:
            raise ValueError(f"Formato {formato} no soportado")
        
        return self.exportadores[formato].exportar(gastos)
    
    def exportar_a_archivo(self, gastos: List[Gasto], formato: str, ruta_archivo: str) -> None:
        """Exportar gastos a un archivo específico"""
        if formato not in self.exportadores:
            raise ValueError(f"Formato {formato} no soportado")
        
        contenido = self.exportadores[formato].exportar(gastos)
        
        # Crear directorio si no existe
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
    
    def obtener_nombre_archivo_sugerido(self, formato: str) -> str:
        """Generar nombre de archivo sugerido con timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"gastos_exportacion_{timestamp}.{formato}"
    
    def obtener_estadisticas_exportacion(self, gastos: List[Gasto]) -> dict:
        """Obtener estadísticas de los datos a exportar"""
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