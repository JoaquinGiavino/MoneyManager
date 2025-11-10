"""
Módulo Presentation - Interfaz de usuario del Gestor Económico
==========================================================
Contiene toda la capa de presentación:
- Interfaz gráfica principal
- Vistas y componentes
- Controladores
- Utilidades de UI
"""

from .gui import GestionGastosApp, ControllerGastos, PantallaPrincipal
from .views import FormularioGastoView, ListaGastosView, GraficoTendenciasView, ExportacionDialog
from .utils import ValidadorDatos, FormatoRegional, GastoFactory

__all__ = [
    'GestionGastosApp', 'ControllerGastos', 'PantallaPrincipal',
    'FormularioGastoView', 'ListaGastosView', 'GraficoTendenciasView', 'ExportacionDialog',
    'ValidadorDatos', 'FormatoRegional', 'GastoFactory'
]