"""
Módulo Application - Servicios y casos de uso del Gestor Económico
==========================================================
Contiene la lógica de aplicación:
- Servicios de negocio
- Estrategias de análisis
- Exportadores de datos
- Factories para creación de objetos
"""

from .services import ServicioGastos, AnalizadorGastos, GestorReportes, ComparadorMensual, ServicioCategorias
from .strategies import AnalisisTotal, AnalisisPorCategoria, AnalisisTendencias
from .exporters import ExportadorCSV, ExportadorJSON, ExportadorXML, GestorExportacion
from .factories import GastoFactory

__all__ = [
    'ServicioGastos', 'AnalizadorGastos', 'GestorReportes', 'ComparadorMensual', 'ServicioCategorias',
    'AnalisisTotal', 'AnalisisPorCategoria', 'AnalisisTendencias',
    'ExportadorCSV', 'ExportadorJSON', 'ExportadorXML', 'GestorExportacion',
    'GastoFactory'
]