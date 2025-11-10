from src.domain.entities import TipoAlerta, Usuario
from src.domain.interfaces import Notificable

class NotificadorConsola(Notificable):
    def enviar_alerta(self, tipo: TipoAlerta, mensaje: str, usuario: Usuario) -> None:
        iconos = {
            TipoAlerta.PRESUPUESTO_EXCEDIDO: "⚠️",
            TipoAlerta.NUEVO_GASTO: "💸",
            TipoAlerta.SINCRONIZACION: "🔄"
        }
        
        icono = iconos.get(tipo, "📢")
        print(f"{icono} [{tipo.value}] {mensaje}")