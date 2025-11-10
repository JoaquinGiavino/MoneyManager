from src.domain.entities import TipoAlerta, Usuario
from .notificador_consola import NotificadorConsola
from .notificador_push import NotificadorPush

class GestorNotificaciones:
    def __init__(self):
        self.notificadores = [
            NotificadorConsola(),
            NotificadorPush()
        ]
    
    def enviar_alerta(self, tipo: TipoAlerta, mensaje: str, usuario: Usuario) -> None:
        for notificador in self.notificadores:
            try:
                notificador.enviar_alerta(tipo, mensaje, usuario)
            except Exception as e:
                print(f"Error en notificador {type(notificador).__name__}: {e}")