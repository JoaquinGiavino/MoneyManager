"""
Gestor Económico - Sistema de Gestión de Gastos Personales
==========================================================
Módulo principal que contiene toda la funcionalidad
para el control y análisis de gastos personales.

Características:
- Registro inteligente de gastos
- Análisis y reportes detallados
- Sistema de alertas y notificaciones
- Exportación múltiple de datos
- Arquitectura modular y extensible
"""

__version__ = '1.0.0'
__author__ = 'Gestor Económico Team'
__description__ = 'Sistema completo de gestión financiera personal'

# Importaciones principales para facilitar el acceso
from . import core
from . import domain
from . import application
from . import infrastructure
from . import presentation

__all__ = ['core', 'domain', 'application', 'infrastructure', 'presentation']