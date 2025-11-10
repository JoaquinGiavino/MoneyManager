from src.domain.entities import TipoAlerta, Usuario
from src.domain.interfaces import Notificable

class NotificadorPush(Notificable):
    def enviar_alerta(self, tipo: TipoAlerta, mensaje: str, usuario: Usuario) -> None:
        print(f"🔔 NOTIFICACIÓN PUSH [{tipo.value}] para {usuario.nombre}: {mensaje}")