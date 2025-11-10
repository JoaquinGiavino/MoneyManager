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
        contenido = self.exportar(gastos, formato)
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)