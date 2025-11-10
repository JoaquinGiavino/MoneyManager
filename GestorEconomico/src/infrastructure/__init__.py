"""
Módulo Infrastructure - Implementaciones técnicas del Gestor Económico
==========================================================
Contiene las implementaciones concretas de:
- Persistencia de datos (SQLite)
- Sistema de notificaciones
- Servicios externos
"""

from .persistence import PersistenciaSQLite
from .notifications import NotificadorPush, NotificadorConsola, GestorNotificaciones

__all__ = [
    'PersistenciaSQLite', 
    'NotificadorPush', 
    'NotificadorConsola', 
    'GestorNotificaciones'
]