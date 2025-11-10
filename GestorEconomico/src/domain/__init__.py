"""
Módulo Domain - Entidades y contratos del dominio del Gestor Económico
"""
from .entities import Usuario, Gasto, Categoria, Moneda, TipoAlerta, ComparacionGastos, ReporteGastos
from .interfaces import IServicioGastos, IPersistenciaLocal, Exportable, Notificable, AnalisisStrategy

__all__ = [
    'Usuario', 'Gasto', 'Categoria', 'Moneda', 'TipoAlerta', 
    'ComparacionGastos', 'ReporteGastos', 'IServicioGastos', 
    'IPersistenciaLocal', 'Exportable', 'Notificable', 'AnalisisStrategy'
]